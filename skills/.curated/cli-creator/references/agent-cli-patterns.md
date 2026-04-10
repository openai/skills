# Codex CLI Patterns

Use this reference when designing the command surface for a new CLI Codex should run.

## Mental model

The CLI is Codex's command layer. It should turn a service, app, API, log source, or database into shell commands Codex can run repeatedly from any repo.

Good CLIs for Codex expose composable primitives. Avoid a single command that tries to "do the whole investigation" when smaller discover, read, resolve, download, inspect, draft, and upload commands would compose better.

## Help is interface

Write `--help` for a future Codex thread that only has the binary and a vague task. Each command should have a short description and flags with literal names from the product or API.

Good top-level help should answer:

- What containers can I discover?
- What exact objects can I read?
- What stable IDs can I resolve?
- What files can I download or upload?
- Which write actions exist?
- What is the raw escape hatch?

## Prefer this command shape

Use product nouns, then verbs:

```bash
tool-name --json doctor
tool-name --json accounts list
tool-name --json projects list
tool-name --json channels resolve --name codex
tool-name --json messages search "exact phrase"
tool-name --json messages context <message-id> --before 3 --after 3
tool-name --json logs download <build-url> --failed --out ./logs
tool-name --json media upload --file ./image.png
tool-name --json drafts create --body-file draft.json
```

For APIs whose native noun is already strong, direct verbs can be fine:

```bash
tool-name --json social-sets
tool-name --json drafts list --social-set <id>
tool-name --json request get /v2/me
```

The important rule is consistency. Do not mix many styles unless the product vocabulary demands it.

## Useful shapes from mature CLIs

Prefer these patterns over clever agent-only abstractions:

```bash
# Field-selected structured output: make common reads scriptable.
tool-name issues list --json number,title,url,state
tool-name issues list --json number,title --jq '.[] | select(.state == "open")'

# Human text by default, full API object when requested.
tool-name pods get <name>
tool-name pods get <name> -o json

# Product workflow commands, not just REST nouns.
tool-name logs tail
tool-name webhooks listen --forward-to localhost:4242/webhooks
tool-name webhooks trigger checkout.completed
```

Only implement filtering or templating if the user will actually need it. Stable JSON plus narrow read commands are the baseline.

## Discovery, resolve, read, context

Design first-pass commands in this order:

1. **Discover** broad containers: workspaces, accounts, social sets, repos, projects, channels, queues.
2. **Resolve** human input into IDs: user names, channel names, permalinks, PR URLs, build URLs, customer slugs.
3. **Read** an exact object: issue, event, thread, draft, customer, job, run, media item.
4. **Context** around an anchor when useful: nearby messages, parent thread, surrounding logs, audit history.

Do not force Codex to repeatedly search when it already has a stable ID.

## Text, JSON, files, exit codes

Support human text by default if it helps. Support `--json` everywhere Codex will parse or pipe results.

For `--json`:

- Emit JSON to stdout only.
- Send progress and diagnostics to stderr.
- Keep success and error shapes documented.
- Redact tokens, cookies, customer secrets, private headers, and unrelated payloads.

For downloads and exports:

- Write files under a user-provided `--out` path when possible.
- In JSON output, return the file path, byte count if cheap, source URL or ID, and follow-up command.

For exit codes:

- Exit zero when the command succeeded, including an empty result.
- Exit nonzero for auth failure, invalid input, network failure, parse failure, API error, or incomplete upload/download.
- Make `doctor --json` usable even when auth is missing. It should report missing auth rather than crashing.

## Pagination and breadth

Start shallow by default. Add explicit knobs for breadth:

```bash
tool-name --json messages search "topic" --limit 10
tool-name --json messages search "topic" --limit 50 --all-pages --max-pages 3
tool-name --json drafts list --limit 20 --offset 40
```

Return `next_cursor`, `next_url`, `offset`, `page_count`, or whatever is real for the provider.

## Raw escape hatch

The raw command is a repair hatch, not the main interface.

Good raw commands still use configured auth, base URL, JSON parsing, redaction, status/error handling, and `--json`.

Make reads easy:

```bash
tool-name --json request get /v2/me
```

Treat raw writes as live writes. Do not hide POST/PUT/PATCH/DELETE behind a "debug" command.

## Companion skill pattern

The companion skill should be smaller than the CLI README. It should teach the path through the tool:

```md
Start with:

tool-name --json doctor
tool-name --json accounts list

For [common job]:

tool-name --json ... 
tool-name --json ...

Rules:

- Prefer installed `tool-name` on PATH.
- Use --json when analyzing output.
- Create drafts by default.
- Do not publish/delete/retry/submit unless the user asked.
- Use `request get ...` only when high-level commands are missing.
```

Include JSON shape notes only when Codex needs them to choose the next command.
