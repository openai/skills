#!/usr/bin/env python3
"""Helper utilities for standardized agent-team protocol tags."""

from __future__ import annotations

import argparse
import json
import re


def _normalize_value(value: str) -> str:
    text = (value or "").strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text)
    text = text.strip("-")
    return text


def build_protocol_tags(
    *,
    task_id: str,
    state: str,
    owner_role: str,
    handoff_id: str,
    project: str,
) -> list[str]:
    fields = {
        "task_id": task_id,
        "state": state,
        "owner_role": owner_role,
        "handoff_id": handoff_id,
        "project": project,
    }

    missing = [key for key, value in fields.items() if not str(value or "").strip()]
    if missing:
        raise ValueError("missing required protocol tag field(s): " + ", ".join(missing))

    tags = []
    for key, value in fields.items():
        normalized = _normalize_value(str(value))
        if not normalized:
            raise ValueError(f"protocol tag value for '{key}' normalizes to empty")
        tags.append(f"{key}:{normalized}")
    return tags


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--owner-role", required=True)
    parser.add_argument("--handoff-id", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--output", choices=("json", "text"), default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        tags = build_protocol_tags(
            task_id=args.task_id,
            state=args.state,
            owner_role=args.owner_role,
            handoff_id=args.handoff_id,
            project=args.project,
        )
    except Exception as exc:
        payload = {"status": "error", "error": str(exc)}
        if args.output == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(f"protocol tag error: {exc}")
        return 2

    payload = {
        "status": "ok",
        "tags": tags,
        "query": " ".join(tags),
    }
    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print("tags:")
        for row in tags:
            print(f"- {row}")
        print(f"query: {payload['query']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
