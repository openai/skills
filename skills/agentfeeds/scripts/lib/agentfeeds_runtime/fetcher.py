#!/usr/bin/env python3
"""Reference fetcher for Agent Feeds v0.3."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import jsonschema
import requests

from agentfeeds_runtime.adapters import run_adapter as run_adapter_impl
from agentfeeds_runtime.constants import REQUEST_TIMEOUT_SECONDS

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows import compatibility.
    fcntl = None

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


SPEC_VERSION = "0.3"
DEFAULT_ROOT = Path.home() / ".agentfeeds"
DEFAULT_CATALOG_BASE_URL = "https://raw.githubusercontent.com/verkyyi/agentfeeds-catalog/main"
PARAMETER_PATTERN = re.compile(r"{([A-Za-z_][A-Za-z0-9_]*)}")
SECRET_REF_PATTERN = re.compile(r"\{\{secret:([A-Za-z_][A-Za-z0-9_.-]*)\}\}")
SENSITIVE_OUTPUT_PATTERN = re.compile(
    r"(?i)(authorization|token|api[-_ ]?key|secret|cookie)([\"'\s:=]+)([^\"'\s,}]+)"
)
UNSAFE_NAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")
LOCK_FILE_NAME = "agentfeeds-fetch.lock"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def safe_name_part(value: str, fallback: str = "part", max_chars: int = 96) -> str:
    compact = UNSAFE_NAME_PATTERN.sub("-", value).strip("-._")
    if not compact:
        compact = fallback
    if len(compact) > max_chars:
        compact = compact[:max_chars].rstrip("-._") or fallback
    return compact


def query_name_part(query: str) -> str:
    compact = safe_name_part(query.replace("&", "-"), "query", 96)
    digest = hashlib.sha256(query.encode("utf-8")).hexdigest()[:12]
    return f"{compact}.{digest}"


def state_path_for_stream(stream_uri: str, root: Path = DEFAULT_ROOT) -> Path:
    parsed = urlparse(stream_uri)
    if parsed.scheme != "feed" or not parsed.netloc:
        raise ValueError(f"invalid feed URI: {stream_uri}")

    path = ".".join(safe_name_part(part, "path") for part in parsed.path.split("/") if part)
    name = path or "index"
    if parsed.netloc == "local.file":
        params = parse_qs(parsed.query, keep_blank_values=True)
        local_path = (params.get("path") or [""])[0]
        stem = safe_name_part(Path(local_path).name, "file")
        digest = hashlib.sha256(parsed.query.encode("utf-8")).hexdigest()[:12]
        return root / "state" / parsed.netloc / f"{name}.{stem}.{digest}.json"
    if parsed.query:
        name = f"{name}.{query_name_part(parsed.query)}"
    return root / "state" / parsed.netloc / f"{name}.json"


def atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    tmp_path.replace(path)


def status_path_for_subscription(root: Path, subscription_id: str) -> Path:
    parts = [part for part in subscription_id.split("/") if part]
    if not parts:
        parts = ["unknown"]
    safe_parts = [re.sub(r"[^A-Za-z0-9._-]+", "-", part).strip("-") or "unknown" for part in parts]
    safe_parts[-1] = f"{safe_parts[-1]}.json"
    return root / "status" / "subscriptions" / Path(*safe_parts)


def load_fetch_status(root: Path, subscription_id: str) -> dict:
    return load_existing_state(status_path_for_subscription(root, subscription_id)) or {}


def redact_sensitive_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = re.sub(r"(?i)(authorization[\"'\s:=]+)[^,\n}]+", r"\1[redacted]", value)
    return SENSITIVE_OUTPUT_PATTERN.sub(lambda match: f"{match.group(1)}{match.group(2)}[redacted]", value)


def write_fetch_status(
    root: Path,
    subscription: dict,
    stream: dict | None,
    *,
    attempted_at: str,
    succeeded: bool,
    error: str | None = None,
    state_path: Path | None = None,
) -> None:
    subscription_id = str(subscription.get("id", "<unknown>"))
    previous = load_fetch_status(root, subscription_id)
    payload = {
        "subscription_id": subscription_id,
        "template_id": template_id_for(subscription) if subscription.get("template") else None,
        "title": subscription_title(subscription, stream or {}) if stream else str(subscription.get("title") or subscription_id),
        "last_attempt_at": attempted_at,
        "last_success_at": attempted_at if succeeded else previous.get("last_success_at"),
        "last_error_at": None if succeeded else attempted_at,
        "last_error": None if succeeded else redact_sensitive_text(error),
        "consecutive_failures": 0 if succeeded else int(previous.get("consecutive_failures") or 0) + 1,
        "state_path": str(state_path.relative_to(root)) if state_path and root in state_path.parents else previous.get("state_path"),
    }
    atomic_write_json(status_path_for_subscription(root, subscription_id), payload)


@contextlib.contextmanager
def fetch_lock(root: Path):
    if fcntl is None:
        raise RuntimeError("Agent Feeds background locking requires a POSIX platform such as macOS, Linux, or WSL")
    path = root / LOCK_FILE_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            handle.seek(0)
            handle.truncate()
            handle.write(f"pid={os.getpid()} acquired_at={now_utc()}\n")
            handle.flush()
            os.fsync(handle.fileno())
            yield True
        finally:
            handle.seek(0)
            handle.truncate()
            handle.flush()
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def ensure_root(root: Path) -> None:
    (root / "approvals" / "local-command").mkdir(parents=True, exist_ok=True)
    (root / "catalog-cache").mkdir(parents=True, exist_ok=True)
    (root / "secrets").mkdir(parents=True, exist_ok=True)
    (root / "state").mkdir(parents=True, exist_ok=True)
    (root / "templates" / "streams").mkdir(parents=True, exist_ok=True)
    (root / "templates" / "schemas" / "event-types").mkdir(parents=True, exist_ok=True)
    subscriptions = root / "subscriptions.yaml"
    if not subscriptions.exists():
        subscriptions.write_text(
            'version: "0.3"\n'
            "defaults:\n"
            "  poll_interval_seconds: 600\n"
            "  history_limit: 50\n"
            "subscriptions: []\n",
            encoding="utf-8",
        )


def load_subscriptions(root: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read subscriptions.yaml")
    path = root / "subscriptions.yaml"
    if not path.exists():
        return {"version": SPEC_VERSION, "subscriptions": []}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def templates_root(root: Path) -> Path:
    return root / "templates"


def template_streams_root(root: Path) -> Path:
    return templates_root(root) / "streams"


def template_schemas_root(root: Path) -> Path:
    return templates_root(root) / "schemas" / "event-types"


def catalog_cache_root(root: Path) -> Path:
    return root / "catalog-cache"


def cached_catalog_file(root: Path, relative_path: str) -> Path:
    return catalog_cache_root(root) / relative_path


def bundled_catalog_root() -> Path:
    return repo_root() / "catalog"


def local_catalog_root() -> Path | None:
    configured = os.environ.get("AGENTFEEDS_CATALOG_DIR")
    candidates = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.append(repo_root())

    for candidate in candidates:
        if (candidate / "catalog" / "INDEX.json").exists():
            return candidate
        if candidate.name == "catalog" and (candidate / "INDEX.json").exists():
            return candidate.parent
    return None


def catalog_base_url() -> str:
    return os.environ.get("AGENTFEEDS_CATALOG_BASE_URL", DEFAULT_CATALOG_BASE_URL).rstrip("/")


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(content, encoding="utf-8")
    tmp_path.replace(path)


def copy_catalog_cache_from_dir(root: Path, source_root: Path) -> None:
    cache_root = catalog_cache_root(root)
    catalog_root = source_root / "catalog"
    index_text = (catalog_root / "INDEX.json").read_text(encoding="utf-8")
    write_text_atomic(cache_root / "INDEX.json", index_text)
    write_text_atomic(cache_root / "catalog" / "INDEX.json", index_text)

    for path in sorted(catalog_root.glob("**/*")):
        if path.is_file():
            relative_path = path.relative_to(source_root)
            write_text_atomic(cache_root / relative_path, path.read_text(encoding="utf-8"))


def download_catalog_cache(root: Path) -> None:
    cache_root = catalog_cache_root(root)
    base_url = catalog_base_url()
    index_response = requests.get(f"{base_url}/catalog/INDEX.json", timeout=REQUEST_TIMEOUT_SECONDS)
    index_response.raise_for_status()
    index_text = index_response.text
    index = json.loads(index_text)

    write_text_atomic(cache_root / "INDEX.json", index_text)
    write_text_atomic(cache_root / "catalog" / "INDEX.json", index_text)

    schema_names = {"stream-definition.v0.3.json", "envelope.v0.3.json"}
    for stream in index.get("streams", []):
        relative_path = stream["path"]
        response = requests.get(f"{base_url}/{relative_path}", timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        stream_text = response.text
        write_text_atomic(cache_root / relative_path, stream_text)
        stream_payload = yaml.safe_load(stream_text)
        schema_names.add(stream_payload["schema_url"].rstrip("/").split("/")[-1])

    for name in sorted(schema_names):
        if name in {"stream-definition.v0.3.json", "envelope.v0.3.json"}:
            relative_path = f"catalog/schemas/{name}"
        else:
            relative_path = f"catalog/schemas/event-types/{name}"
        response = requests.get(f"{base_url}/{relative_path}", timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        write_text_atomic(cache_root / relative_path, response.text)


def update_catalog_cache(root: Path) -> None:
    source_root = local_catalog_root()
    if source_root is not None:
        copy_catalog_cache_from_dir(root, source_root)
        return
    download_catalog_cache(root)


def load_catalog_index(root: Path) -> dict:
    cache = catalog_cache_root(root) / "INDEX.json"
    if not cache.exists():
        update_catalog_cache(root)
    index = json.loads(cache.read_text(encoding="utf-8"))
    streams = {stream["id"]: {**stream, "source": stream.get("source") or "builtin"} for stream in index.get("streams", [])}
    for path in sorted(template_streams_root(root).glob("**/*.yaml")):
        stream = stream_summary(path, root)
        if stream["id"] in streams:
            continue
        streams[stream["id"]] = stream
    merged = {**index, "streams": sorted(streams.values(), key=lambda item: item["id"])}
    merged["stream_count"] = len(merged["streams"])
    return merged


def stream_summary(path: Path, root: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    try:
        rel_path = str(path.relative_to(catalog_cache_root(root)))
        source = "builtin"
    except ValueError:
        try:
            rel_path = str(path.relative_to(repo_root()))
            source = "builtin"
        except ValueError:
            rel_path = str(path)
            source = "local"
    try:
        path.relative_to(template_streams_root(root))
        rel_path = str(path)
        source = "local"
    except ValueError:
        pass
    return {
        "id": data["id"],
        "title": data["title"],
        "description": data["description"],
        "type": data["type"],
        "mode": data["mode"],
        "tags": data.get("tags", []),
        "parameters": [param["name"] for param in data.get("parameters", [])],
        "auth": data["auth"],
        "quality_tier": data["quality_tier"],
        "path": rel_path,
        "source": source,
    }


def stream_definition_schema_path(root: Path) -> Path:
    candidates = [
        cached_catalog_file(root, "catalog/schemas/stream-definition.v0.3.json"),
        bundled_catalog_root() / "schemas" / "stream-definition.v0.3.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    update_catalog_cache(root)
    cached = cached_catalog_file(root, "catalog/schemas/stream-definition.v0.3.json")
    if cached.exists():
        return cached
    raise FileNotFoundError("stream definition schema not found in catalog cache")


def builtin_stream_paths(root: Path):
    yield from (catalog_cache_root(root) / "catalog" / "streams").glob("**/*.yaml")
    yield from (bundled_catalog_root() / "streams").glob("**/*.yaml")


def cached_event_schemas_root(root: Path) -> Path:
    return cached_catalog_file(root, "catalog/schemas/event-types")


def load_stream_definition(root: Path, stream_id: str, _refreshed: bool = False) -> dict:
    index = load_catalog_index(root)
    match = next((item for item in index.get("streams", []) if item.get("id") == stream_id), None)
    if not match:
        raise KeyError(f"stream id not found in catalog: {stream_id}")

    candidate_paths = []
    if match.get("path"):
        match_path = Path(match["path"])
        if match_path.is_absolute():
            candidate_paths.append(match_path)
        else:
            candidate_paths.append(repo_root() / match["path"])
            candidate_paths.append(root / "catalog-cache" / match["path"])
            candidate_paths.append(templates_root(root) / match["path"])
    candidate_paths.extend(template_streams_root(root).glob("**/*.yaml"))
    candidate_paths.extend(builtin_stream_paths(root))

    for path in candidate_paths:
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data.get("id") == stream_id:
            return data
    if match.get("source") != "local" and not _refreshed:
        update_catalog_cache(root)
        return load_stream_definition(root, stream_id, _refreshed=True)
    raise FileNotFoundError(f"stream definition not found for {stream_id}")


def schema_path_for_url(root: Path, schema_url: str) -> Path:
    name = schema_url.rstrip("/").split("/")[-1]
    for path in [
        template_schemas_root(root) / name,
        cached_event_schemas_root(root) / name,
        bundled_catalog_root() / "schemas" / "event-types" / name,
    ]:
        if path.exists():
            return path
    update_catalog_cache(root)
    cached = cached_event_schemas_root(root) / name
    if cached.exists():
        return cached
    raise FileNotFoundError(f"referenced schema not found locally: {schema_url}")


def validate_stream_file(path: Path, root: Path = DEFAULT_ROOT) -> None:
    stream = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema = json.loads(stream_definition_schema_path(root).read_text(encoding="utf-8"))
    jsonschema.validate(stream, schema)

    schema_path = schema_path_for_url(root, stream["schema_url"])
    json.loads(schema_path.read_text(encoding="utf-8"))

    adapter_kind = stream["adapter"]["kind"]
    if adapter_kind in {"json_http", "paginated_json_http"}:
        for required in ("url", "method", "transform"):
            if required not in stream["adapter"]:
                raise ValueError(f"{path}: adapter.{required} is required for {adapter_kind}")
    if adapter_kind in {"rss", "ical"} and "url" not in stream["adapter"]:
        raise ValueError(f"{path}: adapter.url is required for {adapter_kind}")
    path_based_adapters = {"local_file", "filesystem_scan", "markdown_scan", "git_status", "plist_reading_list"}
    if adapter_kind in path_based_adapters and "path" not in stream["adapter"]:
        raise ValueError(f"{path}: adapter.path is required for {adapter_kind}")
    if adapter_kind == "local_command":
        command = stream["adapter"].get("command")
        if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
            raise ValueError(f"{path}: adapter.command must be a non-empty string array for local_command")
        if stream["mode"] == "event" and stream["adapter"].get("parse") != "json":
            raise ValueError(f"{path}: local_command event streams require adapter.parse: json")
    if adapter_kind == "apple_automation":
        for required in ("script", "columns"):
            if required not in stream["adapter"]:
                raise ValueError(f"{path}: adapter.{required} is required for apple_automation")
    if adapter_kind == "sqlite_query":
        for required in ("database", "query", "columns"):
            if required not in stream["adapter"]:
                raise ValueError(f"{path}: adapter.{required} is required for sqlite_query")
    tcc_adapters = {"apple_automation", "sqlite_query"}
    if adapter_kind in tcc_adapters and "tcc_permission" not in stream["adapter"]:
        raise ValueError(f"{path}: adapter.tcc_permission is required for {adapter_kind}")


def validate_template_tree(root: Path) -> list[Path]:
    stream_paths = sorted(template_streams_root(root).glob("**/*.yaml"))
    seen: dict[str, Path] = {}
    index = load_catalog_index(root)
    builtin_ids = {stream["id"] for stream in index.get("streams", []) if stream.get("source") != "local"}
    for path in stream_paths:
        validate_stream_file(path, root)
        stream_id = yaml.safe_load(path.read_text(encoding="utf-8"))["id"]
        if stream_id in builtin_ids:
            raise ValueError(f"{path}: local template id conflicts with built-in template: {stream_id}")
        if stream_id in seen:
            raise ValueError(f"{path}: duplicate local template id also defined in {seen[stream_id]}: {stream_id}")
        seen[stream_id] = path
    return stream_paths


def substitute(value: object, parameters: dict) -> object:
    if isinstance(value, str):
        return PARAMETER_PATTERN.sub(
            lambda match: str(parameters[match.group(1)])
            if match.group(1) in parameters
            else match.group(0),
            value,
        )
    if isinstance(value, list):
        return [substitute(item, parameters) for item in value]
    if isinstance(value, dict):
        return {key: substitute(item, parameters) for key, item in value.items()}
    return value


def source_uri_for(stream: dict, parameters: dict) -> str:
    return substitute(stream["source_uri_template"], parameters)


def secret_path(root: Path, name: str) -> Path:
    safe = safe_name_part(name, "secret")
    return root / "secrets" / f"{safe}.txt"


def read_secret(root: Path, name: str) -> str:
    if sys.platform == "darwin":
        result = subprocess.run(
            ["security", "find-generic-password", "-s", "agentfeeds", "-a", name, "-w"],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            return result.stdout.rstrip("\n")
    path = secret_path(root, name)
    if not path.exists():
        raise KeyError(f"secret {name} not set; user can run `python3 scripts/agentfeeds.py admin secrets set {name}`")
    return path.read_text(encoding="utf-8").rstrip("\n")


def write_secret(root: Path, name: str, value: str) -> None:
    if sys.platform == "darwin":
        result = subprocess.run(
            ["security", "add-generic-password", "-U", "-s", "agentfeeds", "-a", name, "-w", value],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            return
    path = secret_path(root, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip("\n") + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


def resolve_secret_refs(root: Path, value: object) -> object:
    if isinstance(value, str):
        return SECRET_REF_PATTERN.sub(lambda match: read_secret(root, match.group(1)), value)
    if isinstance(value, list):
        return [resolve_secret_refs(root, item) for item in value]
    if isinstance(value, dict):
        return {key: resolve_secret_refs(root, item) for key, item in value.items()}
    return value


def add_auth_service_secret(adapter: dict) -> dict:
    service = adapter.get("auth_service")
    if not service:
        return adapter
    resolved = {**adapter}
    headers = dict(resolved.get("headers") or {})
    headers.setdefault("Authorization", f"Bearer {{{{secret:{service}_token}}}}")
    resolved["headers"] = headers
    return resolved


def validate_parameters(stream: dict, parameters: dict) -> None:
    missing = [
        parameter["name"]
        for parameter in stream.get("parameters", [])
        if parameter.get("required") and parameter["name"] not in parameters
    ]
    if missing:
        raise ValueError(f"{stream['id']}: missing required parameters: {', '.join(missing)}")


def local_command_approval_digest(stream: dict, adapter: dict) -> str:
    clean_stream = {key: value for key, value in stream.items() if not key.startswith("__") and key != "pending"}
    payload = {
        "stream": clean_stream,
        "command": adapter.get("command"),
        "cwd": adapter.get("cwd"),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def local_command_approval_path(root: Path, stream_id: str) -> Path:
    parts = [part for part in stream_id.split("/") if part]
    if not parts:
        parts = ["unknown"]
    safe_parts = [safe_name_part(part, "unknown") for part in parts]
    safe_parts[-1] = f"{safe_parts[-1]}.json"
    return root / "approvals" / "local-command" / Path(*safe_parts)


def write_local_command_approval(root: Path, stream: dict, adapter: dict) -> dict:
    digest = local_command_approval_digest(stream, adapter)
    payload = {
        "version": SPEC_VERSION,
        "stream_id": stream["id"],
        "digest": digest,
        "command": adapter.get("command"),
        "cwd": adapter.get("cwd"),
        "approved_at": now_utc(),
    }
    atomic_write_json(local_command_approval_path(root, stream["id"]), payload)
    return payload


def require_local_command_approval(root: Path, stream: dict, adapter: dict) -> None:
    approval_path = local_command_approval_path(root, stream["id"])
    approval = load_existing_state(approval_path)
    digest = local_command_approval_digest(stream, adapter)
    if not approval or approval.get("digest") != digest:
        rel_path = approval_path.relative_to(root)
        raise PermissionError(
            f"{stream['id']}: local_command is not approved for this command digest; "
            f"review the command and run `python3 scripts/agentfeeds.py admin templates approve-command {stream['id']}` "
            f"to write {rel_path}"
        )


def publisher_for(stream_uri: str) -> str:
    return urlparse(stream_uri).netloc


def run_adapter(stream: dict, parameters: dict, root: Path | None = None) -> tuple[str, list[dict]]:
    validate_parameters(stream, parameters)
    adapter = substitute(stream["adapter"], parameters)
    adapter = add_auth_service_secret(adapter)
    adapter = resolve_secret_refs(root, adapter) if root is not None else adapter
    if adapter.get("kind") == "local_command":
        if root is None:
            raise PermissionError(f"{stream['id']}: local_command execution requires an Agent Feeds root for approval lookup")
        if stream.get("pending"):
            raise PermissionError(f"{stream['id']}: local_command template is pending operator approval")
        require_local_command_approval(root, stream, adapter)
    resolved_stream = {**stream, "adapter": adapter}
    return run_adapter_impl(
        resolved_stream,
        parameters,
        validate_parameters=validate_parameters,
        source_uri_for=source_uri_for,
        substitute=substitute,
    )


def value_at_path(payload: dict, dotted_path: str) -> object:
    current: object = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def comparison_matches(actual: object, expected: object) -> bool:
    if not isinstance(expected, dict):
        return actual == expected
    for operator, value in expected.items():
        if operator == "gte" and not (actual is not None and actual >= value):
            return False
        if operator == "gt" and not (actual is not None and actual > value):
            return False
        if operator == "lte" and not (actual is not None and actual <= value):
            return False
        if operator == "lt" and not (actual is not None and actual < value):
            return False
        if operator == "eq" and actual != value:
            return False
    return True


def event_matches_filter(event: dict, filters: dict | None) -> bool:
    if not filters:
        return True
    for path, expected in filters.items():
        payload = event["data"] if path.startswith("data.") else event
        lookup = path.removeprefix("data.")
        if not comparison_matches(value_at_path(payload, lookup), expected):
            return False
    return True


def load_existing_state(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def poll_interval(subscription: dict, stream: dict, defaults: dict) -> int:
    return int(
        subscription.get("poll_interval_seconds")
        or defaults.get("poll_interval_seconds")
        or stream.get("recommended_poll_interval_seconds")
        or 600
    )


def template_id_for(subscription: dict) -> str:
    return str(subscription["template"])


def subscription_title(subscription: dict, stream: dict) -> str:
    return str(subscription.get("title") or stream.get("title") or subscription["id"])


def state_path_for_subscription(root: Path, subscription: dict) -> Path:
    stream = load_stream_definition(root, template_id_for(subscription))
    stream_uri = source_uri_for(stream, subscription.get("parameters") or {})
    return state_path_for_stream(stream_uri, root)


def is_due(path: Path, interval_seconds: int, force: bool) -> bool:
    if force or not path.exists():
        return True
    existing = load_existing_state(path)
    if not existing:
        return True
    updated = parse_utc(existing.get("_meta", {}).get("last_updated"))
    if not updated:
        return True
    return datetime.now(UTC) - updated >= timedelta(seconds=interval_seconds)


def schema_validation_enabled() -> bool:
    value = os.environ.get("AGENTFEEDS_VALIDATE")
    if value is None:
        return True
    return value.lower() not in {"0", "false", "no", "off"}


def validate_events_for_stream(root: Path, stream: dict, events: list[dict]) -> None:
    if not schema_validation_enabled():
        return
    schema = json.loads(schema_path_for_url(root, stream["schema_url"]).read_text(encoding="utf-8"))
    for index, event in enumerate(events):
        try:
            jsonschema.validate(event.get("data"), schema)
        except jsonschema.ValidationError as exc:
            raise ValueError(f"{stream['id']}: event {index} does not match {stream['schema_url']}: {exc.message}") from exc


def state_payload(
    subscription: dict,
    stream: dict,
    stream_uri: str,
    events: list[dict],
    existing: dict | None,
    interval_seconds: int,
    history_limit: int,
) -> dict:
    updated_at = now_utc()
    next_due = (
        datetime.now(UTC).replace(microsecond=0) + timedelta(seconds=interval_seconds)
    ).isoformat().replace("+00:00", "Z")
    meta = {
        "stream": stream_uri,
        "type": stream["type"],
        "mode": stream["mode"],
        "last_updated": updated_at,
        "next_poll_due": next_due,
        "schema_url": stream["schema_url"],
        "schema_version": stream["schema_version"],
        "publisher": publisher_for(stream_uri),
        "stale": False,
        "subscription_id": subscription["id"],
        "template_id": stream["id"],
        "title": subscription_title(subscription, stream),
    }

    if stream["mode"] == "snapshot":
        if not events:
            raise ValueError(f"{stream['id']}: snapshot adapter produced no events")
        return {"_meta": meta, "data": events[0]["data"]}

    if stream["mode"] == "event":
        old_events = existing.get("data", []) if existing else []
        merged = []
        seen = set()
        for event in [*events, *old_events]:
            event_id = event.get("id")
            if event_id in seen:
                continue
            seen.add(event_id)
            merged.append(event)
        return {"_meta": meta, "data": merged[:history_limit]}

    if stream["mode"] == "delta":
        current = existing.get("data", {}) if existing else {}
        for event in events:
            current.update(event["data"])
        return {"_meta": meta, "data": current}

    raise ValueError(f"unsupported mode: {stream['mode']}")


def regenerate_catalog(root: Path) -> None:
    lines = [
        "# Agent Feeds - Active Subscriptions",
        "",
        "This file lists data streams currently subscribed. Prefer `python3 scripts/agentfeeds.py streams read <subscription-id> --json` for normal agent access.",
        "",
    ]
    state_entries = []
    subscriptions = load_subscriptions(root).get("subscriptions") or []
    for subscription in subscriptions:
        stream = load_stream_definition(root, template_id_for(subscription))
        parameters = subscription.get("parameters") or {}
        stream_uri = source_uri_for(stream, parameters)
        path = state_path_for_stream(stream_uri, root)
        payload = load_existing_state(path) if path.exists() else {}
        meta = (payload or {}).get("_meta", {})
        state_entries.append((subscription, stream, stream_uri, path, meta))
    if not state_entries:
        lines.extend(["No active state files found.", ""])

    for subscription, stream, stream_uri, path, meta in state_entries:
        title = subscription_title(subscription, stream)
        rel_path = path.relative_to(root)
        lines.extend(
            [
                f"## {title}",
                f"- **ID:** `{subscription.get('id', '')}`",
                f"- **Template:** `{template_id_for(subscription)}`",
                f"- **Stream:** `{meta.get('stream') or stream_uri}`",
                f"- **Path:** `{rel_path}`",
                f"- **Updated:** {meta.get('last_updated', 'never')}",
                f"- **Stale:** {'yes' if meta.get('stale') else 'no'}",
                f"- **Mode:** {meta.get('mode') or stream.get('mode', 'unknown')}",
                "",
            ]
        )

    lines.extend(
        [
            "---",
            f"*Last regenerated: {now_utc()}.*",
            "",
        ]
    )
    (root / "catalog.md").write_text("\n".join(lines), encoding="utf-8")


def run_fetch(args: argparse.Namespace, root: Path) -> int:
    subscriptions = load_subscriptions(root)
    defaults = subscriptions.get("defaults") or {}
    active = subscriptions.get("subscriptions") or []
    if args.once:
        active = [sub for sub in active if sub.get("id") == args.once]
    if args.stream:
        active = [sub for sub in active if sub.get("id") == args.stream]

    if not active:
        regenerate_catalog(root)
        return 0

    force = args.all or bool(args.stream) or bool(args.once)
    failures = 0
    for subscription in active:
        attempted_at = now_utc()
        stream = None
        path = None
        try:
            stream = load_stream_definition(root, template_id_for(subscription))
            parameters = subscription.get("parameters") or {}
            stream_uri = source_uri_for(stream, parameters)
            path = state_path_for_stream(stream_uri, root)
            interval_seconds = poll_interval(subscription, stream, defaults)
            if not is_due(path, interval_seconds, force):
                continue

            stream_uri, events = run_adapter(stream, parameters, root)
            events = [event for event in events if event_matches_filter(event, subscription.get("filter"))]
            validate_events_for_stream(root, stream, events)
            history_limit = int(subscription.get("history_limit") or defaults.get("history_limit") or 50)
            existing = load_existing_state(path)
            payload = state_payload(subscription, stream, stream_uri, events, existing, interval_seconds, history_limit)
            atomic_write_json(path, payload)
            write_fetch_status(root, subscription, stream, attempted_at=attempted_at, succeeded=True, state_path=path)
        except Exception as exc:  # noqa: BLE001 - keep cron-friendly failure reporting.
            failures += 1
            write_fetch_status(root, subscription, stream, attempted_at=attempted_at, succeeded=False, error=str(exc), state_path=path)
            print(f"{subscription.get('id', '<unknown>')}: {exc}", file=sys.stderr)

    regenerate_catalog(root)
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch Agent Feeds subscriptions")
    parser.add_argument("--all", action="store_true", help="refresh every subscription")
    parser.add_argument("--stream", help="refresh one subscription id")
    parser.add_argument("--once", help="one-shot fetch for a subscription id")
    parser.add_argument("--regenerate-catalog", action="store_true", help="regenerate catalog.md without polling")
    parser.add_argument("--update-catalog", action="store_true", help="refresh the local catalog cache")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="agentfeeds root directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser()
    ensure_root(root)

    if args.update_catalog:
        update_catalog_cache(root)
    if args.regenerate_catalog:
        regenerate_catalog(root)
        return 0
    with fetch_lock(root) as acquired:
        if not acquired:
            print(f"agentfeeds-fetch already running for {root}; skipping", file=sys.stderr)
            return 1
        return run_fetch(args, root)


if __name__ == "__main__":
    raise SystemExit(main())
