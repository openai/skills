#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_run_dir(base_dir: Path, run_dir_arg: str | None) -> Path:
    if run_dir_arg:
        return Path(run_dir_arg).resolve()
    latest_path = base_dir / "latest.json"
    if latest_path.exists():
        try:
            latest = load_json(latest_path)
            run_dir = latest.get("run_dir")
            if run_dir:
                return Path(run_dir)
        except Exception:
            pass
    if (base_dir / "evidence.json").exists():
        return base_dir.resolve()
    return base_dir.resolve()


def result(
    status: str,
    rationale: str,
    evidence_path: str | None = None,
    quote: str | None = None,
    recommendations=None,
    confidence: float = 1.0,
) -> dict:
    if recommendations is None:
        recommendations = []
    evidence_quotes = []
    if evidence_path and quote:
        evidence_quotes.append({"path": evidence_path, "quote": quote})
    return {
        "status": status,
        "rationale": rationale,
        "evidence_quotes": evidence_quotes,
        "recommendations": recommendations,
        "confidence": confidence,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def rule_agents_exists(evidence: dict) -> dict:
    agents = evidence.get("agents_md", {})
    path = agents.get("path")
    if agents.get("exists") and path and Path(path).exists():
        return result(
            "PASS",
            "AGENTS.md exists in the current directory.",
            recommendations=[],
        )
    return result(
        "FAIL",
        "AGENTS.md is missing in the current directory.",
        recommendations=["Add an AGENTS.md in the current directory with onboarding context."],
        confidence=1.0,
    )


PLAN_HEADINGS = [
    "## Purpose / Big Picture",
    "## Progress",
    "## Decision Log",
    "## Outcomes & Retrospective",
    "## Surprises & Discoveries",
]


def _clean_markdown_ref(raw_ref: str) -> str:
    if not raw_ref:
        return ""
    cleaned = raw_ref.strip()
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip()
    cleaned = re.split(r"[?#]", cleaned, maxsplit=1)[0]
    cleaned = cleaned.strip().strip("`'\"()[]{}<>.,:;")
    return cleaned


def _is_markdown_path(ref: str) -> bool:
    if not ref:
        return False
    try:
        name = Path(ref).name.lower()
    except Exception:
        return False
    return name.endswith((".md", ".markdown"))


def _extract_markdown_refs(text: str) -> list[tuple[str, str]]:
    references: list[tuple[str, str]] = []
    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = _clean_markdown_ref(match.group(1))
        if _is_markdown_path(target):
            start = text.rfind("\n", 0, match.start())
            end = text.find("\n", match.start())
            line = text[start + 1 : end if end != -1 else None]
            references.append((target, line.strip()))
    for line in text.splitlines():
        for token in re.findall(r"(?i)[A-Za-z0-9_./\\-]*\.(?:md|markdown)", line):
            cleaned = _clean_markdown_ref(token)
            if _is_markdown_path(cleaned):
                references.append((cleaned, line.strip()))
    return references


def _is_plan_named(path: Path) -> bool:
    return "plan" in path.name.lower()


def _has_planning_conventions(text: str) -> bool:
    lowered = text.lower()
    matches = sum(1 for heading in PLAN_HEADINGS if heading.lower() in lowered)
    return matches >= 3


def rule_plans_reference_exists(evidence: dict) -> dict:
    agents = evidence.get("agents_md", {})
    agents_path = agents.get("path")
    if not (agents.get("exists") and agents_path and Path(agents_path).exists()):
        return result(
            "FAIL",
            "AGENTS.md is missing; cannot resolve referenced plans file.",
            recommendations=["Add an AGENTS.md that references a plans markdown file."],
            confidence=1.0,
        )

    text = read_text(Path(agents_path))
    references = _extract_markdown_refs(text)
    if not references:
        return result(
            "FAIL",
            "No planning markdown file reference found in AGENTS.md.",
            recommendations=[
                "Reference a planning markdown file in AGENTS.md (e.g., PLANS.md or exec-plan.md)."
            ],
            confidence=1.0,
        )

    base_dir = Path(agents_path).parent
    resolved = {}
    for raw_ref, line in references:
        cleaned = _clean_markdown_ref(raw_ref)
        if not _is_markdown_path(cleaned):
            continue
        path = Path(cleaned)
        resolved_path = path if path.is_absolute() else (base_dir / path).resolve()
        if resolved_path not in resolved:
            resolved[resolved_path] = line

    missing = [path for path in resolved if not path.exists()]
    evidence_quotes = []
    for line in resolved.values():
        if line:
            evidence_quotes.append({"path": agents_path, "quote": line[:240]})
        if len(evidence_quotes) >= 3:
            break

    if missing:
        missing_list = ", ".join(str(path) for path in missing)
        return {
            "status": "FAIL",
            "rationale": f"Referenced planning markdown file(s) not found: {missing_list}.",
            "evidence_quotes": evidence_quotes,
            "recommendations": ["Create the referenced planning markdown file(s)."],
            "confidence": 1.0,
        }

    qualifying_paths = []
    non_qualifying_paths = []
    for path in resolved:
        if _is_plan_named(path):
            qualifying_paths.append(path)
            continue
        try:
            content = read_text(path)
        except Exception:
            non_qualifying_paths.append(path)
            continue
        if _has_planning_conventions(content):
            qualifying_paths.append(path)
        else:
            non_qualifying_paths.append(path)

    if qualifying_paths:
        return {
            "status": "PASS",
            "rationale": "Referenced planning markdown file(s) exist and follow planning conventions.",
            "evidence_quotes": evidence_quotes,
            "recommendations": [],
            "confidence": 1.0,
        }

    missing_list = ", ".join(str(path) for path in non_qualifying_paths)
    return {
        "status": "FAIL",
        "rationale": f"Referenced markdown file(s) do not appear to be planning docs: {missing_list}.",
        "evidence_quotes": evidence_quotes,
        "recommendations": [
            "Reference a planning markdown file (name contains 'plan') or add planning headings."
        ],
        "confidence": 1.0,
    }


def rule_agents_line_count_under_300(evidence: dict) -> dict:
    agents = evidence.get("agents_md", {})
    path = agents.get("path")
    if not (agents.get("exists") and path and Path(path).exists()):
        return result(
            "FAIL",
            "AGENTS.md is missing; cannot verify line count.",
            recommendations=["Add an AGENTS.md in the current directory with onboarding context."],
            confidence=1.0,
        )

    text = read_text(Path(path))
    line_count = len(text.splitlines())
    if line_count <= 300:
        return result(
            "PASS",
            f"AGENTS.md has {line_count} lines (<= 300).",
            recommendations=[],
            confidence=1.0,
        )
    return result(
        "FAIL",
        f"AGENTS.md has {line_count} lines (> 300).",
        recommendations=["Trim AGENTS.md to 300 lines or fewer."],
        confidence=1.0,
    )


def rule_config_toml_exists(evidence: dict) -> dict:
    run_context = evidence.get("run_context", {})
    cwd = run_context.get("cwd")
    if not cwd:
        return result(
            "FAIL",
            "Run context missing; cannot resolve config.toml location.",
            recommendations=["Ensure evidence.json includes run_context.cwd."],
            confidence=1.0,
        )

    repo_root = Path(cwd)
    repo_config = repo_root / "config.toml"
    codex_config = repo_root / ".codex" / "config.toml"
    user_codex_config = Path.home() / ".codex" / "config.toml"

    found_paths = []
    if repo_config.exists():
        found_paths.append(str(repo_config))
    if codex_config.exists():
        found_paths.append(str(codex_config))
    if user_codex_config.exists():
        found_paths.append(str(user_codex_config))

    if found_paths:
        return result(
            "PASS",
            f"config.toml found at: {', '.join(found_paths)}.",
            recommendations=[],
            confidence=1.0,
        )

    return result(
        "FAIL",
        "config.toml not found in repo root, repo .codex/, or user .codex/.",
        recommendations=[
            "Add config.toml at the repo root, under .codex/config.toml, or in ~/.codex/config.toml."
        ],
        confidence=1.0,
    )


def rule_execution_summary_status(params: dict) -> dict:
    summary_path = Path(params.get("summary_path", "execution_summary.json"))
    if not summary_path.exists():
        return result(
            "NOT_RUN",
            "Execution summary not found; execution was not run.",
            recommendations=["Run execute mode to validate the documented dev/build/test loop."],
            confidence=1.0,
        )
    try:
        summary = load_json(summary_path)
    except Exception:
        return result(
            "WARN",
            "Execution summary exists but could not be parsed.",
            recommendations=["Review the execution summary JSON for corruption."],
            confidence=1.0,
        )

    status = summary.get("overall_status", "WARN")
    rationale = f"Execution summary reports overall status: {status}."
    return result(
        status,
        rationale,
        recommendations=[],
        confidence=1.0,
    )


RULES = {
    "agents_exists": rule_agents_exists,
    "plans_reference_exists": rule_plans_reference_exists,
    "agents_line_count_under_300": rule_agents_line_count_under_300,
    "config_toml_exists": rule_config_toml_exists,
    "execution_summary_status": rule_execution_summary_status,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic codex-readiness-unit-test rules."
    )
    parser.add_argument(
        "--out-dir", default=".codex-readiness-unit-test", help="Base output directory"
    )
    parser.add_argument("--run-dir", default=None, help="Specific run directory to use")
    parser.add_argument("--evidence", default=None, help="Path to evidence.json (optional)")
    parser.add_argument(
        "--checks",
        default=str(
            Path(__file__).resolve().parents[1]
            / "references"
            / "checks"
            / "checks.json"
        ),
        help="Path to checks.json",
    )
    parser.add_argument("--out", default=None, help="Output path (optional)")
    args = parser.parse_args()

    base_dir = Path(args.out_dir)
    run_dir = resolve_run_dir(base_dir, args.run_dir)
    evidence_path = Path(args.evidence) if args.evidence else (run_dir / "evidence.json")
    checks_path = Path(args.checks)
    if not evidence_path.exists():
        raise SystemExit(f"Evidence file not found: {evidence_path}")
    if not checks_path.exists():
        raise SystemExit(f"Checks file not found: {checks_path}")

    evidence = load_json(evidence_path)
    checks = load_json(checks_path)

    results = {}
    for check in checks.get("checks", []):
        if not check.get("enabled_by_default", False):
            continue
        rule_id = check.get("deterministic_rule_id")
        if not rule_id:
            continue
        rule = RULES.get(rule_id)
        if not rule:
            continue
        params = check.get("deterministic_rule_params", {})
        if rule_id == "execution_summary_status":
            summary_path = params.get("summary_path", "execution_summary.json")
            summary_candidate = Path(summary_path)
            if not summary_candidate.is_absolute():
                summary_candidate = run_dir / summary_candidate
            params = {**params, "summary_path": str(summary_candidate)}
            results[check["id"]] = rule(params)
        else:
            results[check["id"]] = rule(evidence)

    out_path = Path(args.out) if args.out else (run_dir / "deterministic_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
