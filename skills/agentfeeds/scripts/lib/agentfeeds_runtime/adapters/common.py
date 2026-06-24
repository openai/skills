"""Shared adapter helpers."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

import jmespath

from agentfeeds_runtime.constants import AGENTFEEDS_VERSION


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def jmespath_search(expression: str | None, document: object) -> object:
    if not expression:
        return None
    return jmespath.search(expression, document)


def envelope(stream: dict, stream_uri: str, event_id: object, data: dict, event_time: str | None = None) -> dict:
    return {
        "specversion": AGENTFEEDS_VERSION,
        "id": str(event_id or stable_hash(data)),
        "source": stream_uri,
        "type": stream["type"],
        "time": event_time or now_utc(),
        "schema_url": stream["schema_url"],
        "schema_version": stream["schema_version"],
        "mode": stream["mode"],
        "data": data,
    }
