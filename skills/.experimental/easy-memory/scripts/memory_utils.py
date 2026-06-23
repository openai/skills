from __future__ import annotations

import json
import posixpath
import platform
import re
import socket
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from urllib import parse
from uuid import uuid4

ENTRY_PREFIX_RE = re.compile(
    r"^\[ID:(?P<id>[^\]]+)\] "
    r"\[REF:(?P<ref>[^\]]+)\] "
    r"\[FACT:(?P<factual>true|false)\] "
    r"(?P<body>.*)$"
)
TIME_SUFFIX_RE = re.compile(
    r"^(?P<middle>.*) "
    r"\[TIME:(?P<ts>\d{4}-\d{2}-\d{2}:\d{2}:\d{2})\]$"
)

_REF_LEVEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")
INIT_LOG_NAME = "init.log"
AGENTS_FILE_NAME = "AGENTS.MD"
PATHS_TOKEN_PREFIX = " [PATHS:"
ALLOWED_RESOURCE_TYPES = {"local_path", "url"}
ALLOWED_LOCAL_PATH_FORMATS = {"project_relative", "absolute"}
SUPPORTED_URL_SCHEMES = {"http", "https"}
WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|\\\\)")


def _json_error() -> SystemExit:
    return SystemExit("related reference metadata must be valid JSON.")


def log_base_dir(create: bool = False) -> Path:
    base_dir = Path.cwd() / "easy-memory"
    if create:
        base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def log_path_for_date(log_date: date, base_dir: Path) -> Path:
    return base_dir / f"{log_date.strftime('%Y-%m-%d')}.log"


def list_log_files(base_dir: Path) -> list[Path]:
    if not base_dir.exists():
        return []
    return sorted(base_dir.glob("*.log"), reverse=True)


def init_log_path(base_dir: Path) -> Path:
    return base_dir / INIT_LOG_NAME


def init_rules_block() -> str:
    return "\n".join(
        [
            "## easy-memory rules",
            "- At the start of the current session (before the first task), use the "
            "`easy-memory` skill and follow all rules and constraints in its "
            "`SKILL.md`.",
            "- Only re-run memory read/search when necessary for the task.",
        ]
    )


def ensure_initialized(base_dir: Path) -> None:
    init_log = init_log_path(base_dir)
    if init_log.exists():
        return

    base_dir.mkdir(parents=True, exist_ok=True)

    rules_block = init_rules_block()
    agents_path = Path.cwd() / AGENTS_FILE_NAME
    if agents_path.exists():
        existing = agents_path.read_text(encoding="utf-8")
        if existing and not existing.endswith("\n"):
            existing += "\n"
        if existing.strip():
            existing += "\n"
        existing += f"{rules_block}\n"
        agents_path.write_text(existing, encoding="utf-8")
    else:
        agents_path.write_text(f"{rules_block}\n", encoding="utf-8")

    date_stamp = date.today().isoformat()
    init_log_content = f"{rules_block}\nDate: {date_stamp}\n"
    init_log.write_text(init_log_content, encoding="utf-8")


def require_initialized(base_dir: Path) -> None:
    init_log = init_log_path(base_dir)
    if not base_dir.exists() or not init_log.exists():
        raise SystemExit(
            "Initialization required. Run `python3 scripts/init_memory.py` "
            "from the project root."
        )


def ensure_single_line(text: str, label: str) -> None:
    if "\n" in text or "\r" in text:
        raise SystemExit(f"{label} must be a single line.")


def normalize_task_context(value: str) -> str:
    context = value.strip()
    if not context:
        raise SystemExit("task-context must not be empty.")
    ensure_single_line(context, "task-context")
    return context


def normalize_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise SystemExit("factual must be 'true' or 'false'.")


def validate_ref_level(value: str) -> str:
    if not value:
        raise SystemExit("ref-level must be a non-empty string.")
    if not _REF_LEVEL_RE.match(value):
        raise SystemExit("ref-level must match [A-Za-z0-9._-]+.")
    return value


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d:%H:%M")


