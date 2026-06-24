# Context Rot Checklist

Use this reference to recover coherence in long sessions.

## Symptoms

- Drift from the original problem definition
- Inconsistent naming conventions
- Silent architectural shifts
- Redundant abstractions
- Scope expansion without explicit intent
- Reintroduction of previously rejected decisions
- Confusion between plan, progress, and implementation logs

## Structural Defenses

- Persist intent in artifacts.
- Summarize phase boundaries explicitly.
- Pause after major implementation batches.
- Reload the plan and guidelines in long sessions.
- Keep context focused on current phase and current batch.

## Re-Anchor Prompt

```text
Re-anchor this session from durable project artifacts.

Read the relevant project artifacts:

- `docs/implementation-plan.md`
- `docs/progress.md`
- `docs/project-guidelines.md`
- `docs/technical-debt.md`

Summarize:

- Current objective
- Current phase
- Completed work
- Active constraints
- Decisions already made
- Open questions
- Next safe action

Separate confirmed facts from assumptions.
Do not make code changes yet.
```

## Rule

Do not maximize context. Maximize relevant, structured signal.
