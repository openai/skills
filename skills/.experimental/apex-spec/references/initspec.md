# initspec

Set up the complete `.spec_system/` directory structure and initial files for a new or existing project.

## Rules

1. **Never overwrite existing `.spec_system/state.json`** without explicit user confirmation
2. **ASCII-only characters** (0-127) in all generated files
3. **Unix LF line endings** only
4. **Minimal structure** - don't over-engineer the initial setup

## Steps

### 1. Check Current State

First, check if the spec system is already initialized:
- Look for `.spec_system/state.json`
- Check for `.spec_system/PRD/` directory
- Check for `.spec_system/specs/` directory

If already initialized, ask the user if they want to reinitialize (this will reset state).

### 2. Gather Project Information

Ask the user for:
- **Project name**: Name of the project
- **Project description**: Brief description of what the project does
- **First phase name**: Name for Phase 00 (default: "Foundation")

### 3. Create Directory Structure

Create the following directories:

```bash
mkdir -p .spec_system/PRD/phase_00
mkdir -p .spec_system/specs
mkdir -p .spec_system/audit
mkdir -p .spec_system/archive/backups
mkdir -p .spec_system/archive/sessions
mkdir -p .spec_system/archive/planning
mkdir -p .spec_system/archive/PRD
mkdir -p .spec_system/archive/phases
```

### 3a. Brownfield Monorepo Detection

Detect whether the project is a monorepo. **Skip this step entirely for greenfield (empty) projects** -- leave `monorepo: null` in state.json.

For brownfield projects (existing code present):

1. Source common.sh and call `detect_monorepo()` to check for workspace config files (pnpm-workspace.yaml, turbo.json, nx.json, package.json workspaces, Cargo.toml workspace, go.work, lerna.json)

2. If `detect_monorepo()` returns `detected: true`:
   - Display the detected indicator and discovered packages to the user
   - Ask the user to **confirm**, **edit** (add/remove packages), or **skip** (leave as null)
   - **Confirmed**: Set `monorepo: true` and store the packages array in state.json (Step 4)
   - **Edited**: Set `monorepo: true` with user-adjusted packages array
   - **Skipped**: Leave `monorepo: null` -- can be resolved later by createprd

3. If `detect_monorepo()` returns `detected: false`:
   - Leave `monorepo: null` (do NOT set to false here -- createprd may detect monorepo intent from PRD content)

**Important**: Never set `monorepo: false` during initspec. Only `null` (unknown) or `true` (confirmed). The createprd workflow step handles the `false` determination.

### 4. Create state.json

Create `.spec_system/state.json`:

```json
{
  "version": "2.0",
  "project_name": "[PROJECT_NAME]",
  "description": "[PROJECT_DESCRIPTION]",
  "current_phase": 0,
  "current_session": null,
  "monorepo": null,
  "phases": {
    "0": {
      "name": "[PHASE_NAME]",
      "status": "not_started",
      "session_count": 0
    }
  },
  "completed_sessions": [],
  "next_session_history": []
}
```

**If monorepo confirmed in Step 3a**, set `"monorepo": true` and add the packages array:

```json
{
  "monorepo": true,
  "packages": [
    {"name": "web", "path": "apps/web", "stack_hint": "TypeScript"},
    {"name": "api", "path": "apps/api", "stack_hint": "TypeScript"}
  ]
}
```

Otherwise, `"monorepo": null` and no `packages` field.

### 5. Create PRD Template

Create `.spec_system/PRD/PRD.md` with a starter template:

```markdown
# [PROJECT_NAME] - Product Requirements Document

## Overview

[PROJECT_DESCRIPTION]

## Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Phases

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| 00 | [PHASE_NAME] | TBD | Not Started |

## Phase 00: [PHASE_NAME]

### Objectives

1. [Objective 1]
2. [Objective 2]

### Sessions (To Be Defined)

Use plansession to get recommendations for sessions to implement.

## Technical Stack

- [Technology 1]
- [Technology 2]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### 6. Create CONSIDERATIONS.md

Create `.spec_system/CONSIDERATIONS.md` (institutional memory for AI assistants):

```markdown
# Considerations

> Institutional memory for AI assistants. Updated between phases via carryforward.
> **Line budget**: 600 max | **Last updated**: Phase 00 (YYYY-MM-DD)

---

## Active Concerns

Items requiring attention in upcoming phases. Review before each session.

### Technical Debt <!-- Max 5 items -->
*None yet - add items as technical debt accumulates.*

### External Dependencies <!-- Max 5 items -->
*None yet - add items when external API/service risks are identified.*

### Performance / Security <!-- Max 5 items -->
*None yet - add items when thresholds or security requirements emerge.*

### Architecture <!-- Max 5 items -->
*None yet - add items when architectural constraints are discovered.*