def normalize_related_paths(raw_paths: list[str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen_paths: set[tuple[str, str]] = set()
    for raw_path in raw_paths:
        normalized_entry = normalize_single_related_path(raw_path)
        dedupe_key = (
            normalized_entry["resource_type"],
            normalized_entry["path"],
        )
        if dedupe_key in seen_paths:
            continue
        seen_paths.add(dedupe_key)
        entries.append(
            make_related_path_entry(
                normalized_entry["path"],
                resource_type=normalized_entry["resource_type"],
                directory=normalized_entry["directory"],
                path_format=normalized_entry.get("path_format"),
                system_hint=normalized_entry.get("system_hint"),
            )
        )
    return entries


def normalize_single_related_path(raw_path: str) -> dict[str, str]:
    normalized_raw_path = raw_path.strip()
    if not normalized_raw_path:
        raise SystemExit("related-path values must not be empty.")
    ensure_single_line(normalized_raw_path, "related-path")

    normalized_url = _normalize_related_url(normalized_raw_path)
    if normalized_url is not None:
        return normalized_url

    workspace_root = current_workspace_root()
    candidate = Path(normalized_raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = workspace_root / candidate
    if not candidate.exists():
        raise SystemExit(
            "related-path local paths must exist. Use update_memory.py to clear or replace stale paths."
        )
    resolved = candidate.resolve()

    try:
        relative_path = resolved.relative_to(workspace_root)
        normalized_path = path_to_storage_string(relative_path)
        relative_directory = relative_path if resolved.is_dir() else relative_path.parent
        directory = path_to_storage_string(relative_directory)
        return {
            "path": normalized_path,
            "directory": directory,
            "resource_type": "local_path",
            "path_format": "project_relative",
        }
    except ValueError:
        normalized_path = str(resolved)
        directory = normalized_path if resolved.is_dir() else str(resolved.parent)

    return {
        "path": normalized_path,
        "directory": directory,
        "resource_type": "local_path",
        "path_format": "absolute",
        "system_hint": current_system_hint(),
    }


def _normalize_related_url(raw_value: str) -> dict[str, str] | None:
    parsed = parse.urlsplit(raw_value)
    scheme = parsed.scheme.lower()
    if scheme not in SUPPORTED_URL_SCHEMES or not parsed.netloc:
        return None

    normalized_path = parsed.path or ""
    normalized_url = parse.urlunsplit(
        (
            scheme,
            parsed.netloc,
            normalized_path,
            parsed.query,
            parsed.fragment,
        )
    )
    directory = _derive_url_directory(
        scheme=scheme,
        netloc=parsed.netloc,
        path=normalized_path,
    )
    return {
        "path": normalized_url,
        "directory": directory,
        "resource_type": "url",
    }


def _derive_url_directory(*, scheme: str, netloc: str, path: str) -> str:
    normalized_path = path or "/"
    if normalized_path == "/":
        container_path = "/"
    elif normalized_path.endswith("/"):
        container_path = normalized_path.rstrip("/") or "/"
    else:
        parent = posixpath.dirname(normalized_path)
        container_path = parent or "/"
    return parse.urlunsplit((scheme, netloc, container_path, "", ""))


def infer_related_resource_type(
    path_value: str,
    *,
    directory: str | None = None,
) -> str:
    parsed = parse.urlsplit(path_value)
    if parsed.scheme.lower() in SUPPORTED_URL_SCHEMES and parsed.netloc:
        return "url"
    parsed_directory = parse.urlsplit(directory or "")
    if (
        parsed_directory.scheme.lower() in SUPPORTED_URL_SCHEMES
        and parsed_directory.netloc
    ):
        return "url"
    return "local_path"


def infer_local_path_format(
    path_value: str,
    *,
    directory: str | None = None,
) -> str:
    if looks_like_absolute_local_path(path_value):
        return "absolute"
    if looks_like_absolute_local_path(directory or ""):
        return "absolute"
    return "project_relative"


def current_workspace_root() -> Path:
    return Path.cwd().resolve()


def path_to_storage_string(path_value: Path) -> str:
    rendered = path_value.as_posix()
    return rendered if rendered else "."


def current_system_hint() -> str:
    system_name = platform.system() or "UnknownOS"
    machine = platform.machine() or "unknown-arch"
    hostname = socket.gethostname().split(".")[0].strip() or "unknown-host"
    return f"{system_name} {machine} @{hostname}"


def looks_like_absolute_local_path(path_value: str) -> bool:
    if not path_value:
        return False
    if WINDOWS_ABSOLUTE_PATH_RE.match(path_value):
        return True
    return Path(path_value).is_absolute()


def make_related_path_entry(
    path_value: str,
    path_id: Optional[str] = None,
    *,
    resource_type: str | None = None,
    directory: str | None = None,
    path_format: str | None = None,
    system_hint: str | None = None,
) -> dict[str, str]:
    normalized_entry = normalize_single_related_path(path_value)
    normalized_path = normalized_entry["path"]
    normalized_directory = directory or normalized_entry["directory"]
    normalized_type = resource_type or normalized_entry["resource_type"]
    if normalized_type not in ALLOWED_RESOURCE_TYPES:
        raise SystemExit("related reference resource_type must be local_path or url.")
    result = {
        "id": path_id or uuid4().hex,
        "path": normalized_path,
        "directory": normalized_directory,
        "resource_type": normalized_type,
    }
    if normalized_type == "local_path":
        normalized_path_format = (
            path_format
            or normalized_entry.get("path_format")
            or infer_local_path_format(
                normalized_path,
                directory=normalized_directory,
            )
        )
        if normalized_path_format not in ALLOWED_LOCAL_PATH_FORMATS:
            raise SystemExit(
                "related reference path_format must be project_relative or absolute."
            )
        result["path_format"] = normalized_path_format
        normalized_system_hint = (
            system_hint
            or normalized_entry.get("system_hint")
            or ""
        )
        if normalized_path_format == "absolute" and normalized_system_hint:
            result["system_hint"] = normalized_system_hint
    return result


def serialize_related_paths(path_entries: list[dict[str, str]]) -> str:
    return json.dumps(path_entries, ensure_ascii=False, separators=(",", ":"))


def deserialize_related_paths(raw_value: str) -> list[dict[str, str]]:
    try:
        payload = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise _json_error() from exc

    if not isinstance(payload, list):
        raise _json_error()

    parsed_entries: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for item in payload:
        if not isinstance(item, dict):
            raise _json_error()
        path_id = item.get("id")
        path_value = item.get("path")
        directory = item.get("directory")
        resource_type = item.get("resource_type")
        path_format = item.get("path_format")
        system_hint = item.get("system_hint")
        if not isinstance(path_id, str) or not path_id:
            raise _json_error()
        if path_id in seen_ids:
            raise SystemExit("related resource IDs must be unique within one entry.")
        seen_ids.add(path_id)
        if not isinstance(path_value, str):
            raise _json_error()
        if not isinstance(directory, str):
            raise _json_error()
        if resource_type is None:
            resource_type = infer_related_resource_type(
                path_value,
                directory=directory,
            )
        if not isinstance(resource_type, str):
            raise _json_error()
        if resource_type not in ALLOWED_RESOURCE_TYPES:
            raise _json_error()
        parsed_entry = {
            "id": path_id,
            "path": path_value,
            "directory": directory,
            "resource_type": resource_type,
        }
        if resource_type == "local_path":
            if path_format is None:
                path_format = infer_local_path_format(
                    path_value,
                    directory=directory,
                )
            if not isinstance(path_format, str):
                raise _json_error()
            if path_format not in ALLOWED_LOCAL_PATH_FORMATS:
                raise _json_error()
            parsed_entry["path_format"] = path_format
            if system_hint is not None:
                if not isinstance(system_hint, str):
                    raise _json_error()
                if system_hint:
                    parsed_entry["system_hint"] = system_hint
        elif system_hint is not None and not isinstance(system_hint, str):
            raise _json_error()
        parsed_entries.append(parsed_entry)
    return parsed_entries


def clone_related_paths(path_entries: list[dict[str, str]]) -> list[dict[str, str]]:
    return [dict(item) for item in path_entries]


def clear_related_path_entry(path_entries: list[dict[str, str]], path_id: str) -> None:
    for item in path_entries:
        if item["id"] == path_id:
            item["path"] = ""
            item["directory"] = ""
            item.pop("system_hint", None)
            item.pop("path_format", None)
            return
    raise SystemExit(f"Related resource ID not found: {path_id}")


def replace_related_path_entry(
    path_entries: list[dict[str, str]],
    path_id: str,
    path_value: str,
) -> None:
    replacement = make_related_path_entry(path_value, path_id=path_id)
    for item in path_entries:
        if item["id"] == path_id:
            item.update(replacement)
            return
    raise SystemExit(f"Related resource ID not found: {path_id}")


def format_related_path_lines(path_entries: Optional[list[dict[str, str]]]) -> list[str]:
    if path_entries is None:
        return []
    lines = []
    for item in path_entries:
        rendered_path = item["path"] or "<cleared>"
        rendered_directory = item["directory"] or "<cleared>"
        rendered_type = item.get("resource_type") or infer_related_resource_type(
            item["path"],
            directory=item["directory"],
        )
        detail_parts = [rendered_type]
        rendered_path_format = item.get("path_format")
        if (
            not rendered_path_format
            and rendered_type == "local_path"
            and (item["path"] or item["directory"])
        ):
            rendered_path_format = infer_local_path_format(
                item["path"],
                directory=item["directory"],
            )
        if rendered_path_format:
            detail_parts.append(rendered_path_format)
        detail_text = ", ".join(detail_parts)
        extras = []
        system_hint = item.get("system_hint")
        if system_hint:
            extras.append(f"system: {system_hint}")
        extra_text = ""
        if extras:
            extra_text = "; " + "; ".join(extras)
        lines.append(
            f"Related resource ID {item['id']} [{detail_text}]: {rendered_path} "
            f"(container: {rendered_directory}{extra_text})"
        )
    return lines


def format_entry_line(
    entry_id: str,
    ref_level: str,
    factual: bool,
    content: str,
    timestamp: str,
    path_entries: Optional[list[dict[str, str]]] = None,
) -> str:
    fact_value = "true" if factual else "false"
    paths_segment = ""
    if path_entries is not None:
        paths_segment = f" [PATHS:{serialize_related_paths(path_entries)}]"
    return (
        f"[ID:{entry_id}] [REF:{ref_level}] [FACT:{fact_value}] {content}"
        f"{paths_segment} [TIME:{timestamp}]"
    )


def parse_entry_line(line: str) -> Optional[dict]:
    prefix_match = ENTRY_PREFIX_RE.match(line.strip())
    if not prefix_match:
        return None
    time_match = TIME_SUFFIX_RE.match(prefix_match.group("body"))
    if not time_match:
        return None

    middle = time_match.group("middle")
    content = middle
    path_entries: list[dict[str, str]] = []
    has_paths_metadata = False

    paths_idx = middle.rfind(PATHS_TOKEN_PREFIX)
    if paths_idx != -1 and middle.endswith("]"):
        has_paths_metadata = True
        content = middle[:paths_idx]
        raw_paths = middle[paths_idx + len(PATHS_TOKEN_PREFIX) : -1]
        path_entries = deserialize_related_paths(raw_paths)

    return {
        "id": prefix_match.group("id"),
        "ref": prefix_match.group("ref"),
        "factual": prefix_match.group("factual") == "true",
        "content": content,
        "timestamp": time_match.group("ts"),
        "path_entries": path_entries,
        "has_paths_metadata": has_paths_metadata,
    }
