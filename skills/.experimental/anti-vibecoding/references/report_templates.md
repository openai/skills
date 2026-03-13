# Report Templates

Use these templates to keep reports deterministic and easy to review.

## Project Route Template

```markdown
## Project Route
- Selected project: <name/path>
- Why selected: <top evidence>
- Memory source: <existing memory | startup provisional memory>
- Routing confidence: <high|medium|low>
```

## Current Codebase Considerations Template

```markdown
## Current Codebase Considerations
- Confirmed source-of-truth files: <list>
- Important integration boundaries: <list>
- Existing behavior constraints: <list>
- Codebase unknowns still blocking confidence: <list>
```

## Tool Trace Template

```markdown
## Tool Trace
- Tool: <name>
- Why this tool now: <reason>
- What it checked: <scope>
- Result summary: <key fact>
- Impact on certainty: <up/down and why>
```

Emit one block per tool action when verbose tracing is required.

## Milestone Coaching Report Template

```markdown
## Milestone Coaching Report
- Milestone: <name>
- Outcome: <achieved/not achieved>

### Mistakes or Weak Assumptions
1. <issue>
2. <issue>

### Where the Developer Is Wrong
1. <incorrect belief or decision>
   - Correction: <what is correct>
   - Evidence: <facts from session>

### Missing Knowledge Areas
1. <gap>
2. <gap>

### What to Learn Next
1. <topic> - <why it matters now>
2. <topic> - <why it matters now>

### Immediate Next Actions
1. <small concrete action>
2. <small concrete action>
```

Rules:

1. Use direct language and evidence.
2. Avoid vague praise-only summaries.
3. Prioritize highest-impact correction first.
4. Keep learning actions specific and bounded.

## Readiness Score Template

```markdown
## Readiness Score
- Overall: <score>/14 (<RED|YELLOW|GREEN>)
- Requirements: <0-2>
- Project Route and Memory: <0-2>
- Current Codebase Context: <0-2>
- Constraints: <0-2>
- Naming (Micro): <0-2>
- Naming (Macro): <0-2>
- Acceptance Criteria: <0-2>
- Missing for GREEN: <bullet list>
```

## Clarification Pack Template

```markdown
## Clarification Pack
### Requirements
1. <question>

### Project Route and Memory
1. <question>

### Current Codebase Context
1. <question>

### Constraints
1. <question>

### Naming (Micro)
1. <question>

### Naming (Macro)
1. <question>

### Acceptance Criteria
1. <question>
```

## Next Questions Template

```markdown
## Next Questions
1. <highest-priority unresolved question>
2. <second unresolved question>
```
