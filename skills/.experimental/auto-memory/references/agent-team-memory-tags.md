# Agent Team Memory Tags

When storing durable notes for protocol tasks, include the following tags:
- `task_id:<TASK_ID>`
- `state:<STATE>`
- `owner_role:<ROLE>`
- `handoff_id:<HANDOFF_ID>`
- `project:<PROJECT_NAME>`

## Retrieval guidance
- Query with `task_id` and `project` first to avoid cross-task bleed-over.
- Prefer recent notes with matching state when assembling handoff context.
- Never store secret values in protocol notes.

## Save example

```bash
python3 "$AUTO_MEMORY_DIR/scripts/save_memory.py" \
  --project "clawhub-skill-audit-2026-02-19" \
  --title "protocol task TASK-001 handoff" \
  --body-file /tmp/protocol-note.md \
  --protocol-task-id "TASK-001" \
  --protocol-state "review" \
  --protocol-owner-role "Builder" \
  --protocol-handoff-id "HANDOFF-001" \
  --protocol-project "clawhub-skill-audit-2026-02-19"
```

## Build/query tags helper

```bash
python3 "$AUTO_MEMORY_DIR/scripts/protocol_tags.py" \
  --task-id "TASK-001" \
  --state "review" \
  --owner-role "Builder" \
  --handoff-id "HANDOFF-001" \
  --project "clawhub-skill-audit-2026-02-19"
```

## Retrieval example with deterministic filters

```bash
python3 "$AUTO_MEMORY_DIR/scripts/load_memory.py" \
  --project "clawhub-skill-audit-2026-02-19" \
  --query "handoff evidence blockers next action" \
  --require-tag "task_id:task-001" \
  --require-tag "project:clawhub-skill-audit-2026-02-19" \
  --limit 8
```
