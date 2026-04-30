#!/usr/bin/env python3
"""Analyze CHC-3 ProcessIR for process/session prediction feedback."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


BOUNDARY = {
    "does_not_prove_arbitrary_termination": True,
    "does_not_solve_classical_halting": True,
}
VALIDITY_SCOPE = "no_modeled_prediction_feedback_only"


def exec_node(execution: dict[str, Any]) -> str:
    return f"E({execution.get('program', 'Exec')},{execution.get('input', execution.get('id', 'input'))})"


def validate_ids(data: dict[str, Any]) -> list[dict[str, Any]]:
    uncertain: list[dict[str, Any]] = []
    processes = {item.get("id") for item in data.get("processes", []) if isinstance(item, dict)}
    sessions = {item.get("id") for item in data.get("sessions", []) if isinstance(item, dict)}
    channels = {item.get("id") for item in data.get("channels", []) if isinstance(item, dict)}
    executions = {item.get("id") for item in data.get("executions", []) if isinstance(item, dict)}
    results = {item.get("result") for item in data.get("observations", []) if isinstance(item, dict)}

    for item in data.get("executions", []):
        if not isinstance(item, dict):
            continue
        if item.get("process_id") not in processes:
            uncertain.append({"relation": "unknown_process", "exec_id": item.get("id"), "process_id": item.get("process_id")})
        if item.get("session_id") not in sessions:
            uncertain.append({"relation": "unknown_session", "exec_id": item.get("id"), "session_id": item.get("session_id")})
    for item in data.get("observations", []):
        if not isinstance(item, dict):
            continue
        if item.get("target_exec") not in executions:
            uncertain.append({"relation": "unknown_observed_execution", "result_id": item.get("result"), "target_exec": item.get("target_exec")})
        if item.get("observer_process_id") is not None and item.get("observer_process_id") not in processes:
            uncertain.append({"relation": "unknown_observer_process", "result_id": item.get("result"), "observer_process_id": item.get("observer_process_id")})
    for item in data.get("controls", []):
        if not isinstance(item, dict):
            continue
        if item.get("result") not in results:
            uncertain.append({"relation": "unknown_result", "result_id": item.get("result")})
        if item.get("target_exec") is not None and item.get("target_exec") not in executions:
            uncertain.append({"relation": "unknown_control_target", "result_id": item.get("result"), "target_exec": item.get("target_exec")})
        if item.get("channel_id") is not None and item.get("channel_id") not in channels:
            uncertain.append({"relation": "unknown_channel", "result_id": item.get("result"), "channel_id": item.get("channel_id")})
        if item.get("controller_process_id") is not None and item.get("controller_process_id") not in processes:
            uncertain.append({"relation": "unknown_controller_process", "result_id": item.get("result"), "controller_process_id": item.get("controller_process_id")})
    return uncertain


def analyze_process_ir(data: dict[str, Any]) -> dict[str, Any]:
    required = ("processes", "sessions", "channels", "executions", "observations", "controls")
    missing = [key for key in required if not isinstance(data.get(key), list)]
    if missing:
        return result("parse_error", [], [], [], f"ProcessIR requires list field(s): {', '.join(missing)}")

    executions = {item.get("id"): item for item in data["executions"] if isinstance(item, dict)}
    observations = {item.get("result"): item for item in data["observations"] if isinstance(item, dict)}
    process_graph: list[str] = []
    session_graph: list[str] = []
    feedback_paths: list[dict[str, Any]] = []
    uncertain: list[dict[str, Any]] = validate_ids(data)

    for observation in observations.values():
        target = executions.get(observation.get("target_exec"))
        if target is None:
            uncertain.append({"relation": "unknown_observed_execution", "result_id": observation.get("result")})
            continue
        process_graph.append(f"{exec_node(target)} -> R({target.get('program', 'Exec')},{target.get('input', 'input')})")

    for control in data["controls"]:
        if not isinstance(control, dict):
            continue
        observation = observations.get(control.get("result"))
        if observation is None:
            uncertain.append({"relation": "unknown_result", "result_id": control.get("result")})
            continue
        observed = executions.get(observation.get("target_exec"))
        target = executions.get(control.get("target_exec")) if control.get("target_exec") else None
        if observed is None:
            continue
        result_node = f"R({observed.get('program', 'Exec')},{observed.get('input', 'input')})"
        if target is None:
            if control.get("timing") == "external_controller":
                process_graph.append(f"{result_node} -> External({control.get('consumer', 'Controller')})")
                continue
            uncertain.append({"relation": "unknown_control_target", "result_id": control.get("result")})
            continue
        route = [str(item) for item in control.get("route", []) if isinstance(item, str)]
        if route:
            route_nodes = [result_node] + route + [exec_node(target)]
            for source, destination in zip(route_nodes, route_nodes[1:]):
                process_graph.append(f"{source} -> {destination}")
        else:
            process_graph.append(f"{result_node} -> {exec_node(target)}")
        session_graph.append(
            f"Session({observed.get('session_id', 'unknown')}) -> Channel({control.get('channel_id', 'unknown')})"
        )
        if (
            target.get("id") == observation.get("target_exec")
            and control.get("timing") == "during_observed_execution"
        ):
            feedback_paths.append(
                {
                    "relation": "same_execution_process_feedback",
                    "result_id": control.get("result"),
                    "target_exec_id": target.get("id"),
                    "control_channel_id": control.get("channel_id"),
                    "path": [exec_node(observed), result_node] + route + [exec_node(target)],
                }
            )
        if (
            target.get("id") == observation.get("target_exec")
            and control.get("timing") in {None, "unknown"}
        ):
            uncertain.append(
                {
                    "relation": "ambiguous_same_execution_timing",
                    "result_id": control.get("result"),
                    "target_exec_id": target.get("id"),
                    "reason": "Control targets the observed execution but does not state whether it occurs before the execution ends.",
                }
            )
        if control.get("role_collapse") is True:
            feedback_paths.append(
                {
                    "relation": "monitor_controller_role_collapse",
                    "result_id": control.get("result"),
                    "target_exec_id": target.get("id"),
                    "control_channel_id": control.get("channel_id"),
                }
            )

    if feedback_paths:
        return result("causal_paradox", process_graph, session_graph, feedback_paths, "Process/session flow routes an observation result back into the observed execution.")
    if uncertain:
        payload = result("insufficient_info", process_graph, session_graph, [], "ProcessIR has ambiguous process, execution, result, or channel identity.")
        payload["uncertain_paths"] = uncertain
        payload["identity_resolution"]["ambiguous"] = [
            item for item in uncertain if "ambiguous" in str(item.get("relation", ""))
        ]
        payload["identity_resolution"]["missing"] = [
            item for item in uncertain if "ambiguous" not in str(item.get("relation", ""))
        ]
        return payload
    return result("valid_acyclic", process_graph, session_graph, [], "No process/session non-interference violation was found.")


def result(classification: str, process_graph: list[str], session_graph: list[str], feedback_paths: list[dict[str, Any]], explanation: str) -> dict[str, Any]:
    return {
        "classification": classification,
        "chc_level": "CHC-3",
        "process_graph": process_graph,
        "session_graph": session_graph,
        "feedback_paths": feedback_paths,
        "non_interference_status": "failed" if classification == "causal_paradox" else "insufficient_info" if classification == "insufficient_info" else "passed",
        "semantic_status": "not_analyzed",
        "analysis_profile": "trace_identity_limited",
        "capability_boundary": dict(BOUNDARY),
        "validity_scope": VALIDITY_SCOPE,
        "identity_resolution": {
            "resolved": [
                {"edge": edge}
                for edge in process_graph + session_graph
            ],
            "ambiguous": [],
            "missing": [],
            "conflicts": [],
            "assumptions": ["ProcessIR identity is accepted only when process/session/channel/execution IDs resolve."],
        },
        "formal_status": "mechanized",
        "theorem_coverage": {
            "chc_level": "CHC-3",
            "mechanized_core": "mechanized",
            "claims": ["process/session non-interference for modeled channel routes"],
        },
        "explanation": explanation,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze CHC-3 ProcessIR JSON.")
    parser.add_argument("input")
    parser.add_argument("--format", choices=("json", "human"), default="human")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        output = analyze_process_ir(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        output = result("parse_error", [], [], [], str(exc))
    if args.format == "json":
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(f"classification: {output['classification']}")
        print(f"non_interference_status: {output['non_interference_status']}")
        print(f"explanation: {output['explanation']}")
    return 2 if output["classification"] == "parse_error" else 0


if __name__ == "__main__":
    sys.exit(main())
