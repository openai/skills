# Implementation Plan Template

Use this reference to produce an MVP-first phased roadmap.

## Canonical Planning Prompt

```text
Generate a structured development plan for this project based on the defined problem statement.

The plan must:

1. Be divided into clearly defined phases.
2. Isolate a sharply scoped MVP as Phase 1.
3. Explicitly state what is included and excluded from the MVP.
4. Define the hypothesis the MVP is validating.
5. Decompose subsequent phases into incremental expansions.
6. Preserve architectural stability between phases.
7. Avoid unnecessary complexity.
8. Prevent premature optimization.
9. Suggest a recommended tech stack optimized for the problem requirements.

For each phase, include:

- Objective
- Scope
- Key deliverables
- Dependencies
- Risks
- Validation criteria

Constraints:

- Do not design the final system in full detail upfront.
- Favor progressive complexity over full-system design.
- Maintain traceability to the original problem.
- Avoid introducing features that do not directly serve the core problem.

Output the development plan in structured copy-pastable markdown.
```

## Recommended Plan Shape

```markdown
# <Project Name> Implementation Plan

## Problem Traceability

## MVP Definition

### Hypothesis

### Included

### Excluded

### First Testable State

## Recommended Tech Stack

## Phase 1 - MVP

### Objective
### Scope
### Deliverables
### Dependencies
### Risks
### Validation Criteria

## Phase 2 - <Expansion>

## Phase 3 - <Expansion>

## Open Questions
```

## Review Checklist

- Is Phase 1 the smallest system that tests the core hypothesis?
- Are exclusions explicit?
- Does each phase add coherent value?
- Are dependencies ordered logically?
- Are validation criteria observable?
- Did any feature appear without a direct link to the original problem?
