---
name: gmail-triage
description: "Read-only Gmail triage from your local account: fetch unread messages, prioritize by urgency/keyword patterns, and return a ranked action list for quick follow-up. Trigger when you need a short inbox triage pass."
---

# Gmail Triage

Use this skill to triage your Gmail inbox from a local IMAP session.

## Purpose

- Build a priority-ranked list of recent unread messages by urgency keywords.
- Flag action-oriented messages for quick follow-up.
- Keep output compact and machine-readable when needed.

## Scope and constraints

- Read-only by default.
- This is an IMAP client; it does not send mail, archive, delete, or label messages.
- Use `--mark-read` only when explicitly requested.

## Setup

1) Install Python dependencies (standard library only):

```bash
cd gmail-triage
# no third-party dependencies needed
```

2) Configure credentials:

```bash
export GMAIL_USERNAME="you@example.com"
export GMAIL_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```

3) Run triage:

```bash
python3 scripts/triage.py --max 30 --since-days 2
```

You can also keep these values in `~/.config/env/global.env`.

## Commands

- `python3 scripts/triage.py` - unread messages from last 24h (default)
- `python3 scripts/triage.py --format json` - JSON output for automation
- `python3 scripts/triage.py --query "FROM billing"` - add custom IMAP query terms
- `python3 scripts/triage.py --include-read` - include read mail
- `python3 scripts/triage.py --mark-read` - mark triaged emails as read (explicit)

## Output

Each item includes:
- `priority`: `high`, `medium`, `low`
- `score`: numeric urgency score
- `action_hint`: a short recommendation

Sorted by score then newest first.

## Reference

See `references/gmail-setup.md` for credential details and IMAP prep.
