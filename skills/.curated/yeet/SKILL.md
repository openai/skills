---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
---

## Prerequisites

- Require GitHub CLI `gh`. Check `gh --version`. If missing, ask the user to install `gh` and stop.
- Require authenticated `gh` session. Run `gh auth status`. If not authenticated, ask the user to run `gh auth login` (and re-run `gh auth status`) before continuing.

## Instruction Hooks

Before running the workflow, build the effective instructions from the vendor skill plus optional hook files:

- User hook: `${CODEX_HOME:-$HOME/.codex}/PULL_REQUESTS.md`
- Project hook: `<repo-root>/PULL_REQUESTS.md`

Resolve `<repo-root>` from an explicit repo/cwd input when one is provided; otherwise use `git rev-parse --show-toplevel` from the current checkout. Read each hook file only when that exact path exists. Do not scan parent directories, nested directories, or alternate filenames.

Apply instructions in this order: vendor skill, then user hook, then project hook. Later instructions override earlier ones only when they conflict; non-conflicting instructions all apply. Current system, developer, and user messages still outrank all hook files. If a hook file exists but cannot be read, stop and report the unreadable path instead of silently skipping it. If no hook exists, run this vendor skill as written.

## Naming conventions

- Branch: `{description}` when starting from main/master/default.
- Commit: `{description}` (terse).
- PR title: `{description}` summarizing the full diff.

## Workflow

- If on main/master/default, create a branch: `git checkout -b "{description}"`
- Otherwise stay on the current branch.
- Confirm status, then stage everything: `git status -sb` then `git add -A`.
- Commit tersely with the description: `git commit -m "{description}"`
- Run checks if not already. If checks fail due to missing deps/tools, install dependencies and rerun once.
- Push with tracking: `git push -u origin $(git branch --show-current)`
- If git push fails due to workflow auth errors, pull from master and retry the push.
- Open a PR and edit title/body to reflect the description and the deltas: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`
- Write the PR description to a temp file with real newlines (e.g. pr-body.md ... EOF) and run pr-body.md to avoid \\n-escaped markdown.
- PR description (markdown) must be detailed prose covering the issue, the cause and effect on users, the root cause, the fix, and any tests or checks used to validate.
