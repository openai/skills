"""User-facing Agent Feeds management CLI."""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import plistlib
import platform
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from agentfeeds_runtime import fetcher as fetch
from agentfeeds_runtime.polling import install as polling_install
from agentfeeds_runtime.polling import uninstall as polling_uninstall


INSTANCE_ID_PATTERN = re.compile(r"^[a-z0-9-]+/[a-z0-9][a-z0-9-]*$")
ADAPTER_KINDS = {
    "local_file": "Read one local text, Markdown, or JSON file as a snapshot.",
    "filesystem_scan": "Scan a local directory and emit recent file entries.",
    "markdown_scan": "Scan a local Markdown directory and emit recent documents.",
    "git_status": "Read local Git branch, dirty files, and ahead/behind status.",
    "local_command": "Run an argv-only local command for a snapshot or JSON-derived events.",
    "json_http": "Fetch one HTTP JSON document and transform it into a snapshot.",
    "paginated_json_http": "Fetch an HTTP JSON array and transform it into event items.",
    "rss": "Fetch an RSS or Atom feed as event items.",
    "ical": "Fetch an iCalendar URL as event items.",
    "apple_automation": "Run read-only AppleScript automation and map tab-delimited rows to events.",
    "sqlite_query": "Run a read-only SQLite query and map rows to events.",
    "plist_reading_list": "Read Safari-style Reading List entries from a property-list file.",
}
POLLING_LABEL = "dev.agentfeeds.fetch"
POLLING_BEGIN_MARKER = "# BEGIN Agent Feeds polling"
POLLING_END_MARKER = "# END Agent Feeds polling"
SECRET_REF_PATTERN = re.compile(r"\{\{secret:([A-Za-z_][A-Za-z0-9_.-]*)\}\}")
QUERY_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
QUERY_STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "can",
    "could",
    "did",
    "does",
    "for",
    "from",
    "has",
    "have",
    "how",
    "into",
    "latest",
    "me",
    "my",
    "now",
    "of",
    "on",
    "please",
    "say",
    "show",
    "tell",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "who",
    "why",
    "with",
}


def parse_value(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_params(items: list[str]) -> dict[str, Any]:
    params = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"parameters must be key=value, got: {item}")
        key, value = item.split("=", 1)
        if not key:
            raise SystemExit(f"parameter key cannot be empty: {item}")
        params[key] = parse_value(value)
    return params


def save_subscriptions(root: Path, config: dict) -> None:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "subscriptions.yaml"
    tmp_path = path.with_suffix(".yaml.tmp")
    tmp_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    tmp_path.replace(path)


def secret_refs_in_template(value: object) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, str):
        refs.update(SECRET_REF_PATTERN.findall(value))
    elif isinstance(value, list):
        for item in value:
            refs.update(secret_refs_in_template(item))
    elif isinstance(value, dict):
        for item in value.values():
            refs.update(secret_refs_in_template(item))
    return refs


def active_subscriptions(root: Path) -> dict:
    fetch.ensure_root(root)
    return fetch.load_subscriptions(root)


def stream_summary(root: Path, stream_id: str) -> dict:
    return fetch.load_stream_definition(root, stream_id)


def template_id_for(subscription: dict) -> str:
    return str(subscription["template"])


def state_path_for_subscription(root: Path, subscription: dict) -> Path | None:
    try:
        stream = fetch.load_stream_definition(root, template_id_for(subscription))
        stream_uri = fetch.source_uri_for(stream, subscription.get("parameters") or {})
        return fetch.state_path_for_stream(stream_uri, root)
    except Exception:
        return None


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "feed"


def _hash_suffix(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:6]


def _template_id_parts(template_id: str) -> tuple[str, str]:
    if not INSTANCE_ID_PATTERN.match(template_id):
        raise ValueError("template id must look like category/name using lowercase letters, numbers, and hyphens")
    return tuple(template_id.split("/", 1))  # type: ignore[return-value]


def _title_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def _schema_payload(template_id: str, mode: str) -> dict:
    category, name = _template_id_parts(template_id)
    type_name = f"{category}.{name.replace('-', '.')}"
    data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://agentfeeds.dev/schemas/{type_name}.v1.json",
        "title": _title_from_slug(name),
        "type": "object",
        "required": ["title"],
        "properties": {
            "title": {"type": "string"},
            "url": {"type": ["string", "null"]},
            "content": {"type": ["string", "null"]},
            "updated_at": {"type": ["string", "null"]},
            "stdout": {"type": ["string", "null"]},
            "transformed": {},
        },
    }
    if mode == "event":
        data["required"] = ["title"]
    return data


