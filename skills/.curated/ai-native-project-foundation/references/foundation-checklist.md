# Foundation Checklist

Use this reference after an implementation plan exists and before coding begins.

## Plan Persistence Prompt

```text
Produce a structured, phased development plan for an audience of software engineers based on:

<Previously-generated-development-plan>

Separate MVP from subsequent phases.

Persist the output in `docs/implementation-plan.md`.
```

## Agent-Led Plan Review Prompt

```text
Review `docs/implementation-plan.md` critically.

Identify:

- Ambiguous requirements
- Missing constraints
- Hidden complexity
- Unrealistic phase boundaries
- Architectural instability risks
- Implicit assumptions that require clarification

For each issue found:

- Explain the concern
- Ask for explicit clarification
- Suggest a possible refinement if appropriate

Do not modify the plan yet.
First, surface uncertainties and request precision.
```

## Workspace Readiness

Confirm:

- The target project directory is clear.
- `docs/implementation-plan.md` exists and matches the accepted plan.
- The plan has been reviewed for ambiguity.
- Clarifications are resolved or listed explicitly.
- Version control exists or is intentionally initialized.
- No MVP implementation has started before foundation readiness.
