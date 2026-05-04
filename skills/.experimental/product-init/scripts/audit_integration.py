#!/usr/bin/env python3
"""Gate 5 - Integration test audit. Hunts for forbidden HTTP/DB mocks."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

MOCK_RE = re.compile(r"vi\.mock|jest\.mock|unittest\.mock|@patch|MagicMock|sinon\.stub")
NETWORK_RE = re.compile(
    r"\b(requests|httpx|aiohttp|axios|fetch|node-fetch|got|undici|urllib)\b"
)
DB_RE = re.compile(
    r"\b(sqlite|psycopg|psycopg2|prisma|sequelize|knex|sqlalchemy|mongoose|mongo|typeorm|pg|mysql)\b"
)
INT_FILE_RE = re.compile(r"(integration[/\\]|\.integration\.(test|spec)\.|\.integration_test\.)", re.IGNORECASE)


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-integration")
    gate = "Gate 5: QA / Integration"
    found = 0
    for path in project_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {"node_modules", ".git", "dist", "build", ".venv", "venv"} for part in path.parts):
            continue
        if not INT_FILE_RE.search(str(path)):
            continue
        found += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if MOCK_RE.search(text):
            mocks_network = NETWORK_RE.search(text) or DB_RE.search(text)
            sev = Severity.CRITICAL if mocks_network else Severity.MEDIUM
            ev = (
                f"{path.relative_to(project_dir)} mocks "
                f"{'network/DB layer' if mocks_network else 'something'}"
            )
            rep.add_finding(
                sev, gate, "integration-mock",
                ev,
                "Integration tests must hit real HTTP/DB. Move to unit suite or use real backend.",
            )
    if found == 0:
        rep.add_finding(Severity.HIGH, gate, "integration-coverage",
                        "no integration tests found",
                        "Add tests under integration/ or *.integration.test.* hitting real services.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: Integration audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
