---
name: fax-machine
description: Send outbound faxes from text or PDF files with a bundled CLI. Use when the user wants to render text to PDF, stamp text onto an existing PDF, send a fax via Phaxio, or check fax delivery status.
---

# Fax Machine

## What this skill does
- Render plain text into a simple PDF.
- Stamp text onto the first page of an existing PDF.
- Send outbound faxes through Phaxio.
- Check delivery status and fetch the transmitted PDF.

## Prerequisites
- `PHAXIO_API_KEY`
- `PHAXIO_API_SECRET`
- Python 3 with `requests` and `pypdf`

## How to think about auth
- Default to environment variables for local CLI use so secrets do not land in command history, repo files, or skill docs.
- Treat fax providers as account-scoped senders: auth proves which account is sending, while the destination number and PDF are per-request data.
- Prefer API key + secret providers for v1 automation because they work cleanly in headless CLI flows.
- Prefer OAuth or JWT only when the provider requires user delegation, org policy, or scoped multi-user access.
- Never ask the user to paste raw secrets into chat. Ask them to export env vars locally and rerun the command.
- If auth fails, verify missing env vars first, then invalid credentials, then provider account permissions or sender-number restrictions.

## Quick start

Render text to a PDF:

```bash
python skills/.experimental/fax-machine/scripts/fax_cli.py render --text "hello from codex" --out /tmp/fax.pdf
```

Stamp text onto an existing PDF:

```bash
python skills/.experimental/fax-machine/scripts/fax_cli.py overlay --pdf /tmp/input.pdf --text "Approved" --x 72 --y 720 --out /tmp/stamped.pdf
```

Send a fax:

```bash
python skills/.experimental/fax-machine/scripts/fax_cli.py send --to +14155551212 --pdf /tmp/fax.pdf --wait
```

Check status:

```bash
python skills/.experimental/fax-machine/scripts/fax_cli.py status <fax-id> --json
```

Fetch the transmitted PDF:

```bash
python skills/.experimental/fax-machine/scripts/fax_cli.py fetch <fax-id> --out /tmp/sent.pdf
```

## Workflow
1. If the user provides text only, run `render` first.
2. If the user needs text added to an existing document, run `overlay`.
3. Run `send` with the destination number in E.164 format.
4. Use `--wait` for synchronous polling, or `status` for a later check.
5. Use `fetch` when the user needs the final transmitted artifact.

## References
- `references/phaxio.md` for provider auth, endpoints, and response shape.

## Guardrails
- Outbound-only in v1.
- Do not claim HIPAA or compliance guarantees from this skill alone.
- Prefer local PDF generation before upload so the sent artifact is inspectable.
