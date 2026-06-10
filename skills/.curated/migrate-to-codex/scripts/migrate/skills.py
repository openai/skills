"""Convert Claude Code skills and commands into Codex skills.

Reads `.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>.md`, then emits
`.agents/skills/<name>/SKILL.md` plus supported helper directories for directory
skills. Also wraps `.claude/commands/*.md` as
one-file Codex skills. Runtime placeholders, file expansion, shell
interpolation, and unsupported metadata are preserved with manual-review
caveats.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from migrate.common import (
    CODEX_SKILLS_ROOT,
    ArtifactKind,
    ConversionResult,
    GeneratedText,
    MigrationReportItem,
    ParsedDocument,
    PlannedArtifact,
    SimpleYamlFrontmatter,
    append_report_item,
    format_bullets,
    format_frontmatter,
    format_manual_migration_block,
    is_path_within_root,
    manual_report_item,
    parse_frontmatter,
    unsupported_frontmatter_fields,
)
from utils.util import slugify_name


COMMAND_FILE_SOURCES = (
    (Path(".claude") / "commands", "source-command", "source command"),
)

SKILL_SOURCE_ROOTS = (
    Path(".claude") / "skills",
)
SKILL_SUPPORT_DIRS = ("scripts", "references", "assets")


def iter_skill_files(source_root: Path) -> tuple[Path, ...]:
    if not source_root.exists():
        return ()
    single_file_skills = tuple(
        source_file
        for source_file in sorted(source_root.glob("*.md"))
        if source_file.stem != "README"
    )
    directory_skills = tuple(sorted(source_root.glob("*/SKILL.md")))
    return single_file_skills + directory_skills


def skill_target_name(source_file: Path) -> str:
    if source_file.name == "SKILL.md":
        return source_file.parent.name
    return source_file.stem


def command_caveats(
    template: str,
    unsupported_fields: Sequence[str],
) -> tuple[str, ...]:
    caveats: list[str] = []
    if re.search(r"\$(ARGUMENTS|\d+)\b", template):
        caveats.append(
            "Provider argument placeholders like `$ARGUMENTS` or `$1` were preserved as text; rewrite them into natural-language instructions for Codex."
        )
    if "{{" in template and "}}" in template:
        caveats.append(
            "Provider template variables like `{{name}}` were preserved as text; rewrite them into natural-language instructions for Codex."
        )
    if re.search(r"!\s*`", template):
        caveats.append(
            "Provider shell-output interpolation like ``!`command` `` was preserved as text; replace it with explicit Codex instructions to run the command when needed."
        )
    if re.search(r"(^|\s)@[\w./~:-]+", template):
        caveats.append(
            "Provider automatic file-reference expansion was preserved as text; verify Codex should read those files explicitly."
        )
    if unsupported_fields:
        caveats.append(
            "Review unsupported command metadata manually: "
            + ", ".join(f"`{field_name}`" for field_name in unsupported_fields)
            + "."
        )
    return tuple(caveats)


def normalize_skill_names(skill_names: Sequence[str] | None) -> frozenset[str]:
    if not skill_names:
        return frozenset()
    return frozenset(
        slugify_name(skill_name)
        for skill_name in skill_names
        if skill_name and skill_name.strip()
    )


def selected_skill_matches(
    source_file: Path,
    selected_skill_names: frozenset[str],
) -> bool:
    if not selected_skill_names:
        return True

    if slugify_name(skill_target_name(source_file)) in selected_skill_names:
        return True

    document = ParsedDocument.from_file(source_file)
    frontmatter_name = document.frontmatter.optional_string("name")
    return bool(
        frontmatter_name and slugify_name(frontmatter_name) in selected_skill_names
    )


def convert_skills(
    source_root: Path,
    selected_skill_names: frozenset[str] | None = None,
) -> ConversionResult:
    selected_names = selected_skill_names or frozenset()
    result = convert_skill_files(source_root / ".claude" / "skills", selected_names)
    if not selected_names:
        result.add(convert_command_skills(source_root))
    return result


def convert_skill_files(
    source_root: Path,
    selected_skill_names: frozenset[str] | None = None,
) -> ConversionResult:
    result = ConversionResult()
    selected_names = selected_skill_names or frozenset()
    for source_file in iter_skill_files(source_root):
        if not selected_skill_matches(source_file, selected_names):
            continue
        artifacts, report_item = convert_skill_file(source_file)
        result.artifacts.extend(artifacts)
        result.summary.skills += 1
        result.report_items.append(report_item)
    return result


def convert_command_skills(source_root: Path) -> ConversionResult:
    result = ConversionResult()
    for command_source_root, name_prefix, provider in COMMAND_FILE_SOURCES:
        result.add(
            convert_markdown_command_files(
                source_root / command_source_root,
                name_prefix,
                provider,
            )
        )
    return result


def codex_skill_frontmatter(name: str, description: str) -> SimpleYamlFrontmatter:
    return SimpleYamlFrontmatter(
        {
            "name": name,
            "description": description,
        }
    )


def convert_skill_file(source_file: Path) -> tuple[list[PlannedArtifact], MigrationReportItem]:
    document = ParsedDocument.from_file(source_file)
    name = document.frontmatter.required_string("name")
    description = document.frontmatter.required_string("description")
    allowed_tools = document.frontmatter.string_tuple("allowed-tools")
    unsupported_fields = unsupported_frontmatter_fields(
        document.frontmatter.to_dict(),
        ("name", "description", "allowed-tools"),
    )
    artifacts = [
        PlannedArtifact(
            relative_path=CODEX_SKILLS_ROOT / skill_target_name(source_file) / "SKILL.md",
            payload=GeneratedText(
                render_skill(
                    document.body,
                    name=name,
                    description=description,
                    allowed_tools=allowed_tools,
                    unsupported_fields=unsupported_fields,
                )
            ),
            kind=ArtifactKind.SKILL,
        )
    ]
    artifacts.extend(skill_support_artifacts(source_file))
    return artifacts, skill_report_item(source_file, allowed_tools, unsupported_fields)


def skill_support_artifacts(source_file: Path) -> list[PlannedArtifact]:
    if source_file.name != "SKILL.md":
        return []

    artifacts: list[PlannedArtifact] = []
    skill_root = source_file.parent
    target_root = CODEX_SKILLS_ROOT / skill_root.name
    source_files: list[Path] = []
    for dirname in SKILL_SUPPORT_DIRS:
        source_dir = skill_root / dirname
        if not source_dir.exists():
            continue
        source_files.extend(
            source_file
            for source_file in source_dir.rglob("*")
            if source_file.is_file() and is_path_within_root(source_file, skill_root)
        )
    for support_file in sorted(
        source_files,
        key=lambda path: path.relative_to(skill_root).as_posix(),
    ):
        artifacts.append(
            PlannedArtifact.from_source_file(
                support_file,
                target_root / support_file.relative_to(skill_root),
            )
        )
    return artifacts


def render_skill(
    body: str,
    *,
    name: str,
    description: str,
    allowed_tools: tuple[str, ...],
    unsupported_fields: tuple[str, ...],
) -> str:
    return format_frontmatter(
        codex_skill_frontmatter(name, description),
        render_skill_body(body, allowed_tools, unsupported_fields),
    )


def render_skill_body(
    body: str,
    allowed_tools: tuple[str, ...],
    unsupported_fields: tuple[str, ...],
) -> str:
    manual_notes: list[str] = []
    if allowed_tools:
        manual_notes.append(
            "Claude `allowed-tools` was preserved as prompt guidance, not a Codex permission boundary.\n\n"
            "You're allowed to use these tools:\n\n"
            f"{format_bullets(allowed_tools)}"
        )
    if unsupported_fields:
        manual_notes.append(
            "Review unsupported Claude skill fields manually: "
            f"{', '.join(f'`{field_name}`' for field_name in unsupported_fields)}."
        )

    if not manual_notes:
        return body

    return f"{body.rstrip()}\n\n{format_manual_migration_block(manual_notes)}\n"


def skill_report_detail(
    allowed_tools: tuple[str, ...],
    unsupported_fields: tuple[str, ...],
) -> str:
    caveats: list[str] = []
    if allowed_tools:
        caveats.append("allowed-tools")
    caveats.extend(unsupported_fields)
    if not caveats:
        return "Converted Claude skill."
    return (
        "Manual review required for Claude skill fields: "
        + ", ".join(f"`{field_name}`" for field_name in caveats)
        + "."
    )


def skill_report_item(
    source_file: Path,
    allowed_tools: tuple[str, ...],
    unsupported_fields: tuple[str, ...],
) -> MigrationReportItem:
    report_items: list[MigrationReportItem] = []
    detail = skill_report_detail(allowed_tools, unsupported_fields)
    append_report_item(
        report_items,
        allowed_tools or unsupported_fields,
        CODEX_SKILLS_ROOT / skill_target_name(source_file) / "SKILL.md",
        detail,
        detail,
    )
    return report_items[0]


def convert_markdown_command_files(
    source_root: Path,
    name_prefix: str,
    provider: str,
) -> ConversionResult:
    result = ConversionResult()
    if not source_root.exists():
        return result
    for source_file in sorted(source_root.rglob("*.md")):
        artifact, report_item = convert_command_file(
            source_root,
            source_file,
            name_prefix,
            provider,
        )
        result.artifacts.append(artifact)
        result.summary.skills += 1
        result.report_items.append(report_item)
    return result


def convert_command_file(
    source_root: Path,
    source_file: Path,
    name_prefix: str,
    provider: str,
) -> tuple[PlannedArtifact, MigrationReportItem]:
    document = ParsedDocument.from_file(source_file)
    source_name = "-".join(source_file.relative_to(source_root).with_suffix("").parts)
    name = slugify_name(f"{name_prefix}-{source_name}")
    description = document.frontmatter.optional_string("description")
    if not description:
        description = f"Run the migrated {provider} `{source_name}`."
    unsupported_fields = unsupported_frontmatter_fields(
        document.frontmatter.to_dict(),
        ("description",),
    )
    caveats = command_caveats(document.body, unsupported_fields)
    artifact = PlannedArtifact(
        relative_path=CODEX_SKILLS_ROOT / name / "SKILL.md",
        payload=GeneratedText(
            render_command_skill(
                document.body,
                name=name,
                description=description,
                provider=provider,
                source_name=source_name,
                caveats=caveats,
            )
        ),
        kind=ArtifactKind.SKILL,
    )
    return artifact, command_report_item(name, provider, source_name)


def render_command_skill(
    body: str,
    *,
    name: str,
    description: str,
    provider: str,
    source_name: str,
    caveats: tuple[str, ...],
) -> str:
    manual_notes = [
        f"Migrated from {provider} `{source_name}` into a Codex skill. "
        f"Invoke it as `${name}` and manually rewrite any slash-command behavior that depended on provider-specific runtime expansion."
    ]
    manual_notes.extend(caveats)
    template_body = body.strip() or "No command template body was found."
    return format_frontmatter(
        codex_skill_frontmatter(name, description),
        f"# {name}\n\n"
        "Use this skill when the user asks to run the migrated "
        f"{provider} `{source_name}`.\n\n"
        "## Command Template\n\n"
        f"{template_body}\n\n"
        f"{format_manual_migration_block(manual_notes)}\n",
    )


def validate_skill_files(target_root: Path) -> list[MigrationReportItem]:
    skills_root = target_root / CODEX_SKILLS_ROOT
    if not skills_root.exists():
        return []

    report_items: list[MigrationReportItem] = []
    for skill_file in sorted(skills_root.glob("*/SKILL.md")):
        relative_path = skill_file.relative_to(target_root)
        document = parse_frontmatter(skill_file.read_text(), skill_file)
        missing = [
            key
            for key in ("name", "description")
            if not document.frontmatter.optional_string(key)
        ]
        if missing:
            report_items.append(
                MigrationReportItem(
                    "error",
                    relative_path,
                    "skill frontmatter missing " + ", ".join(missing) + ".",
                )
            )
            continue
        report_items.append(
            MigrationReportItem(
                "ok",
                relative_path,
                "skill frontmatter has name and description.",
            )
        )
    return report_items


def command_report_detail(provider: str, source_name: str) -> str:
    return (
        f"Converted {provider} `{source_name}` to a single-file Codex skill; "
        "review invocation and template placeholder semantics."
    )


def command_report_item(
    name: str,
    provider: str,
    source_name: str,
) -> MigrationReportItem:
    return manual_report_item(
        CODEX_SKILLS_ROOT / name / "SKILL.md",
        command_report_detail(provider, source_name),
    )
