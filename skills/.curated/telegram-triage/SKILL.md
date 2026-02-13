---
name: telegram-triage
description: "Read-only triage for Telegram chats from a local Telegram session (unread mentions, priority scoring, and action-ready summaries)."
---

# Telegram Triage

Use this skill when you need a read-only triage pass over Telegram chats from a
local Telegram session: prioritize unread/high-urgency threads and surface messages
that mention you or match keywords.

## Purpose and constraints

- Read-only: this skill does not send messages, edit settings, or join/leave chats.
- Local-first: authentication is stored locally in a Telegram `.session` file for this machine.
- Privacy: only run where you have explicit permission to access the account.

## Setup

1. Install dependencies:

```bash
cd <path-to-skill>
pip install -r requirements.txt
```

2. Create a session one time:

```bash
export TELEGRAM_API_ID=<your_api_id>
export TELEGRAM_API_HASH=<your_api_hash>
export TELEGRAM_SESSION_FILE=~/.telegram-triage/session
python3 <path-to-skill>/scripts/telegram-triage.py login --session-file "$TELEGRAM_SESSION_FILE"
```

You can store credentials in `~/.config/env/global.env` too:

```bash
TELEGRAM_API_ID=...
TELEGRAM_API_HASH=...
TELEGRAM_SESSION_FILE=~/.telegram-triage/session
```

3. Run triage:

```bash
python3 <path-to-skill>/scripts/telegram-triage.py triage --session-file "$TELEGRAM_SESSION_FILE"
```

## Commands

- `login`
  - `python3 scripts/telegram-triage.py login --session-file <path>`
  - Interactively signs in and stores/updates the session file.
- `triage`
  - `python3 scripts/telegram-triage.py triage --session-file <path>`
  - Reads unread/challenging conversations and prints a prioritized digest.
- `triage --json`
  - Emits machine-readable JSON output for automation.

## Useful flags

- `--chat-limit N` default: `40`
- `--message-limit N` default: `10`
- `--since <delta_or_iso>` examples: `30m`, `2h`, `1d`, `2026-02-01T00:00:00Z`
- `--keywords "urgent,invoice,refund"`
- `--include-read` include read chats when keyword filters match
- `--json` machine-readable output
- `--max-results N` default: `20`

## Example

```bash
python3 <path-to-skill>/scripts/telegram-triage.py triage \
  --session-file ~/.telegram-triage/session \
  --keywords "urgent,invoice,refund" \
  --since 12h \
  --json
```

## Notes

- If a session is unauthorized or expired, run `login` again.
- If you need this to run in automation, keep `--session-file` fixed and avoid
  re-authentication prompts.

