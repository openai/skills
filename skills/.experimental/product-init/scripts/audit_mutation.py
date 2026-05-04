#!/usr/bin/env python3
"""Gate 5 - Mutation testing audit (Stryker / mutmut)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402

THRESHOLD = 60.0


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-mutation")
    gate = "Gate 5: QA / Mutation"

    stryker_cfg = None
    for name in ("stryker.conf.mjs", "stryker.conf.js", "stryker.conf.json", "stryker.config.mjs"):
        if (project_dir / name).exists():
            stryker_cfg = project_dir / name
            break
    mutmut_cfg = None
    for name in ("mutmut.cfg", "setup.cfg", "pyproject.toml"):
        p = project_dir / name
        if p.exists() and "mutmut" in p.read_text(encoding="utf-8", errors="ignore").lower():
            mutmut_cfg = p
            break

    if not stryker_cfg and not mutmut_cfg:
        rep.add_finding(Severity.INFO, gate, "mutation-not-configured",
                        "no Stryker or mutmut config",
                        "Optional but recommended: configure mutation testing.")
        return rep

    if stryker_cfg:
        res = run(["npx", "--no", "stryker", "run"], cwd=str(project_dir), timeout=1800)
        json_report = project_dir / "reports" / "mutation" / "mutation-report.json"
        if json_report.exists():
            try:
                data = json.loads(json_report.read_text(encoding="utf-8"))
                score = data.get("mutationScore") or data.get("score") or 0
            except Exception:
                score = 0
        else:
            m = re.search(r"mutation score[:\s]+(\d+\.?\d*)", res.stdout, re.IGNORECASE)
            score = float(m.group(1)) if m else 0
        if score < THRESHOLD:
            rep.add_finding(Severity.HIGH, gate, "stryker-score",
                            f"Stryker mutation score {score:.1f}% < {THRESHOLD}%",
                            "Strengthen tests so they kill more mutants.")

    if mutmut_cfg:
        res = run(["mutmut", "run"], cwd=str(project_dir), timeout=1800)
        result = run(["mutmut", "results"], cwd=str(project_dir))
        text = result.stdout
        killed = len(re.findall(r"killed", text, re.IGNORECASE))
        survived = len(re.findall(r"survived", text, re.IGNORECASE))
        total = killed + survived
        score = (killed / total * 100) if total else 0
        if total and score < THRESHOLD:
            rep.add_finding(Severity.HIGH, gate, "mutmut-score",
                            f"mutmut score {score:.1f}% < {THRESHOLD}%",
                            "Strengthen tests; kill more mutants.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: Mutation audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
