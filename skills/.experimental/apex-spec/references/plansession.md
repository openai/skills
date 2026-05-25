# plansession

Analyze project state, recommend the next session, create its specification, and generate the task checklist -- all in one step.

## Rules

1. **Script first** - Always run `analyze-project.sh --json` before any analysis
2. **Trust the script** - Use JSON output as authoritative state; do not parse `state.json` directly
3. **One session at a time** - Only recommend one session
4. **Respect dependencies** - Don't skip prerequisites
5. **MVP focus** - Recommend core features before polish
6. **Scope discipline** - Sessions must be 12-25 tasks, 2-4 hours
7. **Hard limits**: max 25 tasks, max 4 hours, single clear objective
8. **Do not invent scope** - derive everything from PRD and session stub
9. **Incorporate CONVENTIONS.md** - naming, file structure, and testing philosophy must be reflected in the spec
10. **Incorporate CONSIDERATIONS.md** - address relevant active concerns and lessons learned
11. **ASCII-only characters** and Unix LF line endings in all output
12. **Task sizing**: ~20-25 minutes each, single file focus when possible, clear atomic action
13. **Every task must have**: task ID (`TNNN`), session ref (`[SPPSS]`), action verb, target file path
14. **Mark `[P]`** when tasks create independent files with no interdependency
15. **Sequence by**: dependencies first, then setup -> foundation -> implementation -> testing
16. **Behavioral quality by design** - When a Behavioral Quality Checklist (BQC) applies (session produces application code), embed edge-case handling into task descriptions. "Create delete dialog" becomes "Create delete dialog (with typed confirmation, disable-while-pending, state reset on close)". Explicit requirements get implemented; implicit ones get skipped.

## Steps

### 1. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script to get reliable state facts. Local scripts (`.spec_system/scripts/`) take precedence over plugin scripts if they exist:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

This returns structured JSON with:
- `current_phase` - Current phase number
- `current_session` - Active session (or null)
- `completed_sessions` - List of completed session IDs
- `candidate_sessions` - Sessions in current phase with completion status; each candidate includes a `package` field (parsed from stub `Package:` annotation, or null)
- `phases` - All phases with status and session counts
- `monorepo` - true/false/null from state.json
- `packages` - Array of registered packages (empty if not monorepo)
- `active_package` - Resolved package context from `--package` flag or CWD (null if not applicable)
- `monorepo_detection` - Auto-detection result when monorepo is null (null otherwise)

**IMPORTANT**: Use this JSON output as ground truth for all state facts. Do not re-read state.json directly - the script provides authoritative state data.

### 1a. Determine Package Context (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in the JSON output.

When working in a monorepo, resolve the active package for this session. Priority order:

1. **User statement**: If the user explicitly names a package (e.g., "plan a session for apps/web"), use that
2. **Stub annotation**: If the selected candidate has a `package` field from its stub, use that
3. **active_package from script**: If `analyze-project.sh` resolved a package via `--package` flag or CWD inference, use that
4. **Prompt user**: If none of the above resolves a package, ask the user which package this session targets (or whether it is cross-cutting)

Store the resolved package path for use in Steps 4 and 5.

### 2. Read PRD Content for Semantic Analysis

With the state facts established, read these files for context:
- `.spec_system/PRD/PRD.md` - Master project requirements
- `.spec_system/PRD/PRD_UX.md` - UX requirements (if exists -- use for UI-focused sessions)
- Candidate session files from the JSON output (use the `path` field)
- `.spec_system/CONSIDERATIONS.md` - Institutional memory (if exists)
- `.spec_system/SECURITY-COMPLIANCE.md` - Security posture and GDPR compliance (if exists)
- `.spec_system/CONVENTIONS.md` - Project coding conventions (if exists)

Focus on understanding:
- Session objectives and scope
- Prerequisites and dependencies
- Logical ordering
- **Active Concerns** that may influence session priority or approach
- **Lessons Learned** relevant to candidate sessions
- **Open security findings** that may affect session scope or approach
- Naming, file placement, and testing approach from CONVENTIONS.md
- If CONVENTIONS.md has a "Database Layer" section and the session involves data layer work (new tables, schema changes, migrations), ensure task planning includes migration, seed update, and DB integration test tasks

### 3. Analyze and Recommend

Using the deterministic state + semantic understanding:

**Determine:**
- Which candidates have unmet prerequisites (based on `completed_sessions`)
- Natural next session based on dependencies
- Complexity and scope assessment

**Evaluate each candidate by:**
- Prerequisites met (check against `completed_sessions` array)
- Dependencies completed
- Logical flow in project progression

If multiple sessions ready: Choose based on dependencies, complexity, project flow.
If session blocked: Recommend alternative with explanation.
If phase complete: Suggest running phasebuild for the next phase.

### 4. Create Session Directory and Specification

Create the session directory and generate `spec.md`:

```
.spec_system/specs/phaseNN-sessionNN-name/
|-- spec.md
\-- (tasks.md created in next step)
```

