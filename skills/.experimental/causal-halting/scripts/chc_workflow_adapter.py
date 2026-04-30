#!/usr/bin/env python3
"""Convert generic workflow JSON into Causal Halting trace events.

The supported input is intentionally small and dependency-free:

{
  "design_ir_version": "1.0",
  "executions": [{"id": "run-1", "program": "AgentRun", "input": "task"}],
  "observations": [{"observer": "Supervisor", "target_exec": "run-1", "result": "r-1"}],
  "controls": [{"id": "ctrl-1", "result": "r-1", "target_exec": "run-1", "timing": "during_observed_execution", "purpose": "strategy_change"}]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def workflow_to_events(workflow: dict[str, Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for execution in workflow.get("executions", []):
        events.append(
            {
                "type": "exec_start",
                "exec_id": execution["id"],
                "program": execution.get("program", "Exec"),
                "input": execution.get("input", "input"),
            }
        )
        if execution.get("ended"):
            events.append(
                {
                    "type": "exec_end",
                    "exec_id": execution["id"],
                    "status": execution.get("status", "halted"),
                }
            )
    for observation in workflow.get("observations", []):
        events.append(
            {
                "type": "observe",
                "observer": observation.get("observer", "Observer"),
                "target_exec_id": observation["target_exec"],
                "result_id": observation["result"],
            }
        )
    for control in workflow.get("controls", []):
        events.append(
            {
                "type": "consume",
                "result_id": control["result"],
                "consumer_exec_id": control.get("target_exec"),
                "consumer": control.get("consumer"),
                "purpose": control.get("purpose", control.get("action", "control")),
            }
        )
    return events


def validate_workflow(workflow: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("executions", "observations", "controls"):
        if not isinstance(workflow.get(key), list):
            errors.append(f"{key} must be a list")
    if errors:
        return errors
    exec_ids = {execution.get("id") for execution in workflow["executions"] if isinstance(execution, dict)}
    result_ids = {observation.get("result") for observation in workflow["observations"] if isinstance(observation, dict)}
    for index, execution in enumerate(workflow["executions"]):
        if not isinstance(execution, dict) or not isinstance(execution.get("id"), str):
            errors.append(f"executions[{index}].id must be a string")
    for index, observation in enumerate(workflow["observations"]):
        if not isinstance(observation, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        if observation.get("target_exec") not in exec_ids:
            errors.append(f"observations[{index}].target_exec must reference an execution")
        if not isinstance(observation.get("result"), str):
            errors.append(f"observations[{index}].result must be a string")
    for index, control in enumerate(workflow["controls"]):
        if not isinstance(control, dict):
            errors.append(f"controls[{index}] must be an object")
            continue
        if "id" in control and not isinstance(control.get("id"), str):
            errors.append(f"controls[{index}].id must be a string when present")
        if control.get("result") not in result_ids:
            errors.append(f"controls[{index}].result must reference an observation result")
        target = control.get("target_exec")
        if target is not None and target not in exec_ids:
            errors.append(f"controls[{index}].target_exec must reference an execution when present")
        if target is None and "consumer" in control and not isinstance(control.get("consumer"), str):
            errors.append(f"controls[{index}].consumer must be a string when present")
    return errors


def format_jsonl(events: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(event, sort_keys=True) for event in events)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert generic workflow JSON to CHC trace JSONL.")
    parser.add_argument("input", help="Workflow JSON file.")
    parser.add_argument("--format", choices=("jsonl", "json"), default="jsonl")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        workflow = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not isinstance(workflow, dict):
        print("workflow must be a JSON object", file=sys.stderr)
        return 2
    errors = validate_workflow(workflow)
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 2
    events = workflow_to_events(workflow)
    if args.format == "json":
        print(json.dumps(events, indent=2, sort_keys=True))
    else:
        print(format_jsonl(events))
    return 0


if __name__ == "__main__":
    sys.exit(main())
