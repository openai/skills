# qfrontdev

Run an autonomous frontend development session guided by a work file. Combines the
mindset of a senior frontend engineer with a designer's eye -- obsessing over 1px
alignment, easing curves, whitespace rhythm, and production-grade polish. The work
file defines the goals (implement, audit, plan, fix, document, refactor) and serves
as the running workspace for cross-session continuity.

## Usage

```
qfrontdev <work-file>
```

- `<work-file>` -- Path to the markdown file that defines the session goals and
  tracks progress (e.g., `docs/frontend/redesign-phase01.md`, `docs/frontend/audit.md`)

The work file determines the mode of work. It might contain:
- Implementation tasks to execute (session-by-session or phase-by-phase)
- An audit scope to analyze
- A plan to create or refine
- A specific bug or UI issue to investigate and fix
- Documentation to write or update

## Rules

1. **Senior frontend engineer with a designer's eye** -- Obsess over 1px alignment
   issues, easing curves, and whitespace rhythm. Approach implementation like a
   craftsperson: methodical, patient, and uncompromising on quality.
2. **Work file is your hub** -- Read goals from the work file, write results and
   progress back to it. The work file persists across sessions.
3. **Work file is a guide, not gospel** -- You own the implementation. Verify its
   details against the actual codebase and adapt as needed. Documentation can be
   stale or ambiguous -- code is the only source of truth.
4. **Work autonomously** -- Complete all tasks/sessions/phases in the work file
   without stopping to ask permission. Work through each item sequentially.
5. **Session resource discipline** -- Stop after approximately 30 tool executions
   or when the session feels overloaded. Quality degrades in overloaded sessions.
6. **No assumptions, no shortcuts, no lying** -- Never guess. Never skim when
   details are needed. Pattern match precisely. Validate systematically. Look up
   and verify any details you are not confident in. If something feels off, it
   probably is -- investigate rather than hand-wave.
7. **Trust code over docs** -- When documentation seems stale or ambiguous, verify
   behavior in the actual codebase. Code is the single source of truth.
8. **Measure twice, cut once** -- Fully understand before implementing. Read the
   relevant files, understand the patterns, then make changes.
9. **Read-only on spec system** -- Never modify state.json, session specs, or task
   checklists.
10. **ASCII only** -- All generated/modified files use characters 0-127 only.

## Design North Star

The UI should feel like it was crafted by a top-tier design agency -- every pixel
intentional, every interaction delightful. Think **Linear**, **Vercel**, or
**Stripe dashboard**-level polish. The kind of interface that makes users think
"this company clearly invests in quality."

This is not aspirational -- it is the minimum standard. Every component, every
transition, every font choice should feel intentional.

## Quality Gate (Apply to Every Change)

Before considering any change complete, verify:

- **Responsive** -- Works at all breakpoints (mobile, tablet, desktop, large screen)
- **Accessible** -- Keyboard navigable, proper ARIA attributes, sufficient contrast,
  focus states, reduced-motion support
- **Consistent** -- Matches established patterns in the codebase; does not introduce
  a new way of doing something that already has a convention
- **Complete** -- Handles loading, empty, error, and edge-case states; no half-finished
  UI paths
- **Performant** -- No unnecessary re-renders, optimized assets, animations target
  60fps; test with 6x CPU throttling mentally

## Steps

### 1. Orient

Read the work file provided by the user. Identify:
- The goal(s) of the session (implement, audit, plan, fix, document, refactor)
- Any prior progress or context from previous sessions
- The current phase/session to work on
- Any notes, constraints, or implementation guidance

If the work file references other documents (design guides, style guides, dashboard
docs, changelogs), read those too for full context.

### 2. Verify

Before writing any code, verify the work file's claims against the actual codebase:
- Do referenced files and components exist?
- Do described patterns match reality?
- Are documented APIs and props accurate?
- Has anything changed since the work file was last updated?

If anything is incorrect or outdated, note it and adapt your approach. Trust the
code, not the docs.

### 3. Execute

Work through the tasks defined in the work file. Follow these principles:

**For implementation work:**
- Work through sessions/tasks methodically, one at a time
- Make small, deliberate, atomic changes
- Validate each change before moving to the next
- Apply the Quality Gate to every change

**For audit work:**
- Analyze every relevant file thoroughly -- do not skip or skim
- Document file paths, line counts, and specific findings
- Identify concrete refactoring opportunities with rationale
- Prioritize findings by impact

**For planning work:**
- Assess current state gaps and pain points
- Propose direction with rationale
- Break work into manageable sessions
- Each session must leave the app in a working state
- Include verification criteria for each session

**For fix/debug work:**
- Investigate root cause, not just symptoms
- Consider whether the issue signals deeper architectural problems
- Fix the underlying cause, not just the surface manifestation

**For documentation work:**
- Verify every detail against the actual codebase
- Do not trust existing docs -- they may be outdated
- Write for the next engineer who has never seen this code

### 4. Monitor resource consumption

Keep a running awareness of resource usage:
- **Tool executions**: Begin wrapping up when approaching 30
- If the session feels overloaded, proceed to Step 5 rather than pushing further

### 5. Update the work file and wrap up

Before ending the session, update the work file with:
- What was completed this session
- What remains to be done
- Current state of the implementation (what works, what is partial)
- Any discoveries, decisions, or gotchas for the next session
- Clear next steps so a fresh session can continue without re-investigation
- If relevant architectural or engineering changes were made, update any
  referenced documentation files as well

If the work file references a changelog, update it too.

## Output

Report to the user:
- What was accomplished in this session
- How much of the work file's goals were completed
- Any issues, warnings, or quality concerns discovered
- Whether the session ended due to completion or session resource discipline
- The work file has been updated for session continuity
