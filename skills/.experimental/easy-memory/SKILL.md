---
name: easy-memory
description: Project-local memory logging for history/notes stored as YYYY-MM-DD.log files in ./easy-memory relative to the current working directory. Use when you must read today's memory, search memory by keywords (English preferred), append structured log entries with IDs (English preferred; UTF-8 accepted), or update/delete entries by ID. Logs always go to the working directory even if the skill is installed globally.
---

# Easy Memory

## Overview

Maintain project-local memory logs inside the ./easy-memory directory under the current working directory. Each day uses one log file named `YYYY-MM-DD.log`.

## Installation And Environment Adapters

The canonical source package for this skill must stay compatible with the upstream `openai/skills` repository layout:
- `SKILL.md`
- `agents/openai.yaml`
- `scripts/`
- `references/`
- `assets/`

Do not make Codex-specific, Claude Code-specific, or other host-specific directories a required part of the canonical source tree for this skill.

If an automated installer detects a host environment such as Codex or Claude Code, it may generate or supplement local adapter files and directories during installation so long as:
- the canonical source package remains upstream-compatible,
- generated host-specific files are treated as installer-managed local artifacts rather than source-of-truth skill content,
- secrets and user-specific runtime settings remain outside the tracked skill package.

Read `references/installer-environments.md` before adding installer-specific behavior or host-specific adapter files.

## Initialization (must follow)

Run initialization once per project before any other scripts when:
- `./easy-memory` does not exist, or
- `./easy-memory/init.log` is missing.

Run:

```
python3 scripts/init_memory.py
```

Initialization behavior:
- Create `./easy-memory` if needed.
- Locate `AGENTS.MD` in the project root (current working directory). If missing, create it.
- If `AGENTS.MD` exists, append a rules block to the end:
  ```
  ## easy-memory rules
  - At the start of the current session (before the first task), use the `easy-memory` skill and follow all rules and constraints in its `SKILL.md`.
  - Only re-run memory read/search when necessary for the task.
  ```
- Create `./easy-memory/init.log` containing the same rules block and a `Date: YYYY-MM-DD` line at the end.
- If `init.log` already exists, initialization is skipped and `AGENTS.MD` is not modified.

If you need the absolute usage path for easy-memory scripts, use the directory
containing this `SKILL.md` (the `scripts/` folder sits alongside it). Avoid
persisting absolute paths in project `AGENTS.MD` because different environments
may maintain the same project.

All other scripts require `init.log` to exist and will exit if initialization has not been run.

## Mandatory workflow (must follow)

1. At the start of the current session (before the first task), run `scripts/read_today_log.py` to load the full log for today.
2. At the start of the current session (before the first task), run `scripts/search_memory.py` with English-preferred keywords for the session/task. Only repeat steps 1-2 when necessary for the task. Choose `--max-results` based on task complexity (this is the memory search depth).
3. Before finishing or submitting any task, append a new entry with `scripts/write_memory.py` following the log rules below. When the task is tied to concrete files, pages, or documents, also store project-relative local paths when the targets are inside the current working directory, and store absolute local paths only when the targets are outside the project; highly related URLs/document addresses may also be stored so they can be reopened quickly.
4. Log entries should be written in English when possible; UTF-8 is accepted.
5. `read_today_log.py` and `search_memory.py` must receive a required `--task-context` argument containing the user's question and problem context. Unless a dedicated memory-management agent is enabled, this argument is reserved for future preprocessing and must not alter the default read/search results.

## Remote repository alignment gate (must follow)

Condition precedent. Prior to executing `scripts/write_memory.py`, the agent shall determine, with reasonable diligence, whether any Remote Alignment Operation is expected to occur after the time of writing within the same task or session.

For purposes of this skill, a "Remote Alignment Operation" means any action that publishes, synchronizes, or otherwise updates a remote code repository or mirror, including but not limited to `git push`, `svn commit`, `hg push`, and any API- or UI-based upload of code changes to Git-, SVN-, or similar systems.

If a Remote Alignment Operation is expected or cannot be reasonably ruled out, the agent shall, before initiating any Repository-Change Operation, write memory in accordance with this skill and shall not perform any Repository-Change Operation until the memory entry has been written.

For purposes of this skill, a "Repository-Change Operation" includes any action that modifies tracked files or repository history, including edits to tracked files, staging, commits, amend/merge/rebase/cherry-pick, and related history-rewriting actions.

For avoidance of doubt, if no Remote Alignment Operation is expected after the time of writing and this can be reasonably confirmed, the agent may proceed with the ordinary timing for memory writing, subject to the Mandatory workflow above.

## Log entry format

Each entry is a single line and must end with a timestamp:

```
[ID:<unique-id>] [REF:<ref-level>] [FACT:<true|false>] <content> [PATHS:<json-array>] [TIME:YYYY-MM-DD:HH:MM]
```

