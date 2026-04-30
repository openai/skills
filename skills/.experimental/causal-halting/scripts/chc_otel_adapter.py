#!/usr/bin/env python3
"""Convert explicitly annotated OpenTelemetry JSON spans into CHC trace events.

This adapter does not infer causal meaning from span names or natural language.
It only reads structured `chc.*` attributes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def otel_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    for key in ("stringValue", "intValue", "doubleValue", "boolValue"):
        if key in value:
            return value[key]
    if "arrayValue" in value:
        return value["arrayValue"]
    if "kvlistValue" in value:
        return value["kvlistValue"]
    return value


def attrs_to_dict(attributes: Any) -> dict[str, Any]:
    if isinstance(attributes, dict):
        return attributes
    result: dict[str, Any] = {}
    if not isinstance(attributes, list):
        return result
    for item in attributes:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        if isinstance(key, str):
            result[key] = otel_value(item.get("value"))
    return result


def iter_spans(payload: Any) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return spans
    if isinstance(payload.get("spans"), list):
        spans.extend(item for item in payload["spans"] if isinstance(item, dict))
    for resource_span in payload.get("resourceSpans", []):
        if not isinstance(resource_span, dict):
            continue
        for scope_span in resource_span.get("scopeSpans", []):
            if isinstance(scope_span, dict):
                spans.extend(item for item in scope_span.get("spans", []) if isinstance(item, dict))
        for instrumentation_span in resource_span.get("instrumentationLibrarySpans", []):
            if isinstance(instrumentation_span, dict):
                spans.extend(item for item in instrumentation_span.get("spans", []) if isinstance(item, dict))
    return spans


def span_metadata(carrier: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(carrier, dict):
        return {}
    metadata: dict[str, Any] = {}
    if isinstance(carrier.get("name"), str):
        metadata["event_source"] = carrier["name"]
    if isinstance(carrier.get("spanId"), str):
        metadata["span_id"] = carrier["spanId"]
    if isinstance(carrier.get("parentSpanId"), str):
        metadata["parent_id"] = carrier["parentSpanId"]
    timestamp = carrier.get("timeUnixNano", carrier.get("startTimeUnixNano"))
    if timestamp is not None:
        metadata["timestamp"] = str(timestamp)
    return metadata


def add_metadata(event: dict[str, Any], attrs: dict[str, Any], carrier: dict[str, Any] | None) -> dict[str, Any]:
    metadata = span_metadata(carrier)
    attr_map = {
        "chc.event.source": "event_source",
        "chc.timestamp": "timestamp",
        "chc.span.id": "span_id",
        "chc.parent.id": "parent_id",
        "chc.confidence": "confidence",
    }
    for source_key, target_key in attr_map.items():
        if source_key in attrs:
            metadata[target_key] = attrs[source_key]
    return {**event, **{key: value for key, value in metadata.items() if value is not None}}


def event_from_attrs(attrs: dict[str, Any], carrier: dict[str, Any] | None = None) -> dict[str, Any] | None:
    event_type = attrs.get("chc.event.type")
    if event_type == "exec_start":
        return add_metadata({
            "type": "exec_start",
            "exec_id": attrs.get("chc.exec.id"),
            "program": attrs.get("chc.program"),
            "input": attrs.get("chc.input"),
        }, attrs, carrier)
    if event_type == "exec_end":
        return add_metadata({
            "type": "exec_end",
            "exec_id": attrs.get("chc.exec.id"),
            "status": attrs.get("chc.status", "halted"),
        }, attrs, carrier)
    if event_type == "observe":
        return add_metadata({
            "type": "observe",
            "observer": attrs.get("chc.observer", "Observer"),
            "target_exec_id": attrs.get("chc.target_exec.id"),
            "result_id": attrs.get("chc.result.id"),
        }, attrs, carrier)
    if event_type == "consume":
        event = {
            "type": "consume",
            "result_id": attrs.get("chc.result.id"),
            "consumer_exec_id": attrs.get("chc.consumer_exec.id"),
            "consumer": attrs.get("chc.consumer"),
            "purpose": attrs.get("chc.purpose", "control"),
        }
        return add_metadata({key: value for key, value in event.items() if value is not None}, attrs, carrier)
    if event_type == "control_exec":
        event = {
            "type": "control_exec",
            "controlled_exec_id": attrs.get("chc.controlled_exec.id"),
            "controller_exec_id": attrs.get("chc.controller_exec.id"),
            "controller": attrs.get("chc.controller"),
            "action": attrs.get("chc.action", "control"),
        }
        return add_metadata({key: value for key, value in event.items() if value is not None}, attrs, carrier)
    return None


def otel_to_events(payload: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for span in iter_spans(payload):
        span_event = event_from_attrs(attrs_to_dict(span.get("attributes", [])), span)
        if span_event is not None:
            events.append(span_event)
        for event in span.get("events", []):
            if isinstance(event, dict):
                nested = event_from_attrs(attrs_to_dict(event.get("attributes", [])), event)
                if nested is not None:
                    events.append(nested)
    return events


def validate_events(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, event in enumerate(events):
        event_type = event.get("type")
        if event_type == "exec_start":
            if not isinstance(event.get("exec_id"), str) or not isinstance(event.get("program"), str):
                errors.append(f"event {index}: exec_start requires chc.exec.id and chc.program")
        elif event_type == "exec_end":
            if not isinstance(event.get("exec_id"), str):
                errors.append(f"event {index}: exec_end requires chc.exec.id")
        elif event_type == "observe":
            if not isinstance(event.get("target_exec_id"), str) or not isinstance(event.get("result_id"), str):
                errors.append(f"event {index}: observe requires chc.target_exec.id and chc.result.id")
        elif event_type == "consume":
            if not isinstance(event.get("result_id"), str):
                errors.append(f"event {index}: consume requires chc.result.id")
        elif event_type == "control_exec":
            if not isinstance(event.get("controlled_exec_id"), str):
                errors.append(f"event {index}: control_exec requires chc.controlled_exec.id")
        else:
            errors.append(f"event {index}: unsupported CHC event type {event_type!r}")
    return errors


def format_jsonl(events: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(event, sort_keys=True) for event in events)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert annotated OpenTelemetry JSON to CHC trace JSONL.")
    parser.add_argument("input", help="OpenTelemetry JSON file.")
    parser.add_argument("--format", choices=("jsonl", "json"), default="jsonl")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    events = otel_to_events(payload)
    errors = validate_events(events)
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(events, indent=2, sort_keys=True))
    else:
        print(format_jsonl(events))
    return 0


if __name__ == "__main__":
    sys.exit(main())
