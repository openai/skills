# Agent Memory

A guide to understanding and using the Agent Memory feature in Relevance AI.

## Overview

Agent Memory enables AI agents to persist and recall information across conversations. This creates more personalized and context-aware interactions by allowing agents to "remember" important details about users, preferences, and facts.

### Key Benefits

- **Personalization**: Agents remember user preferences and tailor responses accordingly
- **Continuity**: Information persists across multiple conversation sessions
- **Context Awareness**: Agents can recall relevant facts without users repeating themselves
- **Flexible Scoping**: Choose between project-wide or user-specific memory

### How It Works

When memory is enabled, the agent receives two special "phantom tools" that allow it to add and delete memories. These memories are stored persistently and automatically injected into the agent's system prompt at the start of each conversation.

## Configuration

Agent memory is configured through the `memory` field in the agent configuration.

### Schema

```typescript
interface AgentMemory {
  enabled: boolean; // Master switch for memory
  memory_level: 'project' | 'user'; // Storage scope
  add_memory_prompt?: string; // Custom instructions for add tool
  delete_memory_prompt?: string; // Custom instructions for delete tool
  enable_delete_tool?: boolean; // Enable/disable delete capability
}
```

### Configuration Options

| Setting                | Type                    | Default        | Description                                     |
| ---------------------- | ----------------------- | -------------- | ----------------------------------------------- |
| `enabled`              | boolean                 | `false`        | Master switch - must be `true` to enable memory |
| `memory_level`         | `"project"` \| `"user"` | `"project"`    | Determines the scope of memory storage          |
| `add_memory_prompt`    | string                  | (see defaults) | Custom prompt to guide the add memory tool      |
| `delete_memory_prompt` | string                  | (see defaults) | Custom prompt to guide the delete memory tool   |
| `enable_delete_tool`   | boolean                 | `true`         | Whether the agent can delete memories           |

### Example Configuration

```typescript
// Get agent, add memory config, save and publish
const { agent } = await relevance_get_agent({ agentId: 'my-agent' });

await relevance_save_agent_draft({
  agentId: agent.agent_id,
  agentConfig: {
    ...agent,
    memory: {
      enabled: true,
      memory_level: 'user',
      enable_delete_tool: true,
      add_memory_prompt:
        'Save important user preferences and facts that will help personalize future interactions.',
    },
  },
});

await relevance_publish_agent({ agentId: agent.agent_id });
```

## Memory Levels

### Project-Level Memory (`"project"`)

- **Scope**: Shared across all users within the project
- **Use Case**: Global facts, project-wide settings, shared knowledge

**When to use:**

- Information relevant to all users (e.g., company policies, product information)
- Shared context that doesn't need user isolation
- Single-user applications where user separation isn't needed

### User-Level Memory (`"user"`)

- **Scope**: Isolated per user
- **Use Case**: Personal preferences, user-specific facts, individual instructions

**When to use:**

- Multi-user applications requiring privacy
- Personal assistant scenarios
- When users shouldn't see each other's memories

### Comparison

| Aspect     | Project-Level    | User-Level    |
| ---------- | ---------------- | ------------- |
| Visibility | All users        | Single user   |
| Isolation  | None             | Per user      |
| Best for   | Shared knowledge | Personal data |

## Phantom Tools

When memory is enabled, the agent automatically receives "phantom tools" - built-in tools that are dynamically injected without database entries.

### add_agent_memory

Saves information to the agent's memory store.

**Parameters:**

| Parameter     | Type   | Required | Description                                |
| ------------- | ------ | -------- | ------------------------------------------ |
| `memory_text` | string | Yes      | The content to remember                    |
| `category`    | enum   | Yes      | Classification of the memory               |
| `importance`  | enum   | Yes      | Priority level for retrieval               |
| `reasoning`   | string | Yes      | Why this memory is being saved             |
| `memory_id`   | string | No       | Custom ID (auto-generated if not provided) |

**Categories:**

- `preference` - User preferences (e.g., "Prefers dark mode")
- `fact` - Factual information (e.g., "User's company is Acme Inc")
- `instruction` - Behavioral instructions (e.g., "Always respond in Spanish")

**Importance Levels:**

- `high` - Critical information, always included
- `medium` - Important but secondary
- `low` - Nice to have, may be deprioritized

