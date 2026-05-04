#!/usr/bin/env python3
"""Gate 5 - Static analysis audit. eslint/ruff/mypy/tsc all-strict."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402


def has_node_dep(project: Path, name: str) -> bool:
    pkg = project / "package.json"
    if not pkg.exists():
        return False
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        return False
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    return name in deps


def has_python_tool(project: Path, name: str) -> bool:
    for f in ("pyproject.toml", "requirements.txt", "setup.cfg"):
        p = project / f
        if p.exists() and name in p.read_text(encoding="utf-8", errors="ignore").lower():
            return True
    return False


def _missing_pkg(res) -> bool:
    blob = ((res.stdout or "") + "\n" + (res.stderr or "")).lower()
    needles = (
        "npx canceled due to missing packages",
        "could not determine executable",
        "command not found",
        "binary not found",
        "cannot find module",
        "enoent",
    )
    return any(n in blob for n in needles)


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-static")
    gate = "Gate 5: QA / Static"
    any_run = False

    if has_node_dep(project_dir, "eslint"):
        any_run = True
        res = run(["npx", "--no", "eslint", ".", "--max-warnings", "0"], cwd=str(project_dir), timeout=600)
        if res.exit_code not in (0, 127):
            if _missing_pkg(res):
                rep.add_finding(Severity.MEDIUM, gate, "eslint-not-installed",
                                "eslint binary missing locally; run `npm ci` to install before audit.",
                                "Install dependencies; CI is expected to satisfy this.")
            else:
                rep.add_finding(Severity.CRITICAL, gate, "eslint",
                                (res.stdout or res.stderr)[:500],
                                "Fix all eslint errors and warnings.")
    if has_node_dep(project_dir, "typescript"):
        any_run = True
        res = run(["npx", "--no", "tsc", "--noEmit"], cwd=str(project_dir), timeout=600)
        if res.exit_code not in (0, 127):
            if _missing_pkg(res):
                rep.add_finding(Severity.MEDIUM, gate, "tsc-not-installed",
                                "tsc binary missing locally; run `npm ci` to install before audit.",
                                "Install dependencies; CI is expected to satisfy this.")
            else:
                rep.add_finding(Severity.CRITICAL, gate, "tsc-noemit",
                                (res.stdout or res.stderr)[:500],
                                "Fix TypeScript type errors.")
    if has_python_tool(project_dir, "ruff"):
        any_run = True
        res = run(["ruff", "check", "."], cwd=str(project_dir), timeout=300)
        if res.exit_code not in (0, 127):
            rep.add_finding(Severity.CRITICAL, gate, "ruff",
                            (res.stdout or res.stderr)[:500],
                            "Fix ruff lint errors.")
    if has_python_tool(project_dir, "mypy"):
        any_run = True
        res = run(["mypy", "--strict", "."], cwd=str(project_dir), timeout=600)
        if res.exit_code not in (0, 127):
            rep.add_finding(Severity.CRITICAL, gate, "mypy-strict",
                            (res.stdout or res.stderr)[:500],
                            "Fix mypy --strict errors.")

    if not any_run:
        rep.add_finding(Severity.MEDIUM, gate, "static-analysis-missing",
                        "no eslint/tsc/ruff/mypy detected",
                        "Add at least one strict static analyzer.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: Static audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
