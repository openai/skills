# App-Server Listener

Use `scripts/app_server_compaction_listener.py` to watch app-server signals for:
- compaction handoff (`pre` + `post`)
- optional auto-save from turn/session completion events

## Setup

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export AUTO_MEMORY_DIR="$CODEX_HOME/skills/auto-memory"
```

## One-command launcher

Start listener with defaults:

```bash
"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"
```

Defaults:
- `AUTO_MEMORY_MODE=compaction`
- project: sanitized current directory name (fallback `workspace`)
- objective: carry-forward compaction recovery objective
- reinjection output: `$CODEX_HOME/tmp/auto-memory-reinjection.txt`
- action log: `$CODEX_HOME/tmp/auto-memory-listener.log`
- reinjection mode: emits `turn/start` JSON-RPC request payloads (compaction mode)
- reinjection guardrails: `AUTO_MEMORY_REINJECTION_MAX_CHARS=12000`, `AUTO_MEMORY_REINJECTION_MAX_ESTIMATED_TOKENS=3000`, `AUTO_MEMORY_OVERSIZE_ACTION=skip`
- optional visual status markers: `AUTO_MEMORY_VISUAL_STATUS=1`
- optional compaction alert memory notes: `AUTO_MEMORY_SAVE_COMPACTION_ALERTS=1`

Common overrides:

```bash
AUTO_MEMORY_PROJECT="workspace" \
AUTO_MEMORY_OBJECTIVE="Continue task execution after compaction." \
AUTO_MEMORY_QUERY="blockers next step" \
AUTO_MEMORY_OUTPUT_FRAMING="jsonl" \
AUTO_MEMORY_REINJECTION_MAX_CHARS="12000" \
AUTO_MEMORY_REINJECTION_MAX_ESTIMATED_TOKENS="3000" \
AUTO_MEMORY_OVERSIZE_ACTION="skip" \
"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"
```

Debug-friendly safe mode (no auto injection; keep logs/prompts for inspection):

```bash
AUTO_MEMORY_MODE="compaction" \
AUTO_MEMORY_QUIET="0" \
AUTO_MEMORY_VISUAL_STATUS="1" \
AUTO_MEMORY_SAVE_COMPACTION_ALERTS="1" \
AUTO_MEMORY_INJECT_TURN_START="0" \
AUTO_MEMORY_PROMPT_OUT="$CODEX_HOME/tmp/auto-memory-reinjection.txt" \
AUTO_MEMORY_LOG="$CODEX_HOME/tmp/auto-memory-listener.log" \
"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"
```

## Runtime modes

Compaction only (default):

```bash
AUTO_MEMORY_MODE="compaction" \
"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"
```

Auto-save only:

```bash
AUTO_MEMORY_MODE="autosave" \
AUTO_MEMORY_AUTO_SAVE_EVENTS="turn/complete,turn/completed" \
AUTO_MEMORY_AUTO_SAVE_SUMMARY_FIELDS="summary,objective,next_step,result,status" \
"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"
```

Both compaction and auto-save:

```bash
AUTO_MEMORY_MODE="both" \
AUTO_MEMORY_AUTO_SAVE_EVENTS="turn/complete,turn/completed" \
"$AUTO_MEMORY_DIR/scripts/start_auto_memory_listener.sh"
```

## What It Watches

- Request method: `thread/compact/start`
- Notification method: `thread/compacted`
- Event payloads containing `type: "context_compacted"`
- Configured completion methods from `--auto-save-events` (or `AUTO_MEMORY_AUTO_SAVE_EVENTS`)

## What It Does

1. Run `compaction_handoff.py --mode pre` when `thread/compact/start` appears.
2. Run `compaction_handoff.py --mode post` when compaction completes.
3. Optionally emit a `turn/start` JSON-RPC request with `reinjection_prompt`.
4. Optionally persist structured event memory notes through `save_memory.py` for configured completion events.
5. Optionally persist compaction failures/skips as memory notes when `--save-compaction-alerts` is enabled.
6. Skip auto-save when secret-like indicators are detected in generated note content.

## Basic Usage

Read a protocol stream from stdin and emit a `turn/start` request in JSONL framing:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/app_server_compaction_listener.py" \
  --project "<project>" \
  --objective "<objective>" \
  --inject-turn-start \
  --output-framing jsonl \
  --reinjection-max-chars 12000 \
  --reinjection-max-estimated-tokens 3000 \
  --oversize-action skip \
  --prompt-out "/tmp/auto-memory-reinjection.txt" \
  --jsonl-log "/tmp/auto-memory-listener.log"
```

Replay an existing event capture:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/app_server_compaction_listener.py" \
  --project "<project>" \
  --input-file "/path/to/events.jsonl" \
  --inject-turn-start
```

Enable direct auto-save with explicit event filters:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/app_server_compaction_listener.py" \
  --project "<project>" \
  --disable-compaction \
  --auto-save-events "turn/complete,turn/completed" \
  --auto-save-title-prefix "Auto memory" \
  --auto-save-tags "auto-memory,auto-save" \
  --auto-save-project-field "project" \
  --auto-save-summary-fields "summary,objective,next_step,result,status"
```

Enable compaction alert memory notes for failure/skip capture:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/app_server_compaction_listener.py" \
  --project "<project>" \
  --inject-turn-start \
  --save-compaction-alerts \
  --compaction-alert-title-prefix "Auto memory compaction" \
  --compaction-alert-tags "auto-memory,compaction,failure"
```

## Output Notes

- With `--inject-turn-start`, emitted payloads are valid JSON-RPC requests for method `turn/start`.
- Choose `--output-framing lsp` to emit `Content-Length` framed requests for LSP-style transports.
- `--prompt-out` stores the latest reinjection prompt so an external process can reuse it.
- `start_auto_memory_listener.sh` accepts passthrough listener flags after env defaults.
- Auto-save mode deduplicates repeated event IDs and logs action outcomes (`ok`, `error`, `skipped_secret`) in JSONL.
- Compaction log rows include reinjection metrics and control fields:
  - `reinjection_status`
  - `prompt_chars`, `prompt_tokens_estimated`
  - `prompt_sent_chars`, `prompt_sent_tokens_estimated`
  - `oversize_action`, `oversize_reason`
- With `--save-compaction-alerts`, listener also emits `action=compaction_alert` JSONL rows and persists memory notes for skipped/error outcomes.
- With `--visual-status`, stderr includes concise lifecycle markers such as:
  - `[auto-memory] pre checkpoint_saved file=...`
  - `[auto-memory] post reinjection_prompt_ready chars=... est_tokens=...`
  - `[auto-memory] post reinjection_emitted status=... sent_chars=...`

## Oversize Behavior

- `--oversize-action skip` (default): do not emit `turn/start` when reinjection exceeds configured budget; log `status=skipped_oversize`.
- `--oversize-action truncate`: truncate reinjection prompt to budget and emit when non-empty.
- `--oversize-action allow`: emit prompt even if over budget (for debugging only).
