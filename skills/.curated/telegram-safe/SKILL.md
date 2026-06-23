---
name: telegram-safe
description: Use when you need to safely inspect or operate a Telegram account through a bundled Telethon CLI without destructive actions by default; covers session validation, dialog discovery, history reads, media download, sending, archive, mute, and draft workflows.
metadata:
  short-description: Safe Telegram account workflows in Codex
---

# Telegram Safe

Use this skill when the user needs Telegram account access for read-heavy or ordinary day-to-day actions and destructive changes are out of scope.

## When to use

- dialog discovery and entity inspection
- reading history, messages, and drafts
- downloading media
- ordinary message and file sending
- archive, unarchive, mute, unmute, and mark-read workflows
- session validation and `whoami`

## Skill paths

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export TG_SAFE="$CODEX_HOME/skills/telegram-safe/scripts/tg.py"
```

User-scoped skills install under `$CODEX_HOME/skills` by default.

## Dependencies

Install dependencies only if they are missing:

```bash
uv pip install telethon python-dotenv
```

If `uv` is unavailable:

```bash
python3 -m pip install telethon python-dotenv
```

## Environment

- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `TELEGRAM_SESSION_STRING`
- `TELEGRAM_USER_SESSION` is supported as a backward-compatible alias

If the session string is missing, run:

```bash
python "$TG_SAFE" auth login --json
```

Do not ask the user to paste credentials into chat. Ask them to set env vars locally and confirm when ready.

## Baseline workflow

1. Validate the current session before acting:
   `python "$TG_SAFE" auth validate --json`
2. Resolve or inspect the target before any mutate action:
   `python "$TG_SAFE" dialogs resolve --target <username_or_id> --json`
3. Prefer `--json` for agent workflows.
4. Keep history reads bounded with `--limit` unless the user explicitly asks for a deep scan.

## Core commands

```bash
python "$TG_SAFE" dialogs list --limit 50 --json
python "$TG_SAFE" dialogs inspect --target me --json
python "$TG_SAFE" messages list --chat me --limit 10 --json
python "$TG_SAFE" messages get --chat me --ids 123 124 --json
python "$TG_SAFE" messages send --chat me --text "hello" --json
python "$TG_SAFE" media inspect --chat me --message-id 123 --json
python "$TG_SAFE" media download --chat me --message-id 123 --output-dir /tmp/tg-downloads --json
python "$TG_SAFE" chats participants --target <chat> --limit 100 --json
python "$TG_SAFE" drafts list --json
python "$TG_SAFE" chats archive --targets me @example --json
python "$TG_SAFE" chats mute --target <chat> --hours 24 --json
```

## Guardrails

- Always resolve or inspect before mutate.
- For ambiguous chats, prefer numeric ids or exact usernames over fuzzy titles.
- Use explicit destination paths for upload or download flows.
- If an action changes state, state the target and expected effect before running it.
- Do not use this skill for `delete`, `leave`, `remove-contact`, or `delete-draft`; use `telegram-admin` instead.

## References

- Setup and dependency guidance: `references/setup.md`
