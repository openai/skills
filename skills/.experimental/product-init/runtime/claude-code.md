---
runtime: claude-code
skill: product-init
---

# Runtime Adapter — Claude Code

## Path Resolution

```
SKILL_DIR=~/.claude/skills/product-init
VENV=$SKILL_DIR/.venv/bin/python
SCRIPTS=$SKILL_DIR/scripts/
```

## Builder Map

| Task Type         | Agent Call |
|-------------------|-----------|
| Backend/API/logic | `Agent(subagent_type="mistral-large:mistral-large-rescue", prompt="...")` |
| Frontend/UI       | `Skill(skill="frontend-design:frontend-design")` → `Agent(subagent_type="general-purpose")` |
| Senior reasoning  | `Agent(subagent_type="codex:codex-rescue", prompt="...")` |
| Config/docs       | `Agent(subagent_type="alibaba:alibaba-rescue", prompt="...")` |
| Small fixes       | `Agent(subagent_type="general-purpose")` |

## Sub-Skill Invocation

- **frontend-design**: `Skill(skill="frontend-design:frontend-design")`
- **filter_task**: `Bash("$VENV $SCRIPTS/filter_task.py <args>")`

## File Operations

Write, Edit, Read, and Bash tools are natively available. No shims required.

## Auto-Trigger

Activated by `Skill` tool invocation or the `/product-init` slash command.
