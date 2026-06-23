from __future__ import annotations

import json
import re
import socket
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib import error, parse, request

from memory_agent_config import (
    DEFAULT_CODEX_MODEL,
    MemoryAgentConfig,
    load_system_prompt_text,
)

ALLOWED_MODES = {"read_today_log", "search_memory"}
SUMMARY_PREFIX = "[SUMMARY]"
SUMMARY_MAX_CHARS = 500
_FENCED_BLOCK_RE = re.compile(
    r"^```(?:[^\n`]*)\s*\n(?P<body>.*)\n```$",
    re.DOTALL,
)
_SUMMARY_LINE_RE = re.compile(
    r"^(?:\[SUMMARY\]|SUMMARY:|Summary:)\s*(?P<body>.*)$"
)
_ENTRY_ID_RE = re.compile(r"\[ID:(?P<id>[^\]]+)\]")
_UNSET = object()


class MemoryAgentClientError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        raw_api_response: Mapping[str, Any] | None = None,
        content_text: str | None = None,
        response_body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.raw_api_response = (
            dict(raw_api_response) if raw_api_response is not None else None
        )
        self.content_text = content_text
        self.response_body = response_body

    def attach_context(
        self,
        *,
        raw_api_response: Mapping[str, Any] | object = _UNSET,
        content_text: str | object = _UNSET,
        response_body: str | object = _UNSET,
    ) -> "MemoryAgentClientError":
        if raw_api_response is not _UNSET and self.raw_api_response is None:
            self.raw_api_response = (
                dict(raw_api_response)
                if isinstance(raw_api_response, Mapping)
                else None
            )
        if content_text is not _UNSET and self.content_text is None:
            self.content_text = (
                content_text if isinstance(content_text, str) else None
            )
        if response_body is not _UNSET and self.response_body is None:
            self.response_body = (
                response_body if isinstance(response_body, str) else None
            )
        return self


class MemoryAgentTransportError(MemoryAgentClientError):
    pass


class MemoryAgentProtocolError(MemoryAgentClientError):
    pass


class MemoryAgentSchemaError(MemoryAgentClientError):
    pass


@dataclass(frozen=True)
class MemoryAgentResponse:
    raw_api_response: dict[str, Any]
    content_text: str
    rendered_output: str


def call_memory_agent(
    config: MemoryAgentConfig,
    request_payload: Mapping[str, Any],
) -> MemoryAgentResponse:
    config.require_runtime_ready()

    request_mode = _require_request_mode(request_payload)
    system_prompt = build_runtime_system_prompt(
        canonical_prompt=load_system_prompt_text(config),
        request_mode=request_mode,
        request_payload=request_payload,
    )

    if config.api_style == "codex_exec":
        response_json, content_text = _run_codex_exec(
            config=config,
            system_prompt=system_prompt,
            request_payload=request_payload,
        )
    elif config.api_style == "ollama_native_chat":
        api_payload = build_ollama_chat_payload(
            model=config.model or "",
            system_prompt=system_prompt,
            request_payload=request_payload,
            disable_thinking=config.disable_thinking,
        )
        response_json = _post_ollama_chat(
            base_url=config.base_url or "",
            api_key=config.api_key,
            timeout_seconds=config.timeout_seconds,
            payload=api_payload,
        )
        try:
            content_text = _extract_ollama_message_text(response_json)
        except MemoryAgentClientError as exc:
            raise exc.attach_context(raw_api_response=response_json)
    else:
        api_payload = build_chat_completions_payload(
            model=config.model or "",
            system_prompt=system_prompt,
            request_payload=request_payload,
        )
        response_json = _post_chat_completions(
            base_url=config.base_url or "",
            api_key=config.api_key,
            timeout_seconds=config.timeout_seconds,
            payload=api_payload,
        )
        try:
            content_text = _extract_message_text(response_json)
        except MemoryAgentClientError as exc:
            raise exc.attach_context(raw_api_response=response_json)

    try:
        rendered_output = normalize_agent_response_text(
            content_text=content_text,
            request_payload=request_payload,
        )
    except MemoryAgentClientError as exc:
        raise exc.attach_context(
            raw_api_response=response_json,
            content_text=content_text,
        )

    return MemoryAgentResponse(
        raw_api_response=response_json,
        content_text=content_text,
        rendered_output=rendered_output,
    )