def scaffold_stream(template_id: str, adapter_kind: str) -> tuple[dict, dict, Path, Path]:
    if adapter_kind not in ADAPTER_KINDS:
        raise ValueError(f"unsupported adapter kind: {adapter_kind}")
    category, name = _template_id_parts(template_id)
    title = _title_from_slug(name)
    type_name = f"{category}.{name.replace('-', '.')}"
    mode = (
        "event"
        if adapter_kind in {
            "paginated_json_http",
            "rss",
            "ical",
            "filesystem_scan",
            "markdown_scan",
            "apple_automation",
            "sqlite_query",
            "plist_reading_list",
        }
        else "snapshot"
    )
    schema_name = f"{type_name}.v1.json"
    stream_path = Path(category) / f"{name}.yaml"
    schema_path = Path(schema_name)

    parameters = []
    source_uri_template = f"feed://{type_name}/source"
    adapter: dict[str, object] = {"kind": adapter_kind}
    transform = {
        "language": "jmespath",
        "expression": "{title: title, url: url, content: body, updated_at: updated_at}",
    }

    if adapter_kind == "local_file":
        parameters = [{"name": "path", "type": "string", "description": "Local file path", "required": True}]
        source_uri_template = f"feed://{type_name}/file?path={{path}}"
        adapter = {"kind": "local_file", "path": "{path}"}
    elif adapter_kind == "filesystem_scan":
        parameters = [{"name": "path", "type": "string", "description": "Local directory path", "required": True}]
        source_uri_template = f"feed://{type_name}/directory?path={{path}}"
        adapter = {"kind": "filesystem_scan", "path": "{path}", "order_by": "modified_at", "limit": 25}
    elif adapter_kind == "markdown_scan":
        parameters = [{"name": "path", "type": "string", "description": "Markdown directory path", "required": True}]
        source_uri_template = f"feed://{type_name}/markdown?path={{path}}"
        adapter = {"kind": "markdown_scan", "path": "{path}", "parse_frontmatter": True, "order_by": "modified_at", "limit": 25}
    elif adapter_kind == "git_status":
        parameters = [{"name": "path", "type": "string", "description": "Git repository path", "required": True}]
        source_uri_template = f"feed://{type_name}/git?path={{path}}"
        adapter = {"kind": "git_status", "path": "{path}"}
    elif adapter_kind == "local_command":
        parameters = []
        source_uri_template = f"feed://{type_name}/command"
        adapter = {
            "kind": "local_command",
            "command": ["echo", "{\"title\":\"example\",\"status\":\"ok\"}"],
            "timeout_seconds": 20,
            "max_output_bytes": 1048576,
            "parse": "json",
            "transform": {
                "language": "jmespath",
                "expression": "{title: title, content: status}",
            },
        }
        type_name = "local.command"
        schema_name = "local.command.v1.json"
        schema_path = Path(schema_name)
    elif adapter_kind == "json_http":
        parameters = [{"name": "url", "type": "string", "description": "JSON API URL", "required": True}]
        source_uri_template = f"feed://{type_name}/json?url={{url}}"
        adapter = {"kind": "json_http", "url": "{url}", "method": "GET", "headers": {}, "transform": transform}
    elif adapter_kind == "paginated_json_http":
        parameters = [{"name": "url", "type": "string", "description": "JSON API URL", "required": True}]
        source_uri_template = f"feed://{type_name}/items?url={{url}}"
        adapter = {"kind": "paginated_json_http", "url": "{url}", "method": "GET", "headers": {}, "transform": transform, "id_from": "url"}
    elif adapter_kind == "rss":
        parameters = [{"name": "url", "type": "string", "description": "RSS or Atom URL", "required": True}]
        source_uri_template = f"feed://{type_name}/rss?url={{url}}"
        adapter = {"kind": "rss", "url": "{url}"}
        type_name = "rss.item"
        schema_name = "rss-item.v1.json"
        schema_path = Path(schema_name)
    elif adapter_kind == "ical":
        parameters = [{"name": "url", "type": "string", "description": "iCalendar URL", "required": True}]
        source_uri_template = f"feed://{type_name}/ics?url={{url}}"
        adapter = {"kind": "ical", "url": "{url}"}
        type_name = "ical.event"
        schema_name = "ical-event.v1.json"
        schema_path = Path(schema_name)
    elif adapter_kind == "apple_automation":
        source_uri_template = f"feed://{type_name}/apple-automation"
        adapter = {
            "kind": "apple_automation",
            "tcc_permission": "Automation",
            "script": "set rows to {\"example-id\" & tab & \"Example title\"}\nset AppleScript's text item delimiters to linefeed\nreturn rows as text",
            "columns": ["id", "title"],
            "id_column": "id",
        }
    elif adapter_kind == "sqlite_query":
        parameters = [{"name": "database", "type": "string", "description": "SQLite database path", "required": True}]
        source_uri_template = f"feed://{type_name}/sqlite?database={{database}}"
        adapter = {
            "kind": "sqlite_query",
            "database": "{database}",
            "tcc_permission": "Full Disk Access",
            "query": "SELECT 1 AS id, 'Example title' AS title",
            "columns": ["id", "title"],
            "id_column": "id",
        }
    elif adapter_kind == "plist_reading_list":
        parameters = [{"name": "path", "type": "string", "description": "Property-list file path", "required": True}]
        source_uri_template = f"feed://{type_name}/plist-reading-list?path={{path}}"
        adapter = {"kind": "plist_reading_list", "path": "{path}", "limit": 50}

    stream = {
        "id": template_id,
        "title": title,
        "description": f"Draft template for {title}.",
        "type": type_name,
        "mode": mode,
        "schema_url": f"https://agentfeeds.dev/schemas/{schema_name}",
        "schema_version": "1.0.0",
        "parameters": parameters,
        "source_uri_template": source_uri_template,
        "adapter": adapter,
        "recommended_poll_interval_seconds": 300,
        "auth": "none",
        "tags": [category, adapter_kind.replace("_", "-")],
        "quality_tier": "experimental",
        "contributed_by": "local",
    }
    if adapter_kind == "local_command":
        stream["pending"] = True
    return stream, _schema_payload(template_id, mode), stream_path, schema_path


def _domain_slug(domain: str) -> str:
    return _slugify(domain.removeprefix("www.").rstrip(".").replace(".", "-"))


def _domain_title(domain: str, suffix: str = "RSS feed") -> str:
    base = domain.removeprefix("www.").split(".")[0]
    return f"{base.replace('-', ' ').title()} {suffix}".strip()


def _default_identity(template: dict, params: dict[str, Any]) -> tuple[str, str]:
    template_id = template["id"]
    parameters = template.get("parameters") or []
    if not parameters:
        return template_id, template["title"]

    category = template_id.split("/", 1)[0]
    title = template["title"]

    if template_id == "local/file" and params.get("path"):
        path = Path(str(params["path"])).expanduser()
        name = path.name or "file"
        return f"{category}/{_slugify(name)}", name

    if params.get("owner") and params.get("repo"):
        owner = _slugify(str(params["owner"]))
        repo = _slugify(str(params["repo"]))
        suffixes = {
            "dev/github-issues": "issues",
            "dev/github-prs": "prs",
            "dev/github-releases": "releases",
        }
        suffix = suffixes.get(template_id, template_id.split("/", 1)[1])
        return f"{category}/{owner}-{repo}-{suffix}", f"{params['owner']}/{params['repo']} {suffix}"

    if template_id == "calendar/ics" and params.get("url"):
        parsed = urlparse(str(params["url"]))
        if parsed.netloc:
            return f"{category}/{_domain_slug(parsed.netloc)}", f"{_domain_title(parsed.netloc, 'calendar')}"

    if template_id == "news/rss-generic" and params.get("url"):
        domain = urlparse(str(params["url"])).netloc.lower() or None
        if domain:
            return f"{category}/{_domain_slug(domain)}", _domain_title(domain)

    if params.get("url"):
        parsed = urlparse(str(params["url"]))
        if parsed.netloc:
            return f"{category}/{_domain_slug(parsed.netloc)}", _domain_title(parsed.netloc)

    if params.get("base"):
        base = str(params["base"]).upper()
        return f"{category}/{_slugify(base)}-exchange-rates", f"{base} exchange rates"

    if params.get("lat") is not None and params.get("lon") is not None:
        lat = _slugify(str(params["lat"]))
        lon = _slugify(str(params["lon"]))
        tail = _slugify(template_id.split("/", 1)[1])
        return f"{category}/{tail}-{lat}-{lon}", title

    return f"{category}/{_slugify(template_id)}-{_hash_suffix(params)}", title


def _append_collision_suffix(instance_id: str, template: dict, params: dict[str, Any], existing_ids: set[str]) -> str:
    if instance_id not in existing_ids:
        return instance_id

    path = ""
    if params.get("url"):
        parsed_path = urlparse(str(params["url"])).path.strip("/")
        if parsed_path:
            path = _slugify(parsed_path.split("/")[-2] if parsed_path.endswith("/") else parsed_path.rsplit("/", 1)[-1])
    if path:
        candidate = f"{instance_id}-{path}"
        if candidate not in existing_ids:
            return candidate

    return f"{instance_id}-{_hash_suffix({'template': template['id'], 'parameters': params})}"


