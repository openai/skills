# Autonomy Kernel

The self-improving operator is not just a style guideline. It is a persistent execution loop with a durable backlog.

## Required state files

- `.operator/mission.md`: mission, scope, work sources, stop reasons, and publish mode.
- `.operator/backlog.json`: prioritized work items discovered from repo and GitHub signals.
- `.operator/state.json`: current item, verification state, last stop reason, and `next_action`.
- `.operator/checkpoints/*.md`: durable checkpoints written after verified work.

## Default work sources

- `local_tests`
- `ci_failures`
- `runtime_failures`
- `todo_fixme`
- `docs_handoff_gaps`
- `github_issues`
- `github_pr_reviews`
- `github_discussions`

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

## Default publishing rule

The default publish mode is `checkpoint_commit`: create a checkpoint branch/commit when work reaches a meaningful verified checkpoint, but do not auto-open a PR.
