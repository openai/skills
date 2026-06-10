"""CLI orchestration for migrate-to-codex.

This module owns argument parsing, scan/dry-run/report rendering, deployment
planning, and file writes. Provider-specific conversions live in
`migrate.<surface>` modules; keep this file as the coordinator that combines
instruction, skill, MCP, hook, plugin-report, and subagent conversion results.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from migrate.agents import (
    AGENT_SOURCE_ROOTS,
    convert_agents,
    iter_agent_files,
    validate_agent_files,
)
from migrate.common import (
    CODEX_AGENTS_ROOT,
    CODEX_SKILLS_ROOT,
    ArtifactKind,
    ArtifactPayload,
    ConversionResult,
    GeneratedText,
    MigrationReportItem,
    MigrationSummary,
    PlannedArtifact,
    ScopePaths,
    SourceCopy,
    SourceSymlink,
    format_manual_migration_block,
    path_exists_with_exact_case,
)
from migrate.hooks import report_hooks
from migrate.codex_config import convert_settings, validate_config_toml
from migrate.instructions import (
    INSTRUCTION_SOURCE_CANDIDATES,
    instruction_source_file,
    should_symlink_instructions,
    validate_agents_md_files,
)
from migrate.plugins import report_plugins
from migrate.settings import SOURCE_SCAN_ROOTS, SOURCE_SCOPE_MARKERS
from migrate.skills import (
    COMMAND_FILE_SOURCES,
    SKILL_SOURCE_ROOTS,
    convert_skills,
    iter_skill_files,
    normalize_skill_names,
    validate_skill_files,
)
from utils.scan import (
    render_scope_inventory,
    render_source_inventory,
)
from utils.util import normalize_source_scope_root, resolve_source_root


# Constants

DEFAULT_COMPONENTS = frozenset(("mcp", "skills", "subagents"))
MIGRATION_REPORT_PATH = Path(".codex") / "migrate-to-codex-report.txt"
SCOPE_NAMES = ("global", "project")
SKILL_ROOT = Path(__file__).resolve().parents[1]


class DeployMode(Enum):
    MERGE = "merge"
    REPLACE = "replace"


@dataclass(frozen=True)
class DeploymentPlan:
    artifacts: tuple[PlannedArtifact, ...]
    orphaned_skill_dirs: tuple[Path, ...]
    orphaned_agent_files: tuple[Path, ...]
    colliding_skill_dirs: tuple[Path, ...]
    colliding_agent_files: tuple[Path, ...]
    summary: MigrationSummary

    def warning_messages(self) -> tuple[str, ...]:
        return tuple(
            [
                *(
                    f"warning: overwriting existing Codex skill at {collision}"
                    for collision in self.colliding_skill_dirs
                ),
                *(
                    f"warning: overwriting existing Codex subagent at {collision}"
                    for collision in self.colliding_agent_files
                ),
            ]
        )


@dataclass(frozen=True)
class ScopeDeployment:
    artifacts: tuple[PlannedArtifact, ...]
    target_root: Path
    components: frozenset[str] = DEFAULT_COMPONENTS

    def planned_paths(self, artifact_kind: ArtifactKind) -> frozenset[Path]:
        return frozenset(
            artifact.relative_path.parent
            if artifact_kind == ArtifactKind.SKILL
            else artifact.relative_path
            for artifact in self.artifacts
            if artifact.kind == artifact_kind
        )

    def existing_paths(self, root: Path, pattern: str) -> list[Path]:
        if not root.exists():
            return []
        return sorted(path for path in root.glob(pattern) if path.is_dir() or path.is_file())

    def orphaned_codex_paths(
        self,
        component: str,
        artifact_kind: ArtifactKind,
        codex_root: Path,
        pattern: str,
    ) -> list[Path]:
        if component not in self.components:
            return []

        target_root = self.target_root / codex_root
        planned_paths = self.planned_paths(artifact_kind)
        orphans: list[Path] = []
        for target_path in self.existing_paths(target_root, pattern):
            relative_path = codex_root / target_path.name
            if relative_path not in planned_paths:
                orphans.append(target_path)
        return orphans

    def colliding_codex_paths(
        self,
        component: str,
        artifact_kind: ArtifactKind,
        codex_root: Path,
    ) -> list[Path]:
        if component not in self.components or not (self.target_root / codex_root).exists():
            return []

        collisions: list[Path] = []
        for relative_path in self.planned_paths(artifact_kind):
            target_path = self.target_root / relative_path
            if target_path.exists():
                collisions.append(target_path)
        return collisions

    def plan(self) -> DeploymentPlan:
        orphaned_skill_dirs = tuple(
            self.orphaned_codex_paths(
                "skills",
                ArtifactKind.SKILL,
                CODEX_SKILLS_ROOT,
                "*",
            )
        )
        orphaned_agent_files = tuple(
            self.orphaned_codex_paths(
                "subagents",
                ArtifactKind.AGENT,
                CODEX_AGENTS_ROOT,
                "*.toml",
            )
        )
        colliding_skill_dirs = tuple(
            self.colliding_codex_paths(
                "skills",
                ArtifactKind.SKILL,
                CODEX_SKILLS_ROOT,
            )
        )
        colliding_agent_files = tuple(
            self.colliding_codex_paths(
                "subagents",
                ArtifactKind.AGENT,
                CODEX_AGENTS_ROOT,
            )
        )
        return DeploymentPlan(
            artifacts=self.artifacts,
            orphaned_skill_dirs=orphaned_skill_dirs,
            orphaned_agent_files=orphaned_agent_files,
            colliding_skill_dirs=colliding_skill_dirs,
            colliding_agent_files=colliding_agent_files,
            summary=MigrationSummary(
                orphaned_skills=len(orphaned_skill_dirs),
                orphaned_subagents=len(orphaned_agent_files),
            ),
        )


@dataclass(frozen=True)
class MigrationContext:
    conversion_result: ConversionResult
    deployment_plan: DeploymentPlan
    deployment_target_root: Path


def without_orphan_cleanup(deployment_plan: DeploymentPlan) -> DeploymentPlan:
    return DeploymentPlan(
        artifacts=deployment_plan.artifacts,
        orphaned_skill_dirs=(),
        orphaned_agent_files=(),
        colliding_skill_dirs=deployment_plan.colliding_skill_dirs,
        colliding_agent_files=deployment_plan.colliding_agent_files,
        summary=MigrationSummary(),
    )


# Conversion orchestration


def convert_tree(
    source_root: Path,
    components: frozenset[str] = DEFAULT_COMPONENTS,
    selected_skill_names: frozenset[str] | None = None,
) -> ConversionResult:
    """Convert a fixture tree containing global/ and project/ Claude scopes."""
    result = ConversionResult()
    selected_names = selected_skill_names or frozenset()
    scopes = [
        ScopePaths(source_root / "global", True),
        ScopePaths(source_root / "project", False),
    ]

    for scope_name, scope in zip(SCOPE_NAMES, scopes):
        if scope.source.exists():
            result.add(
                convert_scope(scope, components, selected_names).prefixed(Path(scope_name))
            )

    if "skills" in components and not selected_names:
        result.artifacts.extend(migration_skill_artifacts(source_root))
    return result


def convert_scope(
    scope: ScopePaths,
    components: frozenset[str] = DEFAULT_COMPONENTS,
    selected_skill_names: frozenset[str] | None = None,
) -> ConversionResult:
    result = ConversionResult()

    result.add(convert_instructions(scope))
    result.add(report_plugins(scope))
    result.add(report_hooks(scope))
    if "skills" in components:
        result.add(convert_skills(scope.source, selected_skill_names))
    if "mcp" in components:
        result.add(convert_settings(scope))
    if "subagents" in components:
        result.add(convert_agents(scope.source))
    return result


def convert_instructions(scope: ScopePaths) -> ConversionResult:
    source_file = instruction_source_file(
        scope.source,
        scope.is_global,
        path_exists_with_exact_case,
    )
    if not source_file:
        return ConversionResult()

    content = source_file.read_text()
    payload: ArtifactPayload
    if source_file == scope.source / "AGENTS.md":
        report_item = MigrationReportItem(
            "rewritten",
            Path("AGENTS.md"),
            f"Existing Codex instructions already present at {source_file}.",
        )
        return ConversionResult(
            summary=MigrationSummary(instructions=1),
            report_items=[report_item],
        )
    if should_symlink_instructions(content):
        payload = SourceSymlink(source_file)
        report_item = MigrationReportItem(
            "symlinked",
            Path("AGENTS.md"),
            f"Linked to {source_file}.",
        )
    else:
        manual_block = format_manual_migration_block(
            (
                "Claude-only instructions were copied into `AGENTS.md`. Remove Claude hooks, slash commands, and subagent assumptions before relying on this file in Codex.",
            )
        )
        payload = GeneratedText(f"{content.rstrip()}\n\n{manual_block}\n")
        report_item = MigrationReportItem(
            "manual_fix_required",
            Path("AGENTS.md"),
            "Generated copy contains Claude-only instruction semantics.",
        )
    return ConversionResult(
        summary=MigrationSummary(instructions=1),
        artifacts=[
            PlannedArtifact(
                relative_path=Path("AGENTS.md"),
                payload=payload,
            )
        ],
        report_items=[report_item],
    )


def symlink_target(source_path: Path, target_path: Path) -> str:
    return os.path.relpath(source_path, target_path.parent)


def has_artifact_path(
    conversion_result: ConversionResult,
    suffix: str,
) -> bool:
    return any(
        artifact.relative_path.as_posix().endswith(suffix)
        for artifact in conversion_result.artifacts
    )


def surface_line(status: str, surface: str, detail: str) -> str:
    return f"  {status}: {surface} - {detail}"


def render_migration_surfaces(
    conversion_result: ConversionResult,
    components: frozenset[str],
) -> str:
    summary = conversion_result.summary
    lines = ["", "Migration surfaces:"]

    if summary.instructions:
        lines.append(
            surface_line(
                "active",
                "AGENTS.md",
                f"{summary.instructions} instruction file(s) found.",
            )
        )
    else:
        lines.append(
            surface_line(
                "inactive",
                "AGENTS.md",
                "No supported instruction file found.",
            )
        )

    if "skills" not in components:
        lines.append(surface_line("inactive", "skills", "Not selected by CLI flags."))
    elif summary.skills:
        lines.append(
            surface_line(
                "active",
                "skills",
                f"{summary.skills} skill(s) converted.",
            )
        )
    else:
        lines.append(surface_line("inactive", "skills", "No skills found."))

    if "mcp" not in components:
        lines.append(
            surface_line("inactive", "MCP config", "Not selected by CLI flags.")
        )
    elif has_artifact_path(conversion_result, ".codex/config.toml"):
        lines.append(
            surface_line(
                "active",
                "MCP config",
                f"{summary.mcp_servers} MCP server(s) converted into config.toml.",
            )
        )
    else:
        lines.append(
            surface_line(
                "inactive",
                "MCP config",
                "No settings or MCP config found.",
            )
        )

    if "subagents" not in components:
        lines.append(
            surface_line("inactive", "subagents", "Not selected by CLI flags.")
        )
    elif summary.subagents:
        lines.append(
            surface_line(
                "active",
                "subagents",
                f"{summary.subagents} subagent(s) converted.",
            )
        )
    else:
        lines.append(surface_line("inactive", "subagents", "No subagents found."))

    return "\n".join(lines)


def render_migration_report(
    report_items: Sequence[MigrationReportItem],
    deployment_plan: DeploymentPlan,
    deploy_mode: DeployMode,
    dry_run: bool,
) -> str:
    lines = ["", "Migration report:"]
    for item in report_items:
        lines.append(f"  {item.status}: {item.path.as_posix()} - {item.detail}")
    for collision in deployment_plan.colliding_skill_dirs:
        lines.append(
            f"  overwritten: {collision.as_posix()} - Existing Codex skill will be replaced."
        )
    for collision in deployment_plan.colliding_agent_files:
        lines.append(
            f"  overwritten: {collision.as_posix()} - Existing Codex subagent will be replaced."
        )
    if deploy_mode == DeployMode.REPLACE:
        orphan_status = "would_delete" if dry_run else "deleted"
        for orphan in deployment_plan.orphaned_skill_dirs:
            lines.append(
                f"  {orphan_status}: {orphan.as_posix()} - Orphaned generated skill."
            )
        for orphan in deployment_plan.orphaned_agent_files:
            lines.append(
                f"  {orphan_status}: {orphan.as_posix()} - Orphaned generated subagent."
            )
    return "\n".join(lines)


def validate_target(target_root: Path) -> list[MigrationReportItem]:
    report_items: list[MigrationReportItem] = []
    report_items.extend(validate_config_toml(target_root))
    report_items.extend(validate_skill_files(target_root))
    report_items.extend(validate_agent_files(target_root))
    report_items.extend(validate_agents_md_files(target_root))
    return report_items


def render_validation_report(report_items: list[MigrationReportItem]) -> str:
    lines = ["Validation report:"]
    if not report_items:
        lines.append("  warning: . - no Codex artifacts found to validate.")
        return "\n".join(lines)

    for item in report_items:
        lines.append(f"  {item.status}: {item.path.as_posix()} - {item.detail}")
    return "\n".join(lines)


def write_migration_report(target_root: Path, report_text: str) -> None:
    report_path = target_root / MIGRATION_REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(f"{report_text.lstrip()}\n")


def write_artifact(artifact: PlannedArtifact, target_root: Path) -> None:
    target_path = target_root / artifact.relative_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(artifact.payload, GeneratedText):
        if target_path.is_symlink():
            target_path.unlink()
        target_path.write_text(artifact.payload.content)
        return

    if isinstance(artifact.payload, SourceSymlink):
        if target_path.exists() or target_path.is_symlink():
            target_path.unlink()
        target_path.symlink_to(symlink_target(artifact.payload.source_path, target_path))
        return

    if target_path.is_symlink():
        target_path.unlink()
    shutil.copy2(artifact.payload.source_path, target_path)


# Deployment orchestration


def deploy_tree(
    conversion_result: ConversionResult,
    target_root: Path,
    components: frozenset[str] = DEFAULT_COMPONENTS,
) -> DeploymentPlan:
    summary = MigrationSummary()
    artifacts: list[PlannedArtifact] = []
    orphaned_skill_dirs: list[Path] = []
    orphaned_agent_files: list[Path] = []
    colliding_skill_dirs: list[Path] = []
    colliding_agent_files: list[Path] = []
    for scope_name in SCOPE_NAMES:
        prefixed_scope_artifacts = tuple(
            artifact
            for artifact in conversion_result.artifacts
            if artifact.relative_path.parts
            and artifact.relative_path.parts[0] == scope_name
        )
        scope_artifacts = tuple(
            artifact.without_prefix() for artifact in prefixed_scope_artifacts
        )
        if not scope_artifacts:
            continue
        scope_plan = ScopeDeployment(
            scope_artifacts,
            target_root / scope_name,
            components,
        ).plan()
        summary.add(scope_plan.summary)
        artifacts.extend(prefixed_scope_artifacts)
        orphaned_skill_dirs.extend(scope_plan.orphaned_skill_dirs)
        orphaned_agent_files.extend(scope_plan.orphaned_agent_files)
        colliding_skill_dirs.extend(scope_plan.colliding_skill_dirs)
        colliding_agent_files.extend(scope_plan.colliding_agent_files)
    return DeploymentPlan(
        artifacts=tuple(artifacts),
        orphaned_skill_dirs=tuple(orphaned_skill_dirs),
        orphaned_agent_files=tuple(orphaned_agent_files),
        colliding_skill_dirs=tuple(colliding_skill_dirs),
        colliding_agent_files=tuple(colliding_agent_files),
        summary=summary,
    )


def migration_skill_artifacts(source_root: Path) -> list[PlannedArtifact]:
    artifacts: list[PlannedArtifact] = []
    for scope_name in SCOPE_NAMES:
        if not (source_root / scope_name).exists():
            continue
        artifacts.append(
            PlannedArtifact(
                relative_path=Path(scope_name)
                / ".agents"
                / "skills"
                / "migrate-to-codex"
                / "SKILL.md",
                payload=SourceCopy(SKILL_ROOT / "SKILL.md"),
                kind=ArtifactKind.SKILL,
            )
        )
        artifacts.append(
            PlannedArtifact.from_source_file(
                SKILL_ROOT / "references" / "differences.md",
                Path(scope_name)
                / ".agents"
                / "skills"
                / "migrate-to-codex"
                / "references"
                / "differences.md",
            )
        )
    return artifacts


def render_migration_inventory(source_root: Path) -> str:
    return render_scope_inventory(
        source_root,
        INSTRUCTION_SOURCE_CANDIDATES,
        COMMAND_FILE_SOURCES,
        SKILL_SOURCE_ROOTS,
        AGENT_SOURCE_ROOTS,
        iter_skill_files,
        iter_agent_files,
        path_exists_with_exact_case,
    )


def render_source_inventory_for_scope(source_root: Path) -> str:
    return render_source_inventory(
        source_root,
        SOURCE_SCAN_ROOTS,
        path_exists_with_exact_case,
    )


def normalize_scope_root(path: Path, marker: str) -> Path:
    if path.name == marker:
        return path.parent
    return path


def selected_components(args: argparse.Namespace) -> frozenset[str]:
    components = {
        component
        for component in ("mcp", "skills", "subagents")
        if getattr(args, component, False)
    }
    if getattr(args, "skill_names", None):
        components.add("skills")
    if not components:
        return DEFAULT_COMPONENTS
    return frozenset(components)


def build_migration_context(
    source_root: Path,
    target_root: Path,
    components: frozenset[str],
    selected_skill_names: frozenset[str] | None = None,
) -> MigrationContext:
    selected_names = selected_skill_names or frozenset()
    if (source_root / "global").exists() and (source_root / "project").exists():
        conversion_result = convert_tree(source_root, components, selected_names)
        deployment_target_root = target_root
        deployment_plan = deploy_tree(
            conversion_result,
            deployment_target_root,
            components,
        )
        if selected_names:
            deployment_plan = without_orphan_cleanup(deployment_plan)
        return MigrationContext(
            conversion_result,
            deployment_plan,
            deployment_target_root,
        )

    source_scope_root = normalize_scope_root(source_root, ".claude")
    deployment_target_root = normalize_scope_root(target_root, ".codex")
    scope = ScopePaths(
        source_scope_root,
        source_scope_root == Path.home(),
    )
    conversion_result = convert_scope(scope, components, selected_names)
    deployment_plan = ScopeDeployment(
        tuple(conversion_result.artifacts),
        deployment_target_root,
        components,
    ).plan()
    if selected_names:
        deployment_plan = without_orphan_cleanup(deployment_plan)
    return MigrationContext(conversion_result, deployment_plan, deployment_target_root)


def render_migration_plan(
    conversion_result: ConversionResult,
    deployment_plan: DeploymentPlan,
    deploy_mode: DeployMode,
) -> str:
    lines = [
        "Migration plan:",
        f"  deploy mode: {deploy_mode.value}",
    ]
    summary = conversion_result.summary
    if summary.instructions:
        lines.append(f"  stage: instructions - {summary.instructions} AGENTS.md file(s).")
    if summary.mcp_servers:
        lines.append(f"  stage: mcp - {summary.mcp_servers} MCP server(s).")
    if summary.skills:
        lines.append(f"  stage: skills - {summary.skills} Codex skill artifact(s).")
    if summary.subagents:
        lines.append(f"  stage: subagents - {summary.subagents} Codex custom agent(s).")
    if not any(
        (
            summary.instructions,
            summary.mcp_servers,
            summary.skills,
            summary.subagents,
        )
    ):
        lines.append("  stage: none - no supported migration surfaces found.")

    if conversion_result.artifacts:
        lines.append("  artifacts:")
        for artifact in sorted(
            conversion_result.artifacts,
            key=lambda planned: planned.relative_path.as_posix(),
        ):
            lines.append(f"    - {artifact.relative_path.as_posix()}")

    manual_items = [
        item
        for item in conversion_result.report_items
        if item.status == "manual_fix_required"
    ]
    if manual_items:
        lines.append(f"  manual review: {len(manual_items)} item(s)")
        for item in manual_items:
            lines.append(f"    - {item.path.as_posix()}: {item.detail}")
    else:
        lines.append("  manual review: none")

    if deployment_plan.colliding_skill_dirs or deployment_plan.colliding_agent_files:
        lines.append("  collisions:")
        for collision in deployment_plan.colliding_skill_dirs:
            lines.append(f"    - existing skill: {collision.as_posix()}")
        for collision in deployment_plan.colliding_agent_files:
            lines.append(f"    - existing subagent: {collision.as_posix()}")

    if deployment_plan.orphaned_skill_dirs or deployment_plan.orphaned_agent_files:
        lines.append("  orphan cleanup:")
        for orphan in deployment_plan.orphaned_skill_dirs:
            lines.append(f"    - skill: {orphan.as_posix()}")
        for orphan in deployment_plan.orphaned_agent_files:
            lines.append(f"    - subagent: {orphan.as_posix()}")

    return "\n".join(lines)


def render_doctor_report(
    conversion_result: ConversionResult,
    deployment_plan: DeploymentPlan,
) -> str:
    manual_items = [
        item
        for item in conversion_result.report_items
        if item.status == "manual_fix_required"
    ]
    collision_count = len(deployment_plan.colliding_skill_dirs) + len(
        deployment_plan.colliding_agent_files
    )
    orphan_count = len(deployment_plan.orphaned_skill_dirs) + len(
        deployment_plan.orphaned_agent_files
    )
    risk_count = len(manual_items) + collision_count + orphan_count
    if risk_count == 0:
        readiness = "high"
    elif risk_count <= 3:
        readiness = "medium"
    else:
        readiness = "low"

    lines = [
        "Migration doctor:",
        f"  readiness: {readiness}",
        f"  manual review items: {len(manual_items)}",
        f"  existing Codex collisions: {collision_count}",
        f"  orphaned generated artifacts: {orphan_count}",
    ]
    if manual_items:
        lines.append("  risks:")
        for item in manual_items:
            lines.append(f"    - {item.path.as_posix()}: {item.detail}")
    else:
        lines.append("  risks: none detected by static migration checks.")
    lines.append("  recommended flow: run --plan, run --dry-run, review manual items, migrate, then run --validate-target.")
    return "\n".join(lines)


# CLI


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Claude-style source tree to Codex (--target). "
            "Omit --mcp/--skills/--subagents to run all three. "
            "See migrate-to-codex SKILL.md."
        ),
    )
    parser.add_argument(
        "--source",
        help="Source root (optional global/ + project/ subdirs).",
    )
    parser.add_argument(
        "--target",
        help="Codex root (required for migrate, --plan, and --doctor).",
    )
    parser.add_argument(
        "--mcp", action="store_true", help="Write MCP/settings to config.toml."
    )
    parser.add_argument(
        "--skills", action="store_true", help="Write skills under .agents/skills."
    )
    parser.add_argument(
        "--skill",
        dest="skill_names",
        action="append",
        metavar="NAME",
        help=(
            "Convert only the named Claude skill. Can be passed multiple times; "
            "implies --skills and skips command-to-skill conversion."
        ),
    )
    parser.add_argument(
        "--subagents", action="store_true", help="Write agents under .codex/agents."
    )
    parser.add_argument(
        "--scan-sources",
        action="store_true",
        help="Print source inventory before migrate.",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--scan-only", action="store_true", help="Inventory only; omit --target."
    )
    mode_group.add_argument(
        "--plan",
        action="store_true",
        help="Print staged migration plan; do not write files.",
    )
    mode_group.add_argument(
        "--doctor",
        action="store_true",
        help="Print readiness and manual-review guidance; do not write files.",
    )
    mode_group.add_argument(
        "--validate-target",
        help="Validate an existing migrated Codex target and exit.",
    )
    deploy_group = parser.add_mutually_exclusive_group()
    deploy_group.add_argument(
        "--merge",
        action="store_true",
        help="Keep orphan generated skills/agents (default).",
    )
    deploy_group.add_argument(
        "--replace",
        action="store_true",
        help="Remove orphan generated skills/agents for selected surfaces.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print report; do not write files."
    )
    args = parser.parse_args()

    selected_skill_names = normalize_skill_names(args.skill_names)
    if selected_skill_names and args.validate_target:
        parser.error("--skill is only used during migration, not --validate-target.")
    if selected_skill_names and args.replace:
        parser.error(
            "--replace cannot be used with --skill; selected skill migration "
            "already overwrites matching skills without orphan cleanup."
        )

    if args.validate_target:
        target_root = normalize_scope_root(Path(args.validate_target), ".codex")
        report_items = validate_target(target_root)
        print(render_validation_report(report_items))
        if any(item.status == "error" for item in report_items):
            raise SystemExit(1)
        return

    if not args.source:
        parser.error("--source is required unless --validate-target is set.")

    source_root = resolve_source_root(args.source)
    if not source_root.exists():
        normalized_candidate = normalize_source_scope_root(
            source_root,
            SOURCE_SCOPE_MARKERS,
        )
        if normalized_candidate.exists():
            source_root = normalized_candidate
        else:
            raise SystemExit(f"Missing source root: {source_root}")

    if args.scan_only and args.target:
        parser.error("--scan-only does not use --target.")
    if not args.scan_only and not args.target:
        parser.error("--target is required unless --scan-only or --validate-target is set.")

    if args.scan_only:
        if (source_root / "global").exists() and (source_root / "project").exists():
            print(render_source_inventory_for_scope(source_root / "global"))
            print(render_migration_inventory(source_root / "global"))
            print(render_source_inventory_for_scope(source_root / "project"))
            print(render_migration_inventory(source_root / "project"))
        else:
            normalized_source_root = normalize_source_scope_root(
                source_root,
                SOURCE_SCOPE_MARKERS,
            )
            print(render_source_inventory_for_scope(normalized_source_root))
            print(render_migration_inventory(normalized_source_root))
        return

    target_root = Path(args.target)
    components = selected_components(args)
    deploy_mode = DeployMode.REPLACE if args.replace else DeployMode.MERGE

    context = build_migration_context(
        source_root,
        target_root,
        components,
        selected_skill_names,
    )
    conversion_result = context.conversion_result
    deployment_plan = context.deployment_plan
    deployment_target_root = context.deployment_target_root

    conversion_result.summary.add(deployment_plan.summary)
    if args.plan:
        print(render_migration_plan(conversion_result, deployment_plan, deploy_mode))
        return
    if args.doctor:
        print(render_doctor_report(conversion_result, deployment_plan))
        return

    source_inventory = ""
    migration_inventory = ""
    if args.scan_sources:
        if (source_root / "global").exists() and (source_root / "project").exists():
            source_inventory = (
                render_source_inventory_for_scope(source_root / "global")
                + "\n"
                + render_source_inventory_for_scope(source_root / "project")
            )
        else:
            source_inventory = render_source_inventory_for_scope(
                normalize_source_scope_root(source_root, SOURCE_SCOPE_MARKERS),
            )
    if (source_root / "global").exists() and (source_root / "project").exists():
        migration_inventory = (
            render_migration_inventory(source_root / "global")
            + "\n"
            + render_migration_inventory(source_root / "project")
        )
    else:
        migration_inventory = render_migration_inventory(
            normalize_source_scope_root(source_root, SOURCE_SCOPE_MARKERS),
        )
    migration_surfaces = render_migration_surfaces(conversion_result, components)
    migration_report = render_migration_report(
        conversion_result.report_items,
        deployment_plan,
        deploy_mode,
        args.dry_run,
    )
    for warning_message in deployment_plan.warning_messages():
        print(warning_message, file=sys.stderr)
    if not args.dry_run:
        for artifact in deployment_plan.artifacts:
            write_artifact(artifact, deployment_target_root)
        if deploy_mode == DeployMode.REPLACE:
            for orphan in deployment_plan.orphaned_skill_dirs:
                shutil.rmtree(orphan)
            for orphan in deployment_plan.orphaned_agent_files:
                orphan.unlink()
        write_migration_report(
            deployment_target_root,
            f"{source_inventory}{migration_inventory}{migration_surfaces}{migration_report}",
        )
    print(conversion_result.summary.render(deploy_mode, args.dry_run))
    if source_inventory:
        print(source_inventory)
    if migration_inventory:
        print(migration_inventory)
    print(migration_surfaces)
    print(migration_report)


if __name__ == "__main__":
    main()
