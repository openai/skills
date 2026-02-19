# Auto-memory Integration

This integration is optional. `self-improve` must run without `auto-memory`.

## Setup

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export AUTO_MEMORY_DIR="$CODEX_HOME/skills/auto-memory"
```

## Project Selection

- Prefer active session project.
- Else infer from repository folder name.
- Else ask once for project name.

## Load Before Iteration

```bash
python3 "$AUTO_MEMORY_DIR/scripts/load_memory.py" \
  --project "<project>" \
  --query "<objective> previous decisions regressions blockers" \
  --limit 8
```

## Save After Decision

```bash
python3 "$AUTO_MEMORY_DIR/scripts/save_memory.py" \
  --project "<project>" \
  --title "<repo>: self-improve iteration <id>" \
  --strict-sections \
  --body "<note>" \
  --tags "self-improve,decision,eval"
```

## Fallback When Auto-memory Is Missing

- Store iteration notes in `.self-improve/memory/<timestamp>-iteration.md`.
- Keep the same required sections used by auto-memory notes:
  `Summary`, `Context`, `Decision`, `Rationale`, `Implementation`, `Verification`, `Follow-ups`, `Changelog`.
- When auto-memory becomes available again, optionally migrate durable notes.

## Compaction Handoff

```bash
python3 "$AUTO_MEMORY_DIR/scripts/compaction_handoff.py" \
  --project "<project>" \
  --mode pre \
  --objective "<objective>" \
  --summary "<state and blockers>"
```

```bash
python3 "$AUTO_MEMORY_DIR/scripts/compaction_handoff.py" \
  --project "<project>" \
  --mode post \
  --objective "<objective>"
```

Use `reinjection_prompt` immediately after compaction before continuing.

## Secret Safety

- Never save secret values in memory markdown.
- Persist secrets only with `store_secret_env.py` (for example: `SERVICE_API_TOKEN`).
