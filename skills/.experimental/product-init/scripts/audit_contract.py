#!/usr/bin/env python3
"""Gate 5 - API contract audit. oasdiff for OpenAPI, graphql-inspector for GraphQL."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402


def find_first(project: Path, names):
    for n in names:
        p = project / n
        if p.exists():
            return p
    return None


def get_main_version(project: Path, rel_path: str) -> str:
    res = run(["git", "-C", str(project), "show", f"origin/main:{rel_path}"])
    return res.stdout if res.ok else ""


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-contract")
    gate = "Gate 5: QA / Contract"

    debt_text = ""
    debt = project_dir / "DEBT.md"
    if debt.exists():
        debt_text = debt.read_text(encoding="utf-8", errors="ignore")

    openapi = find_first(project_dir, ["openapi.yaml", "openapi.yml", "openapi.json"])
    if openapi:
        rel = openapi.relative_to(project_dir).as_posix()
        old_text = get_main_version(project_dir, rel)
        if old_text:
            tmp_old = project_dir / ".audit_openapi_main.tmp"
            tmp_old.write_text(old_text, encoding="utf-8")
            try:
                res = run(["oasdiff", "breaking", str(tmp_old), str(openapi)], cwd=str(project_dir))
                if res.exit_code == 127:
                    rep.add_finding(Severity.INFO, gate, "oasdiff-missing",
                                    "oasdiff binary not installed",
                                    "Install oasdiff: https://github.com/Tufin/oasdiff")
                elif res.exit_code != 0 and res.stdout.strip():
                    if "openapi" not in debt_text.lower():
                        rep.add_finding(Severity.CRITICAL, gate, "openapi-breaking",
                                        f"breaking changes detected:\n{res.stdout[:500]}",
                                        "Document the breaking change in DEBT.md or revert the API change.")
            finally:
                try:
                    tmp_old.unlink()
                except OSError:
                    pass
    graphql = find_first(project_dir, ["schema.graphql", "schema.gql"])
    if graphql:
        rel = graphql.relative_to(project_dir).as_posix()
        old_text = get_main_version(project_dir, rel)
        if old_text:
            tmp_old = project_dir / ".audit_schema_main.tmp"
            tmp_old.write_text(old_text, encoding="utf-8")
            try:
                res = run(["graphql-inspector", "diff", str(tmp_old), str(graphql)], cwd=str(project_dir))
                if res.exit_code == 127:
                    rep.add_finding(Severity.INFO, gate, "graphql-inspector-missing",
                                    "graphql-inspector not installed",
                                    "npm i -g @graphql-inspector/cli")
                elif res.exit_code != 0 and "BREAKING" in (res.stdout + res.stderr).upper():
                    if "graphql" not in debt_text.lower():
                        rep.add_finding(Severity.CRITICAL, gate, "graphql-breaking",
                                        "breaking GraphQL change without DEBT.md entry",
                                        "Document or revert.")
            finally:
                try:
                    tmp_old.unlink()
                except OSError:
                    pass

    if not openapi and not graphql:
        rep.add_finding(Severity.INFO, gate, "no-contract",
                        "no openapi.* or schema.graphql found",
                        "If your service has an API, ship a contract file.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: Contract audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
