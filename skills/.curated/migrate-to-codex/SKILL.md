---
name: migrate-to-codex
description: Migrate supported instruction files, skills, agents, and MCP config into Codex project and global files.
---

# Migrate to Codex

## Autonomy

Keep going until the selected migration is completely done: run the migrator, inspect the report, fix migrated Codex instructions/skills/agents/MCP config, and re-run checks without stopping to ask for confirmation of the next step. If the user has selected a target, do not ask before creating, editing, replacing, or deleting generated Codex artifacts in that target (`AGENTS.md`, `.codex/`, `.agents/`, or `~/.codex/`). Preserve unrelated existing Codex config entries in `.codex/config.toml` or `~/.codex/config.toml`, such as `notify`, `projects`, `marketplaces`, or unrelated MCP servers; do not ask about them unless they fail validation or directly conflict with the migration. Do not edit source Claude Code files (`.claude/`, `~/.claude/`, `.mcp.json`, or `.claude.json`), unrelated project code, secrets, or another repository.

## Migration Order

Run the migration in this order for each selected global or project source:

1. Start by using Codex's built-in TODO/task list tool. Do not create `MIGRATION_TODOS.md` or any TODO file unless the user explicitly asks. The TODO list input has a `plan` array whose items each have `step` and `status`; use statuses `pending`, `in_progress`, and `completed`. Make the TODOs specific to the selected artifacts. Before finishing, update the TODO list so every finished step is marked `completed` and no step remains `in_progress`. Use literal source → Codex target labels, for example:
   - Inspect `.claude/commands` → Codex skills/prompts
   - Inspect `.claude/agents` → `.codex/agents`
   - Inspect `.mcp.json` → `.codex/config.toml` MCP servers
   - Inspect `.claude/settings.json` hooks → `.codex/hooks.json`
   - Migrate safe selected artifacts → Codex files
   - Validate generated `.codex/config.toml`
   - Validate generated `.codex/agents`
   - Report migrated artifacts and manual-review items

2. Read `references/differences.md` (and refresh Codex docs if its `Docs last checked` date is old).

3. Scan and inspect before writing:
   - `--scan-only` lists active and inactive source surfaces.
   - `--plan` prints staged Codex artifact paths and report rows.
   - `--doctor` summarizes readiness, manual-review work, and validation risks.

4. Convert surfaces in the same order the CLI uses:
   - instructions: `CLAUDE.md` / `AGENTS.md` to `AGENTS.md`
   - plugins: report Claude plugin trees and marketplaces as manual migration work
   - hooks: rewrite supported Claude hooks into `.codex/hooks.json` and enable `[features].codex_hooks = true`
   - skills and commands: write Codex skills under `.agents/skills/`
   - config: write `.codex/config.toml` from Claude model/sandbox settings and MCP servers, including `personality = "friendly"` when config is generated
   - subagents: write Codex custom agents under `.codex/agents/`

5. Dry-run, then write the selected target. Use `--replace` only when orphan generated skills or agents should be deleted.

6. Inspect the terminal output and `.codex/migrate-to-codex-report.txt` after real runs.

7. Review generated artifacts in this order: `AGENTS.md`, `.agents/skills/`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/agents/`, then report-only plugin items.

8. Run `--validate-target` against each target after edits.

9. Re-run checks and `--dry-run` after edits.

10. Return the final migration report as one markdown table per scope that has rows. The tables cover only the non-native follow-up migration work you performed, such as skills created from slash commands, subagents, MCP servers, hooks, unsupported/local plugin notes, and manual-review caveats. Include programmatic native import rows for config, instructions, skills, or supported plugins only if you personally migrated them in this follow-up run.

    If only one scope has rows, render only the table with no heading. If multiple scopes have rows, render one heading before each table. Use `**User Config**` for user-scope rows. For project-scope rows, use the actual project folder name as the heading, for example `**northstar-support-portal**`; do not use `Current Project` as the heading. Do not add prose before or after the table output.

    Use exactly these columns:

    **northstar-support-portal**

    | Status | Item | Notes |
    | --- | --- | --- |
    | `Added` | `Slash command` pr-review | Converted into a Codex skill |
    | `Added` | `Subagent` release-lead | Added as a Codex subagent |
    | `Check before using` | `Hook` PreToolUse | Converted, but some Claude hook behavior differs in Codex |
    | `Not Added` | `Hook` Notification | Codex does not have an equivalent notification hook |
    | `Not Added` | `Plugin` team-macros | Plugin needs manual setup |

    `Status` must be `Added`, `Check before using`, or `Not Added`. Use `Added` when a Codex-facing artifact was created or changed and needs no special review. Use `Check before using` when a Codex-facing artifact was created or changed but the migration changed semantics, inferred behavior, preserved tool rules as guidance, or dropped unsupported behavior. Use `Not Added` when a source artifact was detected but no Codex-facing artifact was created. `Item` combines the artifact type and concrete item name in one cell. Artifact type must be singular: `Skill`, `Slash command`, `Subagent`, `MCP`, `Hook`, or `Plugin`. Wrap the artifact type in inline code; write the item name as plain text after it. `Notes` is always required; never leave it empty. Keep notes short, plain, and literal. Avoid internal implementation terms such as runtime expansion. Prefer phrases like `Converted into a Codex skill`, `Added as a Codex subagent`, `Added to Codex config`, `Converted into a Codex hook`, `Converted, but some Claude hook behavior differs in Codex`, `Codex does not have an equivalent notification hook`, `Plugin needs manual setup`, or `Plugin marketplace needs manual setup`.

## Self-Healing Loop

Keep looping until the selected migration is complete:

1. Run `--plan` or `--doctor`.
2. Run the migration with `--dry-run`.
3. Run the migration for real.
4. Fix every generated `## MANUAL MIGRATION REQUIRED` block and every `manual_fix_required` or `skipped` report row that can be resolved inside Codex artifacts.
5. Run `--validate-target`.
6. Re-run the migrator and validator until the report and validator have no actionable generated-artifact fixes left.

Do not edit source Claude Code files, unrelated project code, secrets, or another repository during this loop. If a report row requires source-provider changes or product judgment, leave the generated Codex artifact with clear manual guidance instead of changing the source.

## Commands

Choose the migrator command.

   ```bash
   MIGRATE_TO_CODEX='python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py'
   ```

Inspect the migration before writing.

   ```bash
   $MIGRATE_TO_CODEX --source ~/.claude/ --scan-only
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --plan
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --doctor
   ```

Dry-run, then run without `--dry-run`, for global and project.

   ```bash
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --dry-run
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/
   $MIGRATE_TO_CODEX --source ./.claude/ --target ./.codex/ --dry-run
   $MIGRATE_TO_CODEX --source ./.claude/ --target ./.codex/
   ```

Run the post-migration validator against each target after edits.

   ```bash
   $MIGRATE_TO_CODEX --validate-target ~/.codex/
   $MIGRATE_TO_CODEX --validate-target ./.codex/
   ```

Run `$MIGRATE_TO_CODEX --help` for flags (`--scan-only`, `--plan`, `--doctor`, `--validate-target`, defaults, and so on). Deep tables and more links are in `references/differences.md`.
