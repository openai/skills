"""Local command adapter."""

from __future__ import annotations

import json
import os
import signal
import subprocess
from pathlib import Path

from agentfeeds_runtime.adapters.common import envelope, jmespath_search, now_utc, stable_hash
from agentfeeds_runtime.constants import COMMAND_MAX_OUTPUT_BYTES, COMMAND_TIMEOUT_SECONDS


def _decode_limited(raw: bytes, limit: int) -> tuple[str, bool]:
    truncated = len(raw) > limit
    return raw[:limit].decode("utf-8", errors="replace"), truncated


def run_local_command(stream: dict, adapter: dict) -> dict:
    command = adapter.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
        raise ValueError(f"{stream['id']}: local_command adapter.command must be a non-empty string array")

    timeout_seconds = int(adapter.get("timeout_seconds") or COMMAND_TIMEOUT_SECONDS)
    max_output_bytes = int(adapter.get("max_output_bytes") or COMMAND_MAX_OUTPUT_BYTES)
    cwd = adapter.get("cwd")
    if cwd is not None:
        cwd = str(Path(str(cwd)).expanduser())

    started_at = now_utc()
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env={key: os.environ[key] for key in ("HOME", "PATH", "USER", "SHELL") if key in os.environ},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=os.name == "posix",
    )
    timed_out = False
    try:
        stdout_raw, stderr_raw = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:  # pragma: no cover - native Windows is not a supported polling target yet.
            process.kill()
        stdout_raw, stderr_raw = process.communicate()
    ran_at = now_utc()
    stdout, stdout_truncated = _decode_limited(stdout_raw, max_output_bytes)
    stderr, stderr_truncated = _decode_limited(stderr_raw, max_output_bytes)

    parsed_json = None
    transformed = None
    if adapter.get("parse") == "json" and not timed_out:
        parsed_json = json.loads(stdout or "null")
        expression = adapter.get("transform", {}).get("expression")
        transformed = jmespath_search(expression, parsed_json) if expression else parsed_json

    return {
        "command": command,
        "cwd": cwd,
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
        "parsed_json": parsed_json,
        "transformed": transformed,
        "started_at": started_at,
        "ran_at": ran_at,
    }


def fetch_local_command_events(stream: dict, adapter: dict, stream_uri: str, result: dict) -> list[dict]:
    if adapter.get("parse") != "json":
        raise ValueError(f"{stream['id']}: local_command event streams require parse: json")

    items_expression = adapter.get("items_from") or "@"
    items = jmespath_search(items_expression, result["parsed_json"])
    if not isinstance(items, list):
        raise ValueError(f"{stream['id']}: local_command items_from must produce an array")

    transform_expression = adapter.get("transform", {}).get("expression")
    id_expression = adapter.get("id_from")
    time_expression = adapter.get("time_from")
    events = []
    for item in items:
        transformed = jmespath_search(transform_expression, item) if transform_expression else item
        if not isinstance(transformed, dict):
            raise ValueError(f"{stream['id']}: local_command event transform must produce an object")
        event_id = jmespath_search(id_expression, item) if id_expression else None
        if event_id is None:
            event_id = stable_hash(item)
        event_time = jmespath_search(time_expression, item) if time_expression else None
        if event_time is None:
            event_time = result["ran_at"]
        events.append(envelope(stream, stream_uri, event_id, transformed, str(event_time) if event_time else None))
    return events


def fetch_local_command(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    result = run_local_command(stream, adapter)

    if stream["mode"] == "event":
        return fetch_local_command_events(stream, adapter, stream_uri, result)
    if stream["mode"] != "snapshot":
        raise ValueError(f"{stream['id']}: local_command supports snapshot and event modes")

    data = result
    return [envelope(stream, stream_uri, stable_hash(data), data, result["ran_at"])]
