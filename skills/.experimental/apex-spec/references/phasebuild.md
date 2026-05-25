# phasebuild

Create the directory structure, phase PRD, and session stubs for a new phase. Ensures alignment with completed work and lessons learned.

## Rules

1. **ASCII-only characters** and Unix LF line endings in all output
2. **Resolve misalignment before building** - as projects progress, later phases may drift from reality. Reconcile with actual progress before creating artifacts.
3. **If interrupted mid-process**, delete partial artifacts before retrying
4. Each session must have a single clear objective, 12-25 tasks, 2-4 hours scope

## Steps

### 1. Assess Current State

Read `.spec_system/state.json` and `.spec_system/PRD/` to understand:
- What has been accomplished
- Next sequential phase number
- High-level objectives remaining

If `.spec_system/CONSIDERATIONS.md` exists, review it for:
- **Active Concerns** that should influence session ordering or scope
- **Lessons Learned** (patterns to follow or avoid)
- **Tool/Library Notes** relevant to this phase

If `.spec_system/SECURITY-COMPLIANCE.md` exists, review it for:
- **Open Findings** that should be addressed in this phase's sessions
- **GDPR Status** that may affect data-handling session scope

**Monorepo Checkpoint** (skip if `monorepo` is already `true` or `false`):
- If the PRD references multiple packages/services but `state.json` has no `packages` array, alert the user:
  ```
  Warning: PRD references multiple packages but monorepo is not configured.
  Consider running createprd to detect and configure monorepo settings,
  or manually update state.json with monorepo: true and a packages array.
  ```
- This is advisory only -- do not block phase creation

### 2. Create Phase Directory and PRD Markdown

Create directory `.spec_system/PRD/phase_NN/` and markdown `.spec_system/PRD/phase_NN/PRD_phase_NN.md`:

```markdown
# PRD Phase NN: Phase Name

**Status**: Not Started
**Sessions**: N (initial estimate)
**Estimated Duration**: X-Y days

**Progress**: 0/N sessions (0%)

---

## Overview

[Phase description]

---

## Progress Tracker

| Session | Name | Status | Est. Tasks | Validated |
|---------|------|--------|------------|-----------|
| 01 | [Name] | Not Started | ~12-25 | - |
| 02 | [Name] | Not Started | ~12-25 | - |
| 03 | [Name] | Not Started | ~12-25 | - |
| ... | ... | ... | ... | ... |

---

## Completed Sessions

[None yet]

---

## Upcoming Sessions

- Session 01: [Name]

---

## Objectives

1. [Primary objective]
2. [Secondary objective]
3. [Tertiary objective]

---

## Prerequisites

- Phase NN-1 completed (omit for Phase 01)
- [Other prerequisites]

---

## Technical Considerations

### Architecture
[Architecture notes for this phase]

### Technologies
- [Technology 1]
- [Technology 2]

### Risks
- [Risk 1]: [Mitigation]

### Relevant Considerations
<!-- From CONSIDERATIONS.md - remove section if none apply -->
- [P##] **[Item from Active Concerns]**: How it affects this phase
- [P##] **[Lesson Learned]**: How we're applying it

---

## Success Criteria

Phase complete when:
- [ ] All N sessions completed
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Dependencies

### Depends On
- Phase NN-1: [Name]

### Enables
- Phase NN+1: [Name]
```

### 3. Create All Session Stubs

For each session, create `session_NN_name.md` (use `snake_case` for name):

.spec_system/PRD/phase_NN/
|-- PRD_phase_NN.md
|-- session_01_name.md
|-- session_02_name.md
\-- ...

```markdown
# Session NN: Session Name

**Session ID**: `phaseNN-sessionNN-name`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

[Clear single objective for this session]

---

## Scope

### In Scope (MVP)
- [Feature 1]
- [Feature 2]

### Out of Scope
- [Deferred item 1]

---

## Prerequisites

- [ ] [Prerequisite 1]

---

## Deliverables

1. [Deliverable 1]
2. [Deliverable 2]

---

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

**Monorepo package annotation** (only when `monorepo: true` in state.json):

Add a `Package:` or `Packages:` line to the stub header, after the Session ID line:
- Single-package session: `**Package**: apps/web`
- Multi-package session: `**Packages**: apps/web, apps/api`
- Cross-cutting or single-repo: omit the line entirely

This annotation is parsed by `analyze-project.sh` to enable `--package` filtering and package-scoped workflows.

**Cross-package guidance**: When a session touches multiple packages, note which package owns the primary deliverables and which are secondary dependencies. Keep cross-package sessions to 2-3 packages maximum -- split if more are needed.

### 4. Update State

Merge into `.spec_system/state.json` (add to existing `phases` object):

```json
{
  "phases": {
    "NN": {
      "name": "Phase Name",
      "description": "Phase description",
      "status": "not_started",
      "session_count": N
    }
  }
}
```

### 5. Update Master PRD

Add the new phase to the Phases table in `.spec_system/PRD/PRD.md`. Also update any stale info (completed phases marked as such, session counts reflecting reality):

```markdown
## Phases

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| ... | ... | ... | ... |
| NN | Phase Name | N | Not Started |
```

## Phase Planning Guidelines

### Session Count
- Typical phase: 4-8 sessions
- Small phase: 2-3 sessions
- Large phase: Consider splitting

### Session Sizing
- Each session: 12-25 tasks
- Each session: 2-4 hours
- Single clear objective per session

### Dependency Management
- Sessions within phase can depend on each other
- Early sessions provide foundation
- Later sessions build complexity

## Output

Report to user:

```
Phase NN Created: Phase Name

Structure:
- .spec_system/PRD/phase_NN/
  - PRD_phase_NN.md
  - session_01_name.md
  - session_02_name.md
  - session_03_name.md

State Updated:
- Phase added to .spec_system/state.json
- Master PRD updated

Sessions Defined: N

Next Steps:
- Review session definitions
- Adjust scope as needed
- Run plansession to begin
```
