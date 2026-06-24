# Phasekeeper Board Index

This is where agents look first every session. Find the active phase, then read the board or create it through `WORKFLOW.md` if it does not exist yet.

---

## Active Phase

**Phase 01 - <Name>** | Status: NOT OPENED | Spec: _(not approved)_ | Board: _(not created)_

Exactly one phase is active.

---

## Phase Index

| Phase | Spec | Board | Status |
|---|---|---|---|
| 01 - <Name> | _(not opened)_ | _(not opened)_ | PLANNED |

---

## Board Template

When starting implementation of a phase, copy `phase-board.template.md` to `phase_NN_<slug>.md` and fill it in.

Create or update the phase spec first from `docs/specs/phase-spec.template.md`. Only create a board after the operator explicitly approves the spec.
