# Phasekeeper Workflow

Board-first process for phased work. This file defines how work gets opened, tracked, verified, committed, and handed off.

Where this file conflicts with `AGENTS.md`, `AGENTS.md` wins.

---

## Lifecycle

```text
session start
  |
  v
read docs/boards/README.md
  |
  v
active board exists?
  |
  +-- no --> create or approve a phase spec
  |           |
  |           v
  |      create board from template
  |
  +-- yes --> implementation mode
                    |
                    v
              pick up next unchecked step
                    |
                    v
              make scoped change
                    |
                    v
              run relevant verification
                    |
                    v
              update board and PROGRESS.md
                    |
                    v
              commit or hand off completed step
                    |
                    v
              stop at phase gate or wait for continue
```

---

## Session Start

Every session starts with these reads, in order:

1. `docs/boards/README.md`
2. the active board listed there, if it exists
3. the active phase spec listed by the board, if it exists
4. `WORKFLOW.md`
5. any OPEN issues on the active board

Then report:

```text
Phase NN, Step K of N. Open issues: N. Next up: <description>. Ready?
```

No implementation work starts until the operator confirms.

---

## Spec Mode

Use spec mode when the next phase is known but no approved spec exists.

Output:

```text
docs/specs/phase_NN_<slug>.md
```

A phase spec should cover:

- Goal and non-goals
- Scope boundaries
- User-visible behavior or contract changes
- Data model or API changes
- Configuration changes
- Tests and verification gates
- Implementation order
- Open questions

The spec is not approved until the operator explicitly says it is approved.
When approved, update the spec metadata to `Status: APPROVED` and fill in the approval fields.

---

## Board Creation

Create a board after the spec is approved and before implementation starts:

```text
docs/boards/phase_NN_<slug>.md
```

Use `docs/boards/phase-board.template.md`. Populate:

- Current status
- Implementation steps from the approved spec
- Open question resolutions
- Gate interpretations
- References
- Issues
- Tests
- Work log
- Deferred issues

Every issue, decision, and session handoff goes on the board. If it is not on the board, the next session cannot reliably reconstruct it.

---

## Implementation Mode

Before editing code, read:

1. active board
2. approved spec
3. every code file the step will touch
4. relevant tests

For each step:

1. Confirm the worktree state.
2. Write or update the narrowest relevant test when behavior changes.
3. Implement the minimal scoped change.
4. Run the narrowest relevant verification.
5. Update board references with changed files.
6. Update board tests with commands and results.
7. Update the board work log.
8. Update `PROGRESS.md` after the session or accepted phase.
9. Commit the completed step only when repo policy or the operator has already authorized commits; otherwise hand back the completed uncommitted work explicitly.

Do not merge unrelated cleanup into a phase step.

---

## Issue Tracking

Issues live on the active board.

Use this format:

```markdown
### ISS-001 - <short title>
**Status:** OPEN | **Severity:** high/medium/low | **Found:** Step K, YYYY-MM-DD
**Files:** `path/to/file.py:line`
**What is wrong:** <expected vs actual>
**How to reproduce:** <command or scenario>
**Root cause:** _(filled when diagnosed)_
**Resolution:** _(filled when fixed or deferred)_
**Resolved:** _(date + step, or "deferred to Phase NN")_
```

Severity guide:

- High: blocks the phase, threatens core guarantees, or means the spec may be wrong. Stop and ask.
- Medium: must be resolved before phase completion but does not block the current step.
- Low: non-blocking cleanup or clarity issue.

---

## Session End

Before ending a session:

1. Update the board Current Status.
2. Add a Work Log entry with what changed, verification, issues, and next step.
3. Update References for every file created or modified.
4. Update Tests with exact commands and results.
5. Update `PROGRESS.md` for the session or accepted phase.
6. Run `git status --short` and `git log --oneline -10`.
7. Commit completed board steps only when repo policy or the operator has already authorized commits; otherwise hand back the completed uncommitted work explicitly.
8. Tell the operator the next board step.

If a board marks a step DONE, a matching commit must exist or the work must be explicitly handed back as uncommitted.
