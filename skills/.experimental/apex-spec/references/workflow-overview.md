# Workflow Overview

Quick-reference for the Apex Spec System's 13-command workflow.

## Core Philosophy

**1 session = 1 spec = 2-4 hours (12-25 tasks)**

A collection of sessions is a phase. A collection of phases is a mature
technical PRD.

## Session Scope Rules

| Limit | Value |
|-------|-------|
| Maximum tasks | 25 |
| Maximum duration | 4 hours |
| Ideal task count | 12-25 (sweet spot: 20) |
| Objectives | Single clear objective |

## The 3 Stages

### Stage 1: Initialization (One-Time Setup)

| Step | Command | Purpose |
|------|---------|---------|
| 1 | initspec | Set up .spec_system/ in your project |
| 2 | createprd | Generate PRD from requirements doc (optional) |
| 3 | createuxprd | Generate UX PRD from design docs (optional) |
| 4 | phasebuild | Create first phase structure with session stubs |

### Stage 2: Session Workflow (Repeat Until Phase Complete)

| Step | Command | Purpose |
|------|---------|---------|
| 1 | plansession | Analyze project state, create spec + task checklist |
| 2 | implement | AI-led task-by-task implementation |
| 3 | validate | Verify session completeness and quality gates |
| 4 | updateprd | Mark session complete, sync PRD and state |

Repeat this cycle for each session in the phase.

### Stage 3: Phase Transition (After All Phase Sessions Complete)

| Step | Command | Purpose |
|------|---------|---------|
| 1 | audit | Set up local dev tooling (formatter, linter, types, tests) |
| 2 | pipeline | Configure CI/CD workflows (quality, build, security) |
| 3 | infra | Set up production infrastructure (health, security, deploy) |
| 4 | carryforward | Capture lessons learned (optional but recommended) |
| 5 | documents | Audit and update project documentation |
| - | (manual) | Manual testing and LLM audit (highly recommended) |
| 6 | phasebuild | Create next phase structure, return to Stage 2 |

## Workflow Diagram

```
STAGE 1: INIT           STAGE 2: SESSIONS        STAGE 3: TRANSITION

initspec                plansession ----+         audit
    |                       |           |             |
    v                       v           |             v
createprd (opt)         implement       |         pipeline
    |                       |           |             |
    v                       v           |             v
createuxprd (opt)       validate        |         infra
    |                       |           |             |
    v                       v           |             v
phasebuild              updateprd ------+         carryforward
                                                      |
                                                      v
                                                  documents
                                                      |
                                                      v
                                                  phasebuild --> Stage 2
```

## Utility Commands (Safe at Any Time)

These 9 commands run outside the session workflow:

| Command | Purpose |
|---------|---------|
| copush | Pull, version-bump, commit all changes, push to origin |
| sculpt-ui | Guide AI-led creation of distinctive frontend interfaces |
| dockbuild | Quick Docker Compose build and start |
| dockcleanbuild | Clean Docker environment and rebuild from scratch |
| up2imp | Audit upstream changes and curate implementation list |
| qimpl | Context-aware autonomous implementation session |
| qfrontdev | Autonomous frontend implementation session |
| qbackenddev | Autonomous backend/infrastructure development session |
| pullndoc | Git pull upstream repo and document imported changes |

## Command Quick Reference

| Command | Input | Output |
|---------|-------|--------|
| initspec | Project info | .spec_system/ structure |
| createprd | Requirements doc | PRD/PRD.md |
| createuxprd | Design docs | PRD/PRD_UX.md |
| plansession | state.json, PRD | spec.md + tasks.md |
| implement | spec.md, tasks.md | implementation-notes.md |
| validate | All session files | validation.md |
| updateprd | validation.md | Updated state.json |
| audit | CONVENTIONS.md | Updated dev tools |
| pipeline | CONVENTIONS.md | Workflow files |
| infra | CONVENTIONS.md | Config files |
| documents | state.json, PRD | Updated docs |
| carryforward | Phase artifacts | CONSIDERATIONS.md |
| phasebuild | PRD | PRD/phase_NN/ |

## Task Format

```
- [ ] TNNN [SNNMM] [P] Action verb + what + where (`path/to/file`)
```

- `TNNN`: Sequential task ID (T001, T002, ...)
- `[SNNMM]`: Session reference (S0103 = Phase 01, Session 03)
- `[P]`: Optional parallelization marker
