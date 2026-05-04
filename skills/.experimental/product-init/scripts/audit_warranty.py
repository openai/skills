#!/usr/bin/env python3
"""Gate 9 - Warranty: audit scripts wired into CI + branch protection."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None

REQUIRED_SCRIPTS = ["audit_constitution", "audit_build", "audit_qa"]


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate9-warranty")
    gate = "Gate 9: Warranty"

    wf_dir = project_dir / ".github" / "workflows"
    if not wf_dir.exists():
        rep.add_finding(Severity.CRITICAL, gate, "workflows-missing",
                        ".github/workflows missing",
                        "Add CI workflows that run the audit suite.")
        return rep

    seen = set()
    for f in wf_dir.glob("*.yml"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for s in REQUIRED_SCRIPTS + ["audit_unit", "audit_e2e", "audit_integration",
                                     "audit_deploy", "audit_handoff", "audit_uat", "audit_sow"]:
            if s in text:
                seen.add(s)
        if yaml:
            try:
                yaml.safe_load(text)
            except Exception as e:
                rep.add_finding(Severity.HIGH, gate, f"yaml-syntax:{f.name}",
                                str(e)[:200],
                                "Fix YAML syntax in workflow.")
    for req in REQUIRED_SCRIPTS:
        if req not in seen:
            rep.add_finding(Severity.HIGH, gate, f"ci-missing:{req}",
                            f"{req} not referenced in any workflow",
                            f"Wire {req}.py into a CI job.")

    gh = run(["gh", "--version"])
    if gh.exit_code == 0:
        info = run(["gh", "api", "repos/:owner/:repo/branches/main/protection"], cwd=str(project_dir))
        if info.ok:
            try:
                data = json.loads(info.stdout)
                contexts = data.get("required_status_checks", {}).get("contexts", [])
                for req in REQUIRED_SCRIPTS:
                    if not any(req in c for c in contexts):
                        rep.add_finding(Severity.HIGH, gate, f"branch-protection:{req}",
                                        f"{req} not in required status checks",
                                        f"Add {req} to main branch protection required checks.")
            except Exception:
                rep.add_finding(Severity.LOW, gate, "branch-protection-parse",
                                "could not parse gh api output",
                                "Check `gh api repos/:owner/:repo/branches/main/protection` manually.")
        else:
            rep.add_finding(Severity.LOW, gate, "branch-protection-fetch",
                            "gh api failed (auth or repo); manual check required",
                            "Run `gh auth login` and `gh api .../branches/main/protection`.")
    else:
        rep.add_finding(Severity.LOW, gate, "gh-cli-missing",
                        "gh CLI not installed; cannot verify branch protection",
                        "Install gh or verify branch protection manually.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 9: Warranty audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
