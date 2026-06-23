from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ENV_AGENT_CONFIG_FILE = "EASY_MEMORY_AGENT_CONFIG_FILE"
ENV_AGENT_ENABLED = "EASY_MEMORY_AGENT_ENABLED"
ENV_AGENT_BASE_URL = "EASY_MEMORY_AGENT_BASE_URL"
ENV_AGENT_API_KEY = "EASY_MEMORY_AGENT_API_KEY"
ENV_AGENT_MODEL = "EASY_MEMORY_AGENT_MODEL"
ENV_AGENT_API_STYLE = "EASY_MEMORY_AGENT_API_STYLE"
ENV_AGENT_DISABLE_THINKING = "EASY_MEMORY_AGENT_DISABLE_THINKING"
ENV_AGENT_TIMEOUT_SECONDS = "EASY_MEMORY_AGENT_TIMEOUT_SECONDS"
ENV_AGENT_SYSTEM_PROMPT_FILE = "EASY_MEMORY_AGENT_SYSTEM_PROMPT_FILE"
ENV_AGENT_CODEX_BINARY = "EASY_MEMORY_AGENT_CODEX_BINARY"
ENV_AGENT_CODEX_PROFILE = "EASY_MEMORY_AGENT_CODEX_PROFILE"
ENV_AGENT_CODEX_SERVICE_TIER = "EASY_MEMORY_AGENT_CODEX_SERVICE_TIER"
ENV_AGENT_CODEX_REASONING_EFFORT = "EASY_MEMORY_AGENT_CODEX_REASONING_EFFORT"
DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_CODEX_EXEC_TIMEOUT_SECONDS = 120.0
DEFAULT_CONFIG_FILE_NAME = "agent-config.json"
DEFAULT_API_STYLE = "openai_chat_completions"
DEFAULT_CODEX_BINARY = "codex"
DEFAULT_CODEX_MODEL = "gpt-5.3-codex-spark"
DEFAULT_CODEX_SERVICE_TIER = "fast"
DEFAULT_CODEX_REASONING_EFFORT = "medium"
ALLOWED_API_STYLES = {
    "codex_exec",
    "openai_chat_completions",
    "ollama_native_chat",
}

_PROMPT_BLOCK_RE = re.compile(r"```(?:text)?\n(?P<body>.*?)```", re.DOTALL)


class MemoryAgentConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class MemoryAgentConfig:
    enabled: bool
    base_url: str | None
    api_key: str | None
    model: str | None
    api_style: str
    disable_thinking: bool
    codex_binary: str
    codex_profile: str | None
    codex_service_tier: str | None
    codex_reasoning_effort: str | None
    timeout_seconds: float
    config_file: Path
    system_prompt_file: Path
    skill_dir: Path

    def require_runtime_ready(self) -> None:
        if not self.enabled:
            raise MemoryAgentConfigError("Memory agent is disabled.")
        missing = []
        if self.api_style == "codex_exec":
            if not self.codex_binary:
                missing.append(ENV_AGENT_CODEX_BINARY)
        elif not self.base_url:
            missing.append(ENV_AGENT_BASE_URL)
        if not self.model:
            missing.append(ENV_AGENT_MODEL)
        if missing:
            missing_text = ", ".join(missing)
            raise MemoryAgentConfigError(
                f"Memory agent is enabled but missing required configuration: {missing_text}"
            )
        if not self.system_prompt_file.exists():
            raise MemoryAgentConfigError(
                f"System prompt file not found: {self.system_prompt_file}"
            )


def installed_skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def default_system_prompt_file(skill_dir: Path | None = None) -> Path:
    resolved_skill_dir = skill_dir or installed_skill_dir()
    return resolved_skill_dir / "references" / "memory-agent-system-prompt.md"


def default_local_config_file() -> Path:
    return Path.cwd() / "easy-memory" / DEFAULT_CONFIG_FILE_NAME


def parse_enabled_flag(raw_value: Any) -> bool:
    return parse_bool_flag(
        raw_value,
        label=ENV_AGENT_ENABLED,
        default=False,
    )