**Example Tool Call:**

```json
{
  "tool": "add_agent_memory",
  "parameters": {
    "memory_text": "User prefers concise responses without unnecessary explanations",
    "category": "preference",
    "importance": "high",
    "reasoning": "User explicitly stated they want shorter answers"
  }
}
```

### delete_agent_memory

Removes a memory from the store.

**Parameters:**

| Parameter   | Type   | Required | Description                    |
| ----------- | ------ | -------- | ------------------------------ |
| `memory_id` | string | Yes      | The ID of the memory to delete |

**Example Tool Call:**

```json
{
  "tool": "delete_agent_memory",
  "parameters": {
    "memory_id": "mem_abc123"
  }
}
```

**Note:** This tool can be disabled by setting `enable_delete_tool: false` in the configuration.

## Default Prompts

The agent memory system includes default prompts that guide the agent's behavior. These can be customized via configuration.

### Default Add Memory Prompt

```text
Use this tool to save important information about the user or conversation that should be remembered for future interactions.

Consider saving:
- User preferences (communication style, formatting preferences)
- Important facts about the user (name, role, company)
- Specific instructions the user wants you to follow
- Context that would be helpful in future conversations

Choose the appropriate category and importance level:
- Categories: preference, fact, instruction
- Importance: high (critical), medium (useful), low (supplementary)

Always provide reasoning for why you're saving this memory.
```

### Default Delete Memory Prompt

```text
Use this tool to remove outdated, incorrect, or no longer relevant memories.

Delete memories when:
- The information is no longer accurate
- The user explicitly asks you to forget something
- The memory is redundant with other memories
- The information is outdated
```

### Customizing Prompts

```typescript
{
  memory: {
    enabled: true,
    add_memory_prompt: "Only save information that the user explicitly asks you to remember. Focus on professional context and project requirements.",
    delete_memory_prompt: "Delete memories when the user says 'forget' or when information becomes outdated."
  }
}
```

## How Memory Recall Works

When an agent conversation starts, stored memories are automatically retrieved, sorted by importance (high > medium > low), and injected into the agent's system prompt so the agent has context from prior interactions.

## Best Practices

### When to Enable Memory

**Enable memory when:**

- Building personal assistant or support agents
- Users will have multiple conversations over time
- Personalization improves the user experience
- You need to remember user-specific context

**Consider disabling when:**

- Conversations are one-off interactions
- Privacy requirements prohibit data retention
- Memory would add unnecessary complexity

### Choosing Memory Level

| Scenario                           | Recommended Level |
| ---------------------------------- | ----------------- |
| Personal AI assistant              | User              |
| Customer support bot               | User              |
| Internal company bot (single team) | Project           |
| Knowledge base Q&A                 | Project           |
| Multi-tenant SaaS                  | User              |

### Memory Management Tips

1. **Be selective**: Don't save everything - focus on genuinely useful information
2. **Use appropriate importance**: Reserve "high" for truly critical information
3. **Clean up regularly**: Enable delete tool and periodically remove outdated memories
4. **Provide clear prompts**: Custom prompts help agents make better memory decisions
5. **Test thoroughly**: Verify memories are being stored and retrieved correctly

### Category Guidelines

| Category      | Use For                           | Examples                                    |
| ------------- | --------------------------------- | ------------------------------------------- |
| `preference`  | How the user likes things done    | Communication style, formatting, language   |
| `fact`        | Static information about the user | Name, company, role, location               |
| `instruction` | Behavioral directives             | "Always summarize first", "Include sources" |

### Security Considerations

- User-level memories are isolated per user - one user cannot access another's memories
- Avoid storing sensitive information (passwords, API keys, financial data)
- Consider data retention policies for your use case
- Be transparent with users about what is being remembered

## Troubleshooting

### Memories Not Being Saved

1. Verify `memory.enabled` is `true`
2. Check agent has correct permissions
3. Review agent logs for errors

### Memories Not Appearing in Conversations

1. Verify memory level matches your intended scope
2. Check user_id is being passed correctly (for user-level)
3. Ensure memories weren't deleted

### Tool Not Available

1. Confirm `memory.enabled` is `true`
2. For delete tool, check `enable_delete_tool` isn't `false`
3. Verify agent configuration was saved correctly
