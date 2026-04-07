---
name: "sentry"
description: "Use when the user asks to inspect Sentry issues or events, summarize recent production errors, or pull Sentry health data; uses the Sentry CLI for read-only queries with auto-detected org/project."
---


# Sentry (Read-only Observability)

## Quick start

- **Just run the command** — the CLI handles authentication and org/project detection automatically. Don't pre-authenticate or look up org/project before running commands.
- If auth is missing, the CLI prompts interactively. You can also run `sentry auth login` to authenticate.
- The CLI auto-detects org/project from DSNs in `.env` files, source code, config defaults, and directory names. Only specify `<org>/<project>` if auto-detection fails or picks the wrong target.
- Always use `--json` when processing output programmatically. Use `--json --fields` to select specific fields and reduce output size.

If the CLI is not installed, guide the user:
```bash
curl https://cli.sentry.dev/install -fsS | bash
```

If not authenticated:
```bash
sentry auth login
```
- Never ask the user to paste auth tokens in chat.

## Core tasks

### 1) List issues (ordered by most recent)

```bash
sentry issue list \
  --query "is:unresolved" \
  --limit 20 \
  --json --fields shortId,title,priority,level,status,count,firstSeen,lastSeen
```

Add `<org>/<project>` as a positional arg only if auto-detection doesn't work:
```bash
sentry issue list my-org/my-project --query "is:unresolved" --limit 20 --json
```

### 2) Resolve an issue short ID

```bash
sentry issue view PROJECT-123 --json
```

Use the short ID format (e.g., `ABC-123`), not the numeric ID.

### 3) Issue detail

```bash
sentry issue view PROJECT-123
```

For machine-readable output:
```bash
sentry issue view PROJECT-123 --json
```

### 4) Issue events

```bash
sentry issue events PROJECT-123 --limit 20 --json
```

### 5) Event detail

```bash
sentry event view my-org/my-project/EVENT_ID --json
```

### 6) AI-powered analysis

```bash
# Get AI root cause analysis
sentry issue explain PROJECT-123

# Get a fix plan
sentry issue plan PROJECT-123
```

### 7) Explore traces and performance

```bash
# List recent traces
sentry trace list --limit 5

# View a specific trace with span tree
sentry trace view TRACE_ID

# View spans for a trace
sentry span list TRACE_ID

# View logs associated with a trace
sentry trace logs TRACE_ID
```

### 8) Stream logs

```bash
# Stream logs in real-time
sentry log list --follow

# Filter logs by severity
sentry log list --query "severity:error"
```

### 9) Arbitrary API access (fallback)

For endpoints not covered by dedicated commands, use `sentry api`:
```bash
# GET request (default)
sentry api /api/0/organizations/my-org/

# POST request with data
sentry api /api/0/organizations/my-org/projects/ --method POST --data '{"name":"new-project","platform":"python"}'
```

Use `sentry schema` to discover API endpoints:
```bash
sentry schema issues
```

## Inputs and defaults

- `org_slug`, `project_slug`: auto-detected by the CLI. Override with positional `<org>/<project>` if needed.
- Time filtering: use `--period` (alias `-t`) e.g., `--period 24h`, `--period 7d`.
- `--limit`: cap number of results (defaults vary by command, typically 10–100).
- `--query`: uses Sentry search syntax (e.g., `is:unresolved`, `assigned:me`), not free text.

## Output formatting rules

- Issue list: show title, short_id, status, first_seen, last_seen, count, environments, top_tags; order by most recent.
- Event detail: include culprit, timestamp, environment, release, url.
- If no results, state explicitly.
- Redact PII in output (emails, IPs). Do not print raw stack traces.
- Never echo auth tokens.
- Use `-w`/`--web` to open resources in the browser when sharing links is useful.

## Common mistakes to avoid

- **Wrong issue ID format**: Use `PROJECT-123` (short ID), not the numeric ID.
- **Pre-authenticating unnecessarily**: Don't run `sentry auth login` before every command.
- **Missing `--json` for piping**: Human-readable output includes formatting. Use `--json` when parsing output.
- **Specifying org/project when not needed**: Let auto-detection work first.
- **Confusing `--query` syntax**: Uses Sentry search syntax, not free text.

## Golden test inputs

- Issue short ID: `{ABC-123}`

Example prompt: "List the top 10 open issues for prod in the last 24h."
Expected: ordered list with titles, short IDs, counts, last seen.
