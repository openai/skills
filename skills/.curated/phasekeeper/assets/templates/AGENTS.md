# Phasekeeper Agent Rules

This repository uses Phasekeeper: a board-first workflow for long-running agent-assisted software projects.

Optimize for correctness, traceability, and clean handoff. Speed and convenience are secondary when they conflict with those goals.

Where this file conflicts with `WORKFLOW.md`, this file wins.

---

## Session Start

Before implementation work:

1. Read `docs/boards/README.md`.
2. Read the active board listed there, if it exists.
3. Read the active spec listed by the board, if it exists.
4. Read `WORKFLOW.md`.
5. Check the active board for OPEN issues.
6. Tell the operator: `Phase NN, Step K of N. Open issues: N. Next up: <description>. Ready?`
7. Wait for operator confirmation before implementation.

If the active board does not exist, read `WORKFLOW.md` and follow the board/spec creation process. Do not infer phase scope from chat alone.
If the active spec is missing or still marked `DRAFT`, stop in spec mode and get explicit operator approval before creating a board or implementing.

---

## During Work

- Follow the active board one step at a time.
- Do not merge unrelated refactors or cleanup into a phase step.
- If the work changes behavior, write or update tests before implementation when feasible.
- Keep changes scoped to the active phase or explicit operator request.
- Preserve existing local changes that are unrelated to your task.
- Log issues on the active board when found.
- Stop and ask when a decision has multiple valid options, a test suggests the spec is wrong, or a change would weaken a stated invariant.

---

## Session End

Before ending a session:

1. Update the active board Current Status.
2. Add a Work Log entry with what changed, verification, issues, and next step.
3. Update References for every created or modified file.
4. Update Tests with exact commands and results.
5. Update `PROGRESS.md` for the session or accepted phase.
6. Run `git status --short` and `git log --oneline -10`.
7. Commit completed board steps unless the operator explicitly says not to.
8. Tell the operator where the next session picks up.

If a board marks a step DONE, a matching commit must exist or the uncommitted state must be handed back explicitly.

---

## Source Of Truth

| Priority | Source | Purpose |
|---|---|---|
| 0 | `AGENTS.md` | Agent operating rules. |
| 1 | `docs/boards/phase_NN_*.md` | Active phase state, issues, references, tests, and work log. |
| 2 | `docs/boards/README.md` | Active phase pointer, phase index, and board template. |
| 3 | `WORKFLOW.md` | Workflow process manual. |
| 4 | `PROGRESS.md` | Historical accepted phase and session archive. |
