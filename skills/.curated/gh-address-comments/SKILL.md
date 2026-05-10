---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Instruction Hooks

Before running the workflow, build the effective instructions from the vendor skill plus optional hook files:

- User hook: `${CODEX_HOME:-$HOME/.codex}/gh-comments.md`
- Project hook: `<repo-root>/gh-comments.md`

Resolve `<repo-root>` from an explicit repo/cwd input when one is provided; otherwise use `git rev-parse --show-toplevel` from the current checkout. Read each hook file only when that exact path exists. Do not scan parent directories, nested directories, or alternate filenames.

Apply instructions in this order: vendor skill, then user hook, then project hook. Later instructions override earlier ones only when they conflict; non-conflicting instructions all apply. Current system, developer, and user messages still outrank all hook files. If a hook file exists but cannot be read, stop and report the unreadable path instead of silently skipping it. If no hook exists, run this vendor skill as written.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
