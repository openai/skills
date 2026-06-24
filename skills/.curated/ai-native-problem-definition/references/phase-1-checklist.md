# Phase 1 Checklist

Use this reference when the user is shaping an early software idea.

## Core Questions

- Who experiences the problem?
- How often does it happen?
- What is the cost of not solving it?
- What current workaround exists?
- What makes the problem observable?
- What constraints could invalidate the solution?
- What simpler framing might solve the same problem?
- Is the proposed solution addressing the root problem or only a symptom?

## Critique Prompts

Ask direct questions such as:

- What are the weaknesses in this approach?
- What edge cases are being ignored?
- What constraints might invalidate this?
- Is there a simpler framing?
- What would make this project fail even if the implementation works?

## Platform Tradeoffs

Evaluate platform intentionally:

- Web app: easiest distribution, browser constraints, hosting and auth considerations.
- Mobile app: strong device integration, app-store and install friction.
- CLI: excellent for technical users, poor for nontechnical adoption.
- Backend service: useful for integrations and automation, needs API and ops discipline.
- Browser extension: close to browsing workflows, permission and maintenance constraints.

## Naming Test

Use naming to detect conceptual ambiguity. A good name should reflect the core function, avoid feature-level specificity, avoid trend language, and fit the intended user context.

## Completion Artifact

The phase is complete when this can be written clearly:

- Problem statement
- Candidate solution direction
- Constraints and non-goals
- Platform choice
- Stable summary
- Project name or naming direction
