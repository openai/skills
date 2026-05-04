#!/usr/bin/env python3
"""Gate 4 - Build hygiene audit.

- New TODO/FIXME/XXX/HACK markers must have corresponding DEBT.md entries.
- New skipped tests are HIGH.
- Every commit message must contain a ticket id like ABC-123.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402

DEBT_RE = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")
SKIP_RE = re.compile(r"(\.skip\b|\.only\b|it\.todo\b|xfail\b|@pytest\.mark\.skip)")
TEST_FILE_RE = re.compile(r"(test|spec|__tests__)", re.IGNORECASE)
TICKET_RE = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


def is_git(project: Path) -> bool:
    return (project / ".git").exists() or run(["git", "-C", str(project), "rev-parse", "--git-dir"]).ok


def parse_diff_added(diff_text: str):
    cur_file = None
    cur_line = 0
    out = []
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            cur_file = raw[6:]
            cur_line = 0
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            cur_line = int(m.group(1)) if m else 0
        elif raw.startswith("+") and not raw.startswith("+++"):
            out.append((cur_file, cur_line, raw[1:]))
            cur_line += 1
        elif not raw.startswith("-"):
            cur_line += 1
    return out


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate4-build")
    gate = "Gate 4: Build"

    if not is_git(project_dir):
        rep.add_finding(Severity.LOW, gate, "git-repo", "not a git repo",
                        "Initialize git so build hygiene can be enforced.")
        return rep

    diff = run(["git", "-C", str(project_dir), "diff", "origin/main...HEAD"])
    if diff.exit_code != 0:
        diff = run(["git", "-C", str(project_dir), "diff", "HEAD"])
    added = parse_diff_added(diff.stdout)

    debt_text = ""
    debt_path = project_dir / "DEBT.md"
    if debt_path.exists():
        debt_text = debt_path.read_text(encoding="utf-8", errors="ignore")

    for fpath, lineno, content in added:
        if not fpath:
            continue
        if DEBT_RE.search(content):
            needle = f"{fpath}:{lineno}"
            if needle not in debt_text:
                rep.add_finding(
                    Severity.HIGH, gate, "todo-without-debt-ledger",
                    f"{needle} adds TODO/FIXME but no row in DEBT.md",
                    f"Add row to DEBT.md referencing `{needle}` or remove the marker.",
                )
        if TEST_FILE_RE.search(fpath) and SKIP_RE.search(content):
            rep.add_finding(
                Severity.HIGH, gate, "skipped-test",
                f"{fpath}:{lineno} adds skipped/only test",
                "Re-enable the test or delete it; do not check in skipped tests.",
            )

    log = run(["git", "-C", str(project_dir), "log", "--oneline", "origin/main..HEAD"])
    if log.exit_code == 0 and log.stdout.strip():
        for line in log.stdout.splitlines():
            sha, _, msg = line.partition(" ")
            if not TICKET_RE.search(msg):
                rep.add_finding(
                    Severity.MEDIUM, gate, "commit-ticket",
                    f"commit {sha} '{msg}' missing TICKET-123 reference",
                    "Amend commits to include the ticket id (e.g. ABC-123).",
                )
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 4: Build audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
