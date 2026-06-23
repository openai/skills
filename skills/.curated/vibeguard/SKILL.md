---
name: "vibeguard"
description: "Use when working on any coding project to auto-snapshot before changes, check architecture rules after changes, analyze project health, and generate recovery plans for messy codebases. Provides both CLI commands and MCP tools."
---

# VibeGuard — Safety Net for Vibe Coding

Auto-snapshot your project before AI changes break things. Enforce architecture rules. Rescue messy codebases.

## Prerequisite Check

Before using VibeGuard, verify that `npx` and `git` are available:

```bash
command -v npx >/dev/null 2>&1 && command -v git >/dev/null 2>&1
```

If either is missing, ask the user to install Node.js (>= 20) and git.

## Setup

If the current project does not have a `vibeguard.yml` file, initialize it:

```bash
npx @jason_yang0316/vibeguard init
```

This will:
- Initialize git if needed
- Create `vibeguard.yml` with default config
- Create `AGENTS.md` with AI agent instructions
- Update `.gitignore`
- Take an initial snapshot

## Core Workflow

### Step 1: Snapshot Before Changes

Always create a snapshot before making significant code changes:

```bash
npx @jason_yang0316/vibeguard snapshot "before: refactoring auth module"
```

### Step 2: Make Changes

Proceed with the coding task.

### Step 3: Check Architecture Rules

After making changes, verify nothing is broken:

```bash
npx @jason_yang0316/vibeguard check
```

This runs 10 built-in rules:
- **no-circular-deps** — no circular import chains
- **no-cross-layer-imports** — UI must not import from DB layer
- **no-hardcoded-secrets** — no API keys or passwords in source
- **no-god-file** — no files over 300 lines
- **max-complexity** — no overly complex functions
- **no-deep-nesting** — max 4 levels of nesting
- **single-responsibility** — max 3 exports per file
- **consistent-naming** — uniform naming within directories
- **no-duplicate-logic** — no repeated code across files
- **dependency-direction** — dependencies flow one direction

### Step 4: If Something Went Wrong

```bash
npx @jason_yang0316/vibeguard rollback
```

Instantly restores the last snapshot. A safety snapshot of the current state is created first, so you can undo the rollback too.

## Health Analysis

When a project feels messy or the user asks about code quality:

```bash
npx @jason_yang0316/vibeguard analyze
```

Returns a score (0-100) and grade (A-F) across four dimensions:
- Complexity
- Duplication
- File organization
- Dependencies

To get a recovery plan:

```bash
npx @jason_yang0316/vibeguard rescue
```

Returns prioritized steps sorted by risk (quick wins first).

## Continuous Protection

For ongoing protection during a coding session:

```bash
npx @jason_yang0316/vibeguard watch --check
```

This auto-snapshots on every file change AND runs architecture rules after each snapshot.

## All Commands

| Command | Purpose |
|---------|---------|
| `init` | Initialize VibeGuard in a project |
| `watch` | Auto-snapshot on file changes (add `--check` for rules) |
| `snapshot [msg]` | Create a manual snapshot |
| `list` | List all snapshots |
| `diff [id]` | Show what changed |
| `rollback [id]` | Restore a previous snapshot |
| `check` | Run architecture rule checks |
| `rules` | List active rules and presets |
| `analyze` | Health score and grade |
| `rescue` | Step-by-step recovery plan |
| `dashboard` | Compact health overview |

All commands support `--json` for structured output.

Prefix all commands with: `npx @jason_yang0316/vibeguard`

## MCP Server

If the environment supports MCP, the MCP server provides the same functionality as tools:

```json
{
  "mcpServers": {
    "vibeguard": {
      "command": "npx",
      "args": ["vibeguard-mcp-server"]
    }
  }
}
```

MCP tools: `vibeguard_snapshot`, `vibeguard_rollback`, `vibeguard_diff`, `vibeguard_list_snapshots`, `vibeguard_check`, `vibeguard_rules`, `vibeguard_analyze`, `vibeguard_rescue`

## Source

- Repository: https://github.com/chenglin1112/vibeguard
- License: MIT
