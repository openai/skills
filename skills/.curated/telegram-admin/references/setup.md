# Telegram Admin Setup

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

Use the bundled CLI to authenticate:

```bash
python scripts/tg.py auth login --json
```

## Destructive workflow rules

- Validate the session first.
- Resolve the target first.
- Use `--dry-run` first where supported.
- Re-run with `--yes` only after verifying ids and target.
- Keep `--json` enabled so the result stays machine-readable.
