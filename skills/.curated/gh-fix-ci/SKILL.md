---
name: "gh-fix-ci"
description: "Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL."
---


# Gh Pr Checks Plan Fix

## Overview

Use gh to wait for PR checks with adaptive polling, then inspect failures for actionable logs. Summarize failure context, propose a fix plan, and implement only after explicit approval.
- If a plan-oriented skill (for example `create-plan`) is available, use it; otherwise draft a concise plan inline and request approval before implementing.

Prereq: authenticate with the standard GitHub CLI once (for example, run `gh auth login`), then confirm with `gh auth status` (repo + workflow scopes are typically required).

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Quick start

- Wait for checks to settle: `python "<path-to-skill>/scripts/wait_for_pr_checks.py" --repo "." --pr "<number-or-url>"`
- If failures remain, inspect them: `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Add `--json` to either script for machine-friendly output.

## Workflow

1. Verify gh authentication.
   - Run `gh auth status` in the repo.
   - If unauthenticated, ask the user to run `gh auth login` (ensuring repo + workflow scopes) before proceeding.
2. Resolve the PR.
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.
3. Inspect failing checks (GitHub Actions only).
   - First wait for check stabilization (avoids over-polling and catches late checks that appear after matrix jobs):
     - `python "<path-to-skill>/scripts/wait_for_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - Script behavior:
       - Polls faster when many checks are pending.
       - Polls slower when only long-running checks remain.
       - Requires consecutive no-pending polls before declaring success (catches late checks like coverage-summary jobs).
       - Exits non-zero as soon as a failure appears.
   - Preferred: run the bundled script (handles gh field drift and job-log fallbacks):
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - Add `--json` for machine-friendly output.
   - Manual fallback:
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - If a field is rejected, rerun with the available fields reported by `gh`.
     - For each failing check, extract the run id from `detailsUrl` and run:
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - If the run log says it is still in progress, fetch job logs directly:
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. Scope non-GitHub Actions checks.
   - If `detailsUrl` is not a GitHub Actions run, label it as external and only report the URL.
   - Do not attempt Buildkite or other providers; keep the workflow lean.
5. Summarize failures for the user.
   - Provide the failing check name, run URL (if any), and a concise log snippet.
   - Call out missing logs explicitly.
6. Create a plan.
   - Use the `create-plan` skill to draft a concise plan and request approval.
7. Implement after approval.
   - Apply the approved plan, summarize diffs/tests, and ask about opening a PR.
8. Recheck status.
   - After changes, run:
     - `python "<path-to-skill>/scripts/wait_for_pr_checks.py" --repo "." --pr "<number-or-url>"`
   - If it exits non-zero, run:
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`

## Bundled Resources

### scripts/wait_for_pr_checks.py

Wait for PR checks using adaptive polling and stabilization to reduce noisy polling while still detecting late-added checks.

Usage examples:
- `python "<path-to-skill>/scripts/wait_for_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/wait_for_pr_checks.py" --repo "." --pr "123" --timeout-seconds 5400`
- `python "<path-to-skill>/scripts/wait_for_pr_checks.py" --repo "." --pr "123" --json`

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
