---
name: "postman-readiness"
description: "Use when evaluating whether an API is agent-ready, scanning an OpenAPI spec for AI compatibility, or improving an API for AI agent consumption."
metadata:
  short-description: "Assess whether an API is agent-ready"
---

# Postman Readiness

Assess whether an API is discoverable, understandable, callable, and recoverable for AI agents without human intervention.

## When to use

Use this skill when the user asks whether an API is agent-ready, wants a spec scanned for AI compatibility, or wants prioritized remediation guidance.

## Workflow

1. Find the API definition locally or in Postman.
2. Validate that the spec is parseable and contains at least `info` and `paths`.
3. Evaluate the readiness checks and calculate per-check, per-pillar, and overall scores.
4. Present the verdict, pillar breakdown, and top remediation priorities.
5. Suggest next workflows such as docs, mocks, tests, or sync once the API is in better shape.

## Scoring

- Critical failures block practical agent usage.
- A passing result means 70 percent or higher with zero critical failures.

## References

- `references/pillars.md` for the evaluation dimensions.
- `examples/sample-readiness-report.md` for the report shape.