Generate `spec.md` with all sections filled in:

```markdown
# Session Specification

**Session ID**: `phaseNN-sessionNN-name`
**Phase**: NN - Phase Name
**Status**: Not Started
**Created**: [YYYY-MM-DD]
[MONOREPO ONLY - include these lines when monorepo: true]
**Package**: [package-path]
**Package Stack**: [stack]
[END MONOREPO ONLY - omit both lines for single-repo projects]

---

## 1. Session Overview

[2-3 paragraphs explaining what this session accomplishes, why it matters, and how it fits into the larger project]

---

## 2. Objectives

1. [Specific, measurable objective]
2. [Specific, measurable objective]
3. [Specific, measurable objective]
4. [Specific, measurable objective]

---

## 3. Prerequisites

### Required Sessions
- [x] `phaseNN-sessionNN-name` - [what it provides]

### Required Tools/Knowledge
- [tool/knowledge item]

### Environment Requirements
- [environment requirement]

---

## 4. Scope

### In Scope (MVP)
- [PRD requirement in actor/capability form] - [brief implementation note]
- [PRD requirement in actor/capability form] - [brief implementation note]

### Out of Scope (Deferred)
- [PRD requirement] - *Reason: [why deferred]*

---

## 5. Technical Approach

### Architecture
[Describe the technical architecture and design]

### Design Patterns
- [Pattern]: [Why using it]

### Technology Stack
- [Technology and version]

---

## 6. Deliverables

### Files to Create
| File | Purpose | Est. Lines |
|------|---------|------------|
| `path/to/file` | Description | ~100 |

### Files to Modify
| File | Changes | Est. Lines |
|------|---------|------------|
| `path/to/file` | Description | ~20 |

---

## 7. Success Criteria

### Functional Requirements
- [ ] [Testable requirement]

### Testing Requirements
- [ ] Unit tests written and passing
- [ ] Manual testing completed

### Non-Functional Requirements
- [ ] [Relevant NFR from PRD with measurable target]

### Quality Gates
- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions

---

## 8. Implementation Notes

### Key Considerations
- [Important consideration]

### Potential Challenges
- [Challenge]: [Mitigation]

### Relevant Considerations
<!-- From CONSIDERATIONS.md - omit section if none apply -->
- [P##] **[Active Concern]**: How it affects this session and mitigation
- [P##] **[Lesson Learned]**: How we're applying it in this implementation

### Behavioral Quality Focus
<!-- Include when session produces application code. Omit if no BQC applies. -->
Checklist active: Yes
Top behavioral risks for this session:
- [Risk 1 relevant to this session's deliverables]
- [Risk 2 relevant to this session's deliverables]
- [Risk 3 relevant to this session's deliverables]

---

## 9. Testing Strategy

### Unit Tests
- [What to test]

### Integration Tests
- [What to test]

### Manual Testing
- [Test scenario]

### Edge Cases
- [Edge case to handle]

---

## 10. Dependencies

### External Libraries
- [Library]: [version]

### Other Sessions
- **Depends on**: [sessions]
- **Depended by**: [sessions]

---

## Next Steps

Run the implement workflow step to begin AI-led implementation.
```

### 4a. Enrich Task Descriptions with BQC

**Skip if** the session produces no application code.

When BQC applies, enrich task descriptions in Step 5 using this table:

| If task involves... | Append to description... |
|---------------------|--------------------------|
| Scoped lifecycle with async work or subscriptions | "with cleanup on scope exit for all acquired resources" |
| State-mutating action (submit, delete, send, write) | "with duplicate-trigger prevention while in-flight" |
| View or screen that fetches or displays remote data | "with explicit loading, empty, error, and offline states" |
| Handler for external input (endpoint, consumer, deep link, event) | "with schema-validated input and explicit error mapping" |
| Write path (create/update/delete, single or multi-step) | "with idempotency protection, transaction boundaries, and compensation on failure" |
| Call to external system (API, database, third-party service) | "with timeout, retry/backoff, and failure-path handling" |
| Access-controlled resource or action | "with authorization enforced at the boundary closest to the resource" |
| Query or list returning unbounded results | "with bounded pagination, validated filters, and deterministic ordering" |
| Reopenable or revisitable context (dialog, form, screen, connection) | "with state reset or revalidation on re-entry" |
| Permission-gated feature | "with denied/restricted/revoked handling and fallback behavior" |
| Interactive control or element | "with platform-appropriate accessibility labels, focus management, and input support" |
| Optimistic state update | "with scoped rollback on error" |
| Component consuming external contract (API response, event payload) | "with types matching declared contract; exhaustive enum handling" |

These add 5-15 words per task but prevent the 10x-cost bugs found in later audits.

### 5. Generate Task Checklist

From the spec, identify deliverables, success criteria, technical approach, testing requirements, and dependencies between tasks. Then create `tasks.md` in the session directory:

