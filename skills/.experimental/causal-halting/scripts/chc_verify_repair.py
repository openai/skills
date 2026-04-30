#!/usr/bin/env python3
"""Verify that a Causal Halting repair removes same-run feedback."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


CAPABILITY_BOUNDARY = {
    "does_not_prove_arbitrary_termination": True,
    "does_not_solve_classical_halting": True,
}


def load_trace_checker():
    script = Path(__file__).resolve().with_name("chc_trace_check.py")
    spec = importlib.util.spec_from_file_location("chc_trace_check", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load trace checker from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["chc_trace_check"] = module
    spec.loader.exec_module(module)
    return module


def obligation_status(obligation: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    name = obligation.get("obligation")
    result_id = obligation.get("result_id")
    forbidden_consumer = obligation.get("forbidden_consumer_exec_id")
    paths = list(after.get("feedback_paths", [])) + list(after.get("valid_paths", []))
    matching_paths = [path for path in paths if result_id in (None, path.get("result_id"))]

    if name in {
        "prediction_result_not_consumed_by_observed_execution",
        "result_not_consumed_by_observed_execution_before_end",
    }:
        violating = [
            path
            for path in matching_paths
            if (
                path.get("consumer_exec_id") == forbidden_consumer
                or path.get("target_exec_id") == forbidden_consumer
                or path.get("controlled_exec_id") == forbidden_consumer
            )
            and path.get("relation") in {"same_execution", "indirect_same_execution_control"}
            and path.get("before_observed_exec_end")
        ]
        passed = not violating
    elif name in {"result_consumed_only_after_exec_end", "audit_only_after_end"}:
        violating = [
            path
            for path in matching_paths
            if path.get("relation") == "same_execution" and path.get("before_observed_exec_end")
        ]
        passed = not violating and any(path.get("relation") in {"same_execution_after_end", "audit_only"} for path in matching_paths)
    elif name in {"result_consumed_by_external_orchestrator", "external_controller_consumes_result"}:
        passed = any(path.get("relation") == "external_controller" for path in matching_paths)
        violating = []
    elif name in {"future_run_control_only", "future_run_consumes_result"}:
        passed = any(path.get("relation") in {"different_execution", "future_execution"} for path in matching_paths)
        violating = []
    else:
        passed = after.get("classification") == "valid_acyclic"
        violating = []

    return {
        **obligation,
        "status": "passed" if passed else "failed",
        "matching_paths": matching_paths,
        "violating_paths": violating,
    }


def verify_repair(before_text: str, after_text: str, obligations: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    checker = load_trace_checker()
    before = checker.analyze_text(before_text)
    after = checker.analyze_text(after_text)
    base_passed = before["classification"] == "causal_paradox" and after["classification"] == "valid_acyclic"
    proof_obligations = obligations or [
        {
            "obligation": "prediction_result_not_consumed_by_observed_execution",
            "valid_if": [
                "consumer is external_orchestrator",
                "consumer exec starts after observed exec ends",
                "result is audit_only",
                "consumer is a future execution",
            ],
        }
    ]
    checked_obligations = [obligation_status(obligation, after) for obligation in proof_obligations]
    obligations_passed = all(item["status"] == "passed" for item in checked_obligations)
    passed = base_passed and obligations_passed
    return {
        "verification": "passed" if passed else "failed",
        "before_classification": before["classification"],
        "after_classification": after["classification"],
        "before_feedback_paths": before.get("feedback_paths", []),
        "after_feedback_paths": after.get("feedback_paths", []),
        "proof_obligations": checked_obligations,
        "capability_boundary": dict(CAPABILITY_BOUNDARY),
        "analysis_profile": "trace_identity_limited",
        "explanation": (
            "Repair removes same-execution pre-end consumption and satisfies the requested proof obligations."
            if passed
            else "Repair verification requires before=causal_paradox, after=valid_acyclic, and all proof obligations passing."
        ),
    }


def repair_certificate(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "certificate_version": "1.0",
        "claim": "prediction_feedback_removed",
        "before_classification": result["before_classification"],
        "after_classification": result["after_classification"],
        "obligations_checked": result["proof_obligations"],
        "evidence_paths": {
            "before_feedback_paths": result["before_feedback_paths"],
            "after_feedback_paths": result["after_feedback_paths"],
        },
        "result": result["verification"],
        "capability_boundary": result["capability_boundary"],
    }


def format_human(result: dict[str, Any]) -> str:
    lines = [
        f"verification: {result['verification']}",
        f"before_classification: {result['before_classification']}",
        f"after_classification: {result['after_classification']}",
        f"explanation: {result['explanation']}",
        "proof_obligations:",
    ]
    for obligation in result["proof_obligations"]:
        lines.append(f"  {obligation['obligation']}: {obligation['status']}")
    if result["before_feedback_paths"]:
        lines.append("before_feedback_paths:")
        for path in result["before_feedback_paths"]:
            lines.append(f"  {path['target_exec_id']} -> {path['result_id']} -> {path['consumer_exec_id']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify before/after CHC trace repair.")
    parser.add_argument("before", help="Before trace JSONL file.")
    parser.add_argument("after", help="After trace JSONL file.")
    parser.add_argument("--repair", help="Repair JSON file containing proof_obligations.")
    parser.add_argument("--certificate", action="store_true", help="Emit a repair certificate JSON instead of verification JSON.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    obligations = None
    if args.repair:
        try:
            repair = json.loads(Path(args.repair).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        if isinstance(repair, dict) and isinstance(repair.get("proof_obligations"), list):
            obligations = repair["proof_obligations"]
    result = verify_repair(
        Path(args.before).read_text(encoding="utf-8"),
        Path(args.after).read_text(encoding="utf-8"),
        obligations,
    )
    if args.certificate:
        result = repair_certificate(result)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif args.certificate:
        print(f"claim: {result['claim']}")
        print(f"result: {result['result']}")
        print(f"before_classification: {result['before_classification']}")
        print(f"after_classification: {result['after_classification']}")
    else:
        print(format_human(result))
    status = result.get("verification", result.get("result"))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
