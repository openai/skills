# Structured Improvement Playbook

Use this reference after the MVP works and the goal is durability.

## Project Guidelines

`docs/project-guidelines.md` should be short and specific. Keep:

- Architectural invariants
- Non-negotiable constraints
- Testing expectations for critical paths
- Data, API, deployment, or state-management rules that are project-specific

Remove:

- Generic coding advice
- Boilerplate
- Redundant rules
- Long tutorials

## AI-Assisted Code Review Prompt

```text
Review the changes in this feature branch compared to the main branch.

Analyze the diff for:

- Logical errors
- Edge cases
- Unintended behavioral changes
- Performance regressions
- Architectural inconsistencies
- Violations of `docs/project-guidelines.md`
- Increased coupling or hidden complexity
- Missing test coverage (if tests exist)

For each issue:

- Explain the risk clearly.
- Classify severity (low, medium, high).
- Suggest corrective action.
- Indicate whether it should block the merge.

Do not rewrite the code.
Focus on analysis and risk identification.
```

## Technical Debt Template

```markdown
# Technical Debt Roadmap

## <Item Title>

- Description:
- Risk level:
- Expected benefit:
- Estimated complexity:
- Suggested priority:
- Related files or systems:
```

## Refactoring Rules

- Do not change external behavior unintentionally.
- Protect changes with tests when possible.
- Refactor in isolated commits.
- Re-run verification after each improvement.
- Treat new feature work as a new planning cycle.
