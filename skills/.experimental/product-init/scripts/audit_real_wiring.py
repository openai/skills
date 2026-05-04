#!/usr/bin/env python3
"""Cross-cutting: detect mock/stub/localhost references in non-test source."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

ROOTS = ["src", "app", "frontend", "backend", "lib"]
SKIP_PARTS = {"node_modules", ".git", "dist", "build", ".venv", "venv", "__pycache__", "coverage"}
TEST_RE = re.compile(r"(\.test\.|\.spec\.|__tests__|/tests?/)", re.IGNORECASE)
SUSPECT_RE = re.compile(
    r"\b(import\s+.*\bmock\b|fakeApi|stubApi|MockAdapter|localhost|127\.0\.0\.1)",
    re.IGNORECASE,
)


def audit(project_dir: Path) -> Report:
    rep = Report(name="cross-real-wiring")
    gate = "Cross: Real Wiring"
    scanned = 0
    hits = 0
    for root in ROOTS:
        rdir = project_dir / root
        if not rdir.exists():
            continue
        for p in rdir.rglob("*"):
            if not p.is_file():
                continue
            if any(part in SKIP_PARTS for part in p.parts):
                continue
            if TEST_RE.search(str(p)):
                continue
            if p.suffix not in {".ts", ".tsx", ".js", ".jsx", ".py", ".mjs", ".cjs", ".vue", ".svelte"}:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned += 1
            for m in SUSPECT_RE.finditer(text):
                lineno = text[: m.start()].count("\n") + 1
                hits += 1
                rep.add_finding(
                    Severity.HIGH, gate, "mock-or-localhost-in-source",
                    f"{p.relative_to(project_dir)}:{lineno} -> {m.group(0)[:80]}",
                    "Replace with real client; route via env-configured base URL.",
                )
    if scanned == 0:
        rep.add_finding(Severity.INFO, gate, "no-source-roots",
                        "no src/app/frontend/backend/lib directory found",
                        "Confirm project layout; nothing to scan.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Cross: real-wiring audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