def parse_bool_flag(raw_value: Any, *, label: str, default: bool) -> bool:
    if raw_value is None:
        return default
    if isinstance(raw_value, bool):
        return raw_value
    if not isinstance(raw_value, str):
        raise MemoryAgentConfigError(f"{label} must be a boolean or string.")
    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off", ""}:
        return False
    raise MemoryAgentConfigError(
        f"{label} must be one of true/false/1/0/yes/no/on/off."
    )


def parse_timeout_seconds(raw_value: Any, *, default: float) -> float:
    if raw_value is None:
        return default
    if isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool):
        timeout_seconds = float(raw_value)
        if timeout_seconds <= 0:
            raise MemoryAgentConfigError(
                f"{ENV_AGENT_TIMEOUT_SECONDS} must be a positive number."
            )
        return timeout_seconds
    if not isinstance(raw_value, str):
        raise MemoryAgentConfigError(
            f"{ENV_AGENT_TIMEOUT_SECONDS} must be a positive number."
        )
    if not raw_value.strip():
        return default
    try:
        timeout_seconds = float(raw_value.strip())
    except ValueError as exc:
        raise MemoryAgentConfigError(
            f"{ENV_AGENT_TIMEOUT_SECONDS} must be a positive number."
        ) from exc
    if timeout_seconds <= 0:
        raise MemoryAgentConfigError(
            f"{ENV_AGENT_TIMEOUT_SECONDS} must be a positive number."
        )
    return timeout_seconds


def parse_api_style(raw_value: Any) -> str:
    if raw_value is None:
        return DEFAULT_API_STYLE
    if not isinstance(raw_value, str):
        raise MemoryAgentConfigError(
            f"{ENV_AGENT_API_STYLE} must be a string."
        )
    normalized = raw_value.strip()
    if not normalized:
        return DEFAULT_API_STYLE
    if normalized not in ALLOWED_API_STYLES:
        allowed = ", ".join(sorted(ALLOWED_API_STYLES))
        raise MemoryAgentConfigError(
            f"{ENV_AGENT_API_STYLE} must be one of: {allowed}"
        )
    return normalized


def resolve_system_prompt_file(
    raw_value: Any,
    skill_dir: Path,
    config_dir: Path | None = None,
) -> Path:
    if raw_value is None:
        return default_system_prompt_file(skill_dir)
    if not isinstance(raw_value, str):
        raise MemoryAgentConfigError(
            f"{ENV_AGENT_SYSTEM_PROMPT_FILE} must be a string path."
        )
    if not raw_value.strip():
        return default_system_prompt_file(skill_dir)
    candidate = Path(raw_value.strip()).expanduser()
    if not candidate.is_absolute():
        base_dir = config_dir or Path.cwd()
        candidate = (base_dir / candidate).resolve()
    return candidate


def resolve_config_file_path(raw_value: str | None) -> tuple[Path, bool]:
    if raw_value is None or not raw_value.strip():
        return default_local_config_file(), False
    candidate = Path(raw_value.strip()).expanduser()
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate, True


def load_local_config_payload(
    config_file: Path,
    explicit: bool,
) -> dict[str, Any]:
    if not config_file.exists():
        if explicit:
            raise MemoryAgentConfigError(
                f"Memory agent config file not found: {config_file}"
            )
        return {}
    try:
        raw_text = config_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise MemoryAgentConfigError(
            f"Failed to read memory agent config file: {config_file}"
        ) from exc
    if not raw_text.strip():
        return {}
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise MemoryAgentConfigError(
            f"Memory agent config file is not valid JSON: {config_file}"
        ) from exc
    if not isinstance(payload, dict):
        raise MemoryAgentConfigError(
            f"Memory agent config file must contain a JSON object: {config_file}"
        )
    return payload


