# implement

Execute each task in the session's task list, updating progress as you go.

## RULES

1. **Make NO assumptions.** Before editing, read the relevant code and comments; pattern-match precisely, validate systematically.
2. **Follow `CONVENTIONS.md`.** All code must follow project-specific coding standards.
3. **ASCII-only characters** and Unix LF line endings in all output.
4. **Never lie and implement exactly what's in the spec** -- no lying, no extra features, no refactoring unrelated code.
5. **Update `tasks.md` immediately** after completing each task -- never batch checkbox updates.
6. **Write tests as specified** -- ensure they pass before moving on.
7. **Ensure logging and error handling** -- no silent failures.
8. **Prefer cohesive, moderately sized modules** -- avoid multi-thousand-line god files; if a file grows beyond ~400-600 LOC or multiple responsibilities, schedule a refactor.
9. **Behavioral correctness over speed** - Code must handle edge cases, cleanup, and failure paths before a task is marked done. A checked task with a behavioral bug costs 10x more to find in a later audit.

### No Deferral Policy

- NEVER mark a task as "pending", "requires X", or "blocked" if the blocker is something YOU can resolve
- If a service needs to be running, START IT (e.g., `docker compose up -d db`)
- If a dependency needs installing, INSTALL IT
- If a directory needs creating, CREATE IT
- "The environment isn't set up" is NOT a blocker -- setting it up IS the task
- The ONLY valid blocker is something that requires USER input or credentials you don't have
- If you skip a task that was executable, that is a **critical failure**

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

This returns structured JSON including:
- `current_session` - The session to implement
- `current_session_dir_exists` - Whether specs directory exists
- `current_session_files` - Files already in the session directory
- `monorepo` - true/false/null from state.json
- `packages` - Array of registered packages (empty if not monorepo)
- `active_package` - Resolved package context (null if not applicable)

**IMPORTANT**: Use the `current_session` value from this output. If `current_session` is `null`, run plansession yourself to set one up. Only ask the user if that command requires user input.

### 1a. Determine Package Context (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in the JSON output.

Resolve the active package for this session:

1. **spec.md header**: Read the `Package:` field from the session's spec.md (set during plansession)
2. **active_package from script**: If spec.md has no Package field, use `active_package` from the JSON output
3. **Prompt user**: If neither resolves a package, ask the user which package this session targets (or whether it is cross-cutting)

Store the resolved package path for use in Steps 2, 4, and 5. A `null` package means this is a cross-cutting session.

### 2. Verify Environment Prerequisites (REQUIRED)

Run the prerequisite checker to verify the environment is ready. Use the same local-first pattern:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/check-prereqs.sh --json --env
else
  bash scripts/check-prereqs.sh --json --env
fi
```

This verifies:
- `.spec_system/` directory and `state.json` are valid
- `jq` is installed (required for scripts)
- `git` availability (optional)

**Monorepo**: If a package was resolved in Step 1a, add `--package <path>` to verify package-specific prerequisites and workspace tooling:

```bash
# Example: check-prereqs.sh --json --env --package apps/web
```

**If any environment check fails**: FIX the issues yourself. Install missing tools, create missing directories, start required services. The ONLY reason to stop is if you need credentials or input only the user can provide.

**Optional - Tool Verification**: After reading spec.md (next step), if the Prerequisites section lists required tools, also run:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/check-prereqs.sh --json --tools "tool1,tool2,tool3"
else
  bash scripts/check-prereqs.sh --json --tools "tool1,tool2,tool3"
fi
```

This catches missing tools BEFORE implementation starts, preventing mid-session failures.

**Optional - Database Prerequisites**: If `.spec_system/CONVENTIONS.md` has a "Database Layer" section, verify:
1. Database service is running (`docker compose ps` or connection test)
2. Migrations are current (no pending migrations)
If checks fail, resolve them (start services, run migrations) before proceeding.

### 3. Read Session Context

Using the `current_session` value from the script output, read:
- `.spec_system/specs/[current-session]/spec.md` - Full specification
- `.spec_system/specs/[current-session]/tasks.md` - Task checklist
- `.spec_system/specs/[current-session]/implementation-notes.md` - Progress log (if exists)
- `.spec_system/specs/[current-session]/security-compliance.md` - Prior security report (if exists from previous validation run)
- `.spec_system/CONVENTIONS.md` - Project coding conventions (if exists)

**Resuming?** If `implementation-notes.md` and completed tasks already exist, read them to understand current state and resume from the next incomplete task.

### 3a. Load Behavioral Quality Checklist (BQC)

BQC applies when the session produces application code (not pure configuration, documentation, or infrastructure-as-code). If the session is entirely non-code work, skip to Step 4.

---

#### Behavioral Quality Checklist

**Mandatory edge-case checklist** -- verify applicable items before marking EACH task complete:

