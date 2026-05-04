---
name: phasekeeper
description: Use when setting up or operating a Phasekeeper workflow for Codex projects with active phase boards, approved specs, session start gates, issue tracking, verification logs, progress archives, and clean handoffs.
metadata:
  short-description: Board-first workflow for long-running Codex projects
---

# Phasekeeper

Phasekeeper is a board-first workflow for long-running software work. It keeps Codex anchored to explicit phase state instead of relying on chat memory.

Use this skill when the user asks to install, set up, start, continue, close, or repair a Phasekeeper-managed project.

## Operating Rules

1. If the target repo has `AGENTS.md`, read and obey it first.
2. Treat `docs/boards/README.md` as the active phase pointer.
3. Treat the active board as the current state of work.
4. Do not start implementation until the session start gate is complete and the operator confirms.
5. Do not infer phase scope from chat when a board or spec is missing. Create or request the missing workflow artifact.
6. Keep workflow updates auditable: references, tests, issues, work log, progress, and commits should agree.

## Setup Mode

Use setup mode when the user asks to set up, install, initialize, bootstrap, or add Phasekeeper to a repo.

Steps:

1. Inspect the target repo for existing `AGENTS.md`, `WORKFLOW.md`, `PROGRESS.md`, `docs/boards/README.md`, and `docs/specs/`.
2. If this skill's script is available, run `scripts/init_phasekeeper.py <repo-root>`.
3. If existing files are present, do not overwrite them unless the user explicitly asks for overwrite behavior.
4. Report which files were created, skipped, or overwritten.
5. Tell the user that future sessions should start with the Phasekeeper session start protocol.

If the script is unavailable, create the same files from `assets/templates/`.

## Session Start

Use session start when the user asks to start, resume, continue, pick up, or check current Phasekeeper state.

Read in this order:

1. `AGENTS.md`, if present.
2. `docs/boards/README.md`.
3. The active board listed by `docs/boards/README.md`, if it exists.
4. The active spec listed by the board, if it exists.
5. `WORKFLOW.md`.
6. Any OPEN issues on the active board.

Then report exactly:

```text
Phase NN, Step K of N. Open issues: N. Next up: <description>. Ready?
```

Wait for operator confirmation before implementation.

If an active board does not exist, switch to board creation mode. If the phase spec does not exist or is not approved, switch to spec mode.

## Spec Mode

Use spec mode when a phase needs a written plan before implementation.

Create or update:

```text
docs/specs/phase_NN_<slug>.md
```

The spec must define:

- Goal and non-goals.
- Scope boundaries.
- Behavior, API, schema, or contract changes.
- Configuration changes.
- Tests and verification gates.
- Implementation order.
- Open questions.

Do not mark a spec approved unless the operator explicitly approves it.

## Board Creation Mode

Use board creation mode when a spec is approved but no board exists.

Create:

```text
docs/boards/phase_NN_<slug>.md
```

Base it on `docs/boards/phase-board.template.md`. Populate the implementation steps from the approved spec. Update `docs/boards/README.md` so exactly one phase is active.

## Phase Work Mode

Use phase work mode only after the operator confirms the session start prompt.

For each active step:

1. Check worktree state.
2. Read every file the step will touch and the relevant tests.
3. Write or update the narrowest relevant test when behavior changes.
4. Implement the minimal scoped change.
5. Run relevant verification.
6. Update board References, Tests, Issues, and Work Log.
7. Update `PROGRESS.md` after the session or accepted phase.
8. Commit completed board steps unless the operator says not to.

Do not mix unrelated cleanup into a phase step.

## Session Close

Use session close when the user asks to stop, wrap up, close, hand off, finish the session, or summarize next steps.

Before final response:

1. Update the active board Current Status.
2. Add a Work Log entry with what changed, verification, issues, and next step.
3. Update References for every created or modified file.
4. Update Tests with exact commands and results.
5. Update `PROGRESS.md`.
6. Run `git status --short`.
7. Run `git log --oneline -10`.
8. Commit completed board steps unless the operator says not to.
9. Tell the operator exactly where the next session picks up.

If a board marks a step DONE but no matching commit exists, say so explicitly.

## Hard Stops

Stop and ask the operator when:

- The active board or spec contradicts the repo state.
- A test suggests the spec is wrong.
- A high-severity issue appears.
- A change would weaken a stated invariant or project rule.
- A design decision has multiple valid options.
- You are tempted to patch around a symptom instead of fixing the root cause.
