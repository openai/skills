#!/usr/bin/env python3
"""Validate ProjectGraph files in a Codex Project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FORBIDDEN_KEYS = {"confidence", "status", "RawTrace", "LiveMindMap", "StableMap"}
REQUIRED_NODE_KEYS = {"id", "title", "children", "source_refs"}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"JSON parse failed: {path}: {exc}") from exc


def walk_nodes(node: dict[str, Any]):
    yield node
    for child in node.get("children", []):
        yield from walk_nodes(child)


def find_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_KEYS:
                found.append(f"{path}.{key}")
            found.extend(find_forbidden_keys(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            found.extend(find_forbidden_keys(item, f"{path}[{idx}]"))
    return found


def validate_display_views(graph: dict[str, Any], node_ids: set[str]) -> list[str]:
    errors: list[str] = []
    display = graph.get("display", {})
    if not isinstance(display, dict):
        return ["display must be an object when present"]
    views = display.get("views", [])
    if views in (None, []):
        return errors
    if not isinstance(views, list):
        return ["display.views must be a list when present"]

    seen_view_ids: set[str] = set()
    for idx, view in enumerate(views):
        if not isinstance(view, dict):
            errors.append(f"display.views[{idx}] must be an object")
            continue
        view_id = view.get("id")
        if not view_id:
            errors.append(f"display.views[{idx}] missing id")
        elif view_id in seen_view_ids:
            errors.append(f"duplicate display view id: {view_id}")
        else:
            seen_view_ids.add(view_id)
        if not view.get("title"):
            errors.append(f"display view {view_id or idx} missing title")
        root_id = view.get("root_id")
        node_refs = view.get("node_refs", [])
        if not root_id and not node_refs:
            errors.append(f"display view {view_id or idx} needs root_id or node_refs")
        if root_id and root_id not in node_ids:
            errors.append(f"display view {view_id or idx} references missing root_id {root_id}")
        if node_refs and not isinstance(node_refs, list):
            errors.append(f"display view {view_id or idx} node_refs must be a list")
            continue
        for ref in node_refs:
            if ref not in node_ids:
                errors.append(f"display view {view_id or idx} references missing node {ref}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root containing .projectgraph")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    projectgraph = root / ".projectgraph"
    graph_path = projectgraph / "PROJECT_GRAPH.json"
    index_path = projectgraph / "TRACE_INDEX.json"
    html_path = projectgraph / "PROJECT_GRAPH.html"
    md_path = projectgraph / "PROJECT_GRAPH.md"

    graph = load_json(graph_path)
    index = load_json(index_path)

    sources = index.get("sources", {})
    node_sources = index.get("node_sources", {})
    nodes = list(walk_nodes(graph["root"]))

    errors: list[str] = []
    seen_ids: set[str] = set()

    for node in nodes:
        node_id = node.get("id")
        missing = REQUIRED_NODE_KEYS - node.keys()
        if missing:
            errors.append(f"node {node_id!r} missing keys: {sorted(missing)}")
        if node_id in seen_ids:
            errors.append(f"duplicate node id: {node_id}")
        seen_ids.add(node_id)
        if not node.get("source_refs"):
            errors.append(f"node {node_id} has no source_refs")
        for ref in node.get("source_refs", []):
            if ref not in sources:
                errors.append(f"node {node_id} references unknown source {ref}")
        if node_sources.get(node_id) != node.get("source_refs"):
            errors.append(f"node_sources mismatch for {node_id}")

    for node_id in node_sources:
        if node_id not in seen_ids:
            errors.append(f"TRACE_INDEX has node_sources for missing node {node_id}")

    for source_id, source in sources.items():
        if source.get("kind") == "trace":
            source_path = root / source.get("path", "")
            if not source_path.exists():
                errors.append(f"trace source {source_id} path missing: {source.get('path')}")
        if source.get("kind") == "codex_jsonl":
            locator = source.get("locator", {})
            transcript_path = locator.get("transcript_path") if isinstance(locator, dict) else None
            if not transcript_path:
                errors.append(f"codex_jsonl source {source_id} missing locator.transcript_path")
            elif not Path(transcript_path).expanduser().exists():
                errors.append(f"codex_jsonl source {source_id} transcript missing: {transcript_path}")
            transcript_lines = locator.get("transcript_lines", {}) if isinstance(locator, dict) else {}
            if not transcript_lines:
                errors.append(f"codex_jsonl source {source_id} missing locator.transcript_lines")

    for required in (html_path, md_path):
        if not required.exists():
            errors.append(f"required file missing: {required.relative_to(root)}")

    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
        for token in ("PROJECT_GRAPH.json", "TRACE_INDEX.json"):
            if token not in html:
                errors.append(f"PROJECT_GRAPH.html does not reference {token}")

    forbidden = find_forbidden_keys(graph, "PROJECT_GRAPH.json") + find_forbidden_keys(
        index, "TRACE_INDEX.json"
    )
    errors.extend(f"forbidden JSON key present: {item}" for item in forbidden)
    errors.extend(validate_display_views(graph, seen_ids))

    if errors:
        print("ProjectGraph validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "ProjectGraph validation passed: "
        f"{len(nodes)} nodes, {len(sources)} sources, {len([s for s in sources.values() if s.get('kind') == 'trace'])} traces"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
