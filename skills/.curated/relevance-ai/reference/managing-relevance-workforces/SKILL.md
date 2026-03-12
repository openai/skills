---
name: managing-relevance-workforces
description: Manages Relevance AI workforces (multi-agent systems) - creating workflows, configuring nodes/edges, triggering execution, and debugging runs. Use when building multi-agent pipelines, connecting agents together, or debugging workforce execution.
---

# Managing Relevance AI Workforces

Skill for creating, configuring, triggering, and debugging Relevance AI workforces (multi-agent systems).

> **📚 Full API Documentation:** If MCP tools don't cover your use case, see `https://api-{region}.stack.tryrelevance.com/latest/documentation` (replace `{region}` with your project's region)
> **✅ RECOMMENDED APPROACH**: Workforces are the **official way** to build multi-agent systems.
> The legacy pattern of adding sub-agents to an agent's `actions` array is **DEPRECATED**.
> Always use workforces for agent-to-agent orchestration.

## When to Use

- Creating multi-agent workflows (pipelines)
- Connecting agents together with edges
- Configuring handovers between agents
- Triggering workforce execution
- Debugging workforce runs (seeing what each agent produced)

## MCP Tools

| Tool                                    | Description                                |
| --------------------------------------- | ------------------------------------------ |
| `relevance_list_workforces`             | List all workforces                        |
| `relevance_get_workforce`               | Get full workforce config with nodes/edges |
| `relevance_create_workforce`            | Create new workforce with agents           |
| `relevance_update_workforce`            | Update workforce graph/metadata            |
| `relevance_delete_workforce`            | Delete a workforce                         |
| `relevance_trigger_workforce`           | Trigger workforce with a message           |
| `relevance_get_workforce_task_messages` | Get execution details and agent outputs    |

## Quick Start: Create Workforce

```typescript
// 1. Create workforce with agents in sequence
relevance_create_workforce({
  name: 'Research Pipeline',
  description: 'Research -> Summarize -> Report',
  agents: [
    { agentId: 'researcher-agent-id' },
    { agentId: 'summarizer-agent-id' },
    { agentId: 'reporter-agent-id' },
  ],
  // Default: creates linear chain with forced-handover edges
});

// 2. Trigger the workforce
const { workforce_task_id } = await relevance_trigger_workforce({
  workforceId: 'workforce-id',
  message: 'Research AI trends in 2024',
});

// 3. Get execution details (what each agent produced)
const execution = await relevance_get_workforce_task_messages({
  workforceId: 'workforce-id',
  taskId: workforce_task_id,
});
// execution.workforce_state = "completed" | "running" | etc.
// execution.results contains each agent's outputs
```

## Testing: Define Before Building

**IMPORTANT:** Before building any workforce, create a testing rubric and get user approval.

### Rubric Template

```
Testing Rubric for "[Workforce Name]":

□ End-to-End Flow
  - [Trigger → Final output works with typical input]
  - [All agents in chain execute successfully]

□ Agent Handovers
  - [Data passes correctly between agents]
  - [Each agent receives expected context]

□ Edge Cases
  - [Handles agent failures gracefully]
  - [Timeouts are handled appropriately]

□ Output Quality
  - [Final output meets business requirements]
  - [Intermediate outputs are logged/accessible]
```

### Testing Workflow

1. **Present rubric to user** before building
2. **Get approval** or incorporate feedback
3. **Build the workforce**
4. **Trigger with test input** using `relevance_trigger_workforce`
5. **Check execution** using `relevance_get_workforce_task_messages`
6. **Report results** with pass/fail for each check

### Example: Research Pipeline Rubric

```
Testing Rubric for "Lead Research Pipeline":

□ End-to-End Flow
  - Given a LinkedIn URL, produces enriched lead report
  - All 3 agents (Researcher → Enricher → Reporter) complete

□ Agent Handovers
  - Researcher output includes profile data
  - Enricher receives profile and adds company context
  - Reporter receives all data and formats final output

□ Edge Cases
  - Invalid LinkedIn URL produces clear error (not silent failure)
  - Private profiles handled with partial data message

□ Output Quality
  - Final report is structured and actionable
  - Sources/data provenance is clear
```

---

## Reference Files

- [concepts.md](concepts.md) - Core concepts: nodes, edges, threading, handovers
- [debugging.md](debugging.md) - How to debug workforce execution

## URL Patterns

```
# Workforce edit page
https://app.relevanceai.com/workforces/{region}/{project}/{workforceId}

# Workforce task view
https://app.relevanceai.com/workforces/{region}/{project}/{workforceId}/tasks/{taskId}
```
