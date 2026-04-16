---
name: "sentry"
description: "Use when the user asks to inspect Sentry issues or events, summarize recent production errors, or pull basic Sentry data via the Sentry CLI; perform queries using the `sentry` command."
---


# Sentry

## Canonical Reference

This is a quick-start guide. For the complete CLI documentation maintained by Sentry, fetch the upstream skill:

```bash
curl -sL https://raw.githubusercontent.com/getsentry/cli/main/plugins/sentry-cli/skills/sentry-cli/SKILL.md
```

Fetch the upstream when you need: release management, sourcemap uploads, dashboard widget configuration, or detailed command reference beyond what's covered here.

## Quick start

- If not already authenticated, ask the user to run `sentry auth login` or set `SENTRY_AUTH_TOKEN` as an env var.
- The CLI auto-detects org/project from DSNs in `.env` files, source code, config defaults, and directory names. Only specify `<org>/<project>` if auto-detection fails or picks the wrong target.
- Defaults: time range `24h`, environment `production`, limit 20.
- Always use `--json` when processing output programmatically. Use `--json --fields` to select specific fields and reduce output size.
- Use `sentry schema <resource>` to discover API endpoints quickly.

If the CLI is not installed, give the user these steps:
1. Install the Sentry CLI: `curl https://cli.sentry.dev/install -fsS | bash`
2. Or via npm: `npm install -g @sentry/cli`
3. Or zero-install: `npx -y @sentry/cli@latest <command>`
4. Authenticate: `sentry auth login`
5. Confirm authentication: `sentry auth status`
- Never ask the user to paste the full token in chat. Ask them to set it locally and confirm when ready.

## Core tasks (use Sentry CLI)

Use the `sentry` CLI for all queries. It handles authentication, org/project detection, pagination, and retries automatically. Use `--json` for machine-readable output.

### 1) List issues (ordered by most recent)

```bash
sentry issue list \
  --query "is:unresolved environment:production" \
  --period 24h \
  --limit 20 \
  --json --fields shortId,title,priority,level,status
```

If auto-detection doesn't resolve org/project, pass them explicitly:
```bash
sentry issue list {your-org}/{your-project} \
  --query "is:unresolved environment:production" \
  --period 24h \
  --limit 20 \
  --json
```

### 2) Resolve an issue short ID to issue detail

```bash
sentry issue view {ABC-123} --json
```

Use the short ID format (e.g., `ABC-123`), not the numeric ID.

### 3) Issue detail

```bash
sentry issue view {ABC-123}
```

### 4) Issue events

```bash
sentry issue events {ABC-123} --limit 20 --json
```

### 5) Event detail

```bash
sentry event view {your-org}/{your-project}/{event_id} --json
```

### 6) AI-powered root cause analysis

```bash
sentry issue explain {ABC-123}
```

### 7) AI-powered fix plan

```bash
sentry issue plan {ABC-123}
```

### 8) Explore traces and performance

```bash
sentry trace list --limit 5
sentry trace view <trace-id>
sentry span list <trace-id>
sentry trace logs <trace-id>
```

### 9) Inspect logs

```bash
sentry log list --limit 20
sentry log list --query "severity:error" --limit 20
sentry log list --follow    # Stream logs in real-time
```

## Large JSON handling

Sentry JSON can be very large. Do not paste raw `--json` output into context.

Use temp files and `jq`:

```bash
sentry trace view <trace-id> --json > /tmp/sentry-trace.json
jq '.spans[] | {op, description, duration}' /tmp/sentry-trace.json
```

Or use `--fields` to limit output:

```bash
sentry issue list --json --fields shortId,title,priority,level,status --limit 10
```

## Fallback: arbitrary API access

For endpoints not covered by dedicated CLI commands, use `sentry api`:
```bash
sentry api /api/0/organizations/{your-org}/ --method GET
```

Use `sentry schema` to discover available API endpoints:
```bash
sentry schema issues
```

## Inputs and defaults

- `org_slug`, `project_slug`: auto-detected by the CLI from DSNs, env vars, and directory names. Override with positional `{your-org}/{your-project}` if auto-detection fails.
- `time_range`: default `24h` (pass as `--period 24h`).
- `environment`: default `prod` (pass as part of `--query`, e.g., `environment:production`).
- `limit`: default 20 (pass as `--limit`).
- `search_query`: optional `--query` parameter, uses Sentry search syntax (e.g., `is:unresolved`, `assigned:me`).
- `issue_short_id`: use directly with `sentry issue view`.

## Output formatting rules

- Issue list: show title, short_id, status, first_seen, last_seen, count, environments, top_tags; order by most recent.
- Event detail: include culprit, timestamp, environment, release, url.
- If no results, state explicitly.
- Redact PII in output (emails, IPs). Do not print raw stack traces.
- Never echo auth tokens.

## Golden test inputs

- Org: `{your-org}`
- Project: `{your-project}`
- Issue short ID: `{ABC-123}`

Example prompt: "List the top 10 open issues for prod in the last 24h."
Expected: ordered list with titles, short IDs, counts, last seen.
