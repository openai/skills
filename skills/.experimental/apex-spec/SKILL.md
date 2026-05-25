---
name: apex-spec
description: >
  Specification-driven workflow system for AI-assisted development.
  Use when the user mentions "spec system", "session workflow", "create PRD",
  "UX PRD", "plan session", "implement session", "validate session",
  "phase build", "session scope", "task checklist", "initspec", "plansession",
  "audit", "pipeline", "infra", "carryforward", "documents", "copush",
  "sculpt-ui", "docker build", "upstream changes", "quick implement",
  "quick frontend", "quick backend", "pull upstream",
  or when working in a project containing a .spec_system/ directory.
  Philosophy: 1 session = 1 spec = 2-4 hours (12-25 tasks).
version: 2.0.9-codex
---

# Apex Spec Workflow

A specification-driven workflow system for AI-assisted development that breaks
large projects into manageable 2-4 hour sessions with 12-25 tasks each.

## Core Philosophy

**1 session = 1 spec = 2-4 hours (12-25 tasks)**

Break large projects into manageable, well-scoped implementation sessions that
fit within AI context windows and human attention spans.

A collection of sessions is a phase. A collection of phases is a mature/late
technical PRD.

## Session Scope Rules

### Hard Limits (Reject if Exceeded)

| Limit | Value |
|-------|-------|
| Maximum tasks | 25 |
| Maximum duration | 4 hours |
| Objectives | Single clear objective |

### Ideal Targets

| Target | Value |
|--------|-------|
| Task count | 12-25 (sweet spot: 20) |
| Duration | 2-3 hours |
| Focus | Stable/late MVP |

## The 13-Command Workflow

The workflow has **3 distinct stages**:

### Stage 1: INITIALIZATION (One-Time Setup)

```
initspec           ->  Set up spec system in project
      |
      v
createprd          ->  Generate PRD from requirements doc (optional)
  OR                   OR
[User Action]      ->  Manually populate PRD with requirements
      |
      v
createuxprd        ->  Generate UX PRD from design docs (optional)
  OR                   OR
[User Action]      ->  Manually populate UX PRD with requirements
      |
      v
phasebuild         ->  Create first phase structure (session stubs)
```

### Stage 2: SESSIONS WORKFLOW (Repeat Until Phase Complete)

```
plansession    ->  Analyze project, create spec + task checklist
      |
      v
implement      ->  AI-led task-by-task implementation
      |
      v
validate       ->  Verify session completeness
      |
      v
updateprd      ->  Sync PRD, mark session complete
      |
      +-------------> Loop back to plansession
                      until ALL phase sessions complete
```

### Stage 3: PHASE TRANSITION (After All Previous Phase Sessions Are Complete)

```
audit              ->  Local dev tooling (formatter, linter, types, tests)
      |
      v
pipeline           ->  CI/CD workflows (quality, build, security)
      |
      v
infra              ->  Production infrastructure (health, security, deploy)
      |
      v
carryforward       ->  Capture lessons learned (optional but recommended)
      |
      v
documents          ->  Audit and update documentation
      |
      v
[User Action]      ->  Manual testing and LLM audit (HIGHLY recommended)
      |
      v
phasebuild         ->  Create next phase structure
      |
      v
                   ->  Return to Stage 2 for new phase
```

### Utility Commands (Safe at Any Time)

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

---

## Command Dispatch

When the user requests a specific workflow step, read the corresponding
reference document from this skill's references/ directory and follow
its instructions exactly. Match the user's intent to the closest entry
in the table below.

### Stage 1: Initialization Commands

| User Keywords | Reference File | Description |
|---------------|----------------|-------------|
| "init", "initialize", "setup spec" | references/initspec.md | Set up spec system in project |
| "create PRD", "PRD", "requirements" | references/createprd.md | Generate master PRD from requirements |
| "UX PRD", "design PRD" | references/createuxprd.md | Generate UX PRD from design docs |
| "phase", "new phase", "phase build" | references/phasebuild.md | Create phase structure with session stubs |

### Stage 2: Session Workflow Commands

| User Keywords | Reference File | Description |
|---------------|----------------|-------------|
| "plan session", "next session" | references/plansession.md | Analyze project, create spec and task checklist |
| "implement", "execute tasks" | references/implement.md | AI-led task-by-task implementation |
| "validate", "verify session" | references/validate.md | Verify session completeness |
| "update PRD", "mark complete" | references/updateprd.md | Sync PRD, mark session complete |

### Stage 3: Phase Transition Commands

| User Keywords | Reference File | Description |
|---------------|----------------|-------------|
| "audit", "dev tools", "linting" | references/audit.md | Local dev tooling setup |
| "pipeline", "CI/CD", "workflows" | references/pipeline.md | CI/CD workflow configuration |
| "infra", "infrastructure" | references/infra.md | Production infrastructure setup |
| "carry forward", "lessons learned" | references/carryforward.md | Capture lessons and security posture |
| "documents", "documentation" | references/documents.md | Audit and update documentation |

