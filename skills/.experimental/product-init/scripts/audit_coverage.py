#!/usr/bin/env python3
"""Gate 5 - diff coverage audit (>= 80% on changed lines)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402

THRESHOLD = 80.0


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-coverage")
    gate = "Gate 5: QA / Coverage"

    res = run(["diff-cover", "coverage.xml", "--compare-branch=origin/main", "--json-report", "diff-cover.json"],
              cwd=str(project_dir))
    if res.exit_code == 127:
        cov_xml = project_dir / "coverage.xml"
        cov_json = project_dir / "coverage" / "coverage-final.json"
        if cov_xml.exists():
            text = cov_xml.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'line-rate="([\d.]+)"', text)
            pct = float(m.group(1)) * 100 if m else 0
            if pct < THRESHOLD:
                rep.add_finding(Severity.HIGH, gate, "coverage-line-rate",
                                f"coverage.xml line-rate {pct:.1f}% < {THRESHOLD}%",
                                "Raise coverage on changed code or install diff-cover.")
        elif cov_json.exists():
            try:
                data = json.loads(cov_json.read_text(encoding="utf-8"))
                covered = total = 0
                for f in data.values():
                    s = f.get("s", {}) if isinstance(f, dict) else {}
                    total += len(s)
                    covered += sum(1 for v in s.values() if v)
                pct = (covered / total * 100) if total else 0
                if pct < THRESHOLD:
                    rep.add_finding(Severity.HIGH, gate, "coverage-istanbul",
                                    f"overall coverage {pct:.1f}% < {THRESHOLD}%",
                                    "Add tests; install diff-cover for diff-only thresholds.")
            except Exception:
                rep.add_finding(Severity.INFO, gate, "coverage-parse",
                                "could not parse coverage-final.json",
                                "Verify coverage report format.")
        else:
            rep.add_finding(Severity.INFO, gate, "coverage-tool-missing",
                            "diff-cover not installed and no coverage report present",
                            "pip install diff-cover, run with coverage.xml")
        return rep

    report_path = project_dir / "diff-cover.json"
    if report_path.exists():
        try:
            data = json.loads(report_path.read_text(encoding="utf-8"))
            pct = data.get("total_percent_covered", 100)
            if pct < THRESHOLD:
                rep.add_finding(Severity.HIGH, gate, "diff-cover",
                                f"diff coverage {pct:.1f}% < {THRESHOLD}%",
                                "Add tests for changed lines.")
        except Exception:
            pass
    elif res.exit_code != 0:
        rep.add_finding(Severity.HIGH, gate, "diff-cover-failed",
                        f"diff-cover failed: {res.stderr[:200]}",
                        "Inspect diff-cover output.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: Coverage audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
