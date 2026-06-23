# Memory-Agent Runtime Contract

This document defines the canonical runtime contract for the optional
`easy-memory` memory-management agent.

Despite the historical file name, this reference covers:
- OpenAI-compatible HTTP providers
- Ollama native chat providers
- Codex CLI exec as the preferred host-local provider inside Codex environments

## Scope

This contract applies to optional preprocessing during:
- `scripts/read_today_log.py`
- `scripts/search_memory.py`

When the memory-management agent is disabled, both scripts must preserve their
raw behavior.

## Runtime Boundary

`easy-memory` has two storage scopes:
- Shared skill implementation:
  - installed skill files such as `scripts/`, `references/`, `assets/`, and
    `agents/`
- Project-local memory data:
  - `./easy-memory` under the current working directory

The agent may read project-local memory content gathered by the scripts, but it
must not reinterpret the installation directory as the log storage directory.

## Enablement

The memory-management agent is optional.

Required script interface:
- `--task-context` is always required for `read_today_log.py` and
  `search_memory.py`
- when the agent is disabled, scripts must validate that `--task-context` is
  non-empty and then ignore it
- when the agent is enabled, scripts may pass `--task-context` and gathered
  memory blocks to the agent for filtering

## Configuration Placement

Canonical tracked files:
- `references/memory-agent-system-prompt.md`
- `references/openai-compatible-api.md`
- `references/response-schema.md`
- `references/script-output-schema.md`

Local runtime configuration only:
- local config file path
- API key when the provider requires authentication
- base URL
- model ID
- enablement toggle
- timeout policy
- installer-generated host adapter files

Secrets must not be stored in tracked repository files.

## Recommended Local Configuration Keys

Implementations should support:
- `EASY_MEMORY_AGENT_CONFIG_FILE`
- `EASY_MEMORY_AGENT_ENABLED`
- `EASY_MEMORY_AGENT_BASE_URL`
- `EASY_MEMORY_AGENT_API_KEY`
- `EASY_MEMORY_AGENT_MODEL`
- `EASY_MEMORY_AGENT_API_STYLE`
- `EASY_MEMORY_AGENT_DISABLE_THINKING`
- `EASY_MEMORY_AGENT_TIMEOUT_SECONDS`
- `EASY_MEMORY_AGENT_SYSTEM_PROMPT_FILE`
- `EASY_MEMORY_AGENT_CODEX_BINARY`
- `EASY_MEMORY_AGENT_CODEX_PROFILE`
- `EASY_MEMORY_AGENT_CODEX_SERVICE_TIER`
- `EASY_MEMORY_AGENT_CODEX_REASONING_EFFORT`

The default local config file path should be:
- `./easy-memory/agent-config.json`

Recommended precedence:
1. environment variables
2. local config file
3. built-in defaults

## Supported Provider Styles

`api_style` should describe the transport contract used by the runtime
implementation.

Supported values:
- `codex_exec`
- `openai_chat_completions`
- `ollama_native_chat`

### Preferred Codex CLI Exec Provider

Inside Codex environments, `codex_exec` is the preferred default.

Recommended local config:

```json
{
  "enabled": true,
  "api_style": "codex_exec",
  "model": "gpt-5.3-codex-spark",
  "codex_service_tier": "fast",
  "codex_reasoning_effort": "medium",
  "timeout_seconds": 120
}
```

Recommended defaults:
- model: `gpt-5.3-codex-spark`
- service tier: `fast`
- reasoning effort: `medium`
- timeout: `120` seconds

The runtime should invoke `codex exec` in a safe, non-interactive mode:
- read-only sandbox
- ephemeral session
- output written through `--output-last-message`
- no dependency on project-local HTTP credentials

### OpenAI-Compatible Chat Completions

Minimum HTTP compatibility target:
- method: `POST`
- path: `/chat/completions`
- authorization: optional `Bearer <api_key>` when the provider requires it
- content type: `application/json`

`base_url` should point to the API root, typically ending in `/v1`.
If the provider does not require authentication, `api_key` may be omitted or
set to an empty string.

### Optional Ollama Native Chat Extension

Ollama native mode uses:
- method: `POST`
- path: `/api/chat`
- authorization: optional `Bearer <api_key>` when a reverse proxy requires it
- content type: `application/json`

Recommended local config:

```json
{
  "enabled": true,
  "api_style": "ollama_native_chat",
  "base_url": "http://127.0.0.1:11434",
  "model": "qwen3.5:9b",
  "disable_thinking": true,
  "timeout_seconds": 20
}
```

When `disable_thinking` is `true`, the runtime should send Ollama native
`think: false`.

## Request Construction

The request should contain:
- one system prompt derived from
  `references/memory-agent-system-prompt.md` or a local override
- one user payload carrying the preprocessing payload as JSON text

The request payload should contain:
- `schema_version`
- `mode`
- `task_context`
- `cwd`
- `log_dir`
- `entries`

For `search_memory.py`, the payload should also contain:
- `keywords`
- `max_results`

The canonical request schema version for agent calls should be:
- `easy_memory_agent_request_v2`

Each entry object should include:
- `entry_id`
- `log_file` when available
- `ref_level`
- `factual`
- `content`
- `timestamp`
- `paths`
- `rendered_block`

Each `paths` item should include:
- `path_id`
- `resource_type`
- `path`
- `directory`

Each `paths` item may additionally include:
- `path_format`
- `system_hint`

Compatibility naming note:
- `paths` and `path_id` remain the canonical field names in request payloads
  for backward compatibility.
- Each item should nevertheless be interpreted as a related resource that may be
  either a local path or a URL/document address.
- For `resource_type:"local_path"`, `path_format:"project_relative"` means the
  `path` and `directory` values are relative to `cwd`, while
  `path_format:"absolute"` means they are absolute local filesystem values.
- `system_hint` is optional and is intended for external absolute local paths so
  cross-machine logs can be disambiguated quickly.

`rendered_block` is the exact block the agent should copy back if that entry
remains relevant.

## Agent Response Contract

The agent response is plain text, not strict JSON.

The canonical response contract is defined by:
- `references/response-schema.md`

In practice the response should be:

```text
<zero or more retained rendered_block values>

[SUMMARY] <summary no longer than 500 characters>
```

Runtime implementations should keep validation lightweight:
- strip one surrounding code fence when the entire response is fenced
- reject empty responses
- normalize the final summary line to `[SUMMARY] ...`
- avoid strict field-level or schema-level rejection

## Successful Script Output

When the memory-management agent succeeds, the scripts should print the filtered
plain-text result directly.

The canonical source of truth for that final script output contract is:
- `references/script-output-schema.md`

The canonical example file for this final script output should live at:
- `assets/examples/script-output.example.txt`

## Failure Behavior

If agent configuration is missing, invalid, or the agent-side runtime fails:
- the scripts must remain usable in non-agent mode
- raw log reading and raw search behavior must still be available
- the failure must not silently rewrite or delete memory content

This fallback rule applies to:
- network errors
- request timeouts
- provider protocol mismatches
- empty responses
- unexpected runtime exceptions in the agent-processing path

When fallback happens because of an agent-side failure or invalid response, the
implementation should append a diagnostic record containing the full available
response content to a runtime-generated error log under the installed skill
directory, not under the project-local `./easy-memory` directory.

## Source Of Truth Rule

The raw memory logs remain the source of truth.
The memory-management agent is only a filtering layer and must not become the
only way to access stored memory.
