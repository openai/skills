#!/usr/bin/env python3
"""Gate 5 - QA aggregator. Runs all 8 sub-audits and merges findings."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

SUB_AUDITS = [
    "audit_unit",
    "audit_integration",
    "audit_e2e",
    "audit_contract",
    "audit_coverage",
    "audit_mutation",
    "audit_static",
    "audit_console_clean",
]


def run_sub(name: str, project_dir: str) -> tuple[dict | None, int]:
    script = Path(__file__).resolve().parent / f"{name}.py"
    if not script.exists():
        return (None, 0)
    proc = subprocess.run(
        [sys.executable, "-B", str(script), "--project-dir", project_dir, "--json"],
        capture_output=True,
        text=True,
        timeout=1200,
    )
    try:
        data = json.loads(proc.stdout)
    except Exception:
        data = None
    return (data, proc.returncode)


def audit(project_dir: Path) -> tuple[Report, int]:
    rep = Report(name="gate5-qa-aggregate")
    max_exit = 0
    for sub in SUB_AUDITS:
        data, rc = run_sub(sub, str(project_dir))
        max_exit = max(max_exit, rc)
        if not data:
            rep.add_finding(
                Severity.HIGH,
                "Gate 5: QA",
                f"sub-audit:{sub}",
                f"could not parse JSON output from {sub}",
                f"Run `python3 scripts/{sub}.py --project-dir <dir> --json` to debug.",
            )
            continue
        for f in data.get("findings", []):
            try:
                sev = Severity(f.get("severity", "INFO"))
            except ValueError:
                sev = Severity.INFO
            rep.add_finding(
                sev,
                f.get("gate", "Gate 5: QA"),
                f"{sub}:{f.get('check', '')}",
                f.get("evidence", ""),
                f.get("fix", ""),
            )
    return rep, max_exit


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: QA aggregate audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep, sub_max = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return max(rep.exit_code, sub_max)


if __name__ == "__main__":
    sys.exit(main())
