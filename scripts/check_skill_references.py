#!/usr/bin/env python3
"""Validate backticked skill-local resource references in SKILL.md files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


RESOURCE_PREFIXES = (
    "references/",
    "reference/",
    "scripts/",
    "assets/",
    "agents/",
    "examples/",
    "evaluations/",
)

BACKTICK_PATTERN = re.compile(r"`([^`\n]+)`")
EXAMPLE_HINT_PATTERN = re.compile(r"\bexamples?\b", re.IGNORECASE)
IGNORED_SKILL_FILES = {
    Path("skills/.system/skill-creator/SKILL.md"),
}


def _iter_candidate_paths(token: str) -> list[str]:
    candidates: list[str] = []
    cleaned = token.strip().strip("'\"")
    for part in re.split(r"\s+", cleaned):
        part = part.strip().rstrip(".,;:)")
        if not part:
            continue
        if not part.startswith(RESOURCE_PREFIXES):
            continue
        if part in RESOURCE_PREFIXES:
            continue
        if any(ch in part for ch in ("*", "<", ">", "|", "$", "?", "#")):
            continue
        candidates.append(part)
    return candidates


def _check_skill_file(skill_md: Path) -> list[tuple[int, str]]:
    missing: list[tuple[int, str]] = []
    in_fence = False

    for line_no, raw in enumerate(skill_md.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if EXAMPLE_HINT_PATTERN.search(raw):
            continue

        for match in BACKTICK_PATTERN.finditer(raw):
            for rel_path in _iter_candidate_paths(match.group(1)):
                if not (skill_md.parent / rel_path).exists():
                    missing.append((line_no, rel_path))

    return missing


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skills_root = repo_root / "skills"
    if not skills_root.exists():
        print(f"skills root not found: {skills_root}", file=sys.stderr)
        return 2

    problems: list[tuple[Path, int, str]] = []
    for skill_md in sorted(skills_root.glob("**/SKILL.md")):
        if skill_md.relative_to(repo_root) in IGNORED_SKILL_FILES:
            continue
        for line_no, rel_path in _check_skill_file(skill_md):
            problems.append((skill_md, line_no, rel_path))

    if not problems:
        print("check_skill_references: ok")
        return 0

    print("check_skill_references: missing references found")
    for skill_md, line_no, rel_path in problems:
        print(f"- {skill_md}:{line_no}: {rel_path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