def load_memory_agent_config(
    env: Mapping[str, str] | None = None,
    skill_dir: Path | None = None,
) -> MemoryAgentConfig:
    env_map = env or os.environ
    resolved_skill_dir = skill_dir or installed_skill_dir()
    config_file, config_file_explicit = resolve_config_file_path(
        env_map.get(ENV_AGENT_CONFIG_FILE)
    )
    config_payload = load_local_config_payload(
        config_file=config_file,
        explicit=config_file_explicit,
    )
    api_style = parse_api_style(
        _select_raw_value(
            env_map,
            config_payload,
            ENV_AGENT_API_STYLE,
            "api_style",
        )
    )
    model = _normalize_optional_string(
        _select_raw_value(
            env_map,
            config_payload,
            ENV_AGENT_MODEL,
            "model",
        ),
        ENV_AGENT_MODEL,
    )
    if api_style == "codex_exec" and model is None:
        model = DEFAULT_CODEX_MODEL
    timeout_default = (
        DEFAULT_CODEX_EXEC_TIMEOUT_SECONDS
        if api_style == "codex_exec"
        else DEFAULT_TIMEOUT_SECONDS
    )
    codex_binary = _normalize_optional_string(
        _select_raw_value(
            env_map,
            config_payload,
            ENV_AGENT_CODEX_BINARY,
            "codex_binary",
        ),
        ENV_AGENT_CODEX_BINARY,
    ) or DEFAULT_CODEX_BINARY
    codex_service_tier = _normalize_optional_string(
        _select_raw_value(
            env_map,
            config_payload,
            ENV_AGENT_CODEX_SERVICE_TIER,
            "codex_service_tier",
        ),
        ENV_AGENT_CODEX_SERVICE_TIER,
    )
    if api_style == "codex_exec" and codex_service_tier is None:
        codex_service_tier = DEFAULT_CODEX_SERVICE_TIER
    codex_reasoning_effort = _normalize_optional_string(
        _select_raw_value(
            env_map,
            config_payload,
            ENV_AGENT_CODEX_REASONING_EFFORT,
            "codex_reasoning_effort",
        ),
        ENV_AGENT_CODEX_REASONING_EFFORT,
    )
    if api_style == "codex_exec" and codex_reasoning_effort is None:
        codex_reasoning_effort = DEFAULT_CODEX_REASONING_EFFORT

    return MemoryAgentConfig(
        enabled=parse_enabled_flag(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_ENABLED,
                "enabled",
            )
        ),
        base_url=_normalize_optional_string(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_BASE_URL,
                "base_url",
            ),
            ENV_AGENT_BASE_URL,
        ),
        api_key=_normalize_optional_string(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_API_KEY,
                "api_key",
            ),
            ENV_AGENT_API_KEY,
        ),
        model=model,
        api_style=api_style,
        disable_thinking=parse_bool_flag(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_DISABLE_THINKING,
                "disable_thinking",
            ),
            label=ENV_AGENT_DISABLE_THINKING,
            default=False,
        ),
        codex_binary=codex_binary,
        codex_profile=_normalize_optional_string(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_CODEX_PROFILE,
                "codex_profile",
            ),
            ENV_AGENT_CODEX_PROFILE,
        ),
        codex_service_tier=codex_service_tier,
        codex_reasoning_effort=codex_reasoning_effort,
        timeout_seconds=parse_timeout_seconds(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_TIMEOUT_SECONDS,
                "timeout_seconds",
            ),
            default=timeout_default,
        ),
        config_file=config_file,
        system_prompt_file=resolve_system_prompt_file(
            _select_raw_value(
                env_map,
                config_payload,
                ENV_AGENT_SYSTEM_PROMPT_FILE,
                "system_prompt_file",
            ),
            resolved_skill_dir,
            config_dir=config_file.parent,
        ),
        skill_dir=resolved_skill_dir,
    )


def load_system_prompt_text(config: MemoryAgentConfig) -> str:
    config.require_runtime_ready()
    raw_text = config.system_prompt_file.read_text(encoding="utf-8")
    match = _PROMPT_BLOCK_RE.search(raw_text)
    if match:
        prompt_text = match.group("body").strip()
    else:
        prompt_text = raw_text.strip()
    if not prompt_text:
        raise MemoryAgentConfigError(
            f"System prompt file is empty: {config.system_prompt_file}"
        )
    return prompt_text


def _normalize_optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise MemoryAgentConfigError(f"{label} must be a string.")
    normalized = value.strip()
    return normalized or None


def _select_raw_value(
    env_map: Mapping[str, str],
    config_payload: Mapping[str, Any],
    env_key: str,
    config_key: str,
) -> Any:
    if env_key in env_map:
        return env_map.get(env_key)
    return config_payload.get(config_key)