def materialize_subscription(
    template: dict,
    params: dict[str, Any],
    existing_ids: set[str],
    instance_id: str | None = None,
    title: str | None = None,
) -> dict:
    default_id, default_title = _default_identity(template, params)
    if instance_id:
        resolved_id = instance_id
    elif not template.get("parameters"):
        resolved_id = default_id
    else:
        resolved_id = _append_collision_suffix(default_id, template, params, existing_ids)
    resolved_title = title or default_title
    if not INSTANCE_ID_PATTERN.match(resolved_id):
        raise ValueError(
            "subscription id must look like category/name using lowercase letters, numbers, and hyphens"
        )
    if resolved_id in existing_ids:
        raise ValueError(f"subscription id already exists: {resolved_id}")

    subscription = {
        "id": resolved_id,
        "title": resolved_title,
        "template": template["id"],
    }
    if params:
        subscription["parameters"] = params
    return subscription


def subscription_preview(root: Path, stream: dict, subscription: dict) -> dict:
    parameters = subscription.get("parameters") or {}
    stream_uri = fetch.source_uri_for(stream, parameters)
    state_path = fetch.state_path_for_stream(stream_uri, root)
    preview = {
        "subscription": subscription,
        "stream": stream_uri,
        "state_path": str(state_path.relative_to(root)),
        "requires_secrets": sorted(secret_refs_in_template(stream)),
        "next_actions": [],
    }
    if stream.get("pending") and stream.get("adapter", {}).get("kind") == "local_command":
        preview["next_actions"].append(
            {
                "action": "approve_local_command",
                "template_id": stream["id"],
                "command": f"python3 scripts/agentfeeds.py admin templates approve-command {stream['id']}",
                "reason": "local_command template is pending operator approval",
            }
        )
    return preview


def local_template_file(root: Path, template_id: str) -> Path | None:
    for path in sorted(fetch.template_streams_root(root).glob("**/*.yaml")):
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if payload.get("id") == template_id:
            return path
    return None


