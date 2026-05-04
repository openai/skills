---
runtime: codex
skill: product-init
---

# Runtime Adapter — Codex

## Path Resolution

Resolution order:
1. `$PRODUCT_INIT_SKILL_DIR` (env var override)
2. `~/.claude/skills/product-init/` (shared install fallback)

```
VENV=$SKILL_DIR/.venv/bin/python
SCRIPTS=$SKILL_DIR/scripts/
```

## Builder Map

No model selection available — Codex handles routing internally.

| Task Type | Command |
|-----------|---------|
| All tasks | `node "${CODEX_PLUGIN_ROOT}/scripts/codex-companion.mjs" task "<prompt>"` |

## Sub-Skill Fallback

No `Skill` tool available. Embed frontend-design discipline inline in every builder prompt:

> "Design with editorial typography, avoid generic AI-slop aesthetics, use real working
> code with exceptional attention to creative details. No hero gradients, no card-grid spam."

**filter_task**: `$VENV $SCRIPTS/filter_task.py <args>` — same Bash call as claude-code runtime.

## File Operations

Write files via `apply_patch` or direct file write. `Bash` is available.

## Limitations

- No parallel Agent calls — execute builders sequentially.
- No Skill tool — all sub-skill behavior embedded inline in prompts.