- [ ] **Resource cleanup**: Every resource acquired in a scoped lifecycle is released when that scope ends. No leaked timers, dangling subscriptions, unclosed connections, or orphaned async tasks.
- [ ] **Duplicate action prevention**: Every state-mutating operation is protected against duplicate triggers while in-flight. No double-submits, no unguarded retries, no concurrent write races.
- [ ] **State freshness on re-entry**: When a context is re-entered (reopened, revisited, reconnected, retried), state is explicitly reset or revalidated. No stale data from a prior lifecycle.
- [ ] **Trust boundary enforcement**: All inputs crossing a trust boundary are validated with explicit schema or type checks, and all access is authorized at the enforcement point closest to the protected resource. Never trust upstream callers.
- [ ] **Failure path completeness**: Every operation that can fail has an explicit, caller-visible failure path. No silent swallows, no blank screens, no infinite spinners, no generic 500s.
- [ ] **Concurrency safety**: Shared mutable state accessed from multiple execution contexts is protected against races. No unguarded read-modify-write sequences.
- [ ] **External dependency resilience**: Every call to an external system has a timeout, a retry/backoff strategy, and a defined failure path. No unbounded waits.
- [ ] **Contract alignment**: Interfaces between components match their declared contracts. Response shapes match client types. Event payloads match schemas. Enum handling is exhaustive.
- [ ] **Error information boundaries**: Errors exposed to external callers reveal only stable, intentional information. No stack traces, internal paths, or secrets in responses or logs.
- [ ] **Accessibility and platform compliance**: Interactive elements participate in the platform's accessibility model with appropriate labels, focus management, and input method support.

**How to apply**: After each task, check ONLY the items relevant to the code you touched. A task adding a timed background operation must satisfy resource cleanup + failure path. A task adding a write endpoint must satisfy duplicate prevention + trust boundaries + error information boundaries. A task adding an interactive dialog must satisfy state freshness + accessibility. Not every item applies to every task -- but every item applies somewhere.

### 4. Initialize Implementation Notes

If `implementation-notes.md` doesn't exist, create it:

```markdown
# Implementation Notes

**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Started**: [YYYY-MM-DD HH:MM]
**Last Updated**: [YYYY-MM-DD HH:MM]

---

## Session Progress

| Metric | Value |
|--------|-------|
| Tasks Completed | 0 / N |
| Estimated Remaining | X hours |
| Blockers | 0 |

---

## Task Log

### [YYYY-MM-DD] - Session Start

**Environment verified**:
- [x] Prerequisites confirmed
- [x] Tools available
- [x] Directory structure ready
[IF DATABASE SESSION]
- [x] Database running
- [x] Migrations current
[END IF]

---
```

### 5. Work Through Tasks

For each incomplete task:

#### A. Identify Next Task
Find the first unchecked `- [ ]` task in tasks.md

#### B. Implement Task
- Read the task description carefully
- Read surrounding code to match existing patterns before writing new code
- Follow the spec's technical approach and CONVENTIONS.md standards
- If `docs/adr/` exists, review relevant Architecture Decision Records and follow their decisions
- Implement the required changes
- **Monorepo path validation**: If a package was resolved in Step 1a, verify that files being created or modified fall within the declared package directory (e.g., `apps/web/...`). Warn if a task references files outside the package scope -- this may indicate scope creep. Exception: cross-cutting sessions (package: null) may touch any file.
- **Behavioral quality verification** (if BQC loaded in Step 3a): Before marking this task complete, scan your code against the applicable checklist items. Fix violations now -- do not defer. Note any BQC fixes in the task log entry (Step 5D).

#### C. Update Task Status
In `tasks.md`, change:
```markdown
- [ ] T001 [S0101] Task description
```
To:
```markdown
- [x] T001 [S0101] Task description
```

#### D. Log Progress
Add to `.spec_system/specs/[current-session]/implementation-notes.md`:
```markdown
### Task TNNN - [Description]

**Started**: [YYYY-MM-DD HH:MM]
**Completed**: [YYYY-MM-DD HH:MM]
**Duration**: [X] minutes

**Notes**:
- [Implementation details]
- [Decisions made]

**Files Changed**:
- `path/to/file` - [changes made]

**BQC Fixes** (if any):
- [Category]: [What was caught and fixed] (`path/to/file`)

[MONOREPO ONLY - include if any files fall outside the declared package scope]
**Out-of-Scope Files** (files outside declared package):
- `other-package/path/file` - [justification]
[END MONOREPO ONLY]
```

### 6. Handle Blockers

If you encounter an obstacle, RESOLVE IT YOURSELF before documenting:

- **Service not running?** Start it (e.g., `docker compose up -d db`)
- **Dependency missing?** Install it
- **Directory missing?** Create it
- **Config file missing?** Generate it from the spec
- **Database not running?** Start it (`docker compose up -d [service]`)
- **Migrations pending?** Run migration tool to apply them
- **Connection refused?** Check `DATABASE_URL` in `.env`, verify port
- **"The environment isn't set up"** is NOT a blocker -- setting it up IS the task

The ONLY valid reason to pause and ask the user is when you need credentials, API keys, or decisions only a human can make. If you skip a task that was executable, that is a **critical failure**.

After resolving, document in implementation-notes.md:
```markdown
## Blockers & Solutions

### Blocker N: [Title]

**Description**: [What was blocking]
**Impact**: [Which tasks affected]
**Resolution**: [How YOU resolved it]
**Time Lost**: [Duration]
```

### 7. Track Design Decisions

When making implementation choices:

```markdown
## Design Decisions

### Decision N: [Title]

**Context**: [Why decision needed]
**Options Considered**:
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]

**Chosen**: [Option]
**Rationale**: [Why]
```

### 8. Track Progress and Checkpoint

After each task:
- Update Progress Summary table in tasks.md
- Update implementation-notes.md
- Report status to user: tasks done (X of Y), next task

**Checkpoint every 3-5 tasks minimum** and before any risky operations. If approaching context limits, document current state and next task in implementation-notes.md.

## Output

When all tasks complete:
```
Session implementation complete!
Tasks: N/N (100%)
BQC: [X] fixes applied across [Y] tasks [or "N/A - no application code in session"]

Run the validate workflow step to verify session completeness.
```
