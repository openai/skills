# Phantom Tools

Phantom tools are **system-injected tools generated at runtime** from agent settings. They are never stored in the agent's `actions` array — the Relevance AI backend creates them dynamically when the agent runs, based on configuration flags.

## Why This Matters

If phantom tools accidentally end up in `actions`, they bring fields (`studio_id`, `transformations`, `action_config`) that are not allowed on action configs. This causes runtime validation errors:

```
Studio transformation message_agent input validation error:
must NOT have additional properties {"additionalProperty":"studio_id"}
/agent_override/actions/0
```

This typically breaks workforce cloning, marketplace cloning, and any operation that validates agent action configs.

## How Phantom Tools Work

Phantom tools are **derived from agent settings**, not stored as actions:

```
Agent Settings (persisted in DB)         Phantom Tools (generated at runtime)
────────────────────────────────         ────────────────────────────────────
thinking_tool.enabled: true          →   thinking_tool
memory.enabled: true                 →   add_agent_memory, delete_agent_memory
tags: ["support", "vip"]             →   tag_agent_conversation
custom_metadata: { fields... }       →   add_conversation_metadata,
                                         read_conversation_metadata
is_scheduled_triggers_enabled: true  →   create_scheduled_trigger,
                                         delete_scheduled_trigger
escalations: { email/slack config }  →   escalate_to_manager
enable_python_executor: true         →   python_executor
remote_mcp_configs: [...]            →   mcp_remote_tool_call
```

When `relevance_get_agent_tools` returns tools, phantom tools are included with `is_phantom_tool: true`. But they should **never** be written back via `relevance_save_agent_draft`.

## Complete Reference: All 15 Phantom Tools

### Thinking Tool

| Field             | Value                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------- |
| **ID**            | `thinking_tool`                                                                         |
| **Enabled by**    | `thinking_tool.enabled: true`                                                           |
| **Purpose**       | Internal scratchpad — agent uses this to reason through complex decisions before acting |
| **How to enable** | Set `thinking_tool: { enabled: true }` on the agent config                              |

```typescript
// Enable thinking tool
const { agent } = await relevance_get_agent({ agentId });
await relevance_save_agent_draft({
  agentId,
  agentConfig: {
    ...agent,
    thinking_tool: { enabled: true },
  },
});
await relevance_publish_agent({ agentId });
```

### Agent Memory Tools

| Field             | Value                                                 |
| ----------------- | ----------------------------------------------------- |
| **IDs**           | `add_agent_memory`, `delete_agent_memory`             |
| **Enabled by**    | `memory.enabled: true`                                |
| **Purpose**       | Persist and recall information across conversations   |
| **How to enable** | Set `memory: { enabled: true, memory_level: "user" }` |

The `delete_agent_memory` tool is only injected when `memory.enable_delete_tool: true`.

```typescript
// Enable memory tools
await relevance_save_agent_draft({
  agentId,
  agentConfig: {
    ...agent,
    memory: {
      enabled: true,
      memory_level: 'user', // "project" (shared) or "user" (per-user)
      enable_delete_tool: true, // Also inject delete tool
      add_memory_prompt: 'Save important facts and user preferences.',
    },
  },
});
```

See [memory.md](memory.md) for full memory documentation.

### Conversation Tagging Tool

| Field             | Value                                                             |
| ----------------- | ----------------------------------------------------------------- |
| **ID**            | `tag_agent_conversation`                                          |
| **Enabled by**    | `tags` array with at least one tag                                |
| **Purpose**       | Tag conversations with predefined labels for organization/routing |
| **How to enable** | Set `tags: ["support", "billing", "sales"]` on the agent config   |

```typescript
// Enable conversation tagging
await relevance_save_agent_draft({
  agentId,
  agentConfig: {
    ...agent,
    tags: ['support', 'billing', 'technical', 'sales'],
  },
});
```

### Conversation Metadata Tools

| Field             | Value                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------- |
| **IDs**           | `add_conversation_metadata`, `read_conversation_metadata`                                |
| **Enabled by**    | `custom_metadata` object with field definitions                                          |
| **Purpose**       | Store and retrieve structured metadata on conversations (e.g., sentiment, customer tier) |
| **How to enable** | Set `custom_metadata: { fields: [...] }` on the agent config                             |

### Scheduled Trigger Tools

