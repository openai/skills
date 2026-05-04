#!/usr/bin/env python3
"""Gate 2 - Statement of Work audit."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

BANNED = ["RBAC", "compliance", "marketplace", "multi-region", "observability", "integrations"]

DEFERRED_HEADING_MARKERS = ("deferred", "post-mvp", "post mvp", "out of scope", "out-of-scope", "backlog", "not in scope")


def split_active_vs_deferred(text: str) -> tuple[str, str]:
    """Partition markdown text into (active_mvp, deferred) by scanning headings."""
    heading_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
    matches = list(heading_re.finditer(text))
    if not matches:
        return text, ""
    active_parts: list[str] = []
    deferred_parts: list[str] = []
    # Prefix before first heading is always active.
    active_parts.append(text[: matches[0].start()])
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start(): end]
        title = m.group(2).strip().lower()
        is_deferred = any(marker in title for marker in DEFERRED_HEADING_MARKERS)
        if is_deferred:
            deferred_parts.append(block)
        else:
            active_parts.append(block)
    return "".join(active_parts), "".join(deferred_parts)


def extract_block(text: str, heading_substr: str) -> str:
    """Return body of the first heading whose title contains heading_substr (ci)."""
    heading_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
    needle = heading_substr.lower()
    matches = list(heading_re.finditer(text))
    for i, m in enumerate(matches):
        title = m.group(2).strip().lower()
        if needle in title:
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[start:end]
    return ""


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate2-sow")
    gate = "Gate 2: SoW"
    plan_path = project_dir / "PLAN.md"
    tasks_path = project_dir / "TASKS.md"

    if not plan_path.exists():
        rep.add_finding(Severity.CRITICAL, gate, "plan-exists", "PLAN.md missing",
                        "Create PLAN.md from templates/")
        return rep

    plan = read(plan_path)

    # Bug 4 fix: Find ## Appetite section, then look for any numeric value inside.
    appetite_block = extract_block(plan, "appetite")
    appetite_numeric_re = re.compile(
        r"\d+\s*(week|day|sprint|hour|month)s?\b|\$\s*\d|\d+\s*(usd|tl|eur|gbp)\b",
        re.IGNORECASE,
    )
    if not appetite_block or not appetite_numeric_re.search(appetite_block):
        rep.add_finding(Severity.HIGH, gate, "appetite-numeric",
                        "no numeric appetite (e.g., '4 weeks', '$15k')",
                        "Add `Appetite: N weeks` under ## Appetite.")

    # Bug 5 fix: kill criteria bullets — accept dash/star OR numbered list.
    kill_block = extract_block(plan, "kill criteria")
    bullets = re.findall(r"^\s*(?:[-*]|\d+\.)\s+\S", kill_block, re.MULTILINE)
    if len(bullets) < 1:
        rep.add_finding(Severity.HIGH, gate, "kill-criteria",
                        "no kill criteria bullets",
                        "Add at least one falsifiable kill condition.")

    deferred_block = extract_block(plan, "deferred")
    deferred_bullets = re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)", deferred_block, re.MULTILINE)
    if len(deferred_bullets) < 3:
        rep.add_finding(Severity.HIGH, gate, "deferred-list-size",
                        f"only {len(deferred_bullets)} deferred items",
                        "List at least 3 deferred items.")
    hits = sum(1 for b in BANNED if b.lower() in deferred_block.lower())
    if hits < 3:
        rep.add_finding(Severity.HIGH, gate, "deferred-list-coverage",
                        f"only {hits} of {BANNED} mentioned in deferred",
                        "Defer at least 3 of: RBAC, compliance, marketplace, multi-region, observability, integrations.")

    # Bug 3 fix: only flag BANNED terms in the active MVP partition of TASKS.md.
    if tasks_path.exists():
        tasks = read(tasks_path)
        active_tasks, _deferred_tasks = split_active_vs_deferred(tasks)
        for term in BANNED:
            if re.search(rf"\b{re.escape(term)}\b", active_tasks, re.IGNORECASE):
                rep.add_finding(Severity.CRITICAL, gate, f"mvp-bans:{term}",
                                f"'{term}' present in TASKS.md",
                                f"Move {term} to PLAN.md deferred list.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 2: SoW audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
