#!/usr/bin/env python3
"""Convert structured LangGraph-style run JSON into CHC trace events.

This adapter expects explicit causal fields. It does not infer meaning from
node names, edge labels, or prose descriptions.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def metadata_from(source: dict[str, Any], event_source: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {"event_source": event_source}
    for key in ("timestamp", "span_id", "parent_id", "confidence"):
        if key in source:
            metadata[key] = source[key]
    return metadata


def langgraph_to_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for run in payload.get("runs", payload.get("executions", [])):
        events.append(
            {
                "type": "exec_start",
                "exec_id": run["id"],
                "program": run.get("node", run.get("program", "Node")),
                "input": run.get("input", "input"),
                **metadata_from(run, "langgraph.run"),
            }
        )
        if run.get("ended"):
            events.append({"type": "exec_end", "exec_id": run["id"], "status": run.get("status", "halted"), **metadata_from(run, "langgraph.run")})
    for observation in payload.get("observations", []):
        events.append(
            {
                "type": "observe",
                "observer": observation.get("observer_node", observation.get("observer", "Observer")),
                "target_exec_id": observation["target_run"],
                "result_id": observation["result"],
                **metadata_from(observation, "langgraph.observation"),
            }
        )
    for control in payload.get("controls", []):
        if "controlled_run" in control or "controller_run" in control:
            event = {
                "type": "control_exec",
                "controlled_exec_id": control.get("controlled_run"),
                "controller_exec_id": control.get("controller_run"),
                "controller": control.get("controller_node", control.get("controller")),
                "action": control.get("action", "control"),
                **metadata_from(control, "langgraph.control_exec"),
            }
        else:
            event = {
                "type": "consume",
                "result_id": control["result"],
                "consumer_exec_id": control.get("target_run"),
                "consumer": control.get("consumer_node", control.get("consumer")),
                "purpose": control.get("purpose", control.get("action", "control")),
                **metadata_from(control, "langgraph.control"),
            }
        events.append({key: value for key, value in event.items() if value is not None})
    return events


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    runs = payload.get("runs", payload.get("executions"))
    observations = payload.get("observations")
    controls = payload.get("controls")
    if not isinstance(runs, list):
        errors.append("runs or executions must be a list")
    if not isinstance(observations, list):
        errors.append("observations must be a list")
    if not isinstance(controls, list):
        errors.append("controls must be a list")
    if errors:
        return errors
    run_ids = {run.get("id") for run in runs if isinstance(run, dict)}
    result_ids = {observation.get("result") for observation in observations if isinstance(observation, dict)}
    for index, run in enumerate(runs):
        if not isinstance(run, dict) or not isinstance(run.get("id"), str):
            errors.append(f"runs[{index}].id must be a string")
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        if observation.get("target_run") not in run_ids:
            errors.append(f"observations[{index}].target_run must reference a run")
        if not isinstance(observation.get("result"), str):
            errors.append(f"observations[{index}].result must be a string")
    for index, control in enumerate(controls):
        if not isinstance(control, dict):
            errors.append(f"controls[{index}] must be an object")
            continue
        if "controlled_run" not in control and "controller_run" not in control and control.get("result") not in result_ids:
            errors.append(f"controls[{index}].result must reference an observation result")
        target = control.get("target_run")
        if target is not None and target not in run_ids:
            errors.append(f"controls[{index}].target_run must reference a run when present")
        controlled = control.get("controlled_run")
        if controlled is not None and controlled not in run_ids:
            errors.append(f"controls[{index}].controlled_run must reference a run when present")
        controller = control.get("controller_run")
        if controller is not None and controller not in run_ids:
            errors.append(f"controls[{index}].controller_run must reference a run when present")
    return errors


def format_jsonl(events: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(event, sort_keys=True) for event in events)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert structured LangGraph-style JSON to CHC trace JSONL.")
    parser.add_argument("input", help="LangGraph-style JSON file.")
    parser.add_argument("--format", choices=("jsonl", "json"), default="jsonl")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("input must be a JSON object", file=sys.stderr)
        return 2
    errors = validate_payload(payload)
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 2
    events = langgraph_to_events(payload)
    if args.format == "json":
        print(json.dumps(events, indent=2, sort_keys=True))
    else:
        print(format_jsonl(events))
    return 0


if __name__ == "__main__":
    sys.exit(main())
