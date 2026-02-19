---
name: auto-memory
description: Durable project-scoped long-term memory with automatic compaction handoff using markdown notes on disk and secret-safe env persistence. Use when continuity across sessions can change the answer, including prior decisions, "what did we decide", "continue", previous debugging notes, architecture conventions, runbooks, and known-good commands/paths. Supports save_memory/load_memory workflows, deduplication, hybrid keyword plus embedding retrieval, app-server compaction listeners, and post-compaction reinjection prompts.
---

# Auto Memory

## Overview

Persist project memory in `$CODEX_HOME/memory/<project>/` and retrieve it when prior context matters.
Store secret values only in `$CODEX_HOME/env/<project>/.env`; keep memory notes secret-safe by recording only variable names, redacted hints, and storage location.

## Setup

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export AUTO_MEMORY_DIR="$CODEX_HOME/skills/auto-memory"
export AUTO_MEMORY_PYTHON="${AUTO_MEMORY_PYTHON:-python3}"
```

Install required Python packages:

```bash
"$AUTO_MEMORY_PYTHON" -m pip install -r "$AUTO_MEMORY_DIR/requirements.txt"
```

Verify the dependency bootstrap:

```bash
"$AUTO_MEMORY_PYTHON" -c "import yaml; print('ok')"
```

## Operations

### `save_memory(project, title, body, tags?)`

- Required inputs: `project`, `title`, `body`
- Optional input: `tags` (comma-separated or repeatable tags)
- Run:
  - `python3 "$AUTO_MEMORY_DIR/scripts/save_memory.py" --project "<project>" --title "<title>" --body "<body>" --tags "tag1,tag2"`
- Behavior:
  - create or update a markdown note with YAML frontmatter (`title`, `date`, `project`, `tags`)
  - enforce required sections:
    - `Summary`
    - `Context`
    - `Decision`
    - `Rationale`
    - `Implementation`
    - `Verification`
    - `Follow-ups`
    - `Changelog`
  - upsert same-title notes
  - reconcile near-duplicate titles and mark older notes as superseded
  - append changelog entry on every save

### `load_memory(project, query, limit=8)`

- Required inputs: `project`, `query`
- Optional input: `limit` (default `8`)
- Run:
  - `python3 "$AUTO_MEMORY_DIR/scripts/load_memory.py" --project "<project>" --query "<query>" --limit 8`
- Retrieval flow:
  - run keyword search first (title/tags/headings/body weighting)
  - if keyword results are weak or too sparse, run embeddings fallback (`text-embedding-3-small`)
  - if embeddings are unavailable, degrade gracefully to keyword output and report why fallback was skipped
- Return per-result fields:
  - `filename`
  - `title`
  - `date`
  - `tags`
  - `highlights` (1-3)
  - `score`
  - `match_type` (`keyword` or `embedding`)

### Secret persistence helper

- Run:
  - `python3 "$AUTO_MEMORY_DIR/scripts/store_secret_env.py" --project "<project>" --var "SERVICE_API_TOKEN" --value "<secret>"`
- Store secrets only in `$CODEX_HOME/env/<project>/.env`.
- Never store secret values in markdown notes.

### `compaction_handoff(project, mode)`

- Run pre-compaction handoff:
  - `python3 "$AUTO_MEMORY_DIR/scripts/compaction_handoff.py" --project "<project>" --mode pre --objective "<objective>" --summary "<checkpoint summary>"`
- Run post-compaction reinjection:
  - `python3 "$AUTO_MEMORY_DIR/scripts/compaction_handoff.py" --project "<project>" --mode post --objective "<objective>"`
- Use returned `reinjection_prompt` as the first post-compaction context payload in the current session.
- Output also includes:
  - `reinjection_prompt_chars`
  - `reinjection_prompt_estimated_tokens`

### `app_server_compaction_listener(project)`

- Run listener against app-server protocol stream:
  - `python3 "$AUTO_MEMORY_DIR/scripts/app_server_compaction_listener.py" --project "<project>" --objective "<objective>" --inject-turn-start --output-framing jsonl`
- Detect events:
  - `thread/compact/start` for pre-compaction checkpoint
  - `thread/compacted` and `context_compacted` for post-compaction reinjection
- Trigger handoff:
  - run `compaction_handoff.py --mode pre` or `--mode post` on detected events
- Auto-inject:
  - when `--inject-turn-start` is set and a `threadId` is available, emit a ready-to-send `turn/start` JSON-RPC request carrying `reinjection_prompt`
- Reinjection guardrails:
  - `--reinjection-max-chars` sets max prompt size by character count (set `0` to disable)
  - `--reinjection-max-estimated-tokens` sets max prompt size by estimated token count (set `0` to disable)
  - `--oversize-action skip|truncate|allow` controls behavior when prompt exceeds limits (default `skip`)
  - compaction JSONL logs include `reinjection_status`, size metrics, and oversize reasons
- Optional auto-save mode:
  - set `--auto-save-events "turn/complete,turn/completed"` to persist structured event summaries through `save_memory.py`
  - auto-save can infer project from event payload with `--auto-save-project-field`, and can include selected payload fields in summaries with `--auto-save-summary-fields`
  - secret-like payloads are skipped automatically and logged as `skipped_secret`
- Optional compaction alert memory mode:
  - set `--save-compaction-alerts` to persist compaction failure/skip signals as memory notes
  - configure `--compaction-alert-title-prefix` and `--compaction-alert-tags` to tune note metadata
- Persist outputs:
  - use `--prompt-out` for latest reinjection prompt text
  - use `--jsonl-log` for audit/debug records of detected events and handoff actions
  - use `--visual-status` for concise human-readable compaction/reinjection runtime markers on stderr
  - visual status also emits short auto-save signals (persisted/skipped/error) and listener lifecycle markers

### One-command launcher

- Start with defaults:
  - `"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"`
- Default behavior:
  - `AUTO_MEMORY_MODE=compaction` by default
  - project defaults to sanitized current directory name (fallback `workspace`)
  - objective defaults to carry-forward compaction recovery text
  - emits `turn/start` reinjection requests automatically in compaction and both modes
- Override defaults with env vars:
  - `AUTO_MEMORY_PYTHON` (defaults to `python3`)
  - `AUTO_MEMORY_PROJECT`, `AUTO_MEMORY_OBJECTIVE`, `AUTO_MEMORY_LIMIT`
  - `AUTO_MEMORY_QUERY`, `AUTO_MEMORY_PROMPT_OUT`, `AUTO_MEMORY_LOG`
  - `AUTO_MEMORY_OUTPUT_FRAMING`, `AUTO_MEMORY_REQUEST_ID_PREFIX`, `AUTO_MEMORY_INPUT_FILE`, `AUTO_MEMORY_QUIET`
  - `AUTO_MEMORY_VISUAL_STATUS` (defaults to `1` in the launcher; set `0` to silence concise runtime status markers)
  - `AUTO_MEMORY_REINJECTION_MAX_CHARS`, `AUTO_MEMORY_REINJECTION_MAX_ESTIMATED_TOKENS`, `AUTO_MEMORY_OVERSIZE_ACTION`
  - `AUTO_MEMORY_MODE=compaction|autosave|both`
  - `AUTO_MEMORY_AUTO_SAVE_EVENTS`, `AUTO_MEMORY_AUTO_SAVE_TITLE_PREFIX`, `AUTO_MEMORY_AUTO_SAVE_TAGS`
  - `AUTO_MEMORY_AUTO_SAVE_PROJECT_FIELD`, `AUTO_MEMORY_AUTO_SAVE_SUMMARY_FIELDS`, `AUTO_MEMORY_INJECT_TURN_START`
  - `AUTO_MEMORY_SAVE_COMPACTION_ALERTS`, `AUTO_MEMORY_COMPACTION_ALERT_TITLE_PREFIX`, `AUTO_MEMORY_COMPACTION_ALERT_TAGS`

## Project Inference Priority

When project is not explicitly provided, choose project in this order:

1. Reuse active project already used in current session.
2. Infer from current repository/workspace root folder name.
3. If multiple plausible projects exist, ask exactly one disambiguation question with explicit options.
4. If nothing is inferable, ask for project name directly.

Do not guess when wrong-project risk is high.

## Retrieval and Save Policy

- Call `load_memory` before answering when continuity could affect output:
  - previous decisions
  - prior debugging/troubleshooting
  - architecture or operational conventions
  - runbook-like guidance
- Use hybrid retrieval strategy:
  - keyword first
  - embeddings fallback if keyword quality is weak
- Default `limit` to `8` unless the user explicitly asks for deeper recall.

Operate in aggressive save mode:

- Save stable decisions immediately.
- Save validated troubleshooting outcomes (symptom, root cause, fix, verification).
- Save conventions, interfaces, and known-good commands/paths.
- Save reusable checklists/runbooks and durable TODOs.
- Avoid saving raw transcripts, speculation, or transient chatter.

## Compaction Workflow

Use automatic compaction handoff through this skill:

1. When compaction is mentioned or likely, run `compaction_handoff.py --mode pre` before compaction.
2. Immediately after compaction, run `compaction_handoff.py --mode post`.
3. Inject the returned `reinjection_prompt` into the current session before continuing implementation.
4. If pre-compaction checkpoint is missing, run post mode anyway and ask the user for missing objective or unresolved decisions.

For custom app-server integrations, run `app_server_compaction_listener.py` continuously to watch compaction events and emit auto reinjection requests.
Codex currently has protocol-level compaction events but no direct user-configured pre/post hook in `$CODEX_HOME/config.toml`.

## Standalone and Integration

- Standalone first:
  - this skill works by itself using `save_memory.py`, `load_memory.py`, `compaction_handoff.py`, and listener scripts.
- Optional integration with `self-improve`:
  - use memory notes to persist iteration outcomes and acceptance decisions.
- Optional integration with `ralph-wiggum-loop`:
  - use auto-save and compaction handoff to preserve loop progress between sessions.
- Integration is additive, not required:
  - core memory save/load and compaction workflows must continue to work when other skills are absent.

## Secret Safety Rules

Never write secret values to markdown memory.

If a secret must persist:

1. save value in `$CODEX_HOME/env/<project>/.env`
2. reference only env var name and redacted hint in memory note
3. mention storage path without exposing value

Allowed note pattern example:
- `SERVICE_API_TOKEN stored in $CODEX_HOME/env/<project>/.env ([REDACTED])`

## Conflict and Dedup Handling

- If same title exists, update existing canonical note instead of creating duplicate.
- If multiple notes cover same topic, choose canonical note by most recent explicit date.
- Mark older notes superseded with pointer to canonical note.
- Keep canonical note current and append reconciliation details in changelog.

## References

- `references/note-template.md` for required note structure
- `references/secret-redaction-rules.md` for redaction and env-storage policy
- `references/compaction-handoff.md` for pre/post compaction command patterns
- `references/app-server-listener.md` for event listener setup and injection behavior

## Agent Team Protocol Memory Adapter (2026-02-19)

When used with `/Users/maleick/.codex/skills/agent-team-protocol`, store and retrieve memory with protocol tags to prevent bleed-over.

Required tags for protocol durability:
- `task_id:<TASK_ID>`
- `state:<STATE>`
- `owner_role:<ROLE>`
- `handoff_id:<HANDOFF_ID>`
- `project:<PROJECT_NAME>`

Reference: `references/agent-team-memory-tags.md`
