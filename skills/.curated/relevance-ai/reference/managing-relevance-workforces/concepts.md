# Workforce Core Concepts

A **workforce** is a multi-agent system represented as a directed graph of nodes and edges.

## Structure

```typescript
{
  workforce_metadata: {
    name: string,
    type: "default" | "chat",
    description?: string
  },
  workforce_graph: {
    nodes: WorkforceNode[],
    edges: WorkforceEdge[]
  }
}
```

## Nodes

Nodes are the entities in a workforce. Each has a `node_id`, `type`, and `config`.

| Type        | Purpose                           | Config                                                       |
| ----------- | --------------------------------- | ------------------------------------------------------------ |
| `trigger`   | Entry point - starts the workflow | `{ type: "manual" }` or `{ type: "auto", sync_data: {...} }` |
| `agent`     | LLM-powered agent                 | `{ entity_link: { agent_id, project, region } }`             |
| `tool`      | Deterministic tool (no LLM)       | `{ entity_link: { studio_id, project, region } }`            |
| `condition` | Branching logic                   | `{ condition_type: "prompt" \| "rule", prompt?: string }`    |
| `note`      | Documentation only (no execution) | `{ content: string }`                                        |

### Node Example

```typescript
{
  node_id: "agent-researcher",
  type: "agent",
  metadata: { position: { x: 100, y: 300 } },
  config: {
    entity_link: {
      agent_id: "5878a72e-f305-4e03-8321-f1ca2ff2894b",
      project: "a3cd1b1efb8c-4da4-8728-81a8bc7333ca",
      region: "bcbe5a"
    },
    entity_information: {
      name: "Lead Researcher",
      description: "Researches LinkedIn profiles"
    }
  }
}
```

### Trigger Types

| Type     | Description                                                  |
| -------- | ------------------------------------------------------------ |
| `manual` | Started via API (`relevance_trigger_workforce`) or UI button |
| `auto`   | Started by external events - requires `sync_data` config     |

**Auto trigger sync types:** gmail, outlook, slack, teams, webhook, unipile_linkedin, unipile_whatsapp, recurring, and more.

## Edges

Edges connect nodes and define how data/control flows between them.

```typescript
{
  edge_id: string,
  source_node_id: string,
  target_node_id: string,
  source_type: "trigger" | "agent" | "tool" | "condition",
  target_type: "trigger" | "agent" | "tool" | "condition",
  config: {
    edge_type: "forced-handover" | "tool-call",
    config: {
      threading_behavior: { type: "always-same" | "always-create-new" },
      action_config?: { ... }  // Only for tool-call edges
    }
  }
}
```

### Edge Types

| Type              | Behavior                                                                           | When to Use                                             |
| ----------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `forced-handover` | **Deterministic.** Source finishes → target automatically starts. No LLM decision. | Sequential pipelines, trigger→agent, condition outcomes |
| `tool-call`       | **Agent decides.** Target appears as a "tool" the source agent can invoke.         | When invocation should be conditional/optional          |

### Compatibility Matrix

| Source → Target   | forced-handover | tool-call |
| ----------------- | --------------- | --------- |
| trigger → agent   | ✅              | ❌        |
| trigger → tool    | ✅              | ❌        |
| agent → agent     | ✅              | ✅        |
| agent → tool      | ✅              | ✅        |
| agent → condition | ✅              | ❌        |
| tool → agent      | ✅              | ❌        |
| tool → tool       | ✅              | ❌        |
| condition → agent | ✅              | ❌        |

**Rule:** `tool-call` only valid when source is an `agent` (because only agents can decide).

### Edge Example

```typescript
{
  edge_id: "edge-researcher-to-writer",
  source_node_id: "agent-researcher",
  target_node_id: "agent-writer",
  source_type: "agent",
  target_type: "agent",
  config: {
    edge_type: "forced-handover",
    config: {
      threading_behavior: { type: "always-same" }
    }
  }
}
```

## Threading Behavior

Controls whether agents share conversation context.

| Type                | Behavior                                                              | Use Case                                  |
| ------------------- | --------------------------------------------------------------------- | ----------------------------------------- |
| `always-same`       | Agents share the same conversation. Later agents see earlier outputs. | Most pipelines - you want context to flow |
| `always-create-new` | Each agent gets a fresh conversation. No memory of previous steps.    | Isolated tasks, parallel branches         |

**Important:** For sequential pipelines where agents need to see previous outputs, use `always-same`.

## Action Config (tool-call edges only)

When using `tool-call` edges, you can configure how the source agent invokes the target:

```typescript
{
  edge_type: "tool-call",
  config: {
    threading_behavior: { type: "always-same" },
    action_config: {
      action_behaviour: "never-ask",  // "never-ask" | "always-ask"
      wait_for_completion: true,
      prompt_for_when_to_use: "Use this agent when you need to research LinkedIn profiles",
      params_schema: {
        properties: {
          linkedin_url: { type: "string", description: "LinkedIn profile URL" }
        },
        required: ["linkedin_url"]
      }
    }
  }
}
```

| Field                    | Description                                                           |
| ------------------------ | --------------------------------------------------------------------- |
| `action_behaviour`       | `"never-ask"` = auto-approve, `"always-ask"` = require human approval |
| `wait_for_completion`    | Whether source waits for target to finish before continuing           |
| `prompt_for_when_to_use` | Instructions injected into source agent's system prompt               |
| `params_schema`          | JSON Schema for parameters the source can pass to target              |

## Workforce Types

| Type      | Execution Limit               | Use Case                                    |
| --------- | ----------------------------- | ------------------------------------------- |
| `default` | 100 node executions/task/24h  | Task-based workflows that run to completion |
| `chat`    | 5000 node executions/task/24h | Long-lived conversational interfaces        |

## Common Patterns

### Linear Pipeline (forced-handover)

```
Trigger → Agent A → Agent B → Agent C
```

- Each agent runs after the previous one finishes
- Context flows through via `always-same` threading
- Use for: Research → Process → Deliver workflows

### Hub-and-Spoke (tool-call)

```
        → Agent B
Trigger → Agent A (decides) → Agent C
        → Agent D
```

- Agent A decides which agents to call
- Other agents appear as tools to Agent A
- Use for: Routing, orchestration, conditional execution

### Sequential with Branching

```
Trigger → Agent A → Condition → Agent B (if true)
                             → Agent C (if false)
```

- Condition node evaluates and routes
- Use for: Approval workflows, A/B routing