def cmd_templates_search(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    index = fetch.load_catalog_index(args.root)
    query = " ".join(args.query).lower().strip()
    streams = index.get("streams") or []
    if query:
        streams = [
            stream
            for stream in streams
            if query
            in " ".join(
                [
                    stream.get("id", ""),
                    stream.get("title", ""),
                    stream.get("description", ""),
                    " ".join(stream.get("tags") or []),
                    stream.get("type", ""),
                ]
            ).lower()
        ]
    for stream in streams:
        params = ", ".join(stream.get("parameters") or []) or "none"
        source = f", source: {stream.get('source')}" if args.verbose and stream.get("source") else ""
        print(f"{stream['id']}: {stream['title']} [params: {params}, mode: {stream['mode']}{source}]")
        if args.verbose:
            print(f"  {stream.get('description', '')}")
    return 0


def cmd_templates_show(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    try:
        stream = fetch.load_stream_definition(args.root, args.template_id)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    result = {
        "id": stream["id"],
        "title": stream["title"],
        "description": stream["description"],
        "type": stream["type"],
        "mode": stream["mode"],
        "parameters": stream.get("parameters") or [],
        "auth": stream.get("auth"),
        "quality_tier": stream.get("quality_tier"),
        "tags": stream.get("tags") or [],
        "recommended_poll_interval_seconds": stream.get("recommended_poll_interval_seconds"),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    required = [
        parameter["name"]
        for parameter in result["parameters"]
        if parameter.get("required")
    ]
    optional = [
        parameter["name"]
        for parameter in result["parameters"]
        if not parameter.get("required")
    ]
    print(f"{result['id']}: {result['title']}")
    print(result["description"])
    print(f"Type: {result['type']}")
    print(f"Mode: {result['mode']}")
    print(f"Required parameters: {', '.join(required) or 'none'}")
    print(f"Optional parameters: {', '.join(optional) or 'none'}")
    print(f"Auth: {result['auth']}")
    print(f"Quality: {result['quality_tier']}")
    return 0


def cmd_subscribe(args: argparse.Namespace) -> int:
    config = active_subscriptions(args.root)
    config.setdefault("version", fetch.SPEC_VERSION)
    config.setdefault("defaults", {"poll_interval_seconds": 600, "history_limit": 50})
    subscriptions = config.setdefault("subscriptions", [])

    try:
        stream = fetch.load_stream_definition(args.root, args.template_id)
        params = parse_params(args.parameters)
        fetch.validate_parameters(stream, params)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    existing_ids = {str(item.get("id")) for item in subscriptions}
    try:
        if args.update:
            match = next((item for item in subscriptions if item.get("id") == args.update), None)
            if not match:
                raise ValueError(f"subscription id not found for update: {args.update}")
            subscription = dict(match)
            subscription["template"] = stream["id"]
            if args.title:
                subscription["title"] = args.title
            elif "title" not in subscription:
                subscription["title"] = stream.get("title") or args.update
            if params:
                subscription["parameters"] = params
            elif "parameters" in subscription:
                subscription.pop("parameters")
        else:
            subscription = materialize_subscription(stream, params, existing_ids, args.instance_id, args.title)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.poll_interval_seconds:
        subscription["poll_interval_seconds"] = args.poll_interval_seconds
    if args.history_limit:
        subscription["history_limit"] = args.history_limit

    preview = subscription_preview(args.root, stream, subscription)
    if preview["requires_secrets"]:
        preview["next_actions"].append(
            {
                "action": "set_secret",
                "names": preview["requires_secrets"],
                "command": "python3 scripts/agentfeeds.py admin secrets set <name>",
            }
        )
    if args.dry_run:
        if args.json:
            print(json.dumps(preview, indent=2, sort_keys=True))
        else:
            print(f"Subscription: {subscription['id']} ({subscription['title']})")
            print(f"Template: {subscription['template']}")
            print(f"State path: {preview['state_path']}")
            if preview["requires_secrets"]:
                print(f"Secrets: {', '.join(preview['requires_secrets'])}")
        return 0

    pending_approval = next((action for action in preview["next_actions"] if action["action"] == "approve_local_command"), None)
    if pending_approval:
        if args.json:
            print(json.dumps({**preview, "error": "local_command template is pending operator approval"}, indent=2, sort_keys=True))
        else:
            print(f"{stream['id']}: local_command template is pending operator approval", file=sys.stderr)
            print(f"Next: {pending_approval['command']}", file=sys.stderr)
        return 2

    if args.update:
        for index, item in enumerate(subscriptions):
            if item.get("id") == args.update:
                subscriptions[index] = subscription
                break
    else:
        subscriptions.append(subscription)
    save_subscriptions(args.root, config)
    if args.json:
        result = {**preview, "created": not bool(args.update), "updated": bool(args.update)}
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{'Updated' if args.update else 'Subscribed'}: {subscription['id']} ({subscription['title']})")

    if args.no_fetch:
        fetch.regenerate_catalog(args.root)
        return 0
    return fetch.main(["--root", str(args.root), "--once", subscription["id"]])


def cmd_unsubscribe(args: argparse.Namespace) -> int:
    config = active_subscriptions(args.root)
    subscriptions = config.get("subscriptions") or []
    matches = [
        subscription
        for subscription in subscriptions
        if subscription.get("id") == args.subscription_id
    ]
    if not matches:
        print(f"No matching subscription: {args.subscription_id}", file=sys.stderr)
        return 1

    remove_keys = {id(match) for match in matches}
    state_paths = [state_path_for_subscription(args.root, match) for match in matches]
    config["subscriptions"] = [
        subscription for subscription in subscriptions if id(subscription) not in remove_keys
    ]
    save_subscriptions(args.root, config)

    if not args.keep_state:
        for path in state_paths:
            if path and path.exists() and args.root in path.parents:
                path.unlink()

    fetch.regenerate_catalog(args.root)
    print(f"Unsubscribed: {args.subscription_id}")
    return 0


def state_status(root: Path, subscription: dict, defaults: dict) -> dict:
    stream = stream_summary(root, template_id_for(subscription))
    path = state_path_for_subscription(root, subscription)
    interval = fetch.poll_interval(subscription, stream, defaults)
    payload = fetch.load_existing_state(path) if path else None
    meta = (payload or {}).get("_meta", {})
    updated = fetch.parse_utc(meta.get("last_updated"))
    stale = True
    due = True
    if updated:
        age = datetime.now(UTC) - updated
        due = age >= timedelta(seconds=interval)
        stale = age > timedelta(seconds=interval * 2)
    return {
        "id": subscription["id"],
        "title": subscription.get("title") or stream.get("title"),
        "template": subscription.get("template"),
        "parameters": subscription.get("parameters") or {},
        "path": str(path.relative_to(root)) if path else "",
        "exists": bool(path and path.exists()),
        "last_updated": meta.get("last_updated"),
        "next_poll_due": meta.get("next_poll_due"),
        "due": due,
        "stale": stale,
        "mode": stream.get("mode"),
    }


def _stream_rows(root: Path) -> list[dict]:
    config = active_subscriptions(root)
    defaults = config.get("defaults") or {}
    return [state_status(root, subscription, defaults) for subscription in config.get("subscriptions") or []]


def _stream_matches(row: dict, query: str) -> bool:
    haystack = " ".join(
        [
            row.get("id", ""),
            row.get("title", ""),
            row.get("template", ""),
            " ".join(f"{key}={value}" for key, value in sorted((row.get("parameters") or {}).items())),
            row.get("mode", ""),
        ]
    ).lower()
    return query.lower() in haystack


def _print_stream_rows(rows: list[dict]) -> None:
    if not rows:
        print("No active streams.")
        return
    for row in rows:
        freshness = "stale" if row["stale"] else "due" if row["due"] else "fresh"
        exists = "ok" if row["exists"] else "missing"
        print(f"{row['id']}: {row['title']} [{freshness}, {exists}, updated={row['last_updated'] or 'never'}]")


def _active_fetch_error(status: dict) -> bool:
    if int(status.get("consecutive_failures") or 0) <= 0:
        return False
    error_at = fetch.parse_utc(status.get("last_error_at"))
    success_at = fetch.parse_utc(status.get("last_success_at"))
    return bool(error_at and (not success_at or error_at >= success_at))


def _health_state(row: dict, status: dict) -> str:
    if _active_fetch_error(status):
        return "error"
    if not row["exists"]:
        return "missing"
    if row["stale"]:
        return "stale"
    if row["due"]:
        return "due"
    return "ok"


def _stream_health(root: Path) -> dict:
    rows = _stream_rows(root)
    streams = []
    counts = Counter()
    for row in rows:
        status = fetch.load_fetch_status(root, row["id"])
        state = _health_state(row, status)
        counts[state] += 1
        streams.append(
            {
                **row,
                "health": state,
                "last_attempt_at": status.get("last_attempt_at"),
                "last_success_at": status.get("last_success_at"),
                "last_error_at": status.get("last_error_at"),
                "last_error": status.get("last_error"),
                "consecutive_failures": int(status.get("consecutive_failures") or 0),
            }
        )
    summary = {
        "total": len(streams),
        "ok": counts.get("ok", 0),
        "due": counts.get("due", 0),
        "stale": counts.get("stale", 0),
        "missing": counts.get("missing", 0),
        "error": counts.get("error", 0),
    }
    summary["healthy"] = summary["total"] > 0 and summary["missing"] == 0 and summary["error"] == 0 and summary["stale"] == 0
    next_actions = []
    if summary["error"]:
        next_actions.append(
            {
                "action": "inspect_errors",
                "command": "python3 scripts/agentfeeds.py streams health --json",
                "reason": "one or more streams have active fetch errors",
            }
        )
    stale_stream = next((row for row in streams if row["health"] == "stale"), None)
    if stale_stream:
        next_actions.append(
            {
                "action": "refresh_stream",
                "subscription_id": stale_stream["id"],
                "command": f"python3 scripts/agentfeeds.py refresh --stream {stale_stream['id']}",
                "reason": "stream state is stale",
            }
        )
    missing_stream = next((row for row in streams if row["health"] == "missing"), None)
    if missing_stream:
        next_actions.append(
            {
                "action": "refresh_stream",
                "subscription_id": missing_stream["id"],
                "command": f"python3 scripts/agentfeeds.py refresh --stream {missing_stream['id']}",
                "reason": "stream has no local state file yet",
            }
        )
    return {"summary": summary, "streams": streams, "next_actions": next_actions}


def _print_health(result: dict) -> None:
    summary = result["summary"]
    print(
        "Streams: "
        f"{summary['total']} total, {summary['ok']} ok, {summary['due']} due, "
        f"{summary['stale']} stale, {summary['missing']} missing, {summary['error']} error"
    )
    for row in result["streams"]:
        print(f"{row['id']}: {row['health']} [updated={row['last_updated'] or 'never'}]")
        if row.get("last_error"):
            print(f"  error: {row['last_error']}")


def cmd_streams_health(args: argparse.Namespace) -> int:
    result = _stream_health(args.root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    _print_health(result)
    return 0


def _brief_entries(root: Path, max_streams: int, include_freshness: bool) -> tuple[list[dict], bool]:
    rows = _stream_rows(root)
    entries = []
    for row in rows[:max_streams]:
        entry = {"id": row["id"], "title": row["title"]}
        if include_freshness:
            entry.update(
                {
                    "freshness": "stale" if row["stale"] else "due" if row["due"] else "fresh",
                    "exists": row["exists"],
                    "last_updated": row["last_updated"],
                }
            )
        entries.append(entry)
    return entries, len(rows) > max_streams


def _brief_health_summary(health: dict) -> str | None:
    summary = health["summary"]
    degraded = summary["stale"] or summary["missing"] or summary["error"]
    if not degraded:
        return None
    parts = []
    for key in ("stale", "missing", "error"):
        if summary[key]:
            parts.append(f"{summary[key]} {key}")
    return "Ambient health: degraded (" + ", ".join(parts) + ")"


def render_brief(entries: list[dict], truncated: bool, include_freshness: bool, health: dict | None = None) -> str:
    lines = ["<agentfeeds>"]
    if health:
        health_line = _brief_health_summary(health)
        if health_line:
            lines.append(health_line)
    if entries:
        lines.append("Available local streams:")
        for entry in entries:
            line = f"- {entry['id']}: {entry['title']}"
            if include_freshness:
                line += f" [{entry['freshness']}, updated={entry['last_updated'] or 'never'}]"
            lines.append(line)
        if truncated:
            lines.append("- ...")
    else:
        lines.append("No active local streams.")
    lines.append("</agentfeeds>")
    return "\n".join(lines)


def cmd_brief(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    entries, truncated = _brief_entries(args.root, args.max_streams, args.include_freshness)
    health = _stream_health(args.root)
    brief = render_brief(entries, truncated, args.include_freshness, health)
    if args.json:
        print(
            json.dumps(
                {
                    "brief": brief,
                    "health": health["summary"],
                    "streams": entries,
                    "truncated": truncated,
                    "stable": not args.include_freshness,
                    "recommended_prompt_slot": "system",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    print(brief)
    return 0


def _query_terms(query: str) -> list[str]:
    terms = []
    seen = set()
    for raw in QUERY_TOKEN_PATTERN.findall(query.lower()):
        term = raw.strip("._-")
        if len(term) < 2 or term in QUERY_STOPWORDS or term in seen:
            continue
        seen.add(term)
        terms.append(term)
    return terms


def _iter_text_fields(value: object, path: str = "data", depth: int = 0, max_depth: int = 20):
    if depth > max_depth:
        return
    if value is None:
        return
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _iter_text_fields(item, f"{path}.{key}", depth + 1, max_depth)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_text_fields(item, f"{path}[{index}]", depth + 1, max_depth)
        return
    if isinstance(value, (str, int, float, bool)):
        text = str(value)
        if text:
            yield path, text


def _best_field_match(value: object, terms: list[str], match_mode: str, max_field_chars: int) -> dict | None:
    best = None
    fields = [(path, text) for path, text in _iter_text_fields(value)]
    for path, text in fields:
        searchable = text[:max_field_chars]
        lowered = searchable.lower()
        matched_terms = [term for term in terms if term in lowered]
        if match_mode == "all" and len(matched_terms) != len(terms):
            continue
        if match_mode == "any" and not matched_terms:
            continue
        occurrences = sum(lowered.count(term) for term in matched_terms)
        score = len(matched_terms) * 100 + occurrences
        candidate = {
            "path": path,
            "text": searchable,
            "score": score,
            "matched_terms": matched_terms,
        }
        if best is None or candidate["score"] > best["score"]:
            best = candidate
    if best is None and fields:
        combined = " ".join(text for _path, text in fields)[:max_field_chars]
        lowered = combined.lower()
        matched_terms = [term for term in terms if term in lowered]
        if (match_mode == "all" and len(matched_terms) == len(terms)) or (match_mode == "any" and matched_terms):
            occurrences = sum(lowered.count(term) for term in matched_terms)
            best = {
                "path": "data",
                "text": combined,
                "score": len(matched_terms) * 100 + occurrences,
                "matched_terms": matched_terms,
            }
    return best


def _snippet(text: str, terms: list[str], max_chars: int) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= max_chars:
        return compact
    lowered = compact.lower()
    positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
    center = min(positions) if positions else 0
    start = max(0, center - max_chars // 3)
    end = min(len(compact), start + max_chars)
    start = max(0, end - max_chars)
    prefix = "..." if start else ""
    suffix = "..." if end < len(compact) else ""
    return f"{prefix}{compact[start:end].strip()}{suffix}"


def _search_items_for_payload(payload: dict) -> list[dict]:
    data = payload.get("data")
    meta = payload.get("_meta") or {}
    if isinstance(data, list):
        items = []
        for index, event in enumerate(data):
            if isinstance(event, dict):
                items.append(
                    {
                        "kind": "event",
                        "index": index,
                        "id": event.get("id"),
                        "time": event.get("time"),
                        "data": event.get("data", event),
                    }
                )
        return items
    return [
        {
            "kind": "snapshot",
            "index": None,
            "id": None,
            "time": meta.get("last_updated"),
            "data": data,
        }
    ]


def _search_state(root: Path, query: str, *, match_mode: str, limit: int, max_field_chars: int, snippet_chars: int) -> dict:
    terms = _query_terms(query)
    if not terms:
        raise ValueError("search query has no usable terms")

    matches = []
    missing_streams = 0
    for row in _stream_rows(root):
        if not row["exists"] or not row.get("path"):
            missing_streams += 1
            continue
        payload = fetch.load_existing_state(root / row["path"])
        if not payload:
            continue
        for item in _search_items_for_payload(payload):
            best = _best_field_match(item["data"], terms, match_mode, max_field_chars)
            if not best:
                continue
            matches.append(
                {
                    "subscription_id": row["id"],
                    "title": row["title"],
                    "template": row["template"],
                    "mode": row["mode"],
                    "stale": row["stale"],
                    "last_updated": row["last_updated"],
                    "item_kind": item["kind"],
                    "item_index": item["index"],
                    "item_id": item["id"],
                    "item_time": item["time"],
                    "path": best["path"],
                    "matched_terms": best["matched_terms"],
                    "score": best["score"],
                    "snippet": _snippet(best["text"], terms, snippet_chars),
                }
            )
    matches.sort(
        key=lambda match: (
            match["score"],
            match["item_time"] or match["last_updated"] or "",
            match["subscription_id"],
        ),
        reverse=True,
    )
    return {
        "query": query,
        "terms": terms,
        "match": match_mode,
        "matches": matches[:limit],
        "total_matches": len(matches),
        "missing_streams": missing_streams,
    }


def cmd_search(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    query = " ".join(args.query).strip()
    if not query:
        print("search requires a query", file=sys.stderr)
        return 2
    try:
        result = _search_state(
            args.root,
            query,
            match_mode=args.match,
            limit=args.limit,
            max_field_chars=args.max_field_chars,
            snippet_chars=args.snippet_chars,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if not result["matches"]:
        print("No matching local stream state.")
        return 0
    for match in result["matches"]:
        stale = "stale" if match["stale"] else "fresh"
        item = f" item={match['item_id']}" if match["item_id"] else ""
        print(f"{match['subscription_id']}: {match['title']} [{stale}{item}]")
        print(f"  {match['path']}: {match['snippet']}")
    return 0


def cmd_streams_list(args: argparse.Namespace) -> int:
    rows = _stream_rows(args.root)
    if args.json:
        print(json.dumps({"streams": rows}, indent=2, sort_keys=True))
        return 0
    _print_stream_rows(rows)
    return 0


def cmd_streams_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query).strip()
    rows = _stream_rows(args.root)
    if query:
        rows = [row for row in rows if _stream_matches(row, query)]
    if args.json:
        print(json.dumps({"streams": rows}, indent=2, sort_keys=True))
        return 0
    _print_stream_rows(rows)
    return 0


def _subscription_by_id(root: Path, subscription_id: str) -> tuple[dict, dict]:
    config = active_subscriptions(root)
    for subscription in config.get("subscriptions") or []:
        if subscription.get("id") == subscription_id:
            return config, subscription
    raise KeyError(f"No matching subscription: {subscription_id}")


def _stream_detail(root: Path, subscription_id: str) -> dict:
    config, subscription = _subscription_by_id(root, subscription_id)
    defaults = config.get("defaults") or {}
    row = state_status(root, subscription, defaults)
    stream = fetch.load_stream_definition(root, template_id_for(subscription))
    parameters = subscription.get("parameters") or {}
    stream_uri = fetch.source_uri_for(stream, parameters)
    path = fetch.state_path_for_stream(stream_uri, root)
    payload = fetch.load_existing_state(path) if path.exists() else None
    meta = (payload or {}).get("_meta", {})
    data = (payload or {}).get("data")
    data_summary = {"kind": type(data).__name__}
    if isinstance(data, list):
        data_summary["count"] = len(data)
    elif isinstance(data, dict):
        data_summary["keys"] = sorted(data.keys())
    return {
        **row,
        "template": row.get("template"),
        "stream": stream_uri,
        "state_path": str(path.relative_to(root)),
        "meta": meta,
        "data_summary": data_summary,
    }


def cmd_streams_show(args: argparse.Namespace) -> int:
    try:
        result = _stream_detail(args.root, args.subscription_id)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    print(f"{result['id']}: {result['title']}")
    print(f"Template: {result['template']}")
    print(f"Mode: {result['mode']}")
    print(f"Freshness: {'stale' if result['stale'] else 'due' if result['due'] else 'fresh'}")
    print(f"Updated: {result['last_updated'] or 'never'}")
    print(f"State path: {result['state_path']}")
    print(f"Stream: {result['stream']}")
    print(f"Data: {json.dumps(result['data_summary'], sort_keys=True)}")
    return 0


def _limited_data(data: object, limit: int | None) -> object:
    if limit is None:
        return data
    if isinstance(data, list):
        return data[:limit]
    return data


def cmd_streams_read(args: argparse.Namespace) -> int:
    try:
        detail = _stream_detail(args.root, args.subscription_id)
        path = args.root / detail["state_path"]
        payload = fetch.load_existing_state(path)
        if payload is None:
            raise FileNotFoundError(f"state file not found or invalid: {detail['state_path']}")
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    data = _limited_data(payload.get("data"), args.limit)
    result = {
        "id": detail["id"],
        "title": detail["title"],
        "template": detail["template"],
        "state_path": detail["state_path"],
        "stale": detail["stale"],
        "last_updated": detail["last_updated"],
        "data": data,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"{result['id']}: {result['title']}")
    print(f"Template: {result['template']}")
    print(f"State path: {result['state_path']}")
    print(f"Updated: {result['last_updated'] or 'never'}")
    print(f"Stale: {'yes' if result['stale'] else 'no'}")
    print("Data:")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def cmd_refresh(args: argparse.Namespace) -> int:
    if args.all:
        return fetch.main(["--root", str(args.root), "--all"])
    if not args.subscription_id:
        print("refresh requires a subscription id or --all", file=sys.stderr)
        return 2
    return fetch.main(["--root", str(args.root), "--stream", args.subscription_id])


def _current_crontab() -> str:
    try:
        result = subprocess.run(["crontab", "-l"], check=False, text=True, capture_output=True)
    except FileNotFoundError:
        return ""
    return "" if result.returncode else result.stdout


def _cron_block_present(text: str) -> bool:
    return POLLING_BEGIN_MARKER in text and POLLING_END_MARKER in text


def _argv_uses_root(argv: object, root: Path) -> bool:
    if not isinstance(argv, list):
        return False
    items = [str(item) for item in argv]
    if "--root" in items:
        index = items.index("--root")
        return index + 1 < len(items) and Path(items[index + 1]).expanduser() == root
    return root == fetch.DEFAULT_ROOT


def _cron_block_uses_root(text: str, root: Path) -> bool:
    if not _cron_block_present(text):
        return False
    if "--root" in text:
        return str(root) in text
    return root == fetch.DEFAULT_ROOT


def _polling_status(root: Path) -> dict:
    system = platform.system()
    status: dict[str, object] = {
        "root": str(root),
        "platform": system,
        "installed": False,
        "method": "unsupported",
        "fetcher": None,
        "logs": str(root / "logs"),
    }
    try:
        status["fetcher"] = polling_install.fetcher_path()
        status["fetcher_available"] = True
    except Exception as exc:  # noqa: BLE001 - status should be diagnostic, not fatal.
        status["fetcher_available"] = False
        status["fetcher_error"] = str(exc)

    if system == "Darwin":
        plist_path = Path.home() / "Library" / "LaunchAgents" / f"{POLLING_LABEL}.plist"
        installed = False
        if plist_path.exists():
            try:
                payload = plistlib.loads(plist_path.read_bytes())
                installed = _argv_uses_root(payload.get("ProgramArguments"), root)
            except Exception:
                installed = root == fetch.DEFAULT_ROOT
        status.update({"method": "launchd", "installed": installed, "path": str(plist_path)})
        return status
    if system in {"Linux", "FreeBSD"}:
        text = _current_crontab()
        status.update({"method": "cron", "installed": _cron_block_uses_root(text, root)})
        return status
    return status


def _print_polling_status(status: dict) -> None:
    print(f"Polling: {'installed' if status['installed'] else 'not installed'}")
    print(f"Method: {status['method']}")
    print(f"Root: {status['root']}")
    print(f"Fetcher: {status.get('fetcher') or status.get('fetcher_error') or 'unknown'}")
    print(f"Logs: {status['logs']}")


def cmd_polling_status(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    status = _polling_status(args.root)
    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True))
        return 0
    _print_polling_status(status)
    return 0


def cmd_polling_install(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    return polling_install.main(["--root", str(args.root)])


def cmd_polling_uninstall(_args: argparse.Namespace) -> int:
    return polling_uninstall.main([])


def cmd_templates_list(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    index = fetch.load_catalog_index(args.root)
    for stream in index.get("streams") or []:
        params = ", ".join(stream.get("parameters") or []) or "none"
        print(f"{stream['id']}: {stream['title']} [params: {params}, source: {stream.get('source', 'builtin')}]")
    return 0


def cmd_templates_path(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    print(fetch.templates_root(args.root))
    return 0


def cmd_templates_validate(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    try:
        paths = fetch.validate_template_tree(args.root)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not paths:
        print(f"No local templates found in {fetch.template_streams_root(args.root)}")
        return 0
    for path in paths:
        print(f"valid: {path}")
    return 0


def cmd_templates_adapters(_args: argparse.Namespace) -> int:
    for kind, description in ADAPTER_KINDS.items():
        print(f"{kind}: {description}")
    return 0


def cmd_templates_scaffold(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    try:
        stream, schema, stream_rel_path, schema_rel_path = scaffold_stream(args.template_id, args.adapter_kind)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    stream_path = fetch.template_streams_root(args.root) / stream_rel_path
    schema_path = fetch.template_schemas_root(args.root) / schema_rel_path
    if stream_path.exists() and not args.force:
        print(f"template already exists: {stream_path}", file=sys.stderr)
        return 1

    stream_path.parent.mkdir(parents=True, exist_ok=True)
    stream_path.write_text(yaml.safe_dump(stream, sort_keys=False), encoding="utf-8")

    if args.adapter_kind not in {"rss", "ical", "local_command"} and (args.force or not schema_path.exists()):
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote: {stream_path}")
    if args.adapter_kind in {"rss", "ical", "local_command"}:
        print(f"schema: built-in {stream['schema_url']}")
    else:
        print(f"wrote: {schema_path}")
    print("Next: edit the draft, then run `python3 scripts/agentfeeds.py admin templates validate`.")
    return 0


def _event_sample(events: list[dict]) -> object:
    if not events:
        return None
    return events[0].get("data")


def cmd_templates_test(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    try:
        stream = fetch.load_stream_definition(args.root, args.template_id)
        params = parse_params(args.parameters)
        fetch.validate_parameters(stream, params)
        stream_uri, events = fetch.run_adapter(stream, params, args.root)
        state_path = fetch.state_path_for_stream(stream_uri, args.root)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    result = {
        "template": stream["id"],
        "title": stream["title"],
        "mode": stream["mode"],
        "stream": stream_uri,
        "state_path": str(state_path.relative_to(args.root)),
        "event_count": len(events),
        "sample": _event_sample(events),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"Template: {result['template']}")
    print(f"Title: {result['title']}")
    print(f"Mode: {result['mode']}")
    print(f"Stream: {result['stream']}")
    print(f"State path: {result['state_path']}")
    print(f"Events: {result['event_count']}")
    print("Sample:")
    print(json.dumps(result["sample"], indent=2, sort_keys=True))
    return 0


def cmd_templates_approve_command(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    try:
        stream = fetch.load_stream_definition(args.root, args.template_id)
        params = parse_params(args.parameters)
        fetch.validate_parameters(stream, params)
        adapter = fetch.substitute(stream["adapter"], params)
        adapter = fetch.resolve_secret_refs(args.root, adapter)
        if adapter.get("kind") != "local_command":
            raise ValueError(f"{stream['id']}: template is not a local_command template")
        if not sys.stdin.isatty():
            raise PermissionError("local_command approval must be run by the operator in an interactive terminal")
        output = sys.stderr if args.json else sys.stdout
        print("Local command approval required.", file=output)
        print(f"Template: {stream['id']}", file=output)
        print(f"Command: {json.dumps(adapter.get('command'))}", file=output)
        print(f"CWD: {adapter.get('cwd') or os.getcwd()}", file=output)
        if args.json:
            print("Type APPROVE to approve this exact command: ", end="", file=sys.stderr)
            typed = input()
        else:
            typed = input("Type APPROVE to approve this exact command: ")
        if typed != "APPROVE":
            raise PermissionError("approval cancelled")
        stream_path = local_template_file(args.root, stream["id"])
        if stream_path:
            payload = yaml.safe_load(stream_path.read_text(encoding="utf-8")) or {}
            payload["pending"] = False
            stream_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
            stream = fetch.load_stream_definition(args.root, args.template_id)
        approval = fetch.write_local_command_approval(args.root, stream, adapter)
        path = fetch.local_command_approval_path(args.root, stream["id"])
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    result = {
        "template": stream["id"],
        "approval_path": str(path.relative_to(args.root)),
        "digest": approval["digest"],
        "command": approval["command"],
        "cwd": approval.get("cwd"),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"Approved: {result['template']}")
    print(f"Path: {result['approval_path']}")
    print(f"Digest: {result['digest']}")
    print(f"Command: {json.dumps(result['command'])}")
    return 0


def cmd_secrets_set(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    if not sys.stdin.isatty():
        print("secret input must be run by the user in an interactive terminal", file=sys.stderr)
        return 1
    value = getpass.getpass(f"Secret value for {args.name}: ")
    fetch.write_secret(args.root, args.name, value)
    print(f"Secret set: {args.name}")
    return 0


def cmd_secrets_list(args: argparse.Namespace) -> int:
    fetch.ensure_root(args.root)
    names = sorted(path.stem for path in (args.root / "secrets").glob("*.txt"))
    if args.json:
        print(json.dumps({"secrets": names}, indent=2, sort_keys=True))
        return 0
    for name in names:
        print(name)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Agent Feeds subscriptions")
    parser.add_argument("--root", type=Path, default=fetch.DEFAULT_ROOT, help="agentfeeds root directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    brief = subparsers.add_parser("brief", help="print compact stable stream context for prompt injection")
    brief.add_argument("--max-streams", type=int, default=20)
    brief.add_argument("--include-freshness", action="store_true", help="include volatile freshness metadata")
    brief.add_argument("--json", action="store_true")
    brief.set_defaults(func=cmd_brief)

    search = subparsers.add_parser("search", help="search existing local stream state")
    search.add_argument("query", nargs="+")
    search.add_argument("--match", choices=["all", "any"], default="all", help="require all query terms or any term")
    search.add_argument("--limit", type=int, default=10, help="maximum matching items to return")
    search.add_argument("--max-field-chars", type=int, default=20000, help="maximum characters searched per field")
    search.add_argument("--snippet-chars", type=int, default=240, help="maximum snippet characters")
    search.add_argument("--json", action="store_true")
    search.set_defaults(func=cmd_search)

    subscribe = subparsers.add_parser("subscribe", help="add a subscription")
    subscribe.add_argument("template_id")
    subscribe.add_argument("parameters", nargs="*", help="template parameters as key=value")
    subscribe.add_argument("--id", dest="instance_id", help="concrete subscription id to create")
    subscribe.add_argument("--title", help="concrete subscription title")
    subscribe.add_argument("--poll-interval-seconds", type=int)
    subscribe.add_argument("--history-limit", type=int)
    subscribe.add_argument("--no-fetch", action="store_true")
    subscribe.add_argument("--dry-run", action="store_true", help="preview subscription id, state path, and requirements without writing")
    subscribe.add_argument("--update", metavar="SUBSCRIPTION_ID", help="update an existing subscription in place")
    subscribe.add_argument("--json", action="store_true", help="print machine-readable output")
    subscribe.set_defaults(func=cmd_subscribe)

    unsubscribe = subparsers.add_parser("unsubscribe", help="remove a subscription")
    unsubscribe.add_argument("subscription_id")
    unsubscribe.add_argument("--keep-state", action="store_true")
    unsubscribe.set_defaults(func=cmd_unsubscribe)

    refresh = subparsers.add_parser("refresh", help="refresh subscriptions")
    refresh.add_argument("--stream", dest="subscription_id", help="refresh one subscription id")
    refresh.add_argument("--all", action="store_true")
    refresh.set_defaults(func=cmd_refresh)

    streams = subparsers.add_parser("streams", help="inspect and read active streams")
    stream_subparsers = streams.add_subparsers(dest="stream_command", required=True)
    streams_list = stream_subparsers.add_parser("list", help="list active streams")
    streams_list.add_argument("--json", action="store_true")
    streams_list.set_defaults(func=cmd_streams_list)
    streams_find = stream_subparsers.add_parser("find", help="find active streams by metadata")
    streams_find.add_argument("query", nargs="*")
    streams_find.add_argument("--json", action="store_true")
    streams_find.set_defaults(func=cmd_streams_search)
    streams_health = stream_subparsers.add_parser("health", help="show stream freshness and fetch errors")
    streams_health.add_argument("--json", action="store_true")
    streams_health.set_defaults(func=cmd_streams_health)
    streams_read = stream_subparsers.add_parser("read", help="read active stream data")
    streams_read.add_argument("subscription_id")
    streams_read.add_argument("--limit", type=int, default=20, help="limit event-list data rows")
    streams_read.add_argument("--json", action="store_true", help="print machine-readable output")
    streams_read.set_defaults(func=cmd_streams_read)

    templates = subparsers.add_parser("templates", help="browse and test feed templates")
    template_subparsers = templates.add_subparsers(dest="template_command", required=True)
    template_search = template_subparsers.add_parser("find", help="find built-in and local templates")
    template_search.add_argument("query", nargs="*")
    template_search.add_argument("-v", "--verbose", action="store_true")
    template_search.set_defaults(func=cmd_templates_search)
    template_show = template_subparsers.add_parser("show", help="show one template")
    template_show.add_argument("template_id")
    template_show.add_argument("--json", action="store_true")
    template_show.set_defaults(func=cmd_templates_show)

    admin = subparsers.add_parser("admin", help="advanced setup, diagnostics, and template authoring")
    admin_subparsers = admin.add_subparsers(dest="admin_command", required=True)
    admin_polling = admin_subparsers.add_parser("polling", help="manage background refresh")
    admin_polling_subparsers = admin_polling.add_subparsers(dest="polling_command", required=True)
    admin_polling_status = admin_polling_subparsers.add_parser("status", help="show background refresh status")
    admin_polling_status.add_argument("--json", action="store_true")
    admin_polling_status.set_defaults(func=cmd_polling_status)
    admin_polling_subparsers.add_parser("install", help="install or update background refresh").set_defaults(func=cmd_polling_install)
    admin_polling_subparsers.add_parser("uninstall", help="remove background refresh").set_defaults(func=cmd_polling_uninstall)

    admin_templates = admin_subparsers.add_parser("templates", help="template authoring tools")
    admin_template_subparsers = admin_templates.add_subparsers(dest="template_command", required=True)
    admin_template_subparsers.add_parser("adapters", help="list scaffoldable adapter kinds").set_defaults(func=cmd_templates_adapters)
    admin_template_subparsers.add_parser("path", help="print the local template directory").set_defaults(func=cmd_templates_path)
    admin_template_subparsers.add_parser("list", help="list built-in and local templates").set_defaults(func=cmd_templates_list)
    admin_scaffold = admin_template_subparsers.add_parser("scaffold", help="create a draft local template")
    admin_scaffold.add_argument("adapter_kind", choices=sorted(ADAPTER_KINDS))
    admin_scaffold.add_argument("template_id", metavar="template_id")
    admin_scaffold.add_argument("--force", action="store_true", help="overwrite an existing draft")
    admin_scaffold.set_defaults(func=cmd_templates_scaffold)
    admin_test = admin_template_subparsers.add_parser("test", help="run a template once without writing state")
    admin_test.add_argument("template_id", metavar="template_id")
    admin_test.add_argument("parameters", nargs="*", help="template parameters as key=value")
    admin_test.add_argument("--json", action="store_true", help="print machine-readable output")
    admin_test.set_defaults(func=cmd_templates_test)
    admin_approve = admin_template_subparsers.add_parser("approve-command", help="operator-only approval for local_command templates")
    admin_approve.add_argument("template_id", metavar="template_id")
    admin_approve.add_argument("parameters", nargs="*", help="template parameters as key=value")
    admin_approve.add_argument("--json", action="store_true", help="print machine-readable output")
    admin_approve.set_defaults(func=cmd_templates_approve_command)
    admin_template_subparsers.add_parser("validate", help="validate local templates").set_defaults(func=cmd_templates_validate)

    admin_streams = admin_subparsers.add_parser("streams", help="advanced stream diagnostics")
    admin_stream_subparsers = admin_streams.add_subparsers(dest="stream_command", required=True)
    admin_stream_show = admin_stream_subparsers.add_parser("show", help="show active stream metadata")
    admin_stream_show.add_argument("subscription_id")
    admin_stream_show.add_argument("--json", action="store_true")
    admin_stream_show.set_defaults(func=cmd_streams_show)

    admin_secrets = admin_subparsers.add_parser("secrets", help="manage local secret values")
    admin_secret_subparsers = admin_secrets.add_subparsers(dest="secret_command", required=True)
    secret_set = admin_secret_subparsers.add_parser("set", help="set a local secret value")
    secret_set.add_argument("name")
    secret_set.set_defaults(func=cmd_secrets_set)
    secret_list = admin_secret_subparsers.add_parser("list", help="list local secret names")
    secret_list.add_argument("--json", action="store_true")
    secret_list.set_defaults(func=cmd_secrets_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.root = args.root.expanduser()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
