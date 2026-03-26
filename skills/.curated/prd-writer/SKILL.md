---
name: "prd-writer"
description: "Create or refine a Product Requirements Document (PRD) for a software product, feature, or workflow. Use when the user wants a structured PRD with goals, personas, functional requirements, UX flows, success metrics, technical considerations, milestones, and traceable user stories with acceptance criteria."
---

# PRD Writer

Create a build-ready Product Requirements Document for a software product, feature, or workflow.

## Quick start

1. Confirm the product or feature being specified.
2. Identify the audience, problem, goals, constraints, and any non-goals.
3. Draft the PRD using the required outline below.
4. Expand the user stories until primary, alternative, and edge cases are covered.
5. Review the document for clarity, testability, and internal consistency.

If the user asks for a file, write the PRD to the requested path. If no path is requested, provide the PRD in the response and offer to save it afterward.

## Intake

Gather or infer:

- Product or feature scope
- Target users and roles
- Business objective
- Core user problems to solve
- Constraints, dependencies, and timeline expectations
- Any explicit exclusions

If important details are missing, make reasonable assumptions and state them briefly in the document rather than blocking.

## Required outline

Use sentence case for headings, except the document title.

The PRD should include these sections in this order:

1. Product overview
2. Goals
3. User personas
4. Functional requirements
5. User experience
6. Narrative
7. Success metrics
8. Technical considerations
9. Milestones & sequencing
10. User stories

### Section expectations

**Product overview**

- Document title and version
- Short summary of the project or feature
- Problem statement and scope

**Goals**

- Business goals
- User goals
- Non-goals

**User personas**

- Key user types
- Short persona details relevant to the product
- Role-based access expectations where applicable

**Functional requirements**

- Group requirements by theme where useful
- Mark priority for each requirement, preferably `P0`, `P1`, or `P2`
- Keep the wording concrete and implementation-guiding

**User experience**

- Entry points
- Core workflow
- Advanced or secondary flows
- Important UI/UX notes

**Narrative**

- One paragraph from the user's perspective describing the intended experience

**Success metrics**

- User-centric metrics
- Business metrics
- Technical or operational metrics

**Technical considerations**

- Integrations and dependencies
- Data handling, privacy, and security concerns
- Scalability or performance considerations
- Known risks or likely implementation challenges

**Milestones & sequencing**

- Suggested phases
- Rough ordering of work
- Team or delivery assumptions when useful

**User stories**

- Cover primary paths, alternate paths, and edge cases
- Use unique IDs such as `US-001`
- Format each story with:
  - ID
  - Title
  - Description
  - Acceptance criteria

## User story rules

- Every story must be testable.
- Acceptance criteria should be specific and observable.
- Include authentication or authorization stories if the product requires identity, account access, or restricted actions.
- Include operational or admin stories when they are necessary for a complete product.
- Do not stop at happy-path coverage.

## Output rules

- Write in clear product language, not engineering shorthand.
- Be specific enough that design and engineering can execute without reinterpreting basic intent.
- Do not use horizontal rules.
- Do not add a conclusion or footer after the user stories section.
- Keep names, casing, and terminology consistent throughout.
- Prefer "the product", "the feature", or "this tool" over invented marketing names unless the user provided one.

## Final review

Before finishing, verify:

- The goals align with the problem statement.
- Functional requirements map to the described user experience.
- Success metrics match the stated goals.
- User stories cover the scope end to end.
- Acceptance criteria are concrete enough to validate manually or with tests.
