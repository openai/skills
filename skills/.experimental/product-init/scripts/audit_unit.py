#!/usr/bin/env python3
"""Gate 5 - Unit test audit. Detects vitest/jest/pytest, runs, parses results."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402


def detect_node(project: Path):
    pkg = project / "package.json"
    if not pkg.exists():
        return None
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        return None
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    if "vitest" in deps:
        return "vitest"
    if "jest" in deps:
        return "jest"
    return None


def detect_python(project: Path):
    for f in ("pyproject.toml", "setup.cfg", "pytest.ini", "tox.ini"):
        p = project / f
        if p.exists() and "pytest" in p.read_text(encoding="utf-8", errors="ignore").lower():
            return "pytest"
    if any(project.rglob("conftest.py")):
        return "pytest"
    return None


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-unit")
    gate = "Gate 5: QA / Unit"

    runner_node = detect_node(project_dir)
    runner_py = detect_python(project_dir)

    if not runner_node and not runner_py:
        rep.add_finding(Severity.MEDIUM, gate, "test-runner",
                        "no vitest/jest/pytest detected",
                        "Add a unit test runner; this gate cannot pass without one.")
        return rep

    if runner_node == "vitest":
        res = run(["npx", "--no", "vitest", "run", "--reporter=json"], cwd=str(project_dir), timeout=600)
        parse_node_json(res.stdout, rep, gate, res.stderr)
    elif runner_node == "jest":
        res = run(["npx", "--no", "jest", "--json", "--ci"], cwd=str(project_dir), timeout=600)
        parse_node_json(res.stdout, rep, gate, res.stderr)
    if runner_py:
        res = run(["pytest", "--tb=no", "-q", "--json-report", "--json-report-file=-"],
                  cwd=str(project_dir), timeout=600)
        parse_pytest(res.stdout, res.stderr, rep, gate)
    return rep


def _looks_like_missing_package(text: str, stderr: str = "") -> bool:
    blob = (text or "") + "\n" + (stderr or "")
    needles = (
        "npx canceled due to missing packages",
        "could not determine executable",
        "command not found",
        "binary not found",
        "Cannot find module",
        "ENOENT",
    )
    return any(n.lower() in blob.lower() for n in needles)


def parse_node_json(text: str, rep: Report, gate: str, stderr: str = "") -> None:
    try:
        data = json.loads(text)
    except Exception:
        if _looks_like_missing_package(text, stderr):
            rep.add_finding(Severity.MEDIUM, gate, "unit-runner-not-installed",
                            "test runner not installed locally (sandbox/CI may differ)",
                            "Run `npm ci` so vitest/jest is available, then re-run.")
        else:
            rep.add_finding(Severity.HIGH, gate, "unit-runner",
                            "could not parse JSON output from test runner",
                            "Re-run locally and inspect output.")
        return
    failed = data.get("numFailedTests", 0)
    skipped = data.get("numPendingTests", 0) + data.get("numTodoTests", 0)
    if failed:
        rep.add_finding(Severity.CRITICAL, gate, "unit-failed",
                        f"{failed} failing tests", "Fix all failing unit tests.")
    if skipped:
        rep.add_finding(Severity.HIGH, gate, "unit-skipped",
                        f"{skipped} skipped/todo tests",
                        "Skipped tests are forbidden at gate close; re-enable or remove.")


def parse_pytest(stdout: str, stderr: str, rep: Report, gate: str) -> None:
    blob = stdout
    try:
        data = json.loads(blob)
        summary = data.get("summary", {})
        failed = summary.get("failed", 0)
        skipped = summary.get("skipped", 0) + summary.get("xfailed", 0)
    except Exception:
        text = stdout + "\n" + stderr
        m = re.search(r"(\d+)\s+failed", text)
        failed = int(m.group(1)) if m else 0
        m = re.search(r"(\d+)\s+skipped", text)
        skipped = int(m.group(1)) if m else 0
    if failed:
        rep.add_finding(Severity.CRITICAL, gate, "pytest-failed",
                        f"{failed} failing pytest tests", "Fix failing tests.")
    if skipped:
        rep.add_finding(Severity.HIGH, gate, "pytest-skipped",
                        f"{skipped} skipped/xfail",
                        "Re-enable or remove; skipped tests block the gate.")


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: Unit test audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
