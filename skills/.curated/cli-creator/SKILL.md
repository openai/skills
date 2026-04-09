---
name: cli-creator
description: Build an agent-friendly CLI from API docs, an OpenAPI spec, existing curl examples, an SDK, a web app, an admin tool, or a local script. Use when the user wants Codex to create a global command-line tool that can be run from any repo, expose composable read/write commands, return stable JSON, manage auth, and pair with a companion skill.
---

# CLI Creator

Create a real CLI that future Codex threads can run by command name from any working directory.

This skill is for durable tools, not one-off scripts. If a short script in the current repo solves the task, write the script there instead.

If the user needs a connector inside one MCP-aware app, consider an MCP server. Build a CLI when the useful thing is a terminal command that Codex can run from any repo, pipe in shell scripts, smoke-test in CI, wrap in a skill, or call later from an MCP server.

## Start

Name the target tool, its source, and the first real jobs it should do:

- Source: API docs, OpenAPI JSON, SDK docs, curl examples, browser app, existing internal script, article, or working shell history.
- Jobs: literal reads/writes such as `list drafts`, `download failed job logs`, `search messages`, `upload media`, `read queue schedule`.
- Install name: a short binary name such as `typefully-cli`, `slack-cli`, `sentry-cli`, or `buildkite-logs`.

Prefer a new folder under `~/code/clis/<tool-name>` when the user wants a personal/global tool and has not named a repo.

Before scaffolding, check whether the proposed command already exists:

```bash
command -v <tool-name> || true
```

If it exists, choose a clearer install name or ask the user.

## Choose the Runtime

- Prefer **Rust** for a global agent CLI: one fast binary, strong argument parsing, good JSON handling, easy copy/install into `~/.local/bin`.
- Prefer **TypeScript/Node** when the official SDK, auth helper, or browser automation ecosystem is the reason the CLI can be good.
- Prefer **Python** for data science, local file transforms, notebooks, or thin admin scripts that do not need a durable install.

State the choice in one sentence before scaffolding.

## Command Contract

Sketch the command surface in chat before coding. Include the binary name, discovery commands, read commands, write commands, raw escape hatch, auth/config choice, and global install command.

When designing the command surface, read [references/agent-cli-patterns.md](references/agent-cli-patterns.md) for the expected agent-facing CLI shape.

Build toward this surface:

- `tool-name --help` shows every major capability.
- `tool-name --json doctor` verifies config, auth, version, endpoint reachability, and missing setup.
- `tool-name init ...` stores local config when env-only auth is painful.
- Discovery commands find accounts, projects, workspaces, teams, queues, channels, repos, dashboards, or other top-level containers.
- Read commands fetch exact objects and list/search collections. Paginated lists support a bounded `--limit`, cursor, offset, or clearly documented default.
- Write commands do one named action each: create, update, delete, upload, schedule, retry, comment, draft. They accept the narrowest stable resource ID and do not hide writes inside broad commands such as `fix`, `debug`, or `auto`.
- `--json` returns stable machine-readable output.
- A raw escape hatch exists: `request`, `tool-call`, `api`, or the nearest honest name.

Do not expose only a generic `request` command. Give Codex high-level verbs for the repeated jobs.

Document the JSON policy in the CLI README or equivalent: API pass-through versus CLI envelope, success shape, error shape, and one example for each command family. Under `--json`, errors must be machine-readable and must not contain credentials.

## Auth and Config

Support the boring paths first, in this precedence order:

1. `--api-key` or tool-specific token flag, when useful.
2. Environment variable such as `TYPEFULLY_API_KEY`.
3. User config under `~/.<tool-name>/config.toml` or another simple documented path.

Never print full tokens. `doctor --json` should say whether a token is available, the auth source category (`flag`, `env`, `config`, provider default, or missing), and what setup step is missing.

If the CLI can run without network or auth, make that explicit in `doctor --json`: report fixture/offline mode, whether fixture data was found, and whether auth is not required for that mode.

For internal web apps sourced from DevTools curls, create sanitized endpoint notes before implementing: resource name, method/path, required headers, auth mechanism, CSRF behavior, request body, response ID fields, pagination, errors, and one redacted sample response. Never commit copied cookies, bearer tokens, customer secrets, or full production payloads.

Use screenshots to infer workflow, UI vocabulary, fields, and confirmation points. Do not treat screenshots as API evidence unless they are paired with a network request, export, docs page, or fixture.

## Build Workflow

1. Read the source docs just enough to inventory resources, auth, pagination, IDs, media/file flows, rate limits, and dangerous write actions. If the docs expose OpenAPI, download or inspect it before naming commands.
2. Sketch the command list in chat. Keep names short and shell-friendly.
3. Scaffold the CLI with a README or equivalent repo-facing instructions.
4. Implement `doctor`, discovery, read commands, one narrow write path if requested, and the raw escape hatch.
5. Install the CLI globally so `tool-name ...` works outside the source folder.
6. Smoke test from another repo or `/tmp`, not only with `cargo run` or package-manager wrappers. Run `command -v <tool-name>`, `<tool-name> --help`, and `<tool-name> --json doctor`.
7. Run format, typecheck/build, unit tests for request builders, pagination/request-body builders, no-auth `doctor`, help output, and at least one fixture, dry-run, or live read-only API call.

If a live write is needed for confidence, ask first and make it reversible or draft-only.

For raw escape hatches, support read-only calls first. Do not run raw non-GET/HEAD requests against a live service unless the user asked for that specific write.

For media, artifact, or presigned upload flows, test each phase separately: create upload, transfer bytes, poll/read processing status, then attach or reference the resulting ID.

For fixture-backed prototypes, keep fixtures in a predictable project path and make the CLI locate them after installation. Smoke-test from `/tmp` to catch binaries that only work inside the source folder.

For log-oriented CLIs, keep deterministic snippet extraction separate from model interpretation. Prefer a command that emits filenames, line numbers or byte ranges, matched rules, and short excerpts.

## Rust Defaults

When building in Rust, use established crates instead of custom parsers:

- `clap` for commands and help
- `reqwest` for HTTP
- `serde` / `serde_json` for payloads
- `toml` for small config files
- `anyhow` for CLI-shaped error context

Add a `Makefile` target such as `make install-local` that builds release and installs the binary into `~/.local/bin`.

## Companion Skill

After the CLI works, create or update a small skill for it. Use `$CODEX_HOME/skills/<tool-name>/SKILL.md` for a personal/global companion skill unless the user names a repo-local `.codex/skills/...` path or another skill repo.

Write the companion skill in the order a future Codex thread should use the CLI, not as a tour of every feature. Explain:

- How to verify the installed command exists.
- Which command to run first.
- How auth is configured.
- Which discovery command finds the common ID.
- The safe read path.
- The intended draft/write path.
- The raw escape hatch.
- What not to do without explicit user approval.
- Three copy-pasteable command examples.

Keep API reference details in the CLI docs or a skill reference file. Keep the skill focused on ordering, safety, and examples future Codex threads should actually run.