Rules:
- Log file name must be `YYYY-MM-DD.log` and use the current date only.
- If today's log file does not exist, create it; otherwise append to the end.
- Entries should be written in English when possible; UTF-8 is accepted.
- The timestamp must be the final token of the line and must be accurate to minutes.
- Each entry must include a unique ID, a reference level, and a factual flag.
- `PATHS` is optional. When present, it must be a JSON array of objects like `{"id":"<path-id>","path":"<project-relative-path-or-absolute-path-or-url>","directory":"<project-relative-directory-or-absolute-directory-or-container-url>","resource_type":"<local_path|url>"}`.
- Every stored related reference must use a unique related resource ID.
- For `resource_type:"local_path"` inside the current working directory, `path` must be stored as a project-relative path, `directory` must be the corresponding project-relative parent directory (or `.` when the parent is the project root), and `path_format` must be `project_relative`.
- For `resource_type:"local_path"` outside the current working directory, `path` must be an absolute local path, `directory` must be the absolute parent directory (or the directory itself if the stored target is a directory), `path_format` must be `absolute`, and `system_hint` should record a brief host hint such as OS, CPU architecture, and short hostname.
- For `resource_type:"url"`, `path` must be a URL/document address and `directory` must be the derived parent/container URL so the agent can reopen related locations quickly.

Compatibility naming note:
- `PATHS` remains the historical field name in the on-disk log format for backward compatibility.
- `path_id` remains the historical field name inside each stored object, but it should now be interpreted as the unique ID of a related resource, not only a local filesystem path.
- `--related-path`, `--path-update`, and `--path-clear` also retain their historical names for CLI compatibility, even though the stored target may now be either a local path or a URL/document address.
- See `references/compatibility-notes.md` for the consolidated compatibility explanation.

## Scripts

### Initialize memory

```
python3 scripts/init_memory.py
```

Runs one-time initialization to create `AGENTS.MD` rules and `./easy-memory/init.log`.

### Read today's log

```
python3 scripts/read_today_log.py --task-context "User question and problem context"
```

Reads the full log for the current date.
When an entry includes `PATHS` metadata, the output must also return the related resource IDs, related references, resource types, and container values in a readable form.
Older entries without `PATHS` metadata must remain readable without errors.
`--task-context` is required.
- When the memory-management agent is not enabled, the script should only validate that it is non-empty and then ignore it.
- When the memory-management agent is enabled and returns a valid response, the script may return only the retained task-relevant memory blocks in their original format, followed by a final `[SUMMARY]` line.
- If the agent fails or returns unusable output, the script must fall back to the raw log output.

### Search memory

```
python3 scripts/search_memory.py <keyword1> <keyword2> --max-results 5 --task-context "User question and problem context"
```

Searches all `.log` files in the ./easy-memory directory under the current working directory. Keywords should be English; UTF-8 is accepted. Default `--max-results` is 5.
Results are prioritized in this order:
- Factual entries (`FACT:true`) first
- Higher reference level first (`REF:critical` > `high` > `medium` > `low`, or higher numeric values)
- Newer timestamps first
When a matched entry includes `PATHS` metadata, the output must also return the related resource IDs, related references, resource types, and container values in a readable form.
Older entries without `PATHS` metadata must remain searchable without errors.
`--task-context` is required.
- When the memory-management agent is not enabled, the script should only validate that it is non-empty and then ignore it.
- When the memory-management agent is enabled and returns a valid response, the script may return only the retained task-relevant search blocks in their original format, followed by a final `[SUMMARY]` line.
- If the agent fails or returns unusable output, the script must fall back to the raw search output.

### Write memory

```
python3 scripts/write_memory.py --content "..." --factual true --ref-level medium --related-path skills/.experimental/easy-memory/scripts/write_memory.py --related-path /opt/shared/specs/memory-agent.md --related-path https://example.com/docs/memory-agent
```

Appends a new entry to today's log. Content should be English and single-line; UTF-8 is accepted. The script generates the unique ID and timestamp.

Write-memory instructions:
- Use `--related-path` for the current file, related directory, or any highly related URL/document address that should be reopened quickly later. Pass the option multiple times for multiple references.
- Every `--related-path` value must be either a project-local path, an external absolute local path, or a supported URL/document address.
- The script stores project-local targets as project-relative paths. It stores external local targets as absolute paths with `path_format:"absolute"` plus a brief `system_hint`.
- The script stores each related reference with its own unique related resource ID, resource type, derived container string, and any needed path-format metadata.
- If no file, page, or document is materially related to the memory entry, you may omit `--related-path`.

### Update memory

```
python3 scripts/update_memory.py --id <entry-id> --content "..." --ref-level high --factual false
```

Updates the entry matching the ID across all logs. The timestamp is refreshed to the current time.

