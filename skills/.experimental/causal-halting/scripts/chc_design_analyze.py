#!/usr/bin/env python3
"""Deterministic DesignIR analyzer for Causal Halting.

This script intentionally does not understand natural language. The LLM must
interpret prose into DesignIR first. This analyzer only validates and classifies
structured causal roles.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DESIGN_IR_VERSION = "1.0"
CAPABILITY_BOUNDARY = {
    "does_not_prove_arbitrary_termination": True,
    "does_not_solve_classical_halting": True,
}
VALIDITY_SCOPE = "no_modeled_prediction_feedback_only"
ALLOWED_TIMINGS = {
    "during_observed_execution",
    "after_observed_execution",
    "future_execution",
    "external_controller",
    "unknown",
}


def safe_label(value: Any, fallback: str) -> str:
    text = str(value if value is not None else fallback)
    return "".join(char if char.isalnum() or char == "_" else "_" for char in text) or fallback


def exec_node(execution: dict[str, Any]) -> str:
    return f"E({safe_label(execution.get('program'), 'Exec')},{safe_label(execution.get('input'), 'input')})"


def result_node(execution: dict[str, Any]) -> str:
    return f"R({safe_label(execution.get('program'), 'Exec')},{safe_label(execution.get('input'), 'input')})"


def repair_for_self_feedback() -> list[str]:
    return [
        "Move the prediction result to an external orchestrator or controller.",
        "Make the result affect a future execution, not the execution being observed.",
        "Convert current-run self-prediction into post-run audit when possible.",
        "Replace self-halting prediction with bounded local progress metrics.",
        "Keep monitor and controller roles separate.",
    ]


def default_proof_obligation(result_id: str, observed_exec_id: str) -> dict[str, Any]:
    return {
        "obligation": "prediction_result_not_consumed_by_observed_execution",
        "result_id": result_id,
        "forbidden_consumer_exec_id": observed_exec_id,
        "valid_if": [
            "consumer is external_orchestrator",
            "consumer exec starts after observed exec ends",
            "result is audit_only",
            "consumer is a future execution",
        ],
    }


def base_roles() -> dict[str, list[str]]:
    return {
        "Code": [],
        "Exec": [],
        "H": [],
        "HaltResult": [],
    }


def add_boundary(result: dict[str, Any]) -> dict[str, Any]:
    result.setdefault("capability_boundary", dict(CAPABILITY_BOUNDARY))
    result.setdefault("analysis_profile", "complete_for_chc0")
    result.setdefault("validity_scope", VALIDITY_SCOPE)
    result.setdefault(
        "identity_resolution",
        {
            "resolved": [],
            "ambiguous": [],
            "missing": [],
            "conflicts": [],
            "assumptions": ["DesignIR identity is trusted only when explicit IDs reference known objects."],
        },
    )
    result.setdefault("formal_status", "specified")
    result.setdefault(
        "theorem_coverage",
        {
            "chc_level": "DesignIR",
            "mechanized_core": "not_mechanized",
            "claims": ["structured DesignIR feedback classification"],
        },
    )
    return result


def needs_design_ir_result(text: str) -> dict[str, Any]:
    return add_boundary({
        "classification": "needs_design_ir",
        "design_ir": None,
        "inferred_graph": [],
        "roles": base_roles(),
        "uncertain_edges": [],
        "repair": [],
        "explanation": (
            "Natural-language input is not analyzed by this script. "
            "Interpret the design into DesignIR first, then rerun the analyzer."
        ),
        "input_preview": text.strip()[:200],
    })


def validate_design_ir(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("design_ir_version") != DESIGN_IR_VERSION:
        errors.append(f"design_ir_version must be {DESIGN_IR_VERSION!r}")
    if "classification" in data:
        errors.append("classification is script-owned and must not be supplied in DesignIR")
    executions = data.get("executions")
    observations = data.get("observations")
    controls = data.get("controls")
    uncertain = data.get("uncertain", [])
    evidence = data.get("semantic_evidence", [])
    if not isinstance(executions, list):
        errors.append("executions must be a list")
    if not isinstance(observations, list):
        errors.append("observations must be a list")
    if not isinstance(controls, list):
        errors.append("controls must be a list")
    if not isinstance(uncertain, list):
        errors.append("uncertain must be a list when present")
    if not isinstance(evidence, list):
        errors.append("semantic_evidence must be a list when present")
    if errors:
        return errors

    exec_ids: set[str] = set()
    result_ids: set[str] = set()
    observation_ids: set[str] = set()
    for index, execution in enumerate(executions):
        if not isinstance(execution, dict):
            errors.append(f"executions[{index}] must be an object")
            continue
        if not isinstance(execution.get("id"), str):
            errors.append(f"executions[{index}].id must be a string")
            continue
        if not isinstance(execution.get("program"), str):
            errors.append(f"executions[{index}].program must be a string")
        if "input" not in execution:
            errors.append(f"executions[{index}].input is required")
        exec_ids.add(execution["id"])

    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        if not isinstance(observation.get("id"), str):
            errors.append(f"observations[{index}].id must be a string")
        elif observation["id"] in observation_ids:
            errors.append(f"observations[{index}].id must be unique")
        else:
            observation_ids.add(observation["id"])
        if not isinstance(observation.get("observer"), str):
            errors.append(f"observations[{index}].observer must be a string")
        if not isinstance(observation.get("result"), str):
            errors.append(f"observations[{index}].result must be a string")
        if observation.get("target_exec") not in exec_ids:
            errors.append(f"observations[{index}].target_exec must reference an execution")
        if isinstance(observation.get("result"), str):
            result_ids.add(observation["result"])

    for index, control in enumerate(controls):
        if not isinstance(control, dict):
            errors.append(f"controls[{index}] must be an object")
            continue
        if not isinstance(control.get("id"), str):
            errors.append(f"controls[{index}].id must be a string")
        if control.get("result") not in result_ids:
            errors.append(f"controls[{index}].result must reference an observation result")
        timing = control.get("timing")
        if timing not in ALLOWED_TIMINGS:
            errors.append(
                f"controls[{index}].timing must be one of {', '.join(sorted(ALLOWED_TIMINGS))}"
            )
        target = control.get("target_exec")
        if target is not None and target not in exec_ids:
            errors.append(f"controls[{index}].target_exec must reference an execution when present")
        if target is None and not isinstance(control.get("consumer"), str):
            errors.append(f"controls[{index}] requires target_exec or consumer")
        if timing == "external_controller" and not isinstance(control.get("consumer"), str):
            errors.append(f"controls[{index}].consumer must name the external controller")
    return errors


def analyze_design_ir(data: dict[str, Any]) -> dict[str, Any]:
    errors = validate_design_ir(data)
    if errors:
        return add_boundary({
            "classification": "parse_error",
            "design_ir": data,
            "inferred_graph": [],
            "roles": base_roles(),
            "uncertain_edges": [],
            "repair": [],
            "explanation": "; ".join(errors),
        })

    executions = {execution["id"]: execution for execution in data["executions"]}
    observations = {observation["result"]: observation for observation in data["observations"]}
    graph: list[str] = []
    uncertain_edges = list(data.get("uncertain", []))
    identity_resolution = {
        "resolved": [],
        "ambiguous": [],
        "missing": [],
        "conflicts": [],
        "assumptions": [],
    }
    feedback: list[dict[str, Any]] = []
    proof_obligations: list[dict[str, Any]] = []
    roles = {
        "Code": sorted({safe_label(execution.get("program"), "Exec") for execution in data["executions"]}),
        "Exec": [
            f"{safe_label(execution.get('program'), 'Exec')}({safe_label(execution.get('input'), 'input')})"
            for execution in data["executions"]
        ],
        "H": sorted({safe_label(observation.get("observer"), "Observer") for observation in data["observations"]}),
        "HaltResult": sorted(observations.keys()),
    }

    for observation in data["observations"]:
        observed = executions[observation["target_exec"]]
        graph.append(f"{exec_node(observed)} -> {result_node(observed)}")
        identity_resolution["resolved"].append(
            {
                "kind": "observation_target",
                "observation_id": observation["id"],
                "target_exec": observation["target_exec"],
                "result": observation["result"],
            }
        )

    for control in data["controls"]:
        observation = observations[control["result"]]
        observed = executions[observation["target_exec"]]
        target_exec = control.get("target_exec")
        timing = control.get("timing", "unknown")
        if target_exec is None:
            consumer = control.get("consumer")
            if timing == "external_controller" and isinstance(consumer, str):
                graph.append(f"{result_node(observed)} -> External({safe_label(consumer, 'Controller')})")
                identity_resolution["resolved"].append(
                    {
                        "kind": "external_control_boundary",
                        "control_id": control["id"],
                        "result": control["result"],
                        "consumer": consumer,
                    }
                )
            else:
                uncertain_edges.append(
                    {
                        "edge": f"{result_node(observed)} -> ?",
                        "confidence": 0.5,
                        "reason": "Control target is not specified.",
                    }
                )
                identity_resolution["missing"].append(
                    {"kind": "control_target", "control_id": control.get("id"), "result": control.get("result")}
                )
            continue
        controlled = executions[target_exec]
        graph.append(f"{result_node(observed)} -> {exec_node(controlled)}")
        identity_resolution["resolved"].append(
            {
                "kind": "control_target",
                "control_id": control["id"],
                "result": control["result"],
                "target_exec": target_exec,
                "timing": timing,
            }
        )
        if timing == "unknown":
            uncertain_edges.append(
                {
                    "edge": f"{result_node(observed)} -> {exec_node(controlled)}",
                    "confidence": 0.5,
                    "reason": "Control timing is unknown.",
                }
            )
            identity_resolution["ambiguous"].append(
                {"kind": "control_timing", "control_id": control["id"], "result": control["result"]}
            )
        if target_exec == observation["target_exec"] and timing == "during_observed_execution":
            feedback.append(
                {
                    "result": control["result"],
                    "target_exec": target_exec,
                    "action": control.get("action", control.get("purpose", "control")),
                }
            )
            proof_obligations.append(default_proof_obligation(control["result"], observation["target_exec"]))

    if feedback:
        return add_boundary({
            "classification": "causal_paradox",
            "design_ir": data,
            "inferred_graph": graph,
            "roles": roles,
            "uncertain_edges": uncertain_edges,
            "repair": repair_for_self_feedback(),
            "proof_obligations": proof_obligations,
            "identity_resolution": identity_resolution,
            "explanation": "A prediction or observation result controls the same execution it observes.",
        })

    if uncertain_edges:
        return add_boundary({
            "classification": "insufficient_info",
            "design_ir": data,
            "inferred_graph": graph,
            "roles": roles,
            "uncertain_edges": uncertain_edges,
            "repair": ["Specify the consumer execution or external boundary for each observation result."],
            "proof_obligations": [],
            "identity_resolution": identity_resolution,
            "explanation": "The DesignIR leaves at least one result consumer unspecified.",
        })

    return add_boundary({
        "classification": "valid_acyclic",
        "design_ir": data,
        "inferred_graph": graph,
        "roles": roles,
        "uncertain_edges": [],
        "repair": [],
        "proof_obligations": [],
        "identity_resolution": identity_resolution,
        "explanation": "No DesignIR control edge routes an observation result back into its observed execution.",
    })


def analyze_design(text: str) -> dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return needs_design_ir_result(text)
    if isinstance(data, dict) and {"executions", "observations", "controls"}.issubset(data.keys()):
        return analyze_design_ir(data)
    return add_boundary({
        "classification": "parse_error",
        "design_ir": data if isinstance(data, dict) else None,
        "inferred_graph": [],
        "roles": base_roles(),
        "uncertain_edges": [],
        "repair": [],
        "proof_obligations": [],
        "explanation": "Input JSON is not a DesignIR object with executions, observations, and controls.",
    })


def validate_shape(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {
        "causal_paradox",
        "valid_acyclic",
        "unproved",
        "insufficient_info",
        "needs_design_ir",
        "parse_error",
    }
    if result.get("classification") not in allowed:
        errors.append(
            "classification must be one of causal_paradox, valid_acyclic, unproved, insufficient_info, needs_design_ir, parse_error"
        )
    if "design_ir" in result and result.get("design_ir") is not None and not isinstance(result.get("design_ir"), dict):
        errors.append("design_ir must be an object or null when present")
    if not isinstance(result.get("inferred_graph"), list):
        errors.append("inferred_graph must be a list")
    if not isinstance(result.get("roles"), dict):
        errors.append("roles must be an object")
    else:
        for key in ("Code", "Exec", "H", "HaltResult"):
            if not isinstance(result["roles"].get(key), list):
                errors.append(f"roles.{key} must be a list")
    if not isinstance(result.get("uncertain_edges"), list):
        errors.append("uncertain_edges must be a list")
    if not isinstance(result.get("repair"), list):
        errors.append("repair must be a list")
    if "proof_obligations" in result and not isinstance(result.get("proof_obligations"), list):
        errors.append("proof_obligations must be a list when present")
    if not isinstance(result.get("explanation"), str):
        errors.append("explanation must be a string")
    return errors


def read_input(value: str) -> str:
    path = Path(value).expanduser()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def format_human(result: dict[str, Any]) -> str:
    lines = [
        f"classification: {result['classification']}",
        f"explanation: {result['explanation']}",
    ]
    if result.get("inferred_graph"):
        lines.append("inferred_graph:")
        lines.extend(f"  {edge}" for edge in result["inferred_graph"])
    if result.get("uncertain_edges"):
        lines.append("uncertain_edges:")
        for edge in result["uncertain_edges"]:
            label = edge.get("edge") or edge.get("field") or "unknown"
            confidence = edge.get("confidence", "unknown")
            reason = edge.get("reason", "unspecified")
            lines.append(f"  {label} | confidence={confidence} | {reason}")
    if result.get("repair"):
        lines.append("repair:")
        lines.extend(f"  - {item}" for item in result["repair"])
    if result.get("proof_obligations"):
        lines.append("proof_obligations:")
        for obligation in result["proof_obligations"]:
            lines.append(f"  - {obligation['obligation']} for {obligation['result_id']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze Causal Halting DesignIR JSON.")
    parser.add_argument("input", nargs="+", help="DesignIR JSON or a path to a DesignIR JSON file.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = analyze_design(read_input(" ".join(args.input)))
    errors = validate_shape(result)
    if errors:
        result = {
            "classification": "parse_error",
            "design_ir": None,
            "inferred_graph": [],
            "roles": base_roles(),
            "uncertain_edges": [],
            "repair": [],
            "explanation": "; ".join(errors),
        }
        result = add_boundary(result)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_human(result))
    return 2 if result["classification"] == "parse_error" else 0


if __name__ == "__main__":
    sys.exit(main())