```markdown
# Task Checklist

**Session ID**: `phaseNN-sessionNN-name`
**Total Tasks**: [N]
**Estimated Duration**: [X-Y] hours
**Created**: [YYYY-MM-DD]

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallelizable (can run with other [P] tasks)
- `[SNNMM]` = Session reference (NN=phase number, MM=session number)
- `TNNN` = Task ID

---

## Progress Summary

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Setup | N | 0 | N |
| Foundation | N | 0 | N |
| Implementation | N | 0 | N |
| Testing | N | 0 | N |
| **Total** | **N** | **0** | **N** |

---

## Setup (N tasks)

Initial configuration and environment preparation.

- [ ] T001 [SPPSS] Verify prerequisites met (tools, dependencies)
- [ ] T002 [SPPSS] Create directory structure for deliverables

---

## Foundation (N tasks)

Core structures and base implementations.

- [ ] T003 [SPPSS] [P] Create [component] (`path/to/file`)
- [ ] T004 [SPPSS] [P] Define [interface/type] (`path/to/file`)
- [ ] T005 [SPPSS] Implement [base functionality] (`path/to/file`)

---

## Implementation (N tasks)

Main feature implementation.

- [ ] T006 [SPPSS] Implement [feature part 1] (`path/to/file`)
- [ ] T007 [SPPSS] Implement [feature part 2] (`path/to/file`)
- [ ] T008 [SPPSS] [P] Add [component A] (`path/to/file`)
- [ ] T009 [SPPSS] [P] Add [component B] (`path/to/file`)
- [ ] T010 [SPPSS] Wire up [integration] (`path/to/file`)
- [ ] T011 [SPPSS] Add error handling (`path/to/file`)

---

## Testing (N tasks)

Verification and quality assurance.

- [ ] T012 [SPPSS] [P] Write unit tests for [component] (`tests/path`)
- [ ] T013 [SPPSS] [P] Write unit tests for [component] (`tests/path`)
- [ ] T014 [SPPSS] Run test suite and verify passing
- [ ] T015 [SPPSS] Validate ASCII encoding on all files
- [ ] T016 [SPPSS] Manual testing and verification

---

## Completion Checklist

Before marking session complete:

- [ ] All tasks marked `[x]`
- [ ] All tests passing
- [ ] All files ASCII-encoded
- [ ] implementation-notes.md updated
- [ ] Ready for the validate workflow step

---

## Next Steps

Run the implement workflow step to begin AI-led implementation.
```

### Path Scoping Rules (Monorepo Only)

When `monorepo: true`, apply these path conventions in tasks.md:

- **All file paths must be package-relative from the repo root** (e.g., `apps/web/src/auth.ts`, not `src/auth.ts`)
- **Single-package sessions**: All paths should start with the package path prefix
- **Cross-package sessions**: Group tasks by package using subheadings within each category:

```markdown
## Implementation (N tasks)

### apps/web

- [ ] T006 [SPPSS] Implement auth page (`apps/web/src/pages/auth.tsx`)
- [ ] T007 [SPPSS] Add auth hook (`apps/web/src/hooks/useAuth.ts`)

### apps/api

- [ ] T008 [SPPSS] Implement auth endpoint (`apps/api/src/routes/auth.ts`)
```

For single-repo projects, paths remain unchanged (relative to project root as usual).

## Category Budgets

| Category | Tasks | Purpose |
|----------|-------|---------|
| Setup | 2-4 | Environment, directories, config |
| Foundation | 4-8 | Core types, interfaces, base classes |
| Implementation | 8-15 | Main feature logic |
| Testing | 3-5 | Tests, validation, verification |

### 6. Update State

Update `.spec_system/state.json`:

```json
{
  "current_session": "phaseNN-sessionNN-name",
  "next_session_history": [
    {
      "date": "YYYY-MM-DD",
      "session": "phaseNN-sessionNN-name",
      "status": "planned"
    }
  ]
}
```

- Set `current_session` to the session ID
- Add a single entry to `next_session_history` with status `planned`
- **Monorepo only**: Include an optional `package` field in the history entry when a package was resolved in Step 1a:
  ```json
  {
    "date": "YYYY-MM-DD",
    "session": "phaseNN-sessionNN-name",
    "package": "apps/web",
    "status": "planned"
  }
  ```
  Omit the `package` field for single-repo projects or cross-cutting sessions.

### 7. Archive Stale Specs

Keep `.spec_system/specs/` lean by archiving old session specs. **Retention rule**: only keep specs from the current phase and one phase back. Move everything older to `.spec_system/archive/sessions/`.

Example: If currently on Phase 3, keep Phase 2 and Phase 3 specs. Archive Phase 0 and Phase 1 specs.

---

## Output

After creating spec.md and tasks.md, summarize to the user:
- Recommended session name and why it's next
- Key deliverables
- Total task count and category breakdown
- Estimated duration
- Key parallelization opportunities

Prompt them to run the implement workflow step to begin.
