"""Local file adapter."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from agentfeeds_runtime.adapters.common import envelope


def fetch_local_file(stream: dict, adapter: dict, stream_uri: str) -> list[dict]:
    path = Path(adapter["path"]).expanduser()
    if not path.is_absolute():
        path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"{stream['id']}: local file not found: {path}")
    if not path.is_file():
        raise ValueError(f"{stream['id']}: local path is not a file: {path}")

    raw = path.read_bytes()
    stat = path.stat()
    modified_at = datetime.fromtimestamp(stat.st_mtime, UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    data = {
        "path": str(path),
        "name": path.name,
        "extension": path.suffix.lstrip("."),
        "content": raw.decode("utf-8", errors="replace"),
        "size_bytes": stat.st_size,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "modified_at": modified_at,
    }
    return [envelope(stream, stream_uri, data["sha256"], data, modified_at)]
