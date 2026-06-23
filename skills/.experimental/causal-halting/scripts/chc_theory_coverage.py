#!/usr/bin/env python3
"""Report Causal Halting operational/formal theorem coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


EXPECTED = {
    "CHC-0": ["finite reachability", "acyclic_unif decidability", "diagonal rejection"],
    "CHC-1": ["monotone effect summaries", "non-convergence is insufficient_info"],
    "CHC-2": ["effect annotation requirement", "callback composition includes effects"],
    "CHC-3": ["process/session non-interference"],
    "CHC-4": ["happens-before feedback rejection"],
    "CHC-5": ["prediction confidence ignored for feedback classification"],
}


def lean_text() -> str:
    formal = ROOT / "formal" / "lean"
    return "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in formal.rglob("*.lean"))


def coverage() -> dict[str, Any]:
    text = lean_text()
    levels: dict[str, dict[str, Any]] = {}
    for level, claims in EXPECTED.items():
        mechanized = []
        for claim in claims:
            needle = claim.replace("-", "_").replace("/", "_").replace(" ", "_").lower()
            if needle in text.lower():
                mechanized.append(claim)
        levels[level] = {
            "expected_claims": claims,
            "mechanized_claims": mechanized,
            "status": "mechanized" if len(mechanized) == len(claims) else "partial",
        }
    return {
        "coverage_version": "1.0",
        "levels": levels,
        "capability_boundary": {
            "does_not_prove_arbitrary_termination": True,
            "does_not_solve_classical_halting": True,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize CHC theory coverage.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args(argv)
    result = coverage()
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for level, payload in result["levels"].items():
            print(f"{level}: {payload['status']} ({len(payload['mechanized_claims'])}/{len(payload['expected_claims'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
