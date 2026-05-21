---
name: ai-native-implementation-plan
description: "Use when converting a clarified software problem into an MVP-first phased roadmap with scope, risks, dependencies, and validation criteria."
---

# AI Native Implementation Plan

Use this skill after problem definition is stable enough to plan execution. The goal is not to design the final system in full; it is to create a bounded MVP and a phased path forward.

## Workflow

1. Re-anchor on the problem.
   - Load or request the problem statement, target user, candidate solution, constraints, platform, and success criteria.
   - Refuse to plan around vague ambition; return to problem definition if key inputs are missing.

2. Define the MVP sharply.
   - Make Phase 1 the smallest system that validates the core hypothesis.
   - State what is included, what is excluded, and what hypothesis is being tested.
   - If the MVP cannot fit in one concise paragraph, narrow it.

3. Produce a phased roadmap.
   - For each phase include objective, scope, key deliverables, dependencies, risks, and validation criteria.
   - Add value incrementally without forcing rework of prior structure.
   - Keep architectural stability visible between phases.

4. Recommend a practical tech stack.
   - Optimize for the problem, constraints, deployment path, and maintenance burden.
   - Avoid premature optimization and unnecessary infrastructure.

5. Critique the draft plan.
   - Identify hidden complexity, unrealistic ordering, scope creep, unstable architecture, and weak validation criteria.
   - Revise only after making the concern explicit.

## Required Output

Produce copy-pastable markdown suitable for `docs/implementation-plan.md` unless the user asks for a different artifact.

The plan must contain:

- Original problem traceability
- MVP hypothesis
- MVP included scope
- MVP excluded scope
- Recommended tech stack
- Phased roadmap
- Validation criteria for each phase
- Risks and dependencies
- Open clarifications

## Stop Condition

Stop when the roadmap is coherent, bounded, and aligned with the original problem. Do not start implementation.

See `references/plan-template.md` for the canonical prompt and output shape.
