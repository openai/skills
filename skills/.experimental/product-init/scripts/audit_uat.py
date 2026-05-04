#!/usr/bin/env python3
"""Gate 6 - UAT audit. Looks for uat specs, signed UAT report, and uat-v* tag."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402


UAT_FILE_RE = re.compile(r".*\.uat\.spec\.(ts|js|py)$", re.IGNORECASE)


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate6-uat")
    gate = "Gate 6: UAT"

    uat_dir = project_dir / "e2e" / "uat"
    matches = []
    if uat_dir.exists():
        matches = [p for p in uat_dir.rglob("*") if p.is_file() and UAT_FILE_RE.match(p.name)]
    if not matches:
        rep.add_finding(Severity.HIGH, gate, "uat-spec",
                        "no e2e/uat/*.uat.spec.{ts,js,py} found",
                        "Add at least one UAT spec walking the live URL.")

    report_path = project_dir / "UAT_REPORT.md"
    if not report_path.exists():
        rep.add_finding(Severity.CRITICAL, gate, "uat-report",
                        "UAT_REPORT.md missing",
                        "Generate UAT_REPORT.md with sha256 of build and Signed-off-by line.")
    else:
        text = report_path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"^sha256:", text, re.MULTILINE | re.IGNORECASE):
            rep.add_finding(Severity.HIGH, gate, "uat-sha256",
                            "no `sha256:` line in UAT_REPORT.md",
                            "Add `sha256: <hash>` of the artifact under test.")
        if not re.search(r"^Signed-off-by:", text, re.MULTILINE | re.IGNORECASE):
            rep.add_finding(Severity.HIGH, gate, "uat-signoff",
                            "no `Signed-off-by:` line",
                            "Have the user sign off explicitly.")

    res = run(["git", "-C", str(project_dir), "tag", "--list", "uat-v*"])
    if res.ok and not res.stdout.strip():
        rep.add_finding(Severity.HIGH, gate, "uat-tag",
                        "no git tag matching uat-v*",
                        "Tag the commit accepted by the user, e.g. `git tag uat-v1.0.0`.")
    elif res.exit_code == 127:
        rep.add_finding(Severity.LOW, gate, "git-missing",
                        "git not available",
                        "Install git to enable tag verification.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 6: UAT audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