### Utility Commands

| User Keywords | Reference File | Description |
|---------------|----------------|-------------|
| "copush", "push", "bump version" | references/copush.md | Pull, bump, commit, push |
| "sculpt", "UI design", "frontend design" | references/sculpt-ui.md | Distinctive frontend interface design |
| "docker build" | references/dockbuild.md | Docker Compose build and start |
| "docker clean", "docker rebuild" | references/dockcleanbuild.md | Clean Docker rebuild |
| "upstream", "upstream changes" | references/up2imp.md | Audit upstream changes |
| "quick implement" | references/qimpl.md | Context-aware autonomous implementation |
| "quick frontend" | references/qfrontdev.md | Autonomous frontend development |
| "quick backend" | references/qbackenddev.md | Autonomous backend development |
| "pull upstream", "pull and document" | references/pullndoc.md | Pull and document upstream changes |

**Total**: 22 commands mapped to 22 reference files.

---

## Directory Structure

Projects using this system follow this layout:

```
project/
|-- .spec_system/               # All spec system files
|   |-- state.json              # Project state tracking
|   |-- CONSIDERATIONS.md       # Institutional memory (lessons learned)
|   |-- SECURITY-COMPLIANCE.md  # Security posture and compliance
|   |-- CONVENTIONS.md          # Project coding standards
|   |-- PRD/                    # Product requirements
|   |   |-- PRD.md              # Master PRD
|   |   \-- phase_NN/           # Phase definitions
|   |-- specs/                  # Implementation specs
|   |   \-- phaseNN-sessionNN-name/
|   |       |-- spec.md
|   |       |-- tasks.md
|   |       |-- implementation-notes.md
|   |       |-- security-compliance.md
|   |       \-- validation.md
|   |-- scripts/                # Bash automation (copied during init)
|   \-- archive/                # Completed work
\-- (project source files)
```

### Monorepo Support

The system auto-detects monorepo structures. Single `.spec_system/` at the
repo root. Sessions reference their target package in metadata (spec.md
header and state.json), not in directory names. Sessions interleave across
packages within a phase.

---

## Scripts

Project analysis scripts provide deterministic state facts and environment
verification. Scripts are copied to `.spec_system/scripts/` during
initialization (via the initspec workflow step).

### Script Locations

Scripts can be found in two places. **Local scripts take precedence**:

1. **Local** (per-project): `.spec_system/scripts/` -- copied during init
2. **Skill directory**: `scripts/` -- bundled with this skill

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `analyze-project.sh` | Deterministic project state | `bash .spec_system/scripts/analyze-project.sh --json` |
| `check-prereqs.sh` | Environment and tool verification | `bash .spec_system/scripts/check-prereqs.sh --json --env` |
| `common.sh` | Shared functions (sourced by other scripts) | Sourced automatically |

### Local-First Resolution Pattern

Commands that need scripts should check for local copies first:

```bash
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

---

## Task Design

### Task Format

```
- [ ] TNNN [SNNMM] [P] Action verb + what + where (`path/to/file`)
```

Components:
- `TNNN`: Sequential task ID (T001, T002, ...)
- `[SNNMM]`: Session reference (S0103 = Phase 01, Session 03)
- `[P]`: Optional parallelization marker
- Description: Action verb + clear description
- Path: File being created or modified

### ASCII Encoding (Non-Negotiable)

All files must use ASCII-only characters (code points 0-127):
- NO Unicode characters, emoji, smart quotes, or em-dashes
- Use straight quotes (" ') and hyphens (-) only
- Unix LF line endings (no CRLF)

---

## Quick Reference

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| initspec | Initialize spec system | Project info | .spec_system/ structure |
| createprd | Generate master PRD | Requirements doc | PRD/PRD.md |
| createuxprd | Generate UX PRD | Design docs | PRD/PRD_UX.md |
| plansession | Analyze, spec, task list | state.json, PRD | spec.md + tasks.md |
| implement | Code implementation | spec.md, tasks.md | implementation-notes.md |
| validate | Verify completeness | All session files | validation.md |
| updateprd | Mark complete | validation.md | Updated state.json |
| audit | Local dev tooling | CONVENTIONS.md | Updated tools |
| pipeline | CI/CD workflows | CONVENTIONS.md | Workflow files |
| infra | Production infra | CONVENTIONS.md | Config files |
| documents | Audit/update docs | state.json, PRD | Updated docs |
| carryforward | Capture lessons | Phase artifacts | CONSIDERATIONS.md |
| phasebuild | Create new phase | PRD | PRD/phase_NN/ |
