---
name: ai-native-problem-definition
description: "Use when shaping a new software idea before planning: pressure-test problem, assumptions, constraints, platform, MVP direction, and project name."
---

# AI Native Problem Definition

Use this skill to turn an early software idea into bounded clarity before any implementation planning.

## Workflow

1. Establish the concrete problem.
   - Identify who experiences it, how often it occurs, and what it costs when unsolved.
   - Reject vague framing such as "I want to build an app" until the friction is observable.

2. Pressure-test the user's initial direction.
   - Ask what weakness, edge case, constraint, or simpler framing may invalidate the idea.
   - Distinguish root problem from symptom.
   - Compare the candidate solution against at least one simpler alternative when useful.

3. Define constraints and non-goals.
   - Capture platform, distribution, data, privacy, time, budget, integration, maintenance, and user-behavior constraints.
   - Mark assumptions explicitly instead of treating them as facts.

4. Choose the platform intentionally.
   - Explain tradeoffs for web, mobile, CLI, backend service, browser extension, or other candidates.
   - Treat platform as an architectural constraint, not a default.

5. Use naming as a stress test.
   - Generate project-name candidates only after the problem and direction are stable enough.
   - Flag naming difficulty as a possible sign of scope ambiguity.

6. Summarize and iterate.
   - After each major clarification, restate the current understanding.
   - If the summary does not match the user's intent, continue refinement instead of moving to planning.

## Required Output

When the phase is complete, produce a concise artifact containing:

- Problem statement
- Target user or context
- Cost of the unsolved problem
- Candidate solution direction
- Key assumptions
- Constraints and non-goals
- Chosen platform and rationale
- Success criteria
- Project name or naming shortlist
- Open questions, if any

## Stop Condition

Do not generate an implementation plan until the problem can be stated clearly and defended under critique.

See `references/phase-1-checklist.md` for the full checklist and reusable critique questions.
