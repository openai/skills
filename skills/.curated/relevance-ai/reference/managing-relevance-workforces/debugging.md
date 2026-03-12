# Debugging Workforce Execution

## Getting Execution Details

After triggering a workforce, use `relevance_get_workforce_task_messages` to see what happened:

```typescript
// 1. Trigger workforce
const { workforce_task_id } = await relevance_trigger_workforce({
  workforceId: 'my-workforce',
  message: 'Process this request',
});

// 2. Wait for completion, then get details
const execution = await relevance_get_workforce_task_messages({
  workforceId: 'my-workforce',
  taskId: workforce_task_id,
});

// Check overall status: execution.workforce_state
// Possible values: "completed" | "running" | "pending-approval" | "execution-limit-reached" | "errored-pending-approval" | "escalated"
```

## Understanding the Response

The `results` array contains execution events with nested agent messages:

```typescript
{
  workforce_state: "completed",
  results: [
    {
      item_id: "...",
      insert_date_: "2026-01-21T01:00:00Z",
      content: {
        type: "workforce-agent-run",
        node_id: "agent-researcher",
        agent_details: {
          agent_id: "xxx",
          name: "Lead Researcher"
        },
        task_details: {
          conversation_id: "abc123",  // Agent's conversation ID
          finished_state: "completed"
        }
      },
      children: [
        // Nested messages from this agent
        { content: { type: "assistant-message", text: "I found..." } },
        { content: { type: "tool-run", tool_details: { name: "Google Search" }, output: {...} } }
      ]
    },
    // More agent runs...
  ]
}
```

## Content Types

| Type                       | Meaning                           |
| -------------------------- | --------------------------------- |
| `workforce-agent-run`      | Agent execution started           |
| `assistant-message`        | Agent's response text             |
| `tool-run`                 | Tool the agent used (with output) |
| `workforce-agent-handover` | Handoff to another agent          |
| `user-message`             | User input                        |

## Finding Specific Outputs

### Get All Agent Runs

```typescript
const agentRuns = execution.results.filter(
  (r) => r.content.type === 'workforce-agent-run'
);

// Each run contains:
// - run.content.agent_details?.name — Agent name
// - run.content.task_details?.finished_state — Completion status
// - run.content.task_details?.conversation_id — Agent's conversation ID
```

### Find Tool Outputs (e.g., Video URL)

```typescript
function findToolOutput(results, toolName) {
  for (const item of results) {
    // Check children for tool runs
    if (item.children) {
      for (const child of item.children) {
        if (
          child.content?.type === 'tool-run' &&
          child.content?.tool_details?.name?.includes(toolName)
        ) {
          return child.content.output;
        }
      }
    }
  }
  return null;
}

const videoUrl = findToolOutput(execution.results, 'Permanent Save File');
```

### Get Individual Agent Conversation

If you need more details, use the `conversation_id` with `relevance_get_task_view`:

```typescript
// Get conversation_id from workforce task messages
const agentRun = execution.results.find(
  (r) =>
    r.content.type === 'workforce-agent-run' &&
    r.content.agent_details?.name === 'Video Agent'
);
const conversationId = agentRun?.content.task_details?.conversation_id;

// Get full conversation details
const taskView = await relevance_get_task_view({
  agentId: agentRun?.content.agent_details?.agent_id,
  taskId: conversationId,
});
// taskView.agentResponse, taskView.toolCalls, taskView.artifacts
```

## Common Issues

### Workforce stuck in "running"

**Possible causes:**

- Agent waiting for approval (`action_behaviour: "always-ask"`)
- Agent hit autonomy limit
- Tool execution taking long time

**Debug:**

```typescript
const execution = await relevance_get_workforce_task_messages({
  workforceId: '...',
  taskId: '...',
});

// Check execution.pending_approvals — if non-empty, agents are waiting for approval
// Check each item in execution.results where content.type === "workforce-agent-run"
// Look at task_details.finished_state — any agent not "completed" may be the blocker
```

### Agent not receiving context from previous agent

**Cause:** Using `always-create-new` threading instead of `always-same`

**Fix:** Update edge config:

```typescript
{
  config: {
    edge_type: "forced-handover",
    config: {
      threading_behavior: { type: "always-same" }  // Not "always-create-new"
    }
  }
}
```

### Agent with tools appears to have no tools

**Cause:** Wrong `region` in agent's actions

**Debug:**

```typescript
// Call relevance_get_agent_tools({ agentId: "..." })
// If chains is empty, tools are not attached — check region in agent's actions config
```

### Delivery/Send agent runs before content is created

**Cause:** Wrong workflow order

**Fix:** Agents that SEND/DELIVER should be LAST in the pipeline:

```
✅ Research → Generate → Deliver
❌ Research → Deliver → Generate
```
