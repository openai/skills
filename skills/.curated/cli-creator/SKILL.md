---
name: cli-creator
description: Build an agent-friendly CLI from API docs, an OpenAPI spec, existing curl examples, an SDK, a web app, an admin tool, or a local script. Use when the user wants Codex to create a global command-line tool that can be run from any repo, expose composable read/write commands, return stable JSON, manage auth, and pair with a companion skill.
---

# CLI Creator

Create a real CLI that future Codex threads can run by command name from any working directory.

This skill is for durable tools, not one-off scripts. If a short script in the current repo solves the task, write the script there instead.

## Start

Name the target tool, its source, and the first real jobs it should do:

- Source: API docs, OpenAPI JSON, SDK docs, curl examples, browser app, existing internal script, article, or working shell history.
- Jobs: literal reads/writes such as `list drafts`, `download failed job logs`, `search messages`, `upload media`, `read queue schedule`.
- Install name: a short binary name such as `typefully-cli`, `slack-cli`, `sentry-cli`, or `buildkite-logs`.

Prefer a new folder under `~/code/clis/<tool-name>` when the user wants a personal/global tool and has not named a repo.

## Choose the Runtime

- Prefer **Rust** for a global agent CLI: one fast binary, strong argument parsing, good JSON handling, easy copy/install into `~/.local/bin`.
- Prefer **TypeScript/Node** when the official SDK, auth helper, or browser automation ecosystem is the reason the CLI can be good.
- Prefer **Python** for data science, local file transforms, notebooks, or thin admin scripts that do not need a durable install.

State the choice in one sentence before scaffolding.

## Command Contract

Build toward this surface:

- `tool-name --help` shows every major capability.
- `tool-name --json doctor` verifies config, auth, version, endpoint reachability, and missing setup.
- `tool-name init ...` stores local config when env-only auth is painful.
- Discovery commands find accounts, projects, workspaces, teams, queues, channels, repos, dashboards, or other top-level containers.
- Read commands fetch exact objects and list/search collections.
- Write commands do one named action each: create, update, delete, upload, schedule, retry, comment, draft.
- `--json` returns stable machine-readable output.
- A raw escape hatch exists: `request`, `tool-call`, `api`, or the nearest honest name.

Do not expose only a generic `request` command. Give Codex high-level verbs for the repeated jobs.

## Auth and Config

Support the boring paths first:

1. `--api-key` or tool-specific token flag, when useful.
2. Environment variable such as `TYPEFULLY_API_KEY`.
3. User config under `~/.<tool-name>/config.toml` or another simple documented path.

Never print full tokens. `doctor --json` should say whether a token is available and what setup step is missing.

## Build Workflow

1. Read the source docs just enough to inventory resources, auth, pagination, IDs, media/file flows, rate limits, and dangerous write actions.
2. Sketch the command list in chat. Keep names short and shell-friendly.
3. Scaffold the CLI with a README or equivalent repo-facing instructions.
4. Implement `doctor`, discovery, read commands, one narrow write path if requested, and the raw escape hatch.
5. Install the CLI globally so `tool-name ...` works outside the source folder.
6. Smoke test from another repo, not only with `cargo run` or package-manager wrappers.
7. Run format, typecheck/build, unit tests for request builders, no-auth `doctor`, help output, and at least one live read-only API call when credentials exist.

If a live write is needed for confidence, ask first and make it reversible or draft-only.

## Rust Defaults

When building in Rust, use established crates instead of custom parsers:

- `clap` for commands and help
- `reqwest` for HTTP
- `serde` / `serde_json` for payloads
- `toml` for small config files
- `anyhow` for CLI-shaped error context

Add a `Makefile` target such as `make install-local` that builds release and installs the binary into `~/.local/bin`.

## Companion Skill

After the CLI works, create or update a small skill for it. The companion skill should explain:

- Which command to run first.
- How auth is configured.
- Which discovery command finds the common ID.
- The safe read path.
- The intended draft/write path.
- The raw escape hatch.
- What not to do without explicit user approval.

Keep API reference details in the CLI docs or a skill reference file. Keep the skill focused on ordering, safety, and examples future Codex threads should actually run.
