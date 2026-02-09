---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Quick start

- `python "<path-to-skill>/scripts/fetch_comments.py" --repo "."`
- Add `--pr <number-or-url>` to target a specific PR instead of the current branch.
- Add `--json` for machine-friendly output.

## Workflow

### 1) Inspect comments needing attention
- Preferred: run the bundled script:
  - `python "<path-to-skill>/scripts/fetch_comments.py" --repo "."`
  - If the user provides a PR number or URL, pass it: `--pr "<number-or-url>"`
  - Add `--json` if you want machine-friendly output for summarization.
- Manual fallback (if the script is unavailable):
  - Use `gh api graphql` with the GraphQL query to fetch PR comments, reviews, and review threads.

### 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

### 3) If user chooses comments
- Apply fixes for the selected comments

## Bundled Resources

### scripts/fetch_comments.py

Fetch all PR conversation comments, reviews, and inline review threads for a given PR. Outputs JSON to stdout.

Usage examples:
- `python "<path-to-skill>/scripts/fetch_comments.py" --repo "."`
- `python "<path-to-skill>/scripts/fetch_comments.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/fetch_comments.py" --repo "." --pr "https://github.com/org/repo/pull/456" --json`

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