---

## Lessons Learned

Proven patterns and anti-patterns. Reference during implementation.

### What Worked <!-- Max 15 items -->
*None yet - add patterns that prove effective.*

### What to Avoid <!-- Max 10 items -->
*None yet - add anti-patterns discovered during implementation.*

### Tool/Library Notes <!-- Max 5 items -->
*None yet - add key insights about tools and libraries.*

---

## Resolved

Recently closed items (buffer - rotates out after 2 phases).

| Phase | Item | Resolution |
|-------|------|------------|
| - | *No resolved items yet* | - |

*Auto-generated by initspec. Updated by carryforward between phases.*
```

### 7. Create SECURITY-COMPLIANCE.md

Create `.spec_system/SECURITY-COMPLIANCE.md` (cumulative security posture and GDPR compliance record):

```markdown
# Security & Compliance

> Cumulative security posture and GDPR compliance record. Updated between phases via carryforward.
> **Line budget**: 1000 max | **Last updated**: Phase 00 (YYYY-MM-DD)

---

## Current Security Posture

### Overall: CLEAN

| Metric | Value |
|--------|-------|
| Open Findings | 0 |
| Critical/High | 0 |
| Medium/Low | 0 |
| Phases Audited | 0 |
| Last Clean Phase | -- |

## Open Findings

### Critical / High
*No open findings.*

### Medium / Low
*No open findings.*

## GDPR Compliance Status

### Overall: N/A

### Personal Data Inventory
*No personal data collected or processed.*

### Compliance Checklist

| Requirement | Status | Notes |
|------------|--------|-------|
| Data collection has documented purpose | N/A | No data collection yet |
| Consent obtained before data storage | N/A | No data collection yet |
| Data minimization verified | N/A | No data collection yet |
| Deletion/erasure path exists | N/A | No data collection yet |
| No PII in application logs | N/A | No logging yet |
| Third-party transfers documented | N/A | No external services yet |

## Dependency Security
*No dependencies audited yet.*

## Resolved Findings
*No resolved findings yet.*

## Phase History

| Phase | Sessions | Security | GDPR | Findings Opened | Findings Closed |
|-------|----------|----------|------|-----------------|-----------------|
| -- | -- | -- | -- | -- | -- |

## Recommendations
*None -- initial setup. Security review begins with first validate run.*

*Auto-generated by initspec. Updated by carryforward between phases.*
```

### 8. Create CONVENTIONS.md

Create `.spec_system/CONVENTIONS.md` (coding standards and team conventions):

```markdown
# CONVENTIONS.md

## Guiding Principles

- Optimize for readability over cleverness
- Code is written once, read many times
- Consistency beats personal preference
- If it can be automated, automate it
- When writing code: Make NO assumptions. Do not be lazy. Pattern match precisely. Do not skim when you need detailed info from documents. Validate systematically.

## Naming

- Be descriptive over concise: `getUserById` > `getUser` > `fetch`
- Booleans read as questions: `isActive`, `hasPermission`, `shouldRetry`
- Functions describe actions: `calculateTotal`, `validateInput`, `sendNotification`
- Avoid abbreviations unless universally understood (`id`, `url`, `config` are fine)
- Match domain language--use the same terms as product/design/stakeholders

## Files & Structure

- One concept per file where practical
- File names reflect their primary export or purpose
- Group by feature/domain, not by type (prefer `/orders/api.ts` over `/api/orders.ts`)
- Keep nesting shallow--if you're 4+ levels deep, reconsider

## Functions & Modules

- Functions do one thing
- If a function needs a comment explaining what it does, consider renaming it
- Keep functions short enough to read without scrolling
- Avoid side effects where possible; be explicit when they exist

## Comments

- Explain *why*, not *what*
- Delete commented-out code--that's what git is for
- TODOs include context: `// TODO(name): reason, ticket if applicable`
- Update or remove comments when code changes

## Error Handling

- Fail fast and loud in development
- Fail gracefully in production
- Errors should be actionable--include context for debugging
- Don't swallow errors silently

## Database Layer

### Connection
- Connection string source: [env var name -- never hardcoded]
- Pool size: [N]; separate URLs for: app, migrations, tests

### Migrations
- Tool: [detected] | Location: [path] | Naming: [pattern]
- CRITICAL: Never modify a migration already applied to shared environments
- Every migration must have a reverse/down

### Models / Schema
- Location: [path] | Naming: [convention] | Required columns: [timestamps, soft delete, etc.]

### Queries
- Parameterized only (no string concatenation)
- N+1 prevention: [chosen approach] | Transaction boundaries: [when to wrap]

### Seeding
- Script: [path] | Must be idempotent (safe to re-run)

### Testing
- Strategy: [separate DB / transaction rollback / in-memory] | Fixtures: [path]

