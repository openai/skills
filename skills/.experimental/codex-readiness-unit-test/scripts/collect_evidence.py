#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict, cast

SKIP_DIRS = {
    ".git",
    ".codex-readiness-unit-test",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
}

BUILD_SIGNAL_FILES = [
    "package.json",
    "pnpm-workspace.yaml",
    "yarn.lock",
    "pnpm-lock.yaml",
    "package-lock.json",
    "pyproject.toml",
    "setup.py",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    "Makefile",
    "CMakeLists.txt",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "composer.json",
    "mix.exs",
    "gradlew",
    "tox.ini",
    "pytest.ini",
    "jest.config.js",
    "vitest.config.ts",
]

COMMAND_KEYWORDS = [
    "npm ",
    "yarn ",
    "pnpm ",
    "make ",
    "pytest",
    "go test",
    "go build",
    "cargo ",
    "mvn ",
    "gradle ",
    "./gradlew",
    "bundle ",
    "rake ",
    "tox",
    "poetry ",
    "pip ",
    "pipenv ",
    "cmake ",
]

SKILL_REF_PATTERN = re.compile(r"\$([A-Za-z0-9_.-]+)")
SKILL_PATH_PATTERN = re.compile(
    r"(?:\.codex/skills|~/.codex/skills|/\.codex/skills|skills)/([A-Za-z0-9_.-]+)"
)


class SkillReference(TypedDict):
    name: str


class SkillResolved(TypedDict):
    name: str
    path: str


class SkillsInfo(TypedDict):
    roots: list[str]
    referenced: list[str]
    resolved: list[SkillResolved]
    missing: list[SkillReference]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def extract_snippet(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def extract_candidate_commands(text: str) -> list[str]:
    commands = []
    in_code_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            if stripped and not stripped.startswith("#"):
                commands.append(stripped)
            continue
        inline = re.findall(r"`([^`]+)`", line)
        for cmd in inline:
            cmd_str = cmd.strip()
            if cmd_str:
                commands.append(cmd_str)
        if stripped.startswith("$"):
            cmd = stripped.lstrip("$ ")
            if cmd:
                commands.append(cmd)
        if any(keyword in stripped for keyword in COMMAND_KEYWORDS):
            commands.append(stripped)
    # Normalize and dedupe
    normalized = []
    seen = set()
    for cmd in commands:
        cleaned = cmd.strip()
        if not cleaned:
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        normalized.append(cleaned)
    return normalized


def extract_skill_refs(text: str) -> list[str]:
    refs = set(SKILL_REF_PATTERN.findall(text))
    refs.update(SKILL_PATH_PATTERN.findall(text))
    return sorted(refs)


def resolve_skills_roots(repo_root: Path) -> list[Path]:
    candidates = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(Path(codex_home) / "skills")
    candidates.append(repo_root / ".codex" / "skills")
    candidates.append(Path.home() / ".codex" / "skills")

    roots = []
    seen = set()
    for candidate in candidates:
        try:
            resolved = candidate.expanduser().resolve()
        except Exception:
            resolved = candidate.expanduser()
        key = str(resolved)
        if key in seen:
            continue
        seen.add(key)
        if resolved.exists():
            roots.append(resolved)
    return roots


def find_repo_signals(repo_root: Path, max_results: int = 200) -> list[dict]:
    results = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename in BUILD_SIGNAL_FILES:
                path = Path(dirpath) / filename
                results.append(
                    {
                        "path": str(path),
                        "type": "build_signal",
                    }
                )
                if len(results) >= max_results:
                    return results
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect deterministic evidence for codex-readiness-unit-test."
    )
    parser.add_argument(
        "--out-dir", default=".codex-readiness-unit-test", help="Base output directory"
    )
    parser.add_argument("--max-snippet-chars", type=int, default=2000, help="Max chars per snippet")
    args = parser.parse_args()

    cwd = Path.cwd()
    repo_root = cwd
    agents_path = cwd / "AGENTS.md"
    plans_path = cwd / "PLANS.md"

    snippets: list[dict[str, str]] = []
    candidate_commands: list[str] = []
    skill_refs: list[str] = []
    skills_info: SkillsInfo = cast(
        SkillsInfo,
        {
            "roots": [],
            "referenced": [],
            "resolved": [],
            "missing": [],
        },
    )
    if agents_path.exists():
        text = read_text(agents_path)
        if not text:
            text = ""
        snippets.append(
            {
                "path": str(agents_path),
                "snippet": extract_snippet(text, args.max_snippet_chars),
            }
        )
        if text:
            candidate_commands.extend(extract_candidate_commands(text))
            skill_refs = extract_skill_refs(text)

    if skill_refs:
        skills_info["referenced"] = skill_refs
        skills_roots = resolve_skills_roots(repo_root)
        skills_info["roots"] = [str(root) for root in skills_roots]
        for skill_name in skill_refs:
            skill_path = None
            for root in skills_roots:
                candidate = root / skill_name / "SKILL.md"
                if candidate.exists():
                    skill_path = candidate
                    break
            if skill_path is None:
                skills_info["missing"].append({"name": skill_name})
                continue
            skills_info["resolved"].append(
                {
                    "name": skill_name,
                    "path": str(skill_path),
                }
            )
            skill_text = read_text(skill_path)
            snippets.append(
                {
                    "path": str(skill_path),
                    "snippet": extract_snippet(skill_text, args.max_snippet_chars),
                }
            )
            if skill_text:
                candidate_commands.extend(extract_candidate_commands(skill_text))

    # De-duplicate candidate commands
    seen_cmds = set()
    unique_cmds = []
    for cmd in candidate_commands:
        if cmd in seen_cmds:
            continue
        seen_cmds.add(cmd)
        unique_cmds.append(cmd)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_time = datetime.now(timezone.utc)
    run_id = run_time.strftime("%Y-%m-%dT%H-%M-%SZ")
    run_dir = (out_dir / run_id).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    evidence: dict[str, Any] = cast(
        dict[str, Any],
        {
            "run_context": {
                "cwd": str(cwd),
                "repo_root": str(repo_root),
                "run_dir": str(run_dir),
                "run_id": run_id,
                "timestamp": run_time.isoformat(),
            },
            "agents_md": {
                "exists": agents_path.exists(),
                "path": str(agents_path) if agents_path.exists() else None,
            },
            "plans_md": {
                "exists": plans_path.exists(),
                "path": str(plans_path) if plans_path.exists() else None,
            },
            "skills": skills_info,
            "snippets": snippets,
            "inferred": {
                "candidate_commands": unique_cmds[:50],
                "repo_signals": find_repo_signals(repo_root),
            },
        },
    )

    evidence_path = run_dir / "evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    latest_path = out_dir / "latest.json"
    latest_payload = {
        "run_dir": str(run_dir),
        "run_id": run_id,
        "timestamp": evidence["run_context"]["timestamp"],
    }
    latest_path.write_text(json.dumps(latest_payload, indent=2), encoding="utf-8")

    print(str(evidence_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
