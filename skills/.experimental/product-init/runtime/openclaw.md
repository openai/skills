---
runtime: openclaw
skill: product-init
---

# Runtime Adapter — OpenClaw (+ Hermes)

## Path Resolution

Resolution order:
1. `$PRODUCT_INIT_SKILL_DIR` (env var override)
2. `~/.openclaw/skills/product-init/` (symlinked from `~/.claude/skills/product-init/`)
3. `~/.claude/skills/product-init/` (fallback)

```
VENV=$SKILL_DIR/.venv/bin/python
SCRIPTS=$SKILL_DIR/scripts/
```

## Builder Map

| Task Type       | Command |
|-----------------|---------|
| Backend/logic   | `openclaw agent dispatch --model mistral-large/mistral-large-instruct-2411 --task "<prompt>"` |
| Heavy reasoning | `openclaw agent dispatch --model openrouter/nousresearch/hermes-3-llama-3.1-405b --task "<prompt>"` |
| Codex-style     | `openclaw agent dispatch --model openai/gpt-5.4 --task "<prompt>"` |
| Fast/small      | `openclaw agent dispatch --model xiaomi/mimo-v2-flash --task "<prompt>"` |

## Sub-Skill Fallback

No `Skill` tool. Embed frontend-design discipline inline (same text as codex runtime).

## Model Context

- Primary: `claude-sonnet-4-6`
- Fallbacks: `hermes3` (`openrouter/nousresearch/hermes-3-llama-3.1-405b`), `kimi-k2.5`

## Install

Run once to link the shared skill into OpenClaw:

```bash
ln -sf ~/.claude/skills/product-init ~/.openclaw/skills/product-init
```