### Vector / Embeddings (if applicable)
- Store: [pgvector / standalone] | Model: [name + dimensions]
- Index: [HNSW / IVFFlat] | Distance: [cosine / L2 / inner product]

## Testing

- Test behavior, not implementation
- A test's name should describe the scenario and expectation
- If it's hard to test, the design might need rethinking
- Flaky tests get fixed or deleted--never ignored

## Git & Version Control

- Commit messages: imperative mood, concise (`Add user validation` not `Added some validation stuff`)
- One logical change per commit
- Branch names: `type/short-description` (e.g., `feat/user-auth`, `fix/cart-total`)
- Keep commits atomic enough to revert safely

## Pull Requests

- Small PRs get better reviews
- Description explains the *what* and *why*--reviewers can see the *how*
- Link relevant tickets/context
- Review your own PR before requesting others

## Code Review

- Critique code, not people; ask questions rather than make demands
- Approve when it's good enough, not perfect; label nitpicks as such

## Dependencies

- Fewer dependencies = less risk
- Justify additions; prefer well-maintained, focused libraries
- Pin versions; update intentionally

## Local Dev Tools

| Category | Tool | Config |
|----------|------|--------|
| Formatter | not configured | - |
| Linter | not configured | - |
| Type Safety | not configured | - |
| Testing | not configured | - |
| Observability | not configured | - |
| Git Hooks | not configured | - |
| Database | not configured | - |

**Conditional**: The "Database Layer" section above is only included when DB signals are detected during brownfield initspec (docker-compose with DB service, `.env` with `DATABASE_URL`, migration tool config files present). For greenfield projects, this section is deferred to createprd.

## When In Doubt

- Ask
- Leave it better than you found it
- Ship, learn, iterate
```

**If monorepo confirmed in Step 3a**, append a Workspace Structure section to CONVENTIONS.md:

```markdown
## Workspace Structure

| Package | Path | Stack |
|---------|------|-------|
| [name] | [path] | [stack_hint] |

### Cross-Package Rules

- Import from sibling packages via workspace aliases, not relative paths
- Shared types live in a dedicated shared/common package
- Each package owns its own tests; integration tests live at repo root
- Changes spanning multiple packages require explicit cross-package session scope

### Database Ownership
| Database | Owner Package | Type | Shared By |
| [name] | [package path] | [type] | [consumers] |

- Migrations live in the owner package
- Consuming packages use the owner's API, not direct DB access
```

### 9. Create Phase PRD

Create `.spec_system/PRD/phase_00/PRD_phase_00.md`:

```markdown
# Phase 00: [PHASE_NAME]

**Status**: Not Started
**Progress**: 0/0 sessions (0%)

## Overview

[Phase description - to be filled in]

## Progress Tracker

| Session | Name | Status | Validated |
|---------|------|--------|-----------|
| - | No sessions defined | - | - |

## Next Steps

Run plansession to get the first session recommendation.
```

### 10. Copy Scripts Locally (Optional)

Ask user: "Copy scripts locally for customization, or use skill scripts (recommended)?"

- **Skill** (default): `scripts/` directory bundled with this skill - auto-updates with skill
- **Local**: `.spec_system/scripts/` - per-project customization, won't auto-update

If user wants local scripts:

```bash
mkdir -p .spec_system/scripts
cp scripts/*.sh .spec_system/scripts/
chmod +x .spec_system/scripts/*.sh
```

### 11. Report Success

Tell the user:

```
Apex Spec System initialized!

Created:
- .spec_system/state.json (project state tracking)
- .spec_system/PRD/PRD.md (product requirements document)
- .spec_system/PRD/phase_00/PRD_phase_00.md (phase tracker)
- .spec_system/CONSIDERATIONS.md (institutional memory for AI)
- .spec_system/SECURITY-COMPLIANCE.md (security posture & GDPR compliance)
- .spec_system/CONVENTIONS.md (coding standards and team conventions)
- .spec_system/specs/ (session specifications directory)
- .spec_system/audit/ (audit reports directory)
- .spec_system/archive/ (completed work archive)

[If monorepo detected and confirmed:]
Monorepo: Detected via [indicator] with N packages
[If monorepo not detected:]
Monorepo: Not detected (can be set later via createprd)

Next Steps:
1. Edit .spec_system/PRD/PRD.md with your project requirements
2. Customize .spec_system/CONVENTIONS.md with your project's coding standards (optional but recommended)
3. Run phasebuild to define sessions for Phase 00 (recommended for new projects)
   OR run plansession directly if you already know your first session
4. Follow the workflow: plansession -> implement -> validate -> updateprd
5. Repeat step 4 until all sessions in the phase are complete
6. Run carryforward (optional) to capture lessons learned, then phasebuild for next phase
```