def build_codex_exec_prompt(
    *,
    system_prompt: str,
    request_payload: Mapping[str, Any],
) -> str:
    return "\n\n".join(
        [
            "You are running inside Codex CLI exec as a plain-text preprocessing step for easy-memory.",
            (
                "Do not use shell commands, do not inspect the workspace, "
                "do not call MCP tools, and do not modify any files. "
                "Use only the provided request payload."
            ),
            (
                "Keep only task-relevant memory blocks. Copy each retained "
                "rendered_block exactly as provided."
            ),
            (
                f"End the reply with exactly one summary line that starts with "
                f"{SUMMARY_PREFIX} and keep that summary within {SUMMARY_MAX_CHARS} characters."
            ),
            (
                f"If no memory remains relevant after filtering, return only the {SUMMARY_PREFIX} line."
            ),
            "Canonical prompt:",
            system_prompt,
            "Input payload JSON:",
            json.dumps(
                dict(request_payload),
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        ]
    )


def _run_codex_exec(
    *,
    config: MemoryAgentConfig,
    system_prompt: str,
    request_payload: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    prompt_text = build_codex_exec_prompt(
        system_prompt=system_prompt,
        request_payload=request_payload,
    )
    with tempfile.TemporaryDirectory(prefix="easy-memory-codex-exec-") as tmp_dir:
        tmp_path = Path(tmp_dir)
        output_path = tmp_path / "response.txt"
        command = build_codex_exec_command(
            config=config,
            output_path=output_path,
            prompt_text=prompt_text,
        )
        try:
            completed = subprocess.run(
                command,
                cwd=Path.cwd(),
                capture_output=True,
                text=True,
                timeout=config.timeout_seconds,
                check=False,
            )
        except FileNotFoundError as exc:
            raise MemoryAgentTransportError(
                f"Codex CLI executable not found: {config.codex_binary}"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise MemoryAgentTransportError(
                "Codex exec request timed out.",
                raw_api_response={
                    "command": command,
                    "stdout": exc.stdout,
                    "stderr": exc.stderr,
                },
                response_body=_format_codex_exec_output(
                    stdout_text=exc.stdout,
                    stderr_text=exc.stderr,
                ),
            ) from exc

        output_text = (
            output_path.read_text(encoding="utf-8").strip()
            if output_path.exists()
            else ""
        )
        raw_response = {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "output_file": output_text,
        }
        if completed.returncode != 0:
            raise MemoryAgentTransportError(
                f"Codex exec failed with exit code {completed.returncode}.",
                raw_api_response=raw_response,
                response_body=_format_codex_exec_output(
                    stdout_text=completed.stdout,
                    stderr_text=completed.stderr,
                ),
            )

        content_text = output_text or _extract_codex_exec_content(completed.stdout)
        if not content_text:
            raise MemoryAgentProtocolError(
                "Codex exec did not produce a structured response.",
                raw_api_response=raw_response,
                response_body=_format_codex_exec_output(
                    stdout_text=completed.stdout,
                    stderr_text=completed.stderr,
                ),
            )
        return raw_response, content_text


def build_codex_exec_command(
    *,
    config: MemoryAgentConfig,
    output_path: Path,
    prompt_text: str,
) -> list[str]:
    command = [
        config.codex_binary,
        "exec",
        "--ephemeral",
        "--color",
        "never",
        "-s",
        "read-only",
        "--skip-git-repo-check",
        "-m",
        config.model or DEFAULT_CODEX_MODEL,
        "-o",
        str(output_path),
    ]
    if config.codex_profile:
        command.extend(["-p", config.codex_profile])
    if config.codex_service_tier:
        command.extend(
            [
                "-c",
                f"service_tier={_toml_string_literal(config.codex_service_tier)}",
            ]
        )
    if config.codex_reasoning_effort:
        command.extend(
            [
                "-c",
                "model_reasoning_effort="
                f"{_toml_string_literal(config.codex_reasoning_effort)}",
            ]
        )
    command.append(prompt_text)
    return command


def _toml_string_literal(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _extract_codex_exec_content(stdout_text: str) -> str:
    stripped = stdout_text.strip()
    if not stripped:
        return ""
    lines = [line.rstrip() for line in stripped.splitlines() if line.strip()]
    if not lines:
        return ""
    return "\n".join(lines)


def _format_codex_exec_output(
    *,
    stdout_text: str | None,
    stderr_text: str | None,
) -> str:
    sections = []
    if stdout_text:
        sections.append(f"stdout:\n{stdout_text}")
    if stderr_text:
        sections.append(f"stderr:\n{stderr_text}")
    return "\n\n".join(sections) if sections else ""


def build_chat_completions_payload(
    model: str,
    system_prompt: str,
    request_payload: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(
                    dict(request_payload),
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
            },
        ],
        "temperature": 0,
    }


def build_ollama_chat_payload(
    model: str,
    system_prompt: str,
    request_payload: Mapping[str, Any],
    disable_thinking: bool = False,
) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(
                    dict(request_payload),
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
            },
        ],
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }
    if disable_thinking:
        payload["think"] = False
    return payload


def build_runtime_system_prompt(
    canonical_prompt: str,
    request_mode: str,
    request_payload: Mapping[str, Any],
) -> str:
    template_lines = [
        "<copy zero or more rendered_block values exactly as provided>",
        "",
        f"{SUMMARY_PREFIX} <summary no longer than {SUMMARY_MAX_CHARS} characters>",
    ]
    protocol_lines = [
        "Runtime protocol requirements:",
        f'1. mode is "{request_mode}". Use task_context to judge relevance.',
        "2. Remove all unrelated memory blocks completely.",
        "3. For each retained memory, copy the full rendered_block exactly as given.",
        "4. Do not rewrite IDs, timestamps, related resource lines, URLs, or file paths.",
        "5. Do not return JSON, bullets, explanations, or code fences.",
        "6. End the response with exactly one summary line.",
        f"7. That summary line must start with {SUMMARY_PREFIX}.",
        f"8. Keep the summary within {SUMMARY_MAX_CHARS} characters.",
        f"9. If no memory is relevant, return only the {SUMMARY_PREFIX} line.",
        "Reply template:",
        "\n".join(template_lines),
        "Rendered entry index:",
        build_rendered_entry_index(request_payload),
    ]
    return "\n\n".join([canonical_prompt, "\n".join(protocol_lines)])


def build_rendered_entry_index(
    request_payload: Mapping[str, Any],
) -> str:
    entries = request_payload.get("entries")
    if not isinstance(entries, list) or not entries:
        return "No entries available."
    lines = []
    for item in entries:
        if not isinstance(item, Mapping):
            continue
        entry_id = item.get("entry_id")
        if not isinstance(entry_id, str):
            continue
        log_file = item.get("log_file")
        rendered_block = item.get("rendered_block")
        header = f"- {entry_id}"
        if isinstance(log_file, str) and log_file:
            header += f" ({log_file})"
        if isinstance(rendered_block, str) and rendered_block:
            header += f": {rendered_block.splitlines()[0][:160]}"
        lines.append(header)
    return "\n".join(lines) if lines else "No entries available."


def normalize_agent_response_text(
    *,
    content_text: str,
    request_payload: Mapping[str, Any],
) -> str:
    stripped = extract_agent_text(content_text)
    if not stripped:
        raise MemoryAgentProtocolError("Agent returned empty content.")

    lines = [line.rstrip() for line in stripped.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise MemoryAgentProtocolError("Agent returned empty content.")

    summary_index = last_nonempty_index(lines)
    if summary_index is None:
        raise MemoryAgentProtocolError("Agent returned empty content.")

    summary_match = _SUMMARY_LINE_RE.match(lines[summary_index].strip())
    if summary_match:
        body_lines = lines[:summary_index]
        summary_text = summary_match.group("body").strip()
    else:
        body_lines = lines
        summary_text = ""

    summary_text = truncate_summary_text(summary_text)
    if not summary_text:
        summary_text = (
            "Agent filtering completed. Review the retained memories above."
        )

    body_text = "\n".join(body_lines).strip()
    body_text = canonicalize_body_text(
        body_text=body_text,
        request_payload=request_payload,
    )
    summary_line = f"{SUMMARY_PREFIX} {summary_text}"
    if body_text:
        return f"{body_text}\n\n{summary_line}"
    return summary_line


def extract_agent_text(content_text: str) -> str:
    stripped = content_text.strip()
    if not stripped:
        return ""
    fenced_match = _FENCED_BLOCK_RE.fullmatch(stripped)
    if fenced_match:
        return fenced_match.group("body").strip()
    return stripped


def last_nonempty_index(lines: list[str]) -> int | None:
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].strip():
            return index
    return None


def truncate_summary_text(summary_text: str) -> str:
    normalized = " ".join(summary_text.split())
    if len(normalized) <= SUMMARY_MAX_CHARS:
        return normalized
    return normalized[:SUMMARY_MAX_CHARS].rstrip()


def canonicalize_body_text(
    *,
    body_text: str,
    request_payload: Mapping[str, Any],
) -> str:
    if not body_text:
        return ""

    rendered_blocks = collect_rendered_blocks_by_entry_id(request_payload)
    if not rendered_blocks:
        return body_text

    selected_ids: list[str] = []
    seen_ids: set[str] = set()
    for match in _ENTRY_ID_RE.finditer(body_text):
        entry_id = match.group("id")
        if entry_id in rendered_blocks and entry_id not in seen_ids:
            seen_ids.add(entry_id)
            selected_ids.append(entry_id)
    if not selected_ids:
        return body_text
    return "\n\n".join(rendered_blocks[entry_id] for entry_id in selected_ids)


def collect_rendered_blocks_by_entry_id(
    request_payload: Mapping[str, Any],
) -> dict[str, str]:
    entries = request_payload.get("entries")
    if not isinstance(entries, list):
        return {}
    blocks: dict[str, str] = {}
    for item in entries:
        if not isinstance(item, Mapping):
            continue
        entry_id = item.get("entry_id")
        rendered_block = item.get("rendered_block")
        if isinstance(entry_id, str) and isinstance(rendered_block, str):
            blocks[entry_id] = rendered_block.strip()
    return blocks


def _require_request_mode(request_payload: Mapping[str, Any]) -> str:
    mode = request_payload.get("mode")
    if not isinstance(mode, str):
        raise MemoryAgentSchemaError("Request payload must include a string mode.")
    if mode not in ALLOWED_MODES:
        raise MemoryAgentSchemaError(f"Invalid request mode: {mode}")
    return mode


def _post_chat_completions(
    base_url: str,
    api_key: str | None,
    timeout_seconds: float,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    url = _build_chat_completions_url(base_url)
    headers = {
        "Content-Type": "application/json",
    }
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key.strip()}"
    return _post_json_request(
        url=url,
        headers=headers,
        timeout_seconds=timeout_seconds,
        payload=payload,
    )


def _post_ollama_chat(
    base_url: str,
    api_key: str | None,
    timeout_seconds: float,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    url = _build_ollama_chat_url(base_url)
    headers = {
        "Content-Type": "application/json",
    }
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key.strip()}"
    return _post_json_request(
        url=url,
        headers=headers,
        timeout_seconds=timeout_seconds,
        payload=payload,
    )


def _post_json_request(
    *,
    url: str,
    headers: Mapping[str, str],
    timeout_seconds: float,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    raw_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    http_request = request.Request(
        url,
        data=raw_body,
        headers=dict(headers),
        method="POST",
    )
    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise MemoryAgentTransportError(
            f"Memory agent HTTP error {exc.code}: {body}",
            response_body=body,
        ) from exc
    except socket.timeout as exc:
        raise MemoryAgentTransportError(
            "Memory agent request timed out."
        ) from exc
    except TimeoutError as exc:
        raise MemoryAgentTransportError(
            "Memory agent request timed out."
        ) from exc
    except error.URLError as exc:
        raise MemoryAgentTransportError(
            f"Memory agent connection failed: {exc.reason}"
        ) from exc

    try:
        parsed_body = json.loads(body)
    except json.JSONDecodeError as exc:
        raise MemoryAgentProtocolError(
            "Memory agent API did not return valid JSON.",
            response_body=body,
        ) from exc
    if not isinstance(parsed_body, dict):
        raise MemoryAgentProtocolError(
            "Memory agent API response must be a JSON object.",
            response_body=body,
        )
    return parsed_body


def _build_chat_completions_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if not normalized:
        raise MemoryAgentTransportError("base_url must not be empty.")
    parsed_base = parse.urlsplit(normalized)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise MemoryAgentTransportError(
            f"Invalid base_url for memory agent: {base_url}"
        )
    if parsed_base.path.endswith("/chat/completions"):
        return normalized
    if parsed_base.path.endswith("/v1"):
        return f"{normalized}/chat/completions"
    return f"{normalized}/chat/completions"


def _build_ollama_chat_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if not normalized:
        raise MemoryAgentTransportError("base_url must not be empty.")
    parsed_base = parse.urlsplit(normalized)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise MemoryAgentTransportError(
            f"Invalid base_url for memory agent: {base_url}"
        )
    base_without_suffix = normalized
    suffixes = (
        "/api/chat",
        "/v1/chat/completions",
        "/chat/completions",
        "/v1",
    )
    for suffix in suffixes:
        if base_without_suffix.endswith(suffix):
            base_without_suffix = base_without_suffix[: -len(suffix)]
            break
    if base_without_suffix.endswith("/api"):
        return f"{base_without_suffix}/chat"
    return f"{base_without_suffix}/api/chat"


def _extract_message_text(api_response: Mapping[str, Any]) -> str:
    choices = api_response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise MemoryAgentProtocolError(
            "Memory agent API response is missing choices."
        )
    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise MemoryAgentProtocolError(
            "Memory agent API response choice must be an object."
        )
    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise MemoryAgentProtocolError(
            "Memory agent API response is missing message."
        )
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for index, item in enumerate(content):
            if not isinstance(item, dict):
                raise MemoryAgentProtocolError(
                    f"message.content[{index}] must be an object."
                )
            if item.get("type") == "text" and isinstance(item.get("text"), str):
                text_parts.append(item["text"])
        joined = "".join(text_parts).strip()
        if joined:
            return joined
    raise MemoryAgentProtocolError(
        "Memory agent API response does not contain supported message content."
    )


def _extract_ollama_message_text(api_response: Mapping[str, Any]) -> str:
    message = api_response.get("message")
    if not isinstance(message, dict):
        raise MemoryAgentProtocolError(
            "Ollama native response is missing message."
        )
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, (dict, list)):
        return json.dumps(content, ensure_ascii=False)
    raise MemoryAgentProtocolError(
        "Ollama native response does not contain supported message content."
    )
