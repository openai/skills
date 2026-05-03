---
name: agentfeeds
description: Use Agent Feeds for ambient awareness from continuously refreshed local streams under ~/.agentfeeds. Use at session start to install/check background refresh and insert a compact stream brief, and before web search or expensive source-specific queries when a prompt may be covered by changing local context such as RSS/news, GitHub, calendars, weather, local files, personal sources, templates, subscriptions, or subscribed stream state.
version: 0.1.1
author: verkyyi
license: MIT
metadata:
  hermes:
    tags: [Productivity, AI Agents, Personal Context, Local First]
---

# Agent Feeds

Agent Feeds is a local-first ambient context layer for agents. A background fetcher keeps changing stream state warm on disk so agents can answer from local, inspectable context before re-searching, querying, processing, or asking the user to repeat information.

Use this skill at session start, when managing feeds/subscriptions/templates, and before web search or expensive source-specific work if subscribed local state may already cover the prompt.

Requires shell access, Python 3.11+, and either `pip` or `uv` for setup. Background polling is supported on macOS, Linux, FreeBSD, and WSL-style POSIX environments. The bundle includes a frozen template catalog for first use; network access is needed for setup, remote catalog updates, and public feed refreshes.

## Command Map

Use the bundled scripts from the skill root:

```bash
python3 scripts/setup.py
python3 scripts/agentfeeds.py brief
python3 scripts/agentfeeds.py search <topic> --json
python3 scripts/agentfeeds.py streams health --json
python3 scripts/agentfeeds.py streams read <subscription-id> --limit 20 --json
python3 scripts/agentfeeds.py streams find <query> --json
python3 scripts/agentfeeds.py templates find <query>
python3 scripts/agentfeeds.py subscribe <template-id> [key=value ...] --dry-run --json
python3 scripts/agentfeeds.py subscribe <template-id> [key=value ...]
python3 scripts/agentfeeds.py refresh --stream <subscription-id>
```

`python3 scripts/agentfeeds.py` is the agent-facing CLI. `python3 scripts/agentfeeds_fetch.py` is an internal refresh worker used by polling and wrappers; prefer `agentfeeds.py refresh` in agent instructions. Runtime state defaults to `~/.agentfeeds/`; treat the file layout as an implementation detail except when debugging or editing a scaffolded local template.

Vocabulary:

- Template: reusable feed definition. Some templates are ready to subscribe with no parameters; others require parameters.
- Subscription: configured active instance of a template.
- Stream: refreshed readable data for an active subscription.

References to load only when needed:

- Runtime setup details: `references/runtime-setup.md`
- Template authoring details: `references/template-authoring.md`
- Background refresh details: `references/background-refresh.md`
- macOS personal source setup: `references/macos-personal-sources.md`

Built-in templates come from the standalone catalog repo `https://github.com/verkyyi/agentfeeds-catalog` and are cached locally; user-local templates live under `~/.agentfeeds/templates/`.
The release bundle includes a frozen built-in catalog fallback so first-run discovery does not depend on GitHub being reachable.

## Session Start

At the start of each session:

1. If the bundled CLI fails because dependencies are missing, run `python3 scripts/setup.py`.
2. Check background refresh with `python3 scripts/agentfeeds.py admin polling status --json`; if missing, run `python3 scripts/agentfeeds.py admin polling install`.
3. Check stream health with `python3 scripts/agentfeeds.py streams health --json`.
4. Generate stable compact context with `python3 scripts/agentfeeds.py brief`.
5. If the host supports prompt slots, place the exact brief output in a system-level or persistent context slot so stable stream metadata can benefit from model-side prompt caching.

The default brief avoids volatile timestamps. Use `python3 scripts/agentfeeds.py brief --include-freshness` only for freshness/debugging questions.

If health reports errors, missing state, or stale state, continue with available local context but tell the user ambient awareness is degraded when it affects the answer.

## Answering Flow

When a user prompt may be covered by subscribed changing context:

