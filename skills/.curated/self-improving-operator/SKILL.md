---
name: "self-improving-operator"
description: "Use when the user wants Codex to keep iterating on a project, maintain `.operator/` state, keep finding the next safe task, and stop only on a real stop reason."
---

Use this skill when the user wants Codex to keep driving a project forward without stopping after one narrow edit.

Typical triggers:

- `continue pushing this project forward`
- `keep improving this until it feels production-ready`
- `take ownership and keep iterating`
- `do not stop after the first fix`
- `proactively improve this repository`
- `bring this closer to enterprise standard`
- `keep finding the next safe high-leverage task`

## Mission

Operate a repository as an actively improving system that can keep finding safe, high-leverage work until it reaches a real stop reason.

The operator must use persistent repo-local state under `.operator/` so a new thread can resume without rediscovering the whole situation.

## Required loop

1. Infer or load the mission from `.operator/mission.md`.
2. Refresh repo and GitHub signals into `.operator/backlog.json`.
3. Pick the next safe, high-leverage work item.
4. Implement one bounded improvement.
5. Verify with direct evidence.
6. Write a checkpoint into `.operator/checkpoints/` and update `.operator/state.json`.
7. Re-scan and continue until a real stop reason exists.

Planning is not a stopping point. If a broad plan is needed, decompose it into backlog items and keep going.

## Persistent files

- `.operator/mission.md`: mission, scope, work sources, stop reasons, and publish mode.
- `.operator/backlog.json`: prioritized work items discovered from repo and GitHub signals.
- `.operator/state.json`: current item, verification state, last stop reason, and `next_action`.
- `.operator/checkpoints/*.md`: durable checkpoints written after verified work.

## Work sources

- `local_tests`
- `ci_failures`
- `runtime_failures`
- `todo_fixme`
- `docs_handoff_gaps`
- `github_issues`
- `github_pr_reviews`
- `github_discussions`

Only actionable signals should become backlog items. Ignore explanatory prose, string literals, generated outputs, and any stale scan-derived item that no longer appears in the current refresh.

## Priority order

1. broken runtime or ci
2. github blockers
3. existing backlog commitments
4. tests diagnostics onboarding docs
5. cleanup and polish

## Stop reasons

- `needs_user_decision`
- `external_blocker`
- `risk_budget_exceeded`
- `no_safe_work`
- `mission_complete`

Return to the user only when one of the stop reasons is true, and always write the stop reason into `.operator/state.json`.

## Runtime commands

Use the bundled script `scripts/operator_runtime.py` for deterministic state updates.

- `python3 scripts/operator_runtime.py bootstrap --repo /path/to/repo --goal "Ship onboarding reliably"`
- `python3 scripts/operator_runtime.py scan --repo /path/to/repo`
- `python3 scripts/operator_runtime.py next --repo /path/to/repo`
- `python3 scripts/operator_runtime.py ingest-plan --repo /path/to/repo --plan-file /path/to/plan.md`
- `python3 scripts/operator_runtime.py checkpoint --repo /path/to/repo --item-id <id> --summary "..." --verification-status passed --verification-summary "..." --publish-checkpoint`
- `python3 scripts/operator_runtime.py status --repo /path/to/repo`

## Guardrails

- Continue automatically only on safe, in-scope, bounded work.
- Do not invent new product lines, marketing tracks, or unrelated missions unless the mission explicitly includes them.
- Default publish mode is checkpoint branch/commit, not auto-PR.
- If a task needs a different skill for one step, use it, then return to this operator loop.
- Prefer tests over confidence, runtime probes over guesses, and backlog updates over memory.

## Handoff discipline

- Always save `next_action` before stopping.
- Always record what changed, what was verified, and what remains blocked.
- Make the next thread faster by leaving a clean `.operator` state, not just prose in chat.
