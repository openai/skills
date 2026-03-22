---
name: telegram-admin
description: Use when you need to perform destructive or high-risk Telegram operations through a bundled Telethon CLI with explicit preview and confirmation steps; covers delete, leave, remove-contact, and delete-draft workflows.
metadata:
  short-description: Destructive Telegram workflows with preview and confirm
---

# Telegram Admin

Use this skill when the user needs destructive or high-risk Telegram actions and mistakes are expensive.

## When to use

- deleting messages
- leaving chats or deleting dialogs
- removing contacts
- deleting drafts
- any bulk change where a wrong target is costly

## Skill paths

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export TG_ADMIN="$CODEX_HOME/skills/telegram-admin/scripts/tg.py"
```

## Dependencies

Install dependencies only if they are missing:

```bash
uv pip install telethon python-dotenv
```

Fallback:

```bash
python3 -m pip install telethon python-dotenv
```

## Environment

- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `TELEGRAM_SESSION_STRING`

If the session is missing, bootstrap it with:

```bash
python "$TG_ADMIN" auth login --json
```

## Required workflow

1. Validate the current session:
   `python "$TG_ADMIN" auth validate --json`
2. Resolve or inspect every target first.
3. Run a preview with `--dry-run` whenever the command supports it.
4. Only then perform the real action with `--yes`.
5. Keep `--json` enabled for all destructive commands.

## Commands

```bash
python "$TG_ADMIN" dialogs resolve --target <chat_or_user> --json
python "$TG_ADMIN" messages delete --chat <chat> --ids 123 124 --dry-run --json
python "$TG_ADMIN" messages delete --chat <chat> --ids 123 124 --yes --json
python "$TG_ADMIN" chats leave --target <chat> --dry-run --json
python "$TG_ADMIN" chats leave --target <chat> --yes --json
python "$TG_ADMIN" contacts remove --target <user> --dry-run --json
python "$TG_ADMIN" contacts remove --target <user> --yes --json
python "$TG_ADMIN" drafts delete --chat <chat> --dry-run --json
python "$TG_ADMIN" drafts delete --chat <chat> --yes --json
```

## Guardrails

- Never skip resolve or inspect.
- For bulk operations, show the target list and ids first.
- If similar names make a target ambiguous, switch to numeric ids.
- Do not replace `--dry-run` with reasoning; get a real CLI preview first.
- If the task is not destructive, prefer `telegram-safe`.

## References

- Setup and dependency guidance: `references/setup.md`
