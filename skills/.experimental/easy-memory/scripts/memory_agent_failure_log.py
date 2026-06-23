from __future__ import annotations

import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from memory_agent_client import MemoryAgentClientError, MemoryAgentResponse
from memory_agent_config import MemoryAgentConfig

AGENT_FAILURE_LOG_NAME = "agent-failures.jsonl"


def agent_failure_log_path(skill_dir: Path) -> Path:
    return skill_dir / "logs" / AGENT_FAILURE_LOG_NAME


def append_agent_failure_log(
    *,
    config: MemoryAgentConfig,
    request_payload: Mapping[str, Any],
    fallback_reason: str,
    error: BaseException | None = None,
    response: MemoryAgentResponse | None = None,
) -> Path | None:
    log_path = agent_failure_log_path(config.skill_dir)
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "fallback_reason": fallback_reason,
        "mode": request_payload.get("mode"),
        "model": config.model,
        "base_url": config.base_url,
        "api_style": config.api_style,
        "codex_binary": config.codex_binary,
        "codex_profile": config.codex_profile,
        "codex_service_tier": config.codex_service_tier,
        "codex_reasoning_effort": config.codex_reasoning_effort,
        "disable_thinking": config.disable_thinking,
        "timeout_seconds": config.timeout_seconds,
        "request_payload": dict(request_payload),
        "error_type": error.__class__.__name__ if error else None,
        "error_message": str(error) if error else None,
        "raw_api_response": _extract_raw_api_response(error=error, response=response),
        "content_text": _extract_content_text(error=error, response=response),
        "response_body": _extract_response_body(error=error),
        "rendered_output": response.rendered_output if response else None,
        "traceback": _format_traceback(error),
    }
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")
    except OSError:
        return None
    return log_path


def _extract_raw_api_response(
    *,
    error: BaseException | None,
    response: MemoryAgentResponse | None,
) -> dict[str, Any] | None:
    if response is not None:
        return dict(response.raw_api_response)
    if isinstance(error, MemoryAgentClientError) and error.raw_api_response is not None:
        return dict(error.raw_api_response)
    return None


def _extract_content_text(
    *,
    error: BaseException | None,
    response: MemoryAgentResponse | None,
) -> str | None:
    if response is not None:
        return response.content_text
    if isinstance(error, MemoryAgentClientError):
        return error.content_text
    return None


def _extract_response_body(
    *,
    error: BaseException | None,
) -> str | None:
    if isinstance(error, MemoryAgentClientError):
        return error.response_body
    return None


def _format_traceback(error: BaseException | None) -> str | None:
    if error is None or error.__traceback__ is None:
        return None
    return "".join(
        traceback.format_exception(
            type(error),
            error,
            error.__traceback__,
        )
    )
