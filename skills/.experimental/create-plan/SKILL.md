---
name: create-plan
description: Create a concise markdown plan. Use when a user asks for a plan before coding, refactors, migrations, feature work, or any ambiguous task where sequencing and scope control matter. Use only when the user explicitly asks for a plan and keep it read-only: do not run scripts or create/update files.
metadata:
  short-description: Create a plan
---

# Create Plan

## Goal

Turn a user prompt into a **single, actionable plan** delivered in the final assistant message (not saved to a file).

**Output contract**
- Create a plan in markdown using the template below.
- Do **not** implement code changes.
  - Output the plan directly in the response; do not write or update files.
- Keep the plan short, ordered, and executable (default 6–10 checklist items).
- Do not preface the plan with meta explanations; output only the plan.

## When to use

Use when the user asks to plan, design an approach, scope work, or prepare before implementation. Avoid purely mechanical tasks (e.g., “rename a variable”) unless the user explicitly wants a plan.

## Minimal workflow

1. **Scan context quickly**
   - Read `README.md` and any obvious docs (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Skim relevant files (the ones most likely touched).
   - Identify constraints (language, frameworks, CI/test commands, deployment shape).

2. **Ask follow-ups only if blocking**
   - Ask **at most 1–2 questions**.
   - Only ask if you cannot responsibly plan without the answer; prefer multiple-choice.
   - If unsure but not blocked, make a reasonable assumption and proceed.

3. **Create a plan using the template**
   - Start with **1 short paragraph** describing the intent and approach.
   - Clearly call out what is **in scope** and what is **not in scope** in short.
   - Then provide a **small checklist** (default 6–10 items).
   - Each checklist item should be a concrete action and, when helpful, mention files/commands.
   - Include at least one item for **tests/validation** and one for **edge cases/risk** when applicable.

## Writing rules

- **Keep bullets few**: default 6–10 checklist items.
- **Make items atomic and ordered**: discovery → changes → tests → rollout.
- **Verb-first**: “Add…”, “Refactor…”, “Verify…”, “Ship…”.
- Include at least one item for **tests/validation** and one for **edge cases/risk** when applicable.
- If there are unknowns, include a tiny **Open questions** section (max 3).

## Plan template (follow exactly)

```markdown
# Plan

<1–3 sentences: what we’re doing, why, and the high-level approach.>

## Scope
- In:
- Out:

## Action items
[ ] <Step 1>
[ ] <Step 2>
[ ] <Step 3>
[ ] <Step 4>
[ ] <Step 5>
[ ] <Step 6>

## Open questions
- <Question 1>
- <Question 2>
- <Question 3>

## Checklist item guidance
Good checklist items:
- Point to likely files/modules: src/..., app/..., services/...
- Name concrete validation: “Run npm test”, “Add unit tests for X”
- Include safe rollout when relevant: feature flag, migration plan, rollback note

Avoid:
- Vague steps (“handle backend”, “do auth”)
- Too many micro-steps
- Writing code snippets (keep the plan implementation-agnostic
