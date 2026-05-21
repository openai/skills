# Controlled Implementation Rules

Use this reference while implementing from `docs/implementation-plan.md`.

## Kickoff Prompt

```text
Start implementing the project according to `docs/implementation-plan.md`.

Scope Constraints:

- Only implement tasks necessary to reach the first testable state of the MVP.
- Do not implement features beyond the defined MVP scope.
- Respect architectural boundaries defined in the plan.
- Maintain coherence with the existing project structure.

Execution Rules:

- Implement in small, logically grouped batches.
- After completing each major task group, pause.
- Summarize all changes made.
- Clearly describe what is now testable.
- Wait for user validation before continuing.

Progress Tracking:

Create or update `docs/progress.md`.

Stop Condition:

Stop once a minimally testable version of the MVP is achieved.
```

## Progress Rules

- Tasks must be derived from `docs/implementation-plan.md`.
- Each task must be actionable and concrete.
- Use only `[ ]` and `[x]`.
- Append `(Blocked: reason)` when blocked.
- Append `(Deferred)` when intentionally postponed.
- Do not change the file structure.
- Do not invent new sections.
- Do not include implementation logs.
- Do not duplicate plan content.
- Always update `Last updated` when modifying the file.

## Batch Boundary Summary

At each stop, report:

- What changed
- What is testable
- What remains incomplete
- Known limitations
- Suggested next step
