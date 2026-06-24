"""HTTP JSON adapters."""

from __future__ import annotations

import requests

from agentfeeds_runtime.adapters.common import envelope, jmespath_search, stable_hash
from agentfeeds_runtime.constants import REQUEST_TIMEOUT_SECONDS


def fetch_json(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    response = requests.request(
        adapter.get("method", "GET"),
        adapter["url"],
        headers=adapter.get("headers") or {},
        json=adapter.get("body"),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    raw = response.json()
    expression = adapter.get("transform", {}).get("expression")
    transformed = jmespath_search(expression, raw) if expression else raw

    if adapter["kind"] == "json_http" and stream["mode"] == "snapshot":
        if not isinstance(transformed, dict):
            raise ValueError(f"{stream['id']}: json_http transform must produce an object")
        event_id = jmespath_search(adapter.get("id_from"), raw) or stable_hash(transformed)
        return [envelope(stream, stream_uri, event_id, transformed)]

    if not isinstance(transformed, list):
        raise ValueError(f"{stream['id']}: {adapter['kind']} event transform must produce an array")
    events = []
    for item in transformed:
        if not isinstance(item, dict):
            raise ValueError(f"{stream['id']}: {adapter['kind']} event items must be objects")
        event_id = jmespath_search(adapter.get("id_from"), item) or stable_hash(item)
        events.append(envelope(stream, stream_uri, event_id, item))
    return events
