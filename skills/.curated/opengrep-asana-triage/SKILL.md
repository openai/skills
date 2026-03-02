---
name: opengrep-asana-triage
description: Triage OpenGrep/Semgrep findings tracked in Asana with deep code-backed validation, classify each open task into keep/close statuses, and for confirmed false positives patch semgrep-config rules with regression tests and open a draft GitHub PR. Use when asked to process findings from a specific Asana project/section and produce structured triage output.
---

# OpenGrep Asana Triage

Execute this workflow when the user provides an Asana project/section and asks for OpenGrep finding triage with code validation and semgrep rule tuning.
Explicitly use `$asana` for Asana task retrieval and task-detail calls in this workflow.

## Required Inputs

Collect these values before starting:
- `asana_project_gid` (default OpenGrep project: `1204739124513228`)
- `asana_section_gid` (default OpenGrep section: `1213249207168279`)
- `finding_label` (usually `Opengrep`)
- `semgrep_config_path` (for example `../semgrep-config`)
- `base_branch` (for example `origin/master`)

If the user does not provide project/section IDs, use the default OpenGrep GIDs above.

## Workflow

1. Fetch tasks (first pass, section-only)
- Call `asana_get_tasks` with:
  - `section=<asana_section_gid>`
  - `opt_fields=name,completed,permalink_url,gid`
- Paginate until complete.
- Keep only `completed=false` tasks.
- Do not run extra Asana search/discovery unless section lookup fails.

2. Fetch task details (second pass)
- For open task IDs only, call `asana_get_task` with:
  - `opt_fields=gid,name,notes,completed,permalink_url`

3. Parse each task
- From `notes`, extract when present:
  - rule id
  - file path / GitHub blob URL
  - commit hash
  - code snippet
  - links

4. Deep code validation
- Prefer `git show <commit>:<path>` when commit object exists.
- If commit or path is unavailable, inspect current checkout and relevant callers/helpers/tests.
- Validate:
  - authn/authz path
  - IDOR / access control checks
  - exploitability and attacker preconditions
  - existing test coverage and gaps

5. Assign exactly one decision per task
- `TRUE_POSITIVE_KEEP_OPEN`
- `FALSE_POSITIVE_CLOSE`
- `DUPLICATE_CLOSE`
- `ALREADY_FIXED_CLOSE`
- `NEEDS_MANUAL_REVIEW_KEEP_OPEN`

6. Rule updates for false positives
- For every `FALSE_POSITIVE_CLOSE` task:
  - Implement minimal, safe rule changes in `semgrep_config_path`.
  - Prefer narrow `pattern-not` / `pattern-not-inside` / path excludes.
  - Add regression tests for each change.
- Run validation/tests (`opengrep --test rules`, and semgrep equivalent if available).

7. Branch + PR
- Create branch: `rohan/<short-slug>`.
- Commit and push changes.
- Use `gh` CLI only for GitHub operations.
- Open **draft** PR with:
  - Title: `semgrep-config: <descriptive title>`
  - Body sections:
    - `Summary`
    - `Triage decisions`
    - `Rule changes`
    - `Validation`
    - `## Test Plan`
- Preserve markdown/newlines by using `--body-file`.

## Output Contract (No Tables)

Return:
- `Open-task count`
- Compact triage decisions in this exact style:
  - `Close`
    - `1. <full Asana URL> — <decision> (<confidence>): <one-line reason>`
  - `Keep Open`
    - `1. <full Asana URL> — <decision> (<confidence>): <one-line reason>`
- Always use full URL (not shortened) as the first token in each triage line.
- Then include:
  - `Top residual risks`
  - `Fast follow-up checks`
- Add one short mapping line for dedupes when relevant:
  - `Duplicate mapping: <duplicate_task_gid> -> <canonical_task_gid>`

Also include:
- findings to close vs keep open
- exact semgrep-config files changed
- test commands run and results
- draft PR URL

## Blocking/Failure Handling

If blocked, state exactly what failed and continue best-effort:
- missing commit object
- missing file/path
- missing tools
- test command failures

Do not close findings without code-backed evidence.
Do not use destructive git commands.
