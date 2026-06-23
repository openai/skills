#!/usr/bin/env python3
"""Emit a machine-readable certificate for a CHC repair verification."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_verifier():
    script = Path(__file__).resolve().with_name("chc_verify_repair.py")
    spec = importlib.util.spec_from_file_location("chc_verify_repair", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load repair verifier from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["chc_verify_repair"] = module
    spec.loader.exec_module(module)
    return module


def load_obligations(path: str | None) -> list[dict[str, Any]] | None:
    if not path:
        return None
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("proof_obligations"), list):
        return data["proof_obligations"]
    return None


def certificate_from_verification(verification: dict[str, Any]) -> dict[str, Any]:
    return {
        "certificate_version": "1.0",
        "claim": "prediction_feedback_removed",
        "before_classification": verification.get("before_classification"),
        "after_classification": verification.get("after_classification"),
        "obligations_checked": verification.get("proof_obligations", []),
        "evidence_paths": {
            "before_feedback_paths": verification.get("before_feedback_paths", []),
            "after_feedback_paths": verification.get("after_feedback_paths", []),
        },
        "result": verification.get("verification"),
        "capability_boundary": verification.get(
            "capability_boundary",
            {
                "does_not_prove_arbitrary_termination": True,
                "does_not_solve_classical_halting": True,
            },
        ),
        "explanation": verification.get("explanation", ""),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a CHC repair certificate.")
    parser.add_argument("before", help="Before trace JSONL file.")
    parser.add_argument("after", help="After trace JSONL file.")
    parser.add_argument("--repair", help="Repair JSON with proof_obligations.")
    parser.add_argument("--format", choices=("json", "human"), default="json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    verifier = load_verifier()
    obligations = load_obligations(args.repair)
    verification = verifier.verify_repair(
        Path(args.before).read_text(encoding="utf-8"),
        Path(args.after).read_text(encoding="utf-8"),
        obligations,
    )
    certificate = certificate_from_verification(verification)
    if args.format == "json":
        print(json.dumps(certificate, indent=2, sort_keys=True))
    else:
        print(f"claim: {certificate['claim']}")
        print(f"result: {certificate['result']}")
        print(f"before_classification: {certificate['before_classification']}")
        print(f"after_classification: {certificate['after_classification']}")
    return 0 if certificate["result"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
