# qbackenddev

Run an autonomous backend, infrastructure, or general engineering session guided by a
work file. The work file defines the goals (implement, audit, plan, refactor, document,
convert, or review a partner's work) and serves as the running workspace for
cross-session continuity. Covers backend code, infrastructure, DevOps, CLI commands,
API layers, databases, and any non-frontend engineering work.

## Usage

```
qbackenddev <work-file>
```

- `<work-file>` -- Path to the markdown file that defines the session goals and
  tracks progress (e.g., `docs/backend/backend-audit.md`, `docs/infrastructure/infra-plan.md`,
  `tmp/final-plan.md`, `docs/ongoing_projects/MY_TECH_PRD.md`)

The work file determines the mode of work. It might contain:
- Implementation tasks to execute (session-by-session or phase-by-phase)
- An audit scope to analyze (backend files, infrastructure, CLI commands)
- A plan to create, refine, or merge from multiple draft plans
- A refactoring roadmap with architecture improvements
- Documentation to write or verify (API docs, pseudo-code conversions, changelogs)
- A partner engineer's work to review and validate

## Rules

1. **Senior engineer mindset** -- Obsess over pristine code with zero errors, warnings,
   or issues. Approach implementation like a craftsperson: methodical, patient, and
   uncompromising on quality.
2. **Work file is your hub** -- Read goals from the work file, write results and
   progress back to it. The work file persists across sessions.
3. **Work file is a guide, not gospel** -- You own the implementation. Verify its
   details against the actual codebase and adapt as needed.
4. **Work autonomously** -- Complete all tasks/sessions/phases in the work file
   without stopping to ask permission. Work through each item sequentially.
5. **Session resource discipline** -- Stop after approximately 30 tool executions
   or when the session feels overloaded. Quality degrades in overloaded sessions.
6. **No assumptions, no shortcuts, no lying** -- Never guess. Never skim when details
   are needed. Pattern match precisely. Validate systematically. Look up and verify
   any details you are not confident in. If something feels off, it probably is --
   investigate rather than hand-wave.
7. **Trust code over docs** -- When documentation seems stale or ambiguous, verify
   behavior in the actual codebase. Code is the single source of truth.
8. **Measure twice, cut once** -- Fully understand before implementing. Read the
   relevant files, understand the patterns, then make changes.
9. **Read-only on spec system** -- Never modify state.json, session specs, or task
   checklists.
10. **ASCII only** -- All generated/modified files use characters 0-127 only.

## Steps

### 1. Orient

Read the work file provided by the user. Identify:
- The goal(s) of the session (implement, audit, plan, refactor, document, review)
- Any prior progress or context from previous sessions
- The current phase/session/task to work on
- Any notes, constraints, or decisions from earlier sessions

If the work file references other documents (PRDs, changelogs, audit reports,
partner work, design docs, blueprint files), read those too for full context.

### 2. Analyze existing patterns

Before making any changes, study the codebase to understand:
- File/folder structure and naming conventions
- How components are registered, invoked, and connected
- Common patterns (argument parsing, error handling, output formatting, logging)
- Shared utilities, base classes, or middleware used across the codebase
- Database schemas, migration patterns, API contracts

This prevents introducing inconsistencies or reinventing existing solutions.

### 3. Verify

Before writing any code, verify the work file's claims against the actual codebase:
- Do referenced files, modules, and endpoints exist?
- Do described patterns and architectures match reality?
- Are documented APIs, schemas, and configs accurate?
- Has anything changed since the work file was last updated?

If anything is incorrect or outdated, note it and adapt your approach. Trust the
code, not the docs.

### 4. Execute

Work through the tasks defined in the work file. Follow the mode-specific guidance
below.

**For implementation work:**
- Work through sessions/tasks methodically, one at a time
- Make small, deliberate, atomic changes
- Validate each change before moving to the next
- Handle error cases, edge cases, and logging properly
- Follow existing patterns for argument parsing, output formatting, and error handling

**For audit work:**
- Analyze every relevant file thoroughly -- do not skip or skim
- Document file paths, line counts, and specific findings
- Identify concrete refactoring opportunities with rationale: architecture,
  structure, code organization, and developer navigation improvements
- Prioritize findings by impact and effort

**For planning work:**
- Analyze existing implementations to understand conventions before planning
- If merging multiple draft plans, include only clear, objective improvements
  from secondary sources
- Structure with clear headings, bullet points, and code snippets where helpful
- Aim for a document another senior engineer could implement without ambiguity
- No wordiness, no redundancy

**For review/validation work (partner engineer's output):**
- Verify every claim in the partner's document against the actual codebase
- Check for accuracy, completeness, and whether findings are up to date
- Add missing findings, correct inaccuracies, remove stale entries
- Preserve the partner's good work -- only modify what needs correction

**For documentation/conversion work:**
- Verify every detail against the actual codebase or source material
- Do not trust existing docs -- they may be outdated or contain mistakes
- Fact-check every word; no shortcuts, no assumptions, no fabrication
- When converting formats (e.g., blueprints to pseudo-code), preserve all
  functional logic faithfully

### 5. Monitor resource consumption

Keep a running awareness of resource usage:
- **Tool executions**: Begin wrapping up when approaching 30
- If the session feels overloaded, proceed to Step 6 rather than pushing further

### 6. Update the work file and wrap up

Before ending the session, update the work file with:
- What was completed this session
- What remains to be done
- Current state of the implementation (what works, what is partial)
- Any discoveries, decisions, or gotchas for the next session
- Clear next steps so a fresh session can continue without re-investigation
- If concise notes can improve the process moving forward, add them

If the work file references a changelog or other tracking documents, update
those too.

## Output

Report to the user:
- What was accomplished in this session
- How much of the work file's goals were completed
- Any issues, warnings, or quality concerns discovered
- Whether the session ended due to completion or session resource discipline
- The work file has been updated for session continuity
