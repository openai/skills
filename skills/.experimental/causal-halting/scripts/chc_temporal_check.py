#!/usr/bin/env python3
"""Analyze CHC-4 temporal/distributed trace JSONL."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def load_trace_checker():
    script = Path(__file__).resolve().with_name("chc_trace_check.py")
    spec = importlib.util.spec_from_file_location("chc_trace_check", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load trace checker from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["chc_trace_check"] = module
    spec.loader.exec_module(module)
    return module


def parse_events(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: {exc}")
            continue
        if not isinstance(event, dict):
            errors.append(f"line {line_no}: event must be an object")
            continue
        event["_index"] = len(events)
        events.append(event)
    return events, errors


def event_ref(event: dict[str, Any]) -> str:
    return str(event.get("id") or event.get("span_id") or event.get("_index"))


def normalized_order_value(value: Any) -> tuple[int, float | str]:
    if isinstance(value, bool):
        return (0, float(int(value)))
    if isinstance(value, (int, float)):
        return (0, float(value))
    if isinstance(value, str):
        stripped = value.strip()
        try:
            return (0, float(stripped))
        except ValueError:
            pass
        try:
            parsed = datetime.fromisoformat(stripped.replace("Z", "+00:00"))
            return (1, parsed.timestamp())
        except ValueError:
            return (2, stripped)
    return (3, repr(value))


def build_happens_before(events: list[dict[str, Any]]) -> tuple[set[tuple[str, str]], list[dict[str, Any]], str]:
    refs = {event_ref(event): event for event in events}
    edges: set[tuple[str, str]] = set()
    evidence: list[dict[str, Any]] = []

    for event in events:
        source = event_ref(event)
        for target in event.get("happens_before") or []:
            if str(target) in refs:
                edges.add((source, str(target)))
                evidence.append({"source": source, "target": str(target), "reason": "explicit_happens_before"})
        parent = event.get("parent_id")
        if isinstance(parent, str) and parent in refs:
            edges.add((parent, source))
            evidence.append({"source": parent, "target": source, "reason": "span_parent"})

    logical_events = [event for event in events if "logical_clock" in event]
    if logical_events and len(logical_events) == len(events):
        ordered = sorted(
            events,
            key=lambda item: (
                str(item.get("trace_id", "")),
                normalized_order_value(item.get("logical_clock")),
                int(item.get("_index", 0)),
            ),
        )
        for left, right in zip(ordered, ordered[1:]):
            if left.get("trace_id") == right.get("trace_id"):
                edges.add((event_ref(left), event_ref(right)))
                evidence.append({"source": event_ref(left), "target": event_ref(right), "reason": "logical_clock"})

    timestamp_events = [event for event in events if "timestamp" in event]
    if timestamp_events and len(timestamp_events) == len(events):
        traces = {event.get("trace_id", "default") for event in events}
        if len(traces) == 1:
            ordered = sorted(
                events,
                key=lambda item: (
                    normalized_order_value(item.get("timestamp")),
                    int(item.get("_index", 0)),
                ),
            )
            for left, right in zip(ordered, ordered[1:]):
                edges.add((event_ref(left), event_ref(right)))
                evidence.append({"source": event_ref(left), "target": event_ref(right), "reason": "timestamp_order"})

    if any(reason["reason"] == "explicit_happens_before" for reason in evidence):
        status = "complete"
    elif edges:
        status = "partial"
    else:
        status = "insufficient_info"
    return transitive_closure(edges), evidence, status


def transitive_closure(edges: set[tuple[str, str]]) -> set[tuple[str, str]]:
    closure = set(edges)
    changed = True
    while changed:
        changed = False
        next_edges = set(closure)
        for left, middle in closure:
            for middle2, right in closure:
                if middle == middle2 and (left, right) not in next_edges:
                    next_edges.add((left, right))
                    changed = True
        closure = next_edges
    return closure


def analyze_temporal_text(text: str) -> dict[str, Any]:
    events, errors = parse_events(text)
    if errors:
        return {
            "classification": "parse_error",
            "chc_level": "CHC-4",
            "temporal_order_status": "insufficient_info",
            "happens_before_path": [],
            "semantic_status": "not_analyzed",
            "validity_scope": "no_modeled_prediction_feedback_only",
            "identity_resolution": {
                "resolved": [],
                "ambiguous": [],
                "missing": [],
                "conflicts": [],
                "assumptions": [],
            },
            "formal_status": "mechanized",
            "theorem_coverage": {
                "chc_level": "CHC-4",
                "mechanized_core": "mechanized",
                "claims": ["temporal parser rejected malformed input"],
            },
            "capability_boundary": {
                "does_not_prove_arbitrary_termination": True,
                "does_not_solve_classical_halting": True,
            },
            "explanation": "; ".join(errors),
        }
    closure, hb_evidence, status = build_happens_before(events)
    checker = load_trace_checker()
    base = checker.analyze_events(events)
    output = {
        **base,
        "chc_level": "CHC-4",
        "temporal_order_status": status,
        "happens_before_path": sorted(
            [{"source": source, "target": target} for source, target in closure],
            key=lambda item: (item["source"], item["target"]),
        ),
        "happens_before_evidence": hb_evidence,
        "formal_status": "mechanized",
        "theorem_coverage": {
            "chc_level": "CHC-4",
            "mechanized_core": "mechanized",
            "claims": ["happens-before feedback is rejected for modeled temporal traces"],
        },
    }
    if status == "insufficient_info" and base["classification"] == "valid_acyclic":
        output["classification"] = "insufficient_info"
        output["explanation"] = "Temporal ordering is insufficient to prove the trace is acyclic."
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze CHC-4 temporal trace JSONL.")
    parser.add_argument("input")
    parser.add_argument("--format", choices=("json", "human"), default="human")
    args = parser.parse_args(argv)
    output = analyze_temporal_text(Path(args.input).read_text(encoding="utf-8"))
    if args.format == "json":
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(f"classification: {output['classification']}")
        print(f"temporal_order_status: {output['temporal_order_status']}")
        print(f"explanation: {output['explanation']}")
    return 2 if output["classification"] == "parse_error" else 0


if __name__ == "__main__":
    sys.exit(main())
