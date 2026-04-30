#!/usr/bin/env python3
"""Validate Causal Halting design-analysis JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_CLASSIFICATIONS = {
    "causal_paradox",
    "valid_acyclic",
    "unproved",
    "insufficient_info",
    "needs_design_ir",
    "parse_error",
}
ALLOWED_TIMINGS = {
    "during_observed_execution",
    "after_observed_execution",
    "future_execution",
    "external_controller",
    "unknown",
}


def validate_design_analysis(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("classification") not in ALLOWED_CLASSIFICATIONS:
        errors.append("classification must be causal_paradox, valid_acyclic, unproved, or insufficient_info")
    if not isinstance(data.get("inferred_graph"), list) or not all(
        isinstance(edge, str) for edge in data.get("inferred_graph", [])
    ):
        errors.append("inferred_graph must be a list of strings")
    if "design_ir" in data and data.get("design_ir") is not None and not isinstance(data.get("design_ir"), dict):
        errors.append("design_ir must be an object or null when present")
    roles = data.get("roles")
    if not isinstance(roles, dict):
        errors.append("roles must be an object")
    else:
        for key in ("Code", "Exec", "H", "HaltResult"):
            if not isinstance(roles.get(key), list) or not all(isinstance(item, str) for item in roles.get(key, [])):
                errors.append(f"roles.{key} must be a list of strings")
    if not isinstance(data.get("uncertain_edges"), list):
        errors.append("uncertain_edges must be a list")
    if not isinstance(data.get("repair"), list) or not all(isinstance(item, str) for item in data.get("repair", [])):
        errors.append("repair must be a list of strings")
    if "proof_obligations" in data and not isinstance(data.get("proof_obligations"), list):
        errors.append("proof_obligations must be a list when present")
    if not isinstance(data.get("explanation"), str):
        errors.append("explanation must be a string")
    return errors


def validate_design_ir(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("design_ir_version") != "1.0":
        errors.append("design_ir_version must be '1.0'")
    if "classification" in data:
        errors.append("DesignIR must not include classification; the script owns classification")
    for key in ("executions", "observations", "controls", "semantic_evidence"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be a list")
    if errors:
        return errors
    exec_ids = {item.get("id") for item in data["executions"] if isinstance(item, dict)}
    result_ids = {item.get("result") for item in data["observations"] if isinstance(item, dict)}
    for index, execution in enumerate(data["executions"]):
        if not isinstance(execution, dict):
            errors.append(f"executions[{index}] must be an object")
            continue
        for key in ("id", "program"):
            if not isinstance(execution.get(key), str):
                errors.append(f"executions[{index}].{key} must be a string")
        if "input" not in execution:
            errors.append(f"executions[{index}].input is required")
    for index, observation in enumerate(data["observations"]):
        if not isinstance(observation, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        for key in ("id", "observer", "target_exec", "result"):
            if not isinstance(observation.get(key), str):
                errors.append(f"observations[{index}].{key} must be a string")
        if observation.get("target_exec") not in exec_ids:
            errors.append(f"observations[{index}].target_exec must reference an execution")
    for index, control in enumerate(data["controls"]):
        if not isinstance(control, dict):
            errors.append(f"controls[{index}] must be an object")
            continue
        if control.get("result") not in result_ids:
            errors.append(f"controls[{index}].result must reference an observation result")
        if control.get("timing") not in ALLOWED_TIMINGS:
            errors.append(f"controls[{index}].timing is invalid")
        if control.get("target_exec") is None and not isinstance(control.get("consumer"), str):
            errors.append(f"controls[{index}] requires target_exec or consumer")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Causal Halting design-analysis JSON.")
    parser.add_argument("input", help="JSON file to validate.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    else:
        if isinstance(data, dict) and {"executions", "observations", "controls"}.issubset(data.keys()):
            errors = validate_design_ir(data)
        else:
            errors = validate_design_analysis(data if isinstance(data, dict) else {})

    result = {"valid": not errors, "errors": errors}
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif errors:
        print("invalid")
        for error in errors:
            print(f"- {error}")
    else:
        print("valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
