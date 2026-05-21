---
name: ai-native-project-foundation
description: "Use when setting up a project workspace from a plan: persist docs/implementation-plan.md, review ambiguities, and establish version control."
---

# AI Native Project Foundation

Use this skill after a phased implementation plan exists. The goal is to create structural readiness before implementation begins.

## Workflow

1. Inspect the workspace first.
   - Identify whether the user is in an existing repo or creating a new project.
   - Do not overwrite existing plans or source files without reading them.
   - If no workspace is clear, ask for the target directory.

2. Persist the plan.
   - Create `docs/implementation-plan.md` when missing.
   - Use the previously generated plan as source material.
   - Keep the file structured for software engineers, not as conversational notes.

3. Run an agent-led plan review.
   - Surface ambiguous requirements, missing constraints, hidden complexity, unrealistic phase boundaries, architectural risks, and implicit assumptions.
   - Do not silently rewrite the plan before exposing uncertainties.

4. Resolve clarifications.
   - Ask concise questions when the plan cannot be made structurally coherent.
   - Update `docs/implementation-plan.md` only after the clarification is available or a conservative assumption is justified.

5. Establish version-control readiness.
   - If git is already present, report the current branch and dirty state.
   - If no version control exists and the user asked to establish the foundation, initialize it or ask first when the target is ambiguous.
   - Do not begin implementation during this skill.

## Required Output

- Created or confirmed project workspace
- Created or updated `docs/implementation-plan.md`
- Plan-review findings and clarifications
- Version-control status
- Readiness statement for controlled implementation

## Stop Condition

Stop when the plan is persisted, reviewed, clarified, and structurally stable. Do not start coding the MVP.

See `references/foundation-checklist.md` for the persistence prompt and plan-review checklist.
