---
name: gh-merge-queue
description: Manage a GitHub merge queue across many open PRs in the current repo by reviewing each PR, enabling auto-merge when it meets the repo's quality bar, and rebasing the next PR after each merge. Use when a user wants to process multiple open PRs in order, apply consistent review standards, and handle conflicts, age, or quality issues.
---

# Merge Queue

## Overview

Process open PRs in order for the current GitHub repo. Review each PR with a subagent, decide whether it meets the project quality bar, enable auto-merge if it does, and rebase the next PR after the previous merges. Stop when there are no open PRs or when a PR is rejected.

## Workflow

1. Determine repo context.
   - Use the repo in the current working directory.
   - If the repo is unclear, ask the user which GitHub repo to operate on.
2. List open PRs in order.
   - Prefer the repo's merge-queue order if exposed; otherwise sort by updated time or number and state the ordering used.
3. For each PR in order:
   - Gather PR metadata: title, author, status checks, review state, mergeability, conflicts, last update date, and linked issues.
   - Read the repo's quality bar (CONTRIBUTING, README, code owner docs, test requirements).
   - Run a subagent review focused on correctness, safety, tests, and fit with project standards.
4. Decide and act:
   - If the PR meets the bar and is mergeable, enable auto-merge.
   - If the PR is too old, has excessive conflicts, fails checks, or does not meet the bar, reject it and explain why.
5. After a PR merges:
   - Update the next PR from the updated main branch using `gh pr update-branch <pr-number>`.
   - Re-run checks if required by the repo.
   - Continue until all open PRs are processed.

## Decision Rules

- Treat CI failures, missing required approvals, or merge conflicts as blockers.
- Favor smaller, well-scoped PRs; flag broad or risky changes for human review.
- If the repo has specific merge policies (squash/rebase, required checks), follow them strictly.
- If information is missing to determine quality, ask for clarification rather than guessing.