Use update when:
- New factual findings contradict older memory entries (especially results from recent searches).
- The latest task outcomes refine or correct existing memory.

Update-memory instructions:
- If the related files/pages/documents changed substantially, replace the full set with repeated `--related-path`.
- If all stored related references are stale, clear them with `--clear-related-paths`.
- If one stored path or URL is no longer valid or its relevance has dropped, overwrite that specific related reference by ID with `--path-update <path-id>=project/relative/path`, `--path-update <path-id>=/new/absolute/path`, or `--path-update <path-id>=https://new.example/doc`, or clear it with `--path-clear <path-id>`.
- When updating related reference metadata, keep only files, pages, or documents that remain highly relevant to the updated memory content.

### Delete memory

```
python3 scripts/delete_memory.py --id <entry-id>
```

Deletes the entry matching the ID across all logs.

Use delete when:
- Older memory entries are no longer valuable or are misleading.
- A memory entry conflicts with verified facts and should be removed instead of updated.

### Smoke test memory-agent

```
python3 scripts/smoke_test_memory_agent.py --task-context "Smoke test for the current memory-agent configuration"
```

Runs a small end-to-end verification for the current project-local memory-agent setup.
This script is stricter than a connectivity check:
- it requires the current project-local `./easy-memory/agent-config.json` to exist,
- it runs both `search_memory.py` and `read_today_log.py` from the same working directory,
- it expects both commands to return agent-filtered plain-text output ending in a `[SUMMARY]` line rather than raw fallback output.

The default search keywords are `easy-memory`, `memory-agent`, and `codex`.
Override them with repeated `--search-keyword` arguments when validating a different project or provider.
If you want the smoke test to fail whenever the shared installation-directory failure log grows during the run, add `--strict-no-new-failures`.
If you want the final smoke-test report written to disk as well as printed to stdout, add `--json-output-file <path>`.
If you want successful runs to stay silent on stdout and rely only on the report file, add `--quiet` together with `--json-output-file`.

## Log location rule

Logs are always stored under `./easy-memory` relative to the directory where you run the scripts. The skill can be installed globally; logs never go to the install directory.

## Installer Notes

- Installer-facing environment adaptation rules live in `references/installer-environments.md`.
- Future memory-management agent integrations must keep the upstream OpenAI skill layout as the canonical package shape.
- Environment-specific adapter files may be generated by installers after install, but the tracked skill package must remain portable without them.
- The recommended project-local config file for future memory-agent runtime settings is `./easy-memory/agent-config.json`.
- Environment variables should override the local config file so machine-specific or temporary values do not require rewriting project-local state.
- A canonical local config example is available at `assets/examples/agent-config.example.json`.
- In Codex environments, the preferred default provider is `codex_exec`, which uses the installed `codex` CLI instead of direct HTTP model calls.
- The default Codex provider model should be `gpt-5.3-codex-spark`.
- `codex_service_tier` should default to `fast`, and `codex_reasoning_effort` should default to `medium`, while both remain locally configurable.
- `codex_profile` and `codex_binary` may also be provided for host-specific setups.
- For local OpenAI-compatible runtimes, `api_key` may be omitted when the endpoint does not require authentication.
- `api_style` may be used to select `codex_exec`, `openai_chat_completions`, or `ollama_native_chat`.
- `disable_thinking` may be used to request `think:false` when `api_style` is `ollama_native_chat` and the selected Ollama model supports thinking.
- If agent mode is enabled but any agent-side error occurs, including network errors, timeouts, protocol/schema problems, or unexpected runtime exceptions, the scripts must fall back to the same raw output they would produce with agent mode disabled.
- When such an agent-side fallback happens, the scripts should also append a diagnostic error record containing the full available response content to a runtime-generated error log in the installed skill directory, so cross-project model compatibility issues can be audited and corrected later.
- Provider-specific compatibility notes and dated benchmark snapshots may be stored in `references/` as informational documents so long as they do not redefine the canonical protocol. The current OpenRouter evaluation snapshot is in `references/openrouter-tested-models.md`.

## Future Memory-Agent Contract

The canonical source files for future memory-management agent support are:
- `agents/openai.yaml`
- `references/openai-compatible-api.md`
- `references/response-schema.md`
- `references/memory-agent-system-prompt.md`
- `references/script-output-schema.md`

These files define UI metadata, configuration boundaries, the lightweight plain-text filtering contract, and the canonical preprocessing prompt. Runtime implementations in `scripts/` should be added only after these canonical files are stable enough to implement against.

## Reminder to repeat each session

- Log entries should be written in English when possible; UTF-8 is accepted.
- At the start of the current session (before the first task), run `scripts/read_today_log.py` and `scripts/search_memory.py` with English-preferred keywords; adjust `--max-results` based on task complexity. Only repeat when necessary.
- Before finishing or submitting any task, write a log entry using `scripts/write_memory.py` following the rules above.
