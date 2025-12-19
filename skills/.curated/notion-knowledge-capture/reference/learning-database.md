# Learning/Post-Mortem Database

**Purpose**: Capture learnings from incidents, projects, or experiences.

## Schema

| Property | Type | Options | Purpose |
|----------|------|---------|---------|
| **Title** | title | - | Event or project name |
| **Date** | date | - | When it happened |
| **Type** | select | Incident, Project, Experiment, Retrospective | Learning type |
| **Severity** | select | Critical, Major, Minor | Impact level (for incidents) |
| **Team** | people | - | Who was involved |
| **Key Learnings** | number | - | Count of learnings |
| **Action Items** | relation | Links to tasks | Follow-up actions |

## Content Template

Each learning page should include:
- **What Happened**: Situation description
- **What Went Well**: Success factors
- **What Didn't Go Well**: Problems encountered
- **Root Causes**: Why things happened
- **Learnings**: Key takeaways
- **Action Items**: Improvements to implement

## Best Practices

1. **Blameless approach**: Focus on systems and processes, not individuals
2. **Document quickly**: Capture while memory is fresh
3. **Identify root causes**: Go beyond surface-level problems
4. **Create action items**: Turn learnings into improvements
5. **Follow up**: Track that action items are completed
6. **Share widely**: Make learnings accessible to entire team