1. Search local state first: `python3 scripts/agentfeeds.py search <topic> --json`.
2. If matches are non-stale and answer the prompt, read the matching stream with `python3 scripts/agentfeeds.py streams read <subscription-id> --limit 20 --json` and answer from local state.
3. Refresh on demand only when the user asks about current/time-bounded data, the stream is older than 2x its poll interval, or the user explicitly asks to refresh. Use `python3 scripts/agentfeeds.py refresh --stream <subscription-id>`, then search/read again.
4. If health shows a fetch error or missing state, explain the degraded source and ask for reconfiguration only when needed.
5. Use web search or source-specific external tools only when local streams do not cover the prompt, are stale and cannot refresh, or the user explicitly asks for outside/current web information beyond subscribed data.

Use `streams find` only for stream metadata discovery. Use top-level `search` for content snippets.

## Subscribe And Manage

When the user asks to subscribe to a source:

1. Search built-ins first with `python3 scripts/agentfeeds.py templates find <query>`.
2. Inspect likely matches with `python3 scripts/agentfeeds.py templates show <template-id> --json`.
3. Prefer a built-in template when it fits the source shape and auth model.
4. Collect only required parameters, preview with `python3 scripts/agentfeeds.py subscribe <template-id> [key=value ...] --dry-run --json`, then subscribe with `python3 scripts/agentfeeds.py subscribe <template-id> [key=value ...]`.
5. Confirm with `python3 scripts/agentfeeds.py streams health --json` and, if useful, one stream read.

Default to answering first. Subscribe only when the user explicitly asks to subscribe, asks about a recurring topic, or a follow-up would clearly benefit from warm local state. If the user names a category rather than a source, list candidate templates and ask which source they mean.

For unsubscribe:

```bash
python3 scripts/agentfeeds.py streams list
python3 scripts/agentfeeds.py unsubscribe <subscription-id>
```

If the user names a template instead of a concrete subscription, list matching active streams and ask which one to remove.

## Template Strategy

Balance built-in templates and local authoring this way:

- Use built-in templates for common source classes, stable public APIs, shared schemas, and anything many operators would reuse.
- Use parameterized built-ins for source families: RSS/Atom URLs, GitHub repos, iCalendar URLs, weather coordinates, public JSON APIs.
- Use local templates for private files, private dashboards, one-off APIs, local tools, experimental sources, and operator-specific commands.
- Do not author a local template until built-ins have been checked and no suitable template fits.
- If a local template proves broadly useful, suggest upstreaming it to the catalog rather than keeping many near-duplicate local templates.
- Prefer local/private read-only sources before suggesting public feeds when the user wants personal context.

When no built-in template fits:

```bash
python3 scripts/agentfeeds.py admin templates adapters
python3 scripts/agentfeeds.py admin templates scaffold <adapter-kind> <template-id>
python3 scripts/agentfeeds.py admin templates validate
python3 scripts/agentfeeds.py admin templates test <template-id> key=value
```

Read `references/template-authoring.md` before editing scaffolded template YAML.

For `local_command` templates, use argv arrays only. Only create command templates for explicitly requested or approved read-only commands. Avoid commands that mutate files, cloud resources, accounts, or external services. New `local_command` templates are pending and cannot run until approved by the operator.

After scaffolding or installing a `local_command` template, tell the user to run `python3 scripts/agentfeeds.py admin templates approve-command <template-id> [key=value ...]` themselves in an interactive terminal. Do not approve on the user's behalf, even if asked. Explain that approval is tied to the exact template and command digest, and edits revoke it.

For macOS personal context, install local templates with:

```bash
python3 scripts/agentfeeds.py admin macos install-templates
```

This installs pending read-only templates for Calendar, Reminders, and Mail. The operator must approve each one before subscribing or refreshing.

## Safety Rules

- Use `subscribe` and `unsubscribe` for subscription changes.
- Use `agentfeeds.py refresh` for refreshes.
- Do not hand-write state or status files.
- Do not include secret values in template YAML. Use `{{secret:name}}` references and tell the user to set values with `python3 scripts/agentfeeds.py admin secrets set <name>`.
- Treat Agent Feeds as warm changing context, not durable memory, semantic search, or a data warehouse.
