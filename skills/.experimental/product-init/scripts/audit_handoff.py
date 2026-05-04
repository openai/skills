#!/usr/bin/env python3
"""Gate 8 - Handoff package audit."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

REQUIRED = ["README.md", "runbooks/runbook.md", "DEBT.md", "HANDOFF.md"]
HANDOFF_SECTIONS = ["Credentials Vault Link", "Admin Walkthrough Video", "Knowledge Transfer Date"]


def extract_section(text: str, heading: str) -> str:
    # Match any heading line whose visible text contains `heading` (case-insensitive substring).
    heading_line_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
    needle = heading.lower()
    match = None
    for m in heading_line_re.finditer(text):
        title = m.group(2).strip()
        if needle in title.lower():
            match = m
            break
    if not match:
        return ""
    matched_level = len(match.group(1))
    start = match.end()
    boundary_pattern = r"^#{1," + str(matched_level) + r"}[ \t]+"
    nxt = re.search(boundary_pattern, text[start:], re.MULTILINE)
    return text[start: start + nxt.start()] if nxt else text[start:]


def section_filled(text: str, heading: str) -> bool:
    body = extract_section(text, heading)
    if not body:
        return False
    cleaned = re.sub(r"\[FILL[^\]]*\]|TBD|TODO", "", body, flags=re.IGNORECASE).strip()
    return len(cleaned) > 5


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate8-handoff")
    gate = "Gate 8: Handoff"

    for rel in REQUIRED:
        path = project_dir / rel
        if not path.exists() or path.stat().st_size == 0:
            rep.add_finding(Severity.CRITICAL, gate, f"file:{rel}",
                            f"{rel} missing or empty",
                            f"Create {rel} with real content.")

    handoff = project_dir / "HANDOFF.md"
    if handoff.exists():
        text = handoff.read_text(encoding="utf-8", errors="ignore")
        for sec in HANDOFF_SECTIONS:
            if not section_filled(text, sec):
                rep.add_finding(Severity.HIGH, gate, f"handoff-section:{sec}",
                                f"`## {sec}` missing or unfilled",
                                f"Fill `## {sec}` in HANDOFF.md.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 8: Handoff audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
