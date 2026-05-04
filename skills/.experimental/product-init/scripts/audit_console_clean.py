#!/usr/bin/env python3
"""Cross-cutting: golden path must produce 0 console errors/warnings.

Parses Playwright trace JSON files for `type: console` entries with level
error/warning.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402


def walk_obj(obj, count):
    if isinstance(obj, dict):
        if obj.get("type") == "console" and obj.get("level") in ("error", "warning"):
            count[0] += 1
        for v in obj.values():
            walk_obj(v, count)
    elif isinstance(obj, list):
        for v in obj:
            walk_obj(v, count)


def audit(project_dir: Path) -> Report:
    rep = Report(name="cross-console-clean")
    gate = "Cross: Console Clean"
    total = [0]
    found_any = False
    for d in ("test-results", "playwright-report"):
        root = project_dir / d
        if not root.exists():
            continue
        for f in root.rglob("*.json"):
            found_any = True
            try:
                data = json.loads(f.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            walk_obj(data, total)
    if not found_any:
        rep.add_finding(Severity.INFO, gate, "no-traces",
                        "no Playwright trace files in test-results/ or playwright-report/",
                        "Run `npx playwright test` first.")
        return rep
    if total[0] > 0:
        rep.add_finding(Severity.HIGH, gate, "console-pollution",
                        f"{total[0]} console error/warning events on golden path",
                        "Fix console errors/warnings; required count is 0.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Cross: console clean")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
