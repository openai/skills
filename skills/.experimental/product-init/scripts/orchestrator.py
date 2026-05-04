#!/usr/bin/env python3
"""product-init orchestrator. Subcommands: init, gate, filter, audit."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Runtime-portable skill dir resolution:
# 1. $PRODUCT_INIT_SKILL_DIR env var
# 2. ~/.openclaw/skills/product-init/  (if exists and is a real dir)
# 3. ~/.claude/skills/product-init/    (canonical install)
# 4. parent of this script             (fallback for dev/testing)
def _resolve_skill_dir() -> Path:
    if env := os.environ.get("PRODUCT_INIT_SKILL_DIR"):
        return Path(env).resolve()
    for candidate in (
        Path.home() / ".openclaw" / "skills" / "product-init",
        Path.home() / ".claude" / "skills" / "product-init",
    ):
        resolved = candidate.resolve()
        if resolved.is_dir():
            return resolved
    return Path(__file__).resolve().parent.parent

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = _resolve_skill_dir()
TEMPLATES_DIR = SKILL_DIR / "templates"

sys.path.insert(0, str(SCRIPTS_DIR))
from lib.report import Report, Severity  # noqa: E402

GATE_SCRIPTS = {
    1: ["audit_constitution.py"],
    2: ["audit_sow.py"],
    3: [],  # design - manual review (no programmatic audit yet)
    4: ["audit_build.py", "audit_real_wiring.py"],
    5: [
        "audit_unit.py",
        "audit_integration.py",
        "audit_e2e.py",
        "audit_contract.py",
        "audit_coverage.py",
        "audit_mutation.py",
        "audit_static.py",
        "audit_console_clean.py",
    ],
    6: ["audit_uat.py"],
    7: ["audit_deploy.py", "audit_demo_url.py"],
    8: ["audit_handoff.py"],
    9: ["audit_warranty.py"],
}


def run_script(name: str, project_dir: Path, as_json: bool = True):
    cmd = [sys.executable, str(SCRIPTS_DIR / name), "--project-dir", str(project_dir)]
    if as_json:
        cmd.append("--json")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc


def cmd_init(args) -> int:
    project = Path(args.project_dir).resolve()
    project.mkdir(parents=True, exist_ok=True)
    if not TEMPLATES_DIR.exists():
        print(f"Templates not found at {TEMPLATES_DIR}", file=sys.stderr)
        return 2
    copied = []
    for tpl in TEMPLATES_DIR.glob("*.md"):
        dest = project / tpl.name
        if dest.exists() and not args.force:
            continue
        shutil.copy2(tpl, dest)
        copied.append(tpl.name)
    print(f"Initialized product-init in {project}")
    print(f"Idea: {args.idea}")
    print(f"Copied {len(copied)} templates: {', '.join(copied) if copied else '(none new)'}")
    print("Next: fill PRODUCT.md, SPEC.md, PLAN.md, TASKS.md, COMPETITIVE_BENCHMARK.md, then run `gate 1`.")
    return 0


def cmd_gate(args) -> int:
    project = Path(args.project_dir).resolve()
    n = args.n
    scripts = GATE_SCRIPTS.get(n)
    if scripts is None:
        print(f"Unknown gate {n}", file=sys.stderr)
        return 2
    if not scripts:
        print(f"Gate {n}: manual review required (no programmatic audit).")
        return 0
    aggregate = Report(name=f"gate{n}")
    for s in scripts:
        proc = run_script(s, project, as_json=True)
        try:
            data = json.loads(proc.stdout)
            for f in data.get("findings", []):
                aggregate.add_finding(
                    Severity(f["severity"]), f["gate"], f["check"], f["evidence"], f["fix"]
                )
        except Exception:
            print(f"[warn] could not parse {s} output: {proc.stdout[:200]}", file=sys.stderr)
    print(aggregate.to_json() if args.json else aggregate.to_markdown())
    return aggregate.exit_code


def cmd_filter(args) -> int:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "filter_task.py"), args.task],
        capture_output=True, text=True,
    )
    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")
    return proc.returncode


def cmd_audit(args) -> int:
    project = Path(args.project_dir).resolve()
    aggregate = Report(name="full-audit")
    for n in sorted(GATE_SCRIPTS):
        for s in GATE_SCRIPTS[n]:
            proc = run_script(s, project, as_json=True)
            try:
                data = json.loads(proc.stdout)
                for f in data.get("findings", []):
                    aggregate.add_finding(
                        Severity(f["severity"]), f["gate"], f["check"], f["evidence"], f["fix"]
                    )
            except Exception:
                print(f"[warn] could not parse {s}: {proc.stdout[:200]}", file=sys.stderr)
    print(aggregate.to_json() if args.json else aggregate.to_markdown())
    return aggregate.exit_code


def main() -> int:
    p = argparse.ArgumentParser(prog="product-init")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Bootstrap a new product project")
    p_init.add_argument("idea", help="One-line product idea")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_gate = sub.add_parser("gate", help="Run audits for gate N")
    p_gate.add_argument("n", type=int, choices=range(1, 10))
    p_gate.add_argument("--json", action="store_true")
    p_gate.set_defaults(func=cmd_gate)

    p_filter = sub.add_parser("filter", help="Filter a task against the golden path")
    p_filter.add_argument("task", help="Task description")
    p_filter.set_defaults(func=cmd_filter)

    p_audit = sub.add_parser("audit", help="Run all audits")
    p_audit.add_argument("--json", action="store_true")
    p_audit.set_defaults(func=cmd_audit)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
