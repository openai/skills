#!/usr/bin/env python3
"""Listen for app-server events and trigger compaction handoff or optional auto-save."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, BinaryIO, Iterator

from common import MemoryValidationError, detect_secret_indicators, ensure_project_name, now_iso


DEFAULT_AUTO_SAVE_TITLE_PREFIX = "Auto memory"
DEFAULT_AUTO_SAVE_TAGS = "auto-memory,auto-save"
DEFAULT_AUTO_SAVE_PROJECT_FIELD = "project"
DEFAULT_AUTO_SAVE_SUMMARY_FIELDS = "summary,objective,next_step,result,status"
DEFAULT_COMPACTION_ALERT_TITLE_PREFIX = "Auto memory compaction"
DEFAULT_COMPACTION_ALERT_TAGS = "auto-memory,compaction,failure"
DEFAULT_REINJECTION_MAX_CHARS = 12000
DEFAULT_REINJECTION_MAX_ESTIMATED_TOKENS = 3000
DEFAULT_OVERSIZE_ACTION = "skip"
MAX_PAYLOAD_PREVIEW_CHARS = 1400
MAX_FIELD_VALUE_CHARS = 260
EST_CHARS_PER_TOKEN = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch app-server event stream for compaction handoff and optional auto-save."
    )
    parser.add_argument("--project", required=True, help="Project scope for memory operations.")
    parser.add_argument("--objective", default="", help="Objective carried into reinjection prompts.")
    parser.add_argument("--query", default="", help="Optional memory query override.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum memory results per handoff.")
    parser.add_argument(
        "--input-file",
        default="",
        help="Read app-server messages from a file instead of stdin.",
    )
    parser.add_argument(
        "--prompt-out",
        default="",
        help="Write latest reinjection prompt to this file.",
    )
    parser.add_argument(
        "--jsonl-log",
        default="",
        help="Append listener actions as JSONL records.",
    )
    parser.add_argument(
        "--inject-turn-start",
        action="store_true",
        help="Emit a turn/start JSON-RPC request to stdout after post-compaction handoff.",
    )
    parser.add_argument(
        "--output-framing",
        choices=("jsonl", "lsp"),
        default="jsonl",
        help="Framing for emitted turn/start request payloads.",
    )
    parser.add_argument(
        "--request-id-prefix",
        default="auto-memory",
        help="Prefix for emitted turn/start request IDs.",
    )
    parser.add_argument(
        "--reinjection-max-chars",
        type=int,
        default=DEFAULT_REINJECTION_MAX_CHARS,
        help=(
            "Maximum reinjection prompt length in characters before oversize handling applies. "
            "Set to 0 to disable character-based limit."
        ),
    )
    parser.add_argument(
        "--reinjection-max-estimated-tokens",
        type=int,
        default=DEFAULT_REINJECTION_MAX_ESTIMATED_TOKENS,
        help=(
            "Maximum estimated reinjection prompt token count before oversize handling applies. "
            "Set to 0 to disable token-based limit."
        ),
    )
    parser.add_argument(
        "--oversize-action",
        choices=("skip", "truncate", "allow"),
        default=DEFAULT_OVERSIZE_ACTION,
        help=(
            "Behavior when reinjection prompt exceeds configured limits: "
            "'skip' (default), 'truncate', or 'allow'."
        ),
    )
    parser.add_argument(
        "--disable-compaction",
        action="store_true",
        help="Disable compaction pre/post handoff behavior.",
    )
    parser.add_argument(
        "--auto-save-events",
        default="",
        help=(
            "Comma-separated method names that should trigger auto-save "
            "(for example: turn/complete,turn/completed)."
        ),
    )
    parser.add_argument(
        "--auto-save-title-prefix",
        default=DEFAULT_AUTO_SAVE_TITLE_PREFIX,
        help="Title prefix used for auto-saved notes.",
    )
    parser.add_argument(
        "--auto-save-tags",
        default=DEFAULT_AUTO_SAVE_TAGS,
        help="Comma-separated tags to pass to save_memory.py for auto-saved notes.",
    )
    parser.add_argument(
        "--auto-save-project-field",
        default=DEFAULT_AUTO_SAVE_PROJECT_FIELD,
        help=(
            "Field name (or dotted path) used to infer project from event payload. "
            "Falls back to --project if not present."
        ),
    )
    parser.add_argument(
        "--auto-save-summary-fields",
        default=DEFAULT_AUTO_SAVE_SUMMARY_FIELDS,
        help="Comma-separated field names (or dotted paths) pulled into note summary.",
    )
    parser.add_argument(
        "--save-compaction-alerts",
        action="store_true",
        help=(
            "Persist compaction failures/skips as memory notes for downstream "
            "self-improvement workflows."
        ),
    )
    parser.add_argument(
        "--compaction-alert-title-prefix",
        default=DEFAULT_COMPACTION_ALERT_TITLE_PREFIX,
        help="Title prefix used for compaction alert memory notes.",
    )
    parser.add_argument(
        "--compaction-alert-tags",
        default=DEFAULT_COMPACTION_ALERT_TAGS,
        help="Comma-separated tags used for compaction alert memory notes.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error stderr logs.",
    )
    parser.add_argument(
        "--visual-status",
        action="store_true",
        help=(
            "Emit concise compaction/reinjection status lines to stderr for "
            "human-visible runtime feedback."
        ),
    )
    return parser.parse_args()


def _parse_csv(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def _log(message: str, quiet: bool = False) -> None:
    if quiet:
        return
    print(message, file=sys.stderr, flush=True)


def _visual_status(message: str, enabled: bool) -> None:
    if not enabled:
        return
    print(f"[auto-memory] {message}", file=sys.stderr, flush=True)


def _write_jsonl(path: str, payload: dict[str, Any]) -> None:
    if not path:
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _iter_payload_text(stream: BinaryIO) -> Iterator[str]:
    """Yield JSON payload text from either LSP framing or raw JSONL."""
    while True:
        first = stream.readline()
        if not first:
            return
        if not first.strip():
            continue

        lowered = first.lower()
        if lowered.startswith(b"content-length:"):
            try:
                length = int(first.split(b":", 1)[1].strip())
            except ValueError:
                continue
            while True:
                header = stream.readline()
                if not header:
                    return
                if header in (b"\r\n", b"\n"):
                    break
            body = stream.read(length)
            if not body:
                return
            yield body.decode("utf-8", errors="replace")
            continue

        yield first.decode("utf-8", errors="replace").strip()


def _extract_thread_id(payload: Any) -> str | None:
    if isinstance(payload, dict):
        for key in ("threadId", "thread_id"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
        for value in payload.values():
            found = _extract_thread_id(value)
            if found:
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = _extract_thread_id(value)
            if found:
                return found
    return None


def _contains_context_compacted(payload: Any) -> bool:
    if isinstance(payload, dict):
        if payload.get("type") == "context_compacted":
            return True
        return any(_contains_context_compacted(value) for value in payload.values())
    if isinstance(payload, list):
        return any(_contains_context_compacted(value) for value in payload)
    return False


def _normalize_scalar(value: Any, max_chars: int = MAX_FIELD_VALUE_CHARS) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, (int, float)):
        text = str(value)
    elif isinstance(value, str):
        text = value.strip()
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(text.split())
    if not text:
        return None
    if len(text) > max_chars:
        return f"{text[: max_chars - 3]}..."
    return text


def _extract_by_key(payload: Any, key_name: str) -> str | None:
    target = key_name.strip().lower()
    if not target:
        return None
    if isinstance(payload, dict):
        for key, value in payload.items():
            if str(key).strip().lower() == target:
                normalized = _normalize_scalar(value)
                if normalized:
                    return normalized
        for value in payload.values():
            found = _extract_by_key(value, key_name)
            if found:
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = _extract_by_key(value, key_name)
            if found:
                return found
    return None


def _lookup_dotted_path(payload: Any, path: str) -> str | None:
    parts = [part.strip() for part in path.split(".") if part.strip()]
    if not parts:
        return None
    current: Any = payload
    for part in parts:
        if isinstance(current, dict):
            if part in current:
                current = current[part]
                continue
            lowered = part.lower()
            match = next((value for key, value in current.items() if str(key).lower() == lowered), None)
            if match is None:
                return None
            current = match
            continue
        if isinstance(current, list) and part.isdigit():
            index = int(part)
            if 0 <= index < len(current):
                current = current[index]
                continue
        return None
    return _normalize_scalar(current)


def _extract_field_value(payload: Any, field: str) -> str | None:
    if not field:
        return None
    if "." in field:
        dotted = _lookup_dotted_path(payload, field)
        if dotted:
            return dotted
        field = field.rsplit(".", 1)[-1]
    return _extract_by_key(payload, field)


def _extract_event_id(message: Any) -> str | None:
    for field in ("event_id", "eventId", "turn_id", "turnId", "request_id", "requestId", "id"):
        value = _extract_field_value(message, field)
        if value:
            return value
    return None


def _truncate_payload_preview(payload: Any) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except Exception:
        text = repr(payload)
    if len(text) <= MAX_PAYLOAD_PREVIEW_CHARS:
        return text
    return f"{text[: MAX_PAYLOAD_PREVIEW_CHARS - 3]}..."


def _build_auto_save_title(prefix: str, event_kind: str, event_id: str | None, ts_iso: str) -> str:
    safe_prefix = prefix.strip() or DEFAULT_AUTO_SAVE_TITLE_PREFIX
    safe_event = event_kind.strip().replace("/", "-")[:48]
    safe_suffix = (event_id or ts_iso).strip().replace(" ", "-")[:48]
    return f"{safe_prefix}: {safe_event} {safe_suffix}".strip()


def _build_auto_save_body(
    *,
    event_kind: str,
    thread_id: str | None,
    event_id: str | None,
    objective: str,
    summary_values: list[tuple[str, str]],
    payload: Any,
    ts_iso: str,
) -> str:
    summary_lines = [f"- Captured app-server event `{event_kind}` for continuity."]
    if summary_values:
        for key, value in summary_values:
            summary_lines.append(f"- {key}: {value}")
    else:
        summary_lines.append("- No configured summary fields were present in this event.")

    context_lines = [
        f"- Timestamp (UTC): {ts_iso}",
        f"- Thread ID: {thread_id or 'unknown'}",
        f"- Event ID: {event_id or 'missing'}",
        f"- Source method: {event_kind}",
    ]
    if objective.strip():
        context_lines.append(f"- Active objective: {objective.strip()}")

    payload_preview = _truncate_payload_preview(payload)

    return (
        "## Summary\n"
        + "\n".join(summary_lines)
        + "\n\n## Context\n"
        + "\n".join(context_lines)
        + "\n\n## Decision\n"
        + "- Persist a compact event snapshot as durable memory for future retrieval.\n"
        + "\n## Rationale\n"
        + "- Preserve execution continuity without depending on transient runtime buffers.\n"
        + "\n## Implementation\n"
        + "- Event processed by `app_server_compaction_listener.py` auto-save mode.\n"
        + "- Note persisted via `save_memory.py` to project-scoped memory storage.\n"
        + "\n## Verification\n"
        + "- Event matched configured `--auto-save-events` filter.\n"
        + "- Secret indicator scan passed before persistence.\n"
        + "\n## Follow-ups\n"
        + "- Review this note for durable decisions and remove transient detail if needed.\n"
        + "\n## Event Payload (truncated)\n"
        + "```json\n"
        + payload_preview
        + "\n```\n"
        + "\n## Changelog\n"
        + f"- {ts_iso}: created via app_server_compaction_listener auto-save.\n"
    )


def _build_compaction_alert_body(
    *,
    event_kind: str,
    mode: str,
    thread_id: str | None,
    objective: str,
    status: str,
    reinjection_status: str,
    oversize_reason: list[str],
    prompt_chars: int,
    prompt_tokens_estimated: int,
    prompt_sent: bool,
    prompt_sent_chars: int,
    prompt_sent_tokens_estimated: int,
    error: str | None,
    payload: Any,
    ts_iso: str,
) -> str:
    summary_lines = [
        f"- Compaction event `{event_kind}` produced status `{status}`.",
        f"- Reinjection status: `{reinjection_status}`.",
    ]
    if oversize_reason:
        summary_lines.append(f"- Oversize reasons: {', '.join(oversize_reason)}")
    if error:
        summary_lines.append(f"- Error: {error}")

    context_lines = [
        f"- Timestamp (UTC): {ts_iso}",
        f"- Thread ID: {thread_id or 'unknown'}",
        f"- Event kind: {event_kind}",
        f"- Mode: {mode}",
        f"- Objective: {objective or 'unspecified'}",
    ]

    verification_lines = [
        f"- prompt_chars={prompt_chars}",
        f"- prompt_tokens_estimated={prompt_tokens_estimated}",
        f"- prompt_sent={prompt_sent}",
        f"- prompt_sent_chars={prompt_sent_chars}",
        f"- prompt_sent_tokens_estimated={prompt_sent_tokens_estimated}",
    ]

    payload_preview = _truncate_payload_preview(payload)

    return (
        "## Summary\n"
        + "\n".join(summary_lines)
        + "\n\n## Context\n"
        + "\n".join(context_lines)
        + "\n\n## Decision\n"
        + "- Persist this compaction anomaly to durable memory for future iteration and regression prevention.\n"
        + "\n## Rationale\n"
        + "- Compaction skips/failures are high-signal inputs for improving reinjection and prompt-budget strategy.\n"
        + "\n## Implementation\n"
        + "- Event captured by `app_server_compaction_listener.py` compaction alert mode.\n"
        + "- Note persisted via `save_memory.py` under the configured project scope.\n"
        + "\n## Verification\n"
        + "\n".join(verification_lines)
        + "\n\n## Follow-ups\n"
        + "- Feed this note into self-improve and loop orchestration acceptance gates.\n"
        + "- Adjust reinjection budget/action only when repeated similar failures are observed.\n"
        + "\n## Event Payload (truncated)\n"
        + "```json\n"
        + payload_preview
        + "\n```\n"
        + "\n## Changelog\n"
        + f"- {ts_iso}: created via compaction alert auto-save.\n"
    )


def _run_handoff(
    mode: str,
    project: str,
    objective: str,
    query: str,
    limit: int,
) -> dict[str, Any]:
    script_path = Path(__file__).with_name("compaction_handoff.py")
    cmd = [
        sys.executable,
        str(script_path),
        "--project",
        project,
        "--mode",
        mode,
        "--limit",
        str(max(1, limit)),
    ]
    if objective:
        cmd.extend(["--objective", objective])
    if query:
        cmd.extend(["--query", query])
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "handoff execution failed")
    return json.loads(completed.stdout)


def _run_save_memory(project: str, title: str, body: str, tags: str) -> dict[str, Any]:
    script_path = Path(__file__).with_name("save_memory.py")
    cmd = [
        sys.executable,
        str(script_path),
        "--project",
        project,
        "--title",
        title,
        "--strict-sections",
        "--body",
        body,
    ]
    if tags.strip():
        cmd.extend(["--tags", tags.strip()])
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        error_text = completed.stderr.strip() or completed.stdout.strip() or "save_memory execution failed"
        raise RuntimeError(error_text)
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("save_memory output was not valid JSON") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("save_memory output JSON must be an object")
    return parsed


def _emit_turn_start(
    output_framing: str,
    request_id_prefix: str,
    thread_id: str,
    prompt: str,
    counter: int,
) -> None:
    request = {
        "jsonrpc": "2.0",
        "id": f"{request_id_prefix}-{counter}",
        "method": "turn/start",
        "params": {
            "threadId": thread_id,
            "input": [{"type": "text", "text": prompt}],
        },
    }
    serialized = json.dumps(request, ensure_ascii=False)
    if output_framing == "lsp":
        payload = serialized.encode("utf-8")
        header = f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii")
        sys.stdout.buffer.write(header + payload)
        sys.stdout.buffer.flush()
        return

    print(serialized, flush=True)


def _record_event(log_path: str, payload: dict[str, Any]) -> None:
    payload_with_ts = {"ts": int(time.time()), **payload}
    _write_jsonl(log_path, payload_with_ts)


def _estimate_token_count(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + EST_CHARS_PER_TOKEN - 1) // EST_CHARS_PER_TOKEN)


def _is_over_limit(value: int, limit: int) -> bool:
    return limit > 0 and value > limit


def _oversize_reasons(
    *,
    prompt_chars: int,
    prompt_tokens_estimated: int,
    max_chars: int,
    max_tokens: int,
) -> list[str]:
    reasons: list[str] = []
    if _is_over_limit(prompt_chars, max_chars):
        reasons.append(f"chars>{max_chars}")
    if _is_over_limit(prompt_tokens_estimated, max_tokens):
        reasons.append(f"tokens>{max_tokens}")
    return reasons


def _truncate_prompt_to_budget(prompt: str, max_chars: int, max_tokens: int) -> str:
    budget_chars = max_chars if max_chars > 0 else len(prompt)
    if max_tokens > 0:
        budget_chars = min(budget_chars, max_tokens * EST_CHARS_PER_TOKEN)
    budget_chars = max(0, budget_chars)
    if budget_chars == 0:
        return ""
    if len(prompt) <= budget_chars:
        return prompt
    # Keep a visible truncation marker while remaining inside budget.
    marker = "\n[auto-memory reinjection truncated]"
    if budget_chars <= len(marker):
        return prompt[:budget_chars]
    return prompt[: budget_chars - len(marker)].rstrip() + marker


def _should_save_compaction_alert(status: str, reinjection_status: str) -> bool:
    if status == "error":
        return True
    return reinjection_status in (
        "skipped_oversize",
        "skipped_truncate_budget",
        "skipped_missing_thread_id",
    )


def main() -> int:
    args = parse_args()
    try:
        project = ensure_project_name(args.project)
    except MemoryValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    source: BinaryIO
    source_file = None
    if args.input_file:
        source_file = open(args.input_file, "rb")
        source = source_file
    else:
        source = sys.stdin.buffer

    auto_save_events = set(_parse_csv(args.auto_save_events))
    auto_save_summary_fields = _parse_csv(args.auto_save_summary_fields)
    compaction_enabled = not args.disable_compaction

    last_thread_id: str | None = None
    seen_compaction_keys: set[str] = set()
    seen_auto_event_ids: set[str] = set()
    inject_counter = 0

    _log(
        "auto-memory listener started "
        + f"(compaction={'on' if compaction_enabled else 'off'}, autosave={'on' if auto_save_events else 'off'})",
        quiet=args.quiet,
    )
    _visual_status(
        "listener_started "
        + f"compaction={'on' if compaction_enabled else 'off'} "
        + f"autosave={'on' if auto_save_events else 'off'}",
        enabled=args.visual_status,
    )
    if args.prompt_out:
        Path(args.prompt_out).parent.mkdir(parents=True, exist_ok=True)

    try:
        for payload_text in _iter_payload_text(source):
            try:
                message = json.loads(payload_text)
            except json.JSONDecodeError:
                continue
            if not isinstance(message, dict):
                continue

            method = message.get("method")
            if not isinstance(method, str):
                method = ""
            params = message.get("params")
            thread_id = _extract_thread_id(message) or last_thread_id
            if thread_id:
                last_thread_id = thread_id

            if compaction_enabled:
                event_kind = ""
                mode = ""
                if method == "thread/compact/start":
                    event_kind = "thread/compact/start"
                    mode = "pre"
                elif method == "thread/compacted":
                    event_kind = "thread/compacted"
                    mode = "post"
                elif _contains_context_compacted(message):
                    event_kind = "context_compacted"
                    mode = "post"

                if mode:
                    dedupe_key = f"{event_kind}:{thread_id}:{json.dumps(params, sort_keys=True, default=str)}"
                    if dedupe_key not in seen_compaction_keys:
                        seen_compaction_keys.add(dedupe_key)
                        _log(f"detected {event_kind}, running {mode} handoff", quiet=args.quiet)
                        _visual_status(
                            f"{event_kind} detected mode={mode} thread={thread_id or 'unknown'}",
                            enabled=args.visual_status,
                        )
                        result: dict[str, Any] | None = None
                        err: str | None = None
                        reinjection_status = "not_applicable"
                        oversize_reason: list[str] = []
                        prompt_chars = 0
                        prompt_tokens_estimated = 0
                        prompt_sent_chars = 0
                        prompt_sent_tokens_estimated = 0
                        prompt_sent = False
                        try:
                            result = _run_handoff(
                                mode=mode,
                                project=project,
                                objective=args.objective.strip(),
                                query=args.query.strip(),
                                limit=max(1, args.limit),
                            )
                            prompt = (result.get("reinjection_prompt") or "").strip()
                            prompt_chars = int(result.get("reinjection_prompt_chars") or len(prompt))
                            prompt_tokens_estimated = int(
                                result.get("reinjection_prompt_estimated_tokens") or _estimate_token_count(prompt)
                            )
                            if mode == "pre":
                                _visual_status(
                                    "pre checkpoint_saved "
                                    + f"file={result.get('checkpoint_file') or 'unknown'}",
                                    enabled=args.visual_status,
                                )
                            else:
                                _visual_status(
                                    "post reinjection_prompt_ready "
                                    + f"chars={prompt_chars} est_tokens={prompt_tokens_estimated}",
                                    enabled=args.visual_status,
                                )
                            if prompt and args.prompt_out:
                                Path(args.prompt_out).write_text(prompt + "\n", encoding="utf-8")
                            if mode == "post" and prompt and args.inject_turn_start and thread_id:
                                oversize_reason = _oversize_reasons(
                                    prompt_chars=prompt_chars,
                                    prompt_tokens_estimated=prompt_tokens_estimated,
                                    max_chars=max(0, args.reinjection_max_chars),
                                    max_tokens=max(0, args.reinjection_max_estimated_tokens),
                                )
                                send_prompt = prompt
                                if oversize_reason:
                                    if args.oversize_action == "skip":
                                        reinjection_status = "skipped_oversize"
                                        _log(
                                            "reinjection skipped due to oversize "
                                            + f"({','.join(oversize_reason)})",
                                            quiet=False,
                                        )
                                        _visual_status(
                                            "post reinjection_skipped_oversize "
                                            + f"reasons={','.join(oversize_reason)}",
                                            enabled=args.visual_status,
                                        )
                                    elif args.oversize_action == "truncate":
                                        send_prompt = _truncate_prompt_to_budget(
                                            prompt,
                                            max(0, args.reinjection_max_chars),
                                            max(0, args.reinjection_max_estimated_tokens),
                                        )
                                        if not send_prompt.strip():
                                            reinjection_status = "skipped_truncate_budget"
                                            _log(
                                                "reinjection skipped: truncate budget resolved to empty prompt",
                                                quiet=False,
                                            )
                                            _visual_status(
                                                "post reinjection_skipped_empty_truncate_budget",
                                                enabled=args.visual_status,
                                            )
                                        else:
                                            reinjection_status = "truncated_then_emitted"
                                    else:
                                        reinjection_status = "emitted_oversize_allowed"
                                else:
                                    reinjection_status = "emitted"

                                if reinjection_status in (
                                    "emitted",
                                    "truncated_then_emitted",
                                    "emitted_oversize_allowed",
                                ):
                                    prompt_sent_chars = len(send_prompt)
                                    prompt_sent_tokens_estimated = _estimate_token_count(send_prompt)
                                    inject_counter += 1
                                    _emit_turn_start(
                                        output_framing=args.output_framing,
                                        request_id_prefix=args.request_id_prefix,
                                        thread_id=thread_id,
                                        prompt=send_prompt,
                                        counter=inject_counter,
                                    )
                                    prompt_sent = True
                                    _visual_status(
                                        "post reinjection_emitted "
                                        + f"status={reinjection_status} sent_chars={prompt_sent_chars} "
                                        + f"sent_est_tokens={prompt_sent_tokens_estimated}",
                                        enabled=args.visual_status,
                                    )
                            elif mode == "post" and prompt and args.inject_turn_start and not thread_id:
                                reinjection_status = "skipped_missing_thread_id"
                                _visual_status(
                                    "post reinjection_skipped_missing_thread_id",
                                    enabled=args.visual_status,
                                )
                            elif mode == "post" and prompt and not args.inject_turn_start:
                                reinjection_status = "generated_not_injected"
                                _visual_status(
                                    "post reinjection_generated_not_injected",
                                    enabled=args.visual_status,
                                )
                        except Exception as exc:
                            err = str(exc)
                            _log(f"handoff error: {err}", quiet=False)
                            _visual_status(f"{mode} handoff_error {err}", enabled=args.visual_status)

                        status = "ok"
                        if err is not None:
                            status = "error"
                        elif reinjection_status in ("skipped_oversize", "skipped_truncate_budget"):
                            status = "skipped_oversize"

                        compaction_record = {
                            "action": "compaction",
                            "event": event_kind,
                            "mode": mode,
                            "thread_id": thread_id,
                            "status": status,
                            "project": project,
                            "checkpoint_file": None if not result else result.get("checkpoint_file"),
                            "reinjection_status": reinjection_status,
                            "oversize_action": args.oversize_action,
                            "oversize_reason": oversize_reason,
                            "prompt_chars": prompt_chars,
                            "prompt_tokens_estimated": prompt_tokens_estimated,
                            "prompt_sent": prompt_sent,
                            "prompt_sent_chars": prompt_sent_chars,
                            "prompt_sent_tokens_estimated": prompt_sent_tokens_estimated,
                            "reinjection_max_chars": max(0, args.reinjection_max_chars),
                            "reinjection_max_estimated_tokens": max(0, args.reinjection_max_estimated_tokens),
                            "error": err,
                        }
                        _record_event(args.jsonl_log, compaction_record)

                        if args.save_compaction_alerts and _should_save_compaction_alert(status, reinjection_status):
                            ts_iso = now_iso()
                            alert_title = _build_auto_save_title(
                                args.compaction_alert_title_prefix,
                                event_kind,
                                thread_id,
                                ts_iso,
                            )
                            alert_body = _build_compaction_alert_body(
                                event_kind=event_kind,
                                mode=mode,
                                thread_id=thread_id,
                                objective=args.objective.strip(),
                                status=status,
                                reinjection_status=reinjection_status,
                                oversize_reason=oversize_reason,
                                prompt_chars=prompt_chars,
                                prompt_tokens_estimated=prompt_tokens_estimated,
                                prompt_sent=prompt_sent,
                                prompt_sent_chars=prompt_sent_chars,
                                prompt_sent_tokens_estimated=prompt_sent_tokens_estimated,
                                error=err,
                                payload=params if params is not None else message,
                                ts_iso=ts_iso,
                            )
                            alert_secret_indicators = detect_secret_indicators(f"{alert_title}\n{alert_body}")
                            if alert_secret_indicators:
                                _log(
                                    "compaction alert memory note skipped: secret indicators detected "
                                    + f"({','.join(alert_secret_indicators)})",
                                    quiet=False,
                                )
                                _record_event(
                                    args.jsonl_log,
                                    {
                                        "action": "compaction_alert",
                                        "event": event_kind,
                                        "mode": mode,
                                        "thread_id": thread_id,
                                        "status": "skipped_secret",
                                        "project": project,
                                        "title": alert_title,
                                        "secret_indicators": alert_secret_indicators,
                                        "error": None,
                                    },
                                )
                            else:
                                alert_save_result: dict[str, Any] | None = None
                                alert_save_error: str | None = None
                                try:
                                    alert_save_result = _run_save_memory(
                                        project=project,
                                        title=alert_title,
                                        body=alert_body,
                                        tags=args.compaction_alert_tags,
                                    )
                                    _log(
                                        "compaction alert memory note persisted "
                                        + f"for {event_kind} in project {project}",
                                        quiet=args.quiet,
                                    )
                                    _visual_status(
                                        "compaction_alert_persisted "
                                        + f"note={alert_save_result.get('file') if alert_save_result else 'unknown'}",
                                        enabled=args.visual_status,
                                    )
                                except Exception as exc:
                                    alert_save_error = str(exc)
                                    _log(f"compaction alert memory note error: {alert_save_error}", quiet=False)
                                    _visual_status(
                                        f"compaction_alert_error {alert_save_error}",
                                        enabled=args.visual_status,
                                    )

                                _record_event(
                                    args.jsonl_log,
                                    {
                                        "action": "compaction_alert",
                                        "event": event_kind,
                                        "mode": mode,
                                        "thread_id": thread_id,
                                        "status": "ok" if alert_save_error is None else "error",
                                        "project": project,
                                        "title": alert_title,
                                        "note_file": None if not alert_save_result else alert_save_result.get("file"),
                                        "canonical_file": None
                                        if not alert_save_result
                                        else alert_save_result.get("canonical_file"),
                                        "error": alert_save_error,
                                    },
                                )

            if auto_save_events and method in auto_save_events:
                event_id = _extract_event_id(message)
                if event_id:
                    dedupe_token = f"{method}:{event_id}"
                else:
                    digest = hashlib.sha256(
                        f"{method}:{thread_id}:{json.dumps(params, sort_keys=True, default=str)}".encode("utf-8")
                    ).hexdigest()[:16]
                    dedupe_token = f"{method}:{digest}"
                if dedupe_token in seen_auto_event_ids:
                    continue
                seen_auto_event_ids.add(dedupe_token)

                target_project = project
                project_hint = _extract_field_value(params if params is not None else message, args.auto_save_project_field)
                if project_hint:
                    try:
                        target_project = ensure_project_name(project_hint)
                    except MemoryValidationError:
                        _log(
                            f"auto-save project hint rejected ({project_hint!r}); using --project={project!r}",
                            quiet=args.quiet,
                        )

                summary_values: list[tuple[str, str]] = []
                summary_source = params if params is not None else message
                for field_name in auto_save_summary_fields:
                    value = _extract_field_value(summary_source, field_name)
                    if value:
                        summary_values.append((field_name, value))

                ts_iso = now_iso()
                title = _build_auto_save_title(args.auto_save_title_prefix, method, event_id, ts_iso)
                body = _build_auto_save_body(
                    event_kind=method,
                    thread_id=thread_id,
                    event_id=event_id,
                    objective=args.objective,
                    summary_values=summary_values,
                    payload=summary_source,
                    ts_iso=ts_iso,
                )

                secret_indicators = detect_secret_indicators(f"{title}\n{body}")
                if secret_indicators:
                    _log(
                        f"auto-save skipped for {method}: secret indicators detected ({','.join(secret_indicators)})",
                        quiet=False,
                    )
                    _visual_status(
                        "autosave_skipped_secret "
                        + f"event={method} indicators={','.join(secret_indicators)}",
                        enabled=args.visual_status,
                    )
                    _record_event(
                        args.jsonl_log,
                        {
                            "action": "autosave",
                            "event": method,
                            "mode": "autosave",
                            "thread_id": thread_id,
                            "event_id": event_id,
                            "status": "skipped_secret",
                            "project": target_project,
                            "title": title,
                            "secret_indicators": secret_indicators,
                            "error": None,
                        },
                    )
                    continue

                save_result: dict[str, Any] | None = None
                save_error: str | None = None
                try:
                    save_result = _run_save_memory(
                        project=target_project,
                        title=title,
                        body=body,
                        tags=args.auto_save_tags,
                    )
                    _log(f"auto-save persisted for {method} in project {target_project}", quiet=args.quiet)
                    _visual_status(
                        "autosave_persisted "
                        + f"event={method} note={save_result.get('file') if save_result else 'unknown'}",
                        enabled=args.visual_status,
                    )
                except Exception as exc:
                    save_error = str(exc)
                    _log(f"auto-save error: {save_error}", quiet=False)
                    _visual_status(
                        f"autosave_error event={method} error={save_error}",
                        enabled=args.visual_status,
                    )

                _record_event(
                    args.jsonl_log,
                    {
                        "action": "autosave",
                        "event": method,
                        "mode": "autosave",
                        "thread_id": thread_id,
                        "event_id": event_id,
                        "status": "ok" if save_error is None else "error",
                        "project": target_project,
                        "title": title,
                        "note_file": None if not save_result else save_result.get("file"),
                        "canonical_file": None if not save_result else save_result.get("canonical_file"),
                        "error": save_error,
                    },
                )
    finally:
        if source_file:
            source_file.close()

    _log("auto-memory listener stopped", quiet=args.quiet)
    _visual_status("listener_stopped", enabled=args.visual_status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