| Field             | Value                                                              |
| ----------------- | ------------------------------------------------------------------ |
| **IDs**           | `create_scheduled_trigger`, `delete_scheduled_trigger`             |
| **Enabled by**    | `is_scheduled_triggers_enabled: true`                              |
| **Purpose**       | Allow the agent to schedule future actions (reminders, follow-ups) |
| **How to enable** | Set `is_scheduled_triggers_enabled: true`                          |

```typescript
// Enable scheduled triggers
await relevance_save_agent_draft({
  agentId,
  agentConfig: {
    ...agent,
    is_scheduled_triggers_enabled: true,
  },
});
```

### Escalate to Manager Tool

| Field             | Value                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| **ID**            | `escalate_to_manager`                                                                            |
| **Enabled by**    | `escalations` config with email addresses or Slack channels                                      |
| **Purpose**       | Escalate conversations to human managers via email or Slack notifications                        |
| **How to enable** | Set `escalations: { email: { emails: [...] } }` or `escalations: { slack: { channels: [...] } }` |

```typescript
// Enable escalation
await relevance_save_agent_draft({
  agentId,
  agentConfig: {
    ...agent,
    escalations: {
      email: {
        emails: ['manager@company.com'],
      },
      slack: {
        channels: ['#escalations'],
      },
    },
  },
});
```

### Python Executor Tool

| Field             | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| **ID**            | `python_executor`                                           |
| **Enabled by**    | `enable_python_executor: true`                              |
| **Purpose**       | Allow the agent to write and execute Python code at runtime |
| **How to enable** | Set `enable_python_executor: true`                          |

### Remote MCP Tool

| Field             | Value                                                     |
| ----------------- | --------------------------------------------------------- |
| **ID**            | `mcp_remote_tool_call`                                    |
| **Enabled by**    | `remote_mcp_configs` array with MCP server configurations |
| **Purpose**       | Call tools on remote MCP servers                          |
| **How to enable** | Set `remote_mcp_configs: [{ url: "...", ... }]`           |

### Agent Knowledge Tool

| Field             | Value                                              |
| ----------------- | -------------------------------------------------- |
| **ID**            | `agent_knowledge` (prefix — actual IDs vary)       |
| **Enabled by**    | Knowledge sets linked to the agent                 |
| **Purpose**       | Query the agent's knowledge base (RAG)             |
| **How to enable** | Link knowledge sets to the agent via the UI or API |

### Get Current Date Tool

| Field          | Value                                                    |
| -------------- | -------------------------------------------------------- |
| **ID**         | `get_current_date`                                       |
| **Enabled by** | Automatically available for certain agent configurations |
| **Purpose**    | Provide the agent with the current date and time         |

### System-Internal Tools

These are managed by the platform and not typically configured directly:

| ID                             | Purpose                                   |
| ------------------------------ | ----------------------------------------- |
| `preset_agents`                | Tools for preset agent configurations     |
| `workforce_orchestrator_tools` | Workforce coordination and handover tools |

## How to Identify Phantom Tools

When processing agent tool data, use these methods (in order of reliability):

1. **`is_phantom_tool: true` flag** — Set on all phantom tools in the `GetAgentTools` API response. Most reliable.
2. **Known IDs** — Match `chain_id` or `studio_id` against the 15 IDs listed above.
3. **`transformations` field** — Phantom tools have a `transformations` property; regular action configs do not.

## Gotchas and Common Mistakes

### Phantom Tools Are Auto-Stripped on Save

The `relevance_save_agent_draft` tool automatically strips phantom tools before saving. When updating an agent, always use `agent.actions` from `relevance_get_agent` (already clean) — never use `tools.chains` from `relevance_get_agent_tools` (includes phantom tools).

### Enable Features via Settings, Not Actions

To give an agent capabilities like memory or thinking, configure the **setting** — don't manually add the tool to `actions`.

```typescript
// BAD — manually adding phantom tool to actions
actions: [
  ...agent.actions,
  { chain_id: "thinking_tool", title: "Think" }  // Will corrupt agent
]

// GOOD — enable via setting
{ ...agent, thinking_tool: { enabled: true } }
```

### Cloned Agents May Be Pre-Tainted

If an agent was published to the marketplace with phantom tools already leaked into its `actions` (from a previous bug), cloning it reproduces the tainted data. Re-saving the agent via `relevance_save_agent_draft` will automatically clean this up.

### `params_schema` Is Valid — Don't Strip It

A common mistake when cleaning actions is deleting `params_schema`. This field IS valid on action configs and is used for tool input schemas. Don't remove it.
