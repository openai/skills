#!/usr/bin/env python3
"""Convert structured Temporal/Airflow-style JSON into CHC trace events.

This adapter reads explicit causal fields only. It does not infer meaning from
workflow names, task names, DAG labels, or prose descriptions.
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


def execution_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items = payload.get("runs", payload.get("tasks", payload.get("executions", [])))
    return items if isinstance(items, list) else []


def execution_id(item: dict[str, Any]) -> Any:
    return item.get("id", item.get("run_id", item.get("task_id")))


def execution_program(item: dict[str, Any]) -> Any:
    return item.get("workflow", item.get("dag_id", item.get("task", item.get("program", "WorkflowRun"))))


def temporal_airflow_to_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for item in execution_items(payload):
        exec_id = execution_id(item)
        events.append(
            {
                "type": "exec_start",
                "exec_id": exec_id,
                "program": execution_program(item),
                "input": item.get("input", payload.get("workflow_id", payload.get("dag_id", "input"))),
                **metadata_from(item, "temporal_airflow.execution"),
            }
        )
        if item.get("ended"):
            events.append(
                {
                    "type": "exec_end",
                    "exec_id": exec_id,
                    "status": item.get("status", "halted"),
                    **metadata_from(item, "temporal_airflow.execution"),
                }
            )

    for observation in payload.get("observations", []):
        events.append(
            {
                "type": "observe",
                "observer": observation.get("observer", "Observer"),
                "target_exec_id": observation["target_run"],
                "result_id": observation["result"],
                **metadata_from(observation, "temporal_airflow.observation"),
            }
        )

    for control in payload.get("controls", []):
        if "controlled_run" in control or "controller_run" in control:
            event = {
                "type": "control_exec",
                "controlled_exec_id": control.get("controlled_run"),
                "controller_exec_id": control.get("controller_run"),
                "controller": control.get("controller"),
                "action": control.get("action", "control"),
                **metadata_from(control, "temporal_airflow.control_exec"),
            }
        else:
            event = {
                "type": "consume",
                "result_id": control["result"],
                "consumer_exec_id": control.get("target_run"),
                "consumer": control.get("consumer"),
                "purpose": control.get("purpose", control.get("action", "control")),
                **metadata_from(control, "temporal_airflow.control"),
            }
        events.append({key: value for key, value in event.items() if value is not None})
    return events


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    executions = execution_items(payload)
    observations = payload.get("observations")
    controls = payload.get("controls")
    if not isinstance(observations, list):
        errors.append("observations must be a list")
    if not isinstance(controls, list):
        errors.append("controls must be a list")
    if not executions:
        errors.append("runs, tasks, or executions must be a non-empty list")
    if errors:
        return errors

    exec_ids = {execution_id(item) for item in executions if isinstance(item, dict)}
    result_ids = {observation.get("result") for observation in observations if isinstance(observation, dict)}
    for index, item in enumerate(executions):
        if not isinstance(item, dict) or not isinstance(execution_id(item), str):
            errors.append(f"executions[{index}] must have string id, run_id, or task_id")
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        if observation.get("target_run") not in exec_ids:
            errors.append(f"observations[{index}].target_run must reference an execution")
        if not isinstance(observation.get("result"), str):
            errors.append(f"observations[{index}].result must be a string")
    for index, control in enumerate(controls):
        if not isinstance(control, dict):
            errors.append(f"controls[{index}] must be an object")
            continue
        if "controlled_run" not in control and "controller_run" not in control and control.get("result") not in result_ids:
            errors.append(f"controls[{index}].result must reference an observation result")
        for key in ("target_run", "controlled_run", "controller_run"):
            if key in control and control[key] is not None and control[key] not in exec_ids:
                errors.append(f"controls[{index}].{key} must reference an execution when present")
    return errors


def format_jsonl(events: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(event, sort_keys=True) for event in events)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert Temporal/Airflow-style JSON to CHC trace JSONL.")
    parser.add_argument("input", help="Temporal/Airflow-style JSON file.")
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
    events = temporal_airflow_to_events(payload)
    if args.format == "json":
        print(json.dumps(events, indent=2, sort_keys=True))
    else:
        print(format_jsonl(events))
    return 0


if __name__ == "__main__":
    sys.exit(main())
