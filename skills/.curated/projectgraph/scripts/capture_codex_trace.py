#!/usr/bin/env python3
"""Capture a ProjectGraph trace with locators into a Codex JSONL transcript."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def compact_text(value: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", value, flags=re.UNICODE)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "Codex-JSONL-Trace"


def unique_trace_path(traces_dir: Path, today: str, title: str, turn_id: str | None) -> Path:
    base = f"{today}-{slugify(title)}"
    candidate = traces_dir / f"{base}.md"
    if not candidate.exists():
        return candidate
    suffix = datetime.now().astimezone().strftime("%H%M%S")
    if turn_id:
        suffix = f"{str(turn_id)[:8]}-{suffix}"
    return traces_dir / f"{base}-{suffix}.md"


def load_json_maybe(path: str | None) -> dict[str, Any]:
    if path:
        return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if sys.stdin.isatty():
        return {}
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def first_nested_value(value: Any, keys: set[str]) -> Any:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys and item not in (None, ""):
                return item
        for item in value.values():
            found = first_nested_value(item, keys)
            if found not in (None, ""):
                return found
    elif isinstance(value, list):
        for item in value:
            found = first_nested_value(item, keys)
            if found not in (None, ""):
                return found
    return None


def content_text(payload: dict[str, Any]) -> str:
    content = payload.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str):
                    chunks.append(text)
            elif isinstance(item, str):
                chunks.append(item)
        return "\n".join(chunks)
    return ""


def describe_record(record: dict[str, Any]) -> tuple[str, str]:
    record_type = record.get("type")
    payload = record.get("payload")
    if not isinstance(payload, dict):
        payload = {}

    if record_type == "session_meta":
        meta_id = payload.get("id") or payload.get("session_id")
        cwd = payload.get("cwd")
        return "session_meta", compact_text(f"session={meta_id or 'unknown'} cwd={cwd or 'unknown'}")

    payload_type = payload.get("type")
    if record_type == "event_msg":
        if payload_type == "task_started":
            return "task_started", compact_text(f"turn_id={payload.get('turn_id') or 'unknown'}")
        return f"event:{payload_type or 'unknown'}", compact_text(json.dumps(payload, ensure_ascii=False))

    if record_type == "turn_context":
        return "turn_context", compact_text(json.dumps(payload, ensure_ascii=False))

    if record_type == "response_item" and payload_type == "message":
        role = payload.get("role") or "unknown"
        return f"message:{role}", compact_text(content_text(payload))

    if record_type == "response_item" and payload_type == "function_call":
        name = payload.get("name") or "unknown"
        return f"tool_call:{name}", compact_text(str(payload.get("arguments") or ""))

    if record_type == "response_item" and payload_type == "function_call_output":
        return "tool_output", compact_text(str(payload.get("output") or ""))

    return str(record_type or "unknown"), compact_text(json.dumps(record, ensure_ascii=False))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            try:
                item = json.loads(raw)
            except json.JSONDecodeError:
                continue
            kind, excerpt = describe_record(item)
            records.append(
                {
                    "line": line_no,
                    "raw": raw.rstrip("\n"),
                    "record": item,
                    "kind": kind,
                    "excerpt": excerpt,
                    "sha256_16": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16],
                }
            )
    return records


def latest_transcript_for(root: Path, session_id: str | None) -> Path | None:
    sessions_root = Path.home() / ".codex" / "sessions"
    if not sessions_root.exists():
        return None
    candidates = sorted(sessions_root.glob("**/*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    root_text = str(root)
    for candidate in candidates[:300]:
        try:
            records = read_jsonl(candidate)
        except OSError:
            continue
        if not records:
            continue
        first = records[0]["record"]
        payload = first.get("payload") if isinstance(first, dict) else None
        if not isinstance(payload, dict):
            continue
        if session_id and payload.get("id") == session_id:
            return candidate
        if payload.get("cwd") == root_text:
            return candidate
    return None


def select_evidence(records: list[dict[str, Any]], max_tool_lines: int) -> list[dict[str, Any]]:
    selected: dict[int, dict[str, Any]] = {}

    def add(record: dict[str, Any] | None) -> None:
        if record:
            selected[record["line"]] = record

    add(next((item for item in records if item["kind"] == "session_meta"), None))
    add(next((item for item in reversed(records) if item["kind"] == "task_started"), None))
    add(next((item for item in reversed(records) if item["kind"] == "message:user"), None))
    add(
        next(
            (
                item
                for item in reversed(records)
                if item["kind"] == "message:developer"
                and "untrusted_objective" in json.dumps(item["record"], ensure_ascii=False)
            ),
            None,
        )
    )
    add(next((item for item in reversed(records) if item["kind"] == "message:assistant"), None))

    tool_lines = [item for item in records if item["kind"].startswith("tool_call:")]
    for item in tool_lines[-max_tool_lines:]:
        add(item)

    return [selected[line] for line in sorted(selected)]


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def render_trace(
    *,
    title: str,
    locator: dict[str, Any],
    summary: str,
    evidence: list[dict[str, Any]],
    conclusions: list[str],
    graph_impacts: list[str],
) -> str:
    evidence_lines = [
        f"- line {item['line']}: `{item['kind']}` sha256_16=`{item['sha256_16']}` - {item['excerpt']}"
        for item in evidence
    ]
    conclusion_lines = [f"- {item}" for item in conclusions] or [
        "- This trace records Codex JSONL locator facts only; an agent should decide at a meaningful boundary whether to promote them into visible Graph nodes."
    ]
    impact_lines = [f"- {item}" for item in graph_impacts] or [
        "- The script does not rewrite the Graph by default; a later maintainer should use this trace to update `PROJECT_GRAPH.json`, `PROJECT_GRAPH.md`, and `TRACE_INDEX.json`."
    ]
    return "\n".join(
        [
            f"# Trace: {title}",
            "",
            "## locator",
            "",
            "```json",
            json_dumps(locator),
            "```",
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Raw JSONL Location",
            "",
            *(evidence_lines or ["- No readable Codex JSONL was located; see `field_availability_note` in the locator."]),
            "",
            "## Extracted Conclusions",
            "",
            *conclusion_lines,
            "",
            "## Graph Impact",
            "",
            *impact_lines,
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root containing .projectgraph")
    parser.add_argument("--payload", help="Path to a Codex hook JSON payload. Defaults to stdin when piped.")
    parser.add_argument("--transcript-path", help="Absolute Codex JSONL transcript path.")
    parser.add_argument("--session-id")
    parser.add_argument("--codex-thread-id")
    parser.add_argument("--turn-id")
    parser.add_argument("--title", default="Codex JSONL locator record")
    parser.add_argument("--boundary-type", default="Codex JSONL locator capture")
    parser.add_argument("--summary", default="")
    parser.add_argument("--user-quote", default="")
    parser.add_argument("--assistant-action", default="")
    parser.add_argument("--timezone", default=datetime.now().astimezone().tzname() or "local")
    parser.add_argument("--conclusion", action="append", default=[])
    parser.add_argument("--graph-impact", action="append", default=[])
    parser.add_argument("--max-tool-lines", type=int, default=8)
    parser.add_argument("--force", action="store_true", help="Overwrite the trace file when it already exists.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    projectgraph = root / ".projectgraph"
    traces_dir = projectgraph / "TRACES"
    if not traces_dir.exists():
        raise SystemExit(f"ProjectGraph TRACES directory not found: {traces_dir}")

    payload = load_json_maybe(args.payload)
    session_id = args.session_id or first_nested_value(payload, {"session_id", "sessionId"})
    turn_id = args.turn_id or first_nested_value(payload, {"turn_id", "turnId"})
    codex_thread_id = args.codex_thread_id or first_nested_value(payload, {"codex_thread_id", "thread_id", "threadId"})
    transcript_value = args.transcript_path or first_nested_value(payload, {"transcript_path", "transcriptPath"})
    transcript_path = Path(transcript_value).expanduser().resolve() if transcript_value else None
    if transcript_path is None:
        transcript_path = latest_transcript_for(root, str(session_id) if session_id else None)

    records: list[dict[str, Any]] = []
    if transcript_path and transcript_path.exists():
        records = read_jsonl(transcript_path)

    evidence = select_evidence(records, args.max_tool_lines)
    session_meta = next((item for item in records if item["kind"] == "session_meta"), None)
    if session_meta:
        meta_payload = session_meta["record"].get("payload") or {}
        session_id = session_id or meta_payload.get("id")
        codex_thread_id = codex_thread_id or meta_payload.get("id")

    task_started = next((item for item in reversed(records) if item["kind"] == "task_started"), None)
    if task_started:
        task_payload = task_started["record"].get("payload") or {}
        turn_id = turn_id or task_payload.get("turn_id")

    user_quote = args.user_quote
    if not user_quote:
        last_user = next((item for item in reversed(records) if item["kind"] == "message:user"), None)
        user_quote = last_user["excerpt"] if last_user else ""

    today = datetime.now().astimezone().date().isoformat()
    if args.force:
        output_path = traces_dir / f"{today}-{slugify(args.title)}.md"
    else:
        output_path = unique_trace_path(traces_dir, today, args.title, str(turn_id) if turn_id else None)
    if output_path.exists() and not args.force:
        raise SystemExit(f"trace already exists, pass --force to overwrite: {output_path}")

    locator = {
        "project": root.name,
        "cwd": str(root),
        "date": today,
        "timezone": args.timezone,
        "codex_thread_id": codex_thread_id,
        "session_id": session_id,
        "turn_id": turn_id,
        "transcript_path": str(transcript_path) if transcript_path else None,
        "field_availability_note": (
            "transcript_path points to a Codex JSONL file; selected line/hash details are listed in this trace."
            if records
            else "No readable Codex JSONL was found from hook payload, CLI arguments, or ~/.codex/sessions."
        ),
        "boundary_type": args.boundary_type,
        "user_quote": user_quote,
        "assistant_action": args.assistant_action
        or "Record a Codex JSONL locator; later agents decide at meaningful boundaries whether to promote content into the Graph.",
        "transcript_lines": {
            item["kind"]: item["line"] for item in evidence if not item["kind"].startswith("tool_call:")
        },
        "tool_call_lines": [
            {"line": item["line"], "kind": item["kind"], "sha256_16": item["sha256_16"]}
            for item in evidence
            if item["kind"].startswith("tool_call:")
        ],
    }
    summary = args.summary or "This trace was generated by the ProjectGraph capture tool to point the current boundary back to a real Codex JSONL transcript."
    output_path.write_text(
        render_trace(
            title=args.title,
            locator=locator,
            summary=summary,
            evidence=evidence,
            conclusions=args.conclusion,
            graph_impacts=args.graph_impact,
        ),
        encoding="utf-8",
    )
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
