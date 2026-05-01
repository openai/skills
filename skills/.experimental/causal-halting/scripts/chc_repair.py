#!/usr/bin/env python3
"""Generate Causal Halting repair reports from analysis JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_ALLOWED_CONSUMERS = ["orchestrator", "future_run", "post_run_auditor"]


def is_er_node(text: str) -> bool:
    node = text.strip()
    if len(node) < 4 or node[0] not in {"E", "R"} or node[1] != "(" or node[-1] != ")":
        return False
    depth = 0
    for index, char in enumerate(node[1:], start=1):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(node) - 1:
                return False
            if depth < 0:
                return False
    return depth == 0


def parse_edge(edge: str) -> tuple[str, str] | None:
    if "->" not in edge:
        return None
    source, target = (part.strip() for part in edge.split("->", 1))
    if not is_er_node(source) or not is_er_node(target):
        return None
    return source, target


def parse_self_feedback(graph: list[str]) -> tuple[str, str, str] | None:
    e_to_r: dict[str, str] = {}
    r_to_e: dict[str, str] = {}
    for edge in graph:
        parsed = parse_edge(edge)
        if parsed is None:
            continue
        source, target = parsed
        if source.startswith("E(") and target.startswith("R("):
            e_to_r[source] = target
        elif source.startswith("R(") and target.startswith("E("):
            r_to_e[source] = target
    for exec_node, result_node in e_to_r.items():
        if r_to_e.get(result_node) == exec_node:
            return exec_node, result_node, exec_node
    return None


def repair_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    classification = analysis.get("classification")
    graph = analysis.get("graph") or analysis.get("inferred_graph") or []
    if not isinstance(graph, list):
        graph = []

    if classification != "causal_paradox":
        return {
            "classification": classification or "unknown",
            "repair_status": "not_needed",
            "problem": None,
            "repair_graph": graph,
            "proof_obligations": [],
            "recommendations": [],
            "explanation": "No structural causal paradox was reported, so no causal refactoring is required.",
        }

    existing_obligations = analysis.get("proof_obligations")
    if isinstance(existing_obligations, list) and existing_obligations:
        obligations = existing_obligations
    else:
        obligations = []

    feedback = parse_self_feedback([str(edge) for edge in graph])
    if feedback is None:
        target_exec = "observed_execution"
        result_node = "prediction_result"
        problem_graph = graph
    else:
        target_exec, result_node, _ = feedback
        problem_graph = [f"{target_exec} -> {result_node}", f"{result_node} -> {target_exec}"]

    repair_graph = [
        f"{target_exec} -> {result_node}",
        f"{result_node} -> E(Orchestrator,input)",
        "E(Orchestrator,input) -> E(NextAgentRun,input)",
    ]

    if not obligations:
        obligations = [
            {
                "obligation": "prediction_result_not_consumed_by_observed_execution",
                "result_id": result_node,
                "target_exec_id": target_exec,
                "forbidden_consumer_exec_id": target_exec,
                "forbidden_consumer": target_exec,
                "allowed_consumers": DEFAULT_ALLOWED_CONSUMERS,
                "valid_if": [
                    "consumer is external_orchestrator",
                    "consumer exec starts after observed exec ends",
                    "result is audit_only",
                    "consumer is a future execution",
                ],
            },
            {
                "obligation": "result_consumed_by_external_orchestrator",
                "result_id": result_node,
                "valid_if": ["consumer is external_orchestrator"],
            },
            {
                "obligation": "future_run_control_only",
                "result_id": result_node,
                "valid_if": ["consumer exec differs from observed exec"],
            },
            {
                "obligation": "result_consumed_only_after_exec_end",
                "result_id": result_node,
                "valid_if": ["same-execution consumption happens only after exec_end"],
            },
        ]

    return {
        "classification": "causal_paradox",
        "repair_status": "repair_recommended",
        "problem": {
            "graph": problem_graph,
            "why_unsafe": "The current execution consumes a prediction or observation result about itself.",
        },
        "repair_graph": repair_graph,
        "proof_obligations": obligations,
        "recommendations": [
            "Route the prediction result to an external orchestrator.",
            "Let the orchestrator stop, restart, or schedule a future run.",
            "Do not let the observed execution consume its own halting prediction before it ends.",
            "Use bounded progress metrics inside the run instead of self-halting prediction.",
        ],
        "explanation": "The repair moves control from the observed execution to a separate boundary.",
    }


def format_human(result: dict[str, Any]) -> str:
    lines = [
        f"classification: {result['classification']}",
        f"repair_status: {result['repair_status']}",
        f"explanation: {result['explanation']}",
    ]
    problem = result.get("problem")
    if problem:
        lines.append("problem:")
        lines.extend(f"  {edge}" for edge in problem["graph"])
        lines.append(f"  why_unsafe: {problem['why_unsafe']}")
    if result["repair_graph"]:
        lines.append("repair_graph:")
        lines.extend(f"  {edge}" for edge in result["repair_graph"])
    if result["proof_obligations"]:
        lines.append("proof_obligations:")
        for obligation in result["proof_obligations"]:
            forbidden = obligation.get("forbidden_consumer") or obligation.get("forbidden_consumer_exec_id")
            if forbidden:
                lines.append(
                    f"  {obligation['obligation']}: forbid {forbidden} "
                    f"from consuming result {obligation.get('result_id')}"
                )
            else:
                lines.append(f"  {obligation['obligation']}: result {obligation.get('result_id')}")
    if result["recommendations"]:
        lines.append("recommendations:")
        lines.extend(f"  - {item}" for item in result["recommendations"])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a Causal Halting repair report.")
    parser.add_argument("input", help="Analysis JSON file from design or trace analysis.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        analysis = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "classification": "parse_error",
            "repair_status": "error",
            "problem": None,
            "repair_graph": [],
            "proof_obligations": [],
            "recommendations": [],
            "explanation": str(exc),
        }
    else:
        result = repair_analysis(analysis if isinstance(analysis, dict) else {})

    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_human(result))
    return 2 if result["classification"] == "parse_error" else 0


if __name__ == "__main__":
    sys.exit(main())
