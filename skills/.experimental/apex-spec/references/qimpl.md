# qimpl

Run an autonomous implementation session guided by a work file. The work file defines
the goals and serves as the workspace for tracking progress. Designed for focused,
high-quality implementation bursts that stay within session resource limits for optimal
output quality.

## Usage

```
qimpl <work-file>
```

- `<work-file>` -- Path to the markdown work file that defines the session goals
  and serves as the running workspace (e.g., `work.md`, `docs/impl-plan.md`)

## Rules

1. **Senior engineer mindset** -- Approach implementation like a craftsperson who
   obsesses over pristine code with zero errors, warnings, or issues. Be methodical,
   patient, and uncompromising on quality.
2. **Work file is your hub** -- Read goals from the work file, write results back to
   it. The work file persists across sessions as the source of truth.
3. **Work file is a guide, not gospel** -- You own the implementation. Verify its
   details and adapt as needed to accomplish the goals.
4. **Session resource discipline** -- Work autonomously but stop after approximately
   30 tool executions or when the session feels overloaded. Quality degrades in
   overloaded sessions.
5. **No assumptions** -- Never guess. Pattern match precisely. Do not skim when
   details are needed. Validate systematically. Look up and verify any details you
   are not confident in.
6. **No lying or "good enough"** -- Never misrepresent status. If something feels
   off, it probably is. Investigate rather than hand-wave.
7. **Read-only on spec system** -- Never modify state.json, session specs, or task
   checklists.
8. **ASCII only** -- All generated/modified files use characters 0-127 only.

## Steps

### 1. Load the work file

Read the work file provided by the user. Identify:
- The goal(s) of the session
- Any prior progress or context from previous sessions
- Any notes, constraints, or implementation guidance

### 2. Assess and plan

Review the current state of the codebase as it relates to the work file goals.
Verify that the work file's details are accurate -- file paths exist, assumptions
hold, referenced code matches expectations.

If anything in the work file is incorrect or outdated, note it and adapt your
approach accordingly.

### 3. Implement

Execute the work described in the work file. Follow these principles:
- Work through items methodically, one at a time
- Validate each change before moving to the next
- If you encounter uncertainty about an API, library, or pattern, look it up
  rather than guessing
- Track your session resource consumption

### 4. Monitor resource consumption

Keep a running awareness of resource usage:
- **Tool executions**: Begin wrapping up when approaching 30
- If the session feels overloaded, proceed to Step 5 rather than pushing further

### 5. Update the work file

Before ending the session, update the work file with:
- What was completed this session
- What remains to be done
- Current state of the implementation (what works, what is partial)
- Any concise notes that would help the next session pick up efficiently
  (gotchas discovered, decisions made, patterns established)
- Clear next steps so a fresh session can continue without re-investigation

## Output

Report to the user:
- What was accomplished in this session
- How much of the work file's goals were completed
- Whether the session ended due to completion or session resource discipline
- The work file has been updated for session continuity
