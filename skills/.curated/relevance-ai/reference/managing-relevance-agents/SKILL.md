---
name: managing-relevance-agents
description: Manages Relevance AI agents - creating, configuring tools, writing system prompts, setting up triggers, and running conversations. Use when building agents, attaching tools, debugging execution, or viewing agent results.
---

# Managing Relevance AI Agents

Skill for creating, configuring, running, and debugging Relevance AI agents.

> **📚 Full API Documentation:** If MCP tools don't cover your use case, see `https://api-{region}.stack.tryrelevance.com/latest/documentation` (replace `{region}` with your project's region)

## When to Use

- Creating new agents
- Attaching tools/actions to agents
- Writing or updating system prompts
- Configuring agent memory (persistence across conversations)
- Setting up triggers (email, LinkedIn, webhooks, etc.)
- Running agent conversations
- Debugging agent execution issues

## MCP Tools

| Tool                              | Description                                   |
| --------------------------------- | --------------------------------------------- |
| `relevance_list_agents`           | List all agents (supports search)             |
| `relevance_get_agent`             | Get full agent config                         |
| `relevance_upsert_agent`          | Create basic agent                            |
| `relevance_save_agent_draft`      | Save full agent config as draft               |
| `relevance_publish_agent`         | Publish agent draft to live                   |
| `relevance_trigger_agent`         | Send message to agent and poll for completion |
| `relevance_get_agent_tools`       | Get agent's tools with action_ids             |
| `relevance_attach_tools_to_agent` | Attach tools to an agent                      |
| `relevance_get_task_view`         | Get conversation details                      |
| `relevance_list_conversations`    | List agent conversations                      |
| `relevance_list_agent_triggers`   | List agent triggers                           |
| `relevance_create_trigger`        | Create trigger                                |
| `relevance_delete_trigger`        | Delete trigger                                |
| `relevance_list_oauth_accounts`   | List OAuth accounts for triggers              |

## Critical Rules

### Sub-Agents are DEPRECATED

> ⚠️ **Do NOT add agents to another agent's `actions` array.** This pattern is deprecated.
>
> Use **Workforces** instead for multi-agent orchestration. See [Workforce Documentation](../managing-relevance-workforces/SKILL.md).

### NO PARTIAL UPDATES

`relevance_save_agent_draft` does NOT support partial updates. Any field you omit will be WIPED.

```typescript
// WRONG - wipes system_prompt, actions, etc!
relevance_save_agent_draft({
  agentId: 'xxx',
  agentConfig: { emoji: 'new-emoji' },
});

// CORRECT - get first, merge, save everything
const { agent } = await relevance_get_agent({ agentId: 'xxx' });
relevance_save_agent_draft({
  agentId: 'xxx',
  agentConfig: { ...agent, emoji: 'new-emoji' },
});
relevance_publish_agent({ agentId: 'xxx' });
```

### Actions Require project/region (CRITICAL)

Every action MUST include `project` and `region` fields:

```typescript
{
  chain_id: "tool-id",
  project: config.project,    // Your project ID
  region: "f1db6c",           // Tool's region - MAY DIFFER FROM PROJECT!
  title: "My Tool",
  action_behaviour: "never-ask"
}
```

**CRITICAL:** The `region` must be **where the tool exists**, not your project's region!

- Find correct region by checking working agents or tool metadata
- Wrong region = tools silently fail to attach (empty chains)
- See [actions.md](actions.md) for how to find correct region

### Autonomy Settings

```typescript
{
  autonomy_limit: 50,                              // Max tool calls
  autonomy_limit_behaviour: "terminate-conversation"  // Valid: "ask-for-approval" | "terminate-conversation"
}
```

**Note:** `"stop"` is NOT valid for `autonomy_limit_behaviour` - use `"terminate-conversation"`.

Missing project/region causes cloning failures and tool execution errors.

### Action IDs for System Prompts (Two-Pass Required!)

If your system prompt references tools via `{{_actions.ACTION_ID}}`, you need **TWO publish cycles**:

```
Pass 1: Create agent + attach tools + placeholder prompt → Publish
Pass 2: Fetch real action IDs → Update prompt with IDs → Publish again
```

**Why?** Action IDs are backend-generated hex strings that only exist AFTER first publish. You can't write the final system prompt until tools are attached and published.

```typescript
// After first publish, get real action IDs:
const { actionIdMap } = await relevance_get_agent_tools({ agentId });
// actionIdMap: { "my-tool-studio-id": "3261d8205a334a99" }

// Then update system prompt with real IDs and publish again
```

**Skip the second pass** if your prompt doesn't use `{{_actions.*}}` references.

See [creating.md - Action IDs](creating.md#action-ids-vs-studio-ids) for full workflow with code examples.

## Quick Start: Create Agent

1. **Create basic agent:**

   ```
   relevance_upsert_agent({
     name: "Research Assistant",
     description: "Helps research topics",
     system_prompt: "You are a research assistant.\nWhen asked about a topic:\n1. Search for information\n2. Summarize findings"
   })
   ```

2. **Get the agent** to see the generated ID:

   ```
   relevance_get_agent({ agentId: "..." })
   ```

3. **Add tools** — get the full agent config first, then save with actions:

   ```
   relevance_save_agent_draft({
     agentId: "...",
     agentConfig: {
       ...existingAgent,
       actions: [{
         chain_id: "google-search",
         project: "your-project-id",
         region: "tool-region",
         title: "Search Google",
         action_behaviour: "never-ask"
       }]
     }
   })
   ```

4. **Publish:** `relevance_publish_agent({ agentId: "..." })`

5. **Test:** `relevance_trigger_agent({ agentId: "...", message: "Research AI trends" })`

## Reference Files

- [creating.md](creating.md) - Full creation workflow
- [actions.md](actions.md) - Tool/action configuration
- [phantom-tools.md](phantom-tools.md) - Phantom tools reference (thinking, memory, tags, etc.)
- [system-prompts.md](system-prompts.md) - Writing effective prompts
- [memory.md](memory.md) - Agent memory configuration and usage
- [triggers.md](triggers.md) - Email, LinkedIn, webhook triggers
- [running.md](running.md) - Running and testing agents
- [troubleshooting.md](troubleshooting.md) - Common issues and fixes

## URL Patterns

```
# Agent edit page
https://app.relevanceai.com/agents/{region}/{project}/{agentId}/edit/instructions

# Conversation view
https://app.relevanceai.com/agents/{region}/{project}/{agentId}/{taskId}

# Clone link
https://app.relevanceai.com/form/{region}/{project}/clone/agent/{agentId}
```
