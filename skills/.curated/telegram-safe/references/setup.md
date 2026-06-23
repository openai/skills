# Telegram Safe Setup

## Dependencies

Install runtime dependencies:

```bash
uv pip install telethon python-dotenv
```

Fallback:

```bash
python3 -m pip install telethon python-dotenv
```

## Environment variables

```env
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_SESSION_STRING=
```

## Session bootstrap

Use the bundled CLI to authenticate and export a session:

```bash
python scripts/tg.py auth login --json
```

The command returns a `session_string`; keep it in `TELEGRAM_SESSION_STRING` locally.

## Output contract

- `--json` produces machine-readable stdout
- stderr is reserved for errors and runtime logs
- resolve targets before any state-changing action

## Safety defaults

- Use numeric ids or exact usernames when titles are ambiguous.
- Keep history reads bounded.
- Use absolute or explicit output paths for downloads.
- Escalate to `telegram-admin` for destructive workflows.
