# Creating Agents

Complete workflow for creating Relevance AI agents.

## Agent Structure

```typescript
interface AgentConfig {
  agent_id?: string; // Auto-generated if not provided
  name: string; // Display name
  description: string; // Brief description
  system_prompt: string; // Core instructions
  model?: string; // LLM model
  emoji?: string; // Icon
  temperature?: number; // 0-1 creativity
  actions?: AgentAction[]; // Attached tools
  params_schema?: object; // Input variables
  autonomy_limit?: number; // Max tool calls (default: 20)
  autonomy_limit_behaviour?: string; // What happens at limit
}
```

## Agent Features (Enabled via Settings)

Agents have built-in capabilities enabled through settings — **not** by adding tools to `actions`. These generate "phantom tools" at runtime:

| Setting                                           | What It Enables                        |
| ------------------------------------------------- | -------------------------------------- |
| `thinking_tool: { enabled: true }`                | Internal reasoning scratchpad          |
| `memory: { enabled: true, memory_level: "user" }` | Persistent memory across conversations |
| `tags: ["support", "sales"]`                      | Conversation tagging                   |
| `is_scheduled_triggers_enabled: true`             | Agent can schedule future actions      |
| `escalations: { email: { emails: [...] } }`       | Escalate to human managers             |
| `enable_python_executor: true`                    | Agent can write and run Python         |

**See [phantom-tools.md](phantom-tools.md) for the full reference** — how to enable each one, what they do, and critical gotchas about never putting them in `actions`.

## Agent Configuration Options

### Action Behaviour (Tool Execution)

Controls whether the agent asks for user approval before running tools.

| Value          | Behavior                                                      |
| -------------- | ------------------------------------------------------------- |
| `"never-ask"`  | Agent runs tools automatically without approval               |
| `"ask-first"`  | Agent asks for approval on first use, then runs automatically |
| `"always-ask"` | Agent asks for approval before EVERY tool call                |

```typescript
{
  action_behaviour: "never-ask",  // Recommended for most agents
  actions: [
    {
      chain_id: "my-tool",
      action_behaviour: "never-ask"  // Per-tool override
    }
  ]
}
```

**⚠️ Common Issue:** If your agent says "I'll run the tool" but nothing happens, check if `action_behaviour` is set to `"always-ask"`. This blocks execution pending user approval in the UI.

### Autonomy Settings

| Field                      | Valid Values                                     | Description                    |
| -------------------------- | ------------------------------------------------ | ------------------------------ |
| `autonomy_limit`           | number (default: 20)                             | Max tool calls before stopping |
| `autonomy_limit_behaviour` | `"ask-for-approval"`, `"terminate-conversation"` | What happens at limit          |

```typescript
{
  autonomy_limit: 50,
  autonomy_limit_behaviour: "ask-for-approval"  // Recommended
}
```

**⚠️ Critical Behaviour Differences:**

| Value                      | Effect                                           |
| -------------------------- | ------------------------------------------------ |
| `"ask-for-approval"`       | Agent pauses and asks user if it should continue |
| `"terminate-conversation"` | Agent **silently stops** without any response    |

**Common Error:** Using `"stop"` - this value is invalid and causes 422 error.

**⚠️ Silent Termination Issue:** If `autonomy_limit_behaviour: "terminate-conversation"` and the agent runs a tool, it may silently end the conversation without providing results. Use `"ask-for-approval"` to ensure the agent always responds.

## Creation Workflow

### Step 1: Create Basic Agent

```typescript
relevance_upsert_agent({
  name: 'Research Assistant',
  description: 'Helps research topics using web search',
  system_prompt: `You are a helpful research assistant.

When the user asks about a topic:
1. Use Google Search to find relevant information
2. Analyze and synthesize the results
3. Provide a clear summary with sources`,
});
```

### Step 2: Get Agent ID

```typescript
const { agent } = await relevance_get_agent({ agentId: '...' });
```

### Step 3: Add Tools and Configure

```typescript
relevance_save_agent_draft({
  agentId: agent.agent_id,
  agentConfig: {
    ...agent, // CRITICAL: Include all existing fields
    actions: [
      {
        chain_id: 'gtm-google-search',
        project: config.project, // REQUIRED
        region: config.region, // REQUIRED
        title: 'Search Google',
        description: 'Search the web for information',
        action_behaviour: 'never-ask',
      },
    ],
  },
});
```

### Step 4: Publish

```typescript
relevance_publish_agent({ agentId: agent.agent_id });
```

### Step 5: Test

```typescript
relevance_trigger_agent({
  agentId: agent.agent_id,
  message: 'Research the latest AI developments',
});
```

## Best Practice: Examine Working Agents First

Before creating a new agent, check how similar working agents are configured:

```typescript
// 1. List existing agents
const agents = await relevance_list_agents({ pageSize: 10 });

// 2. Find one with similar tools
const { agent } = await relevance_get_agent({ agentId: 'working-agent-id' });

// 3. Inspect the region used in actions
// This is CRITICAL - use the same region for the same tools
// Check agent.actions for chain_id and region values
```

This reveals:

- Correct `region` values for tools (often different from your project region!)
- Working `action_behaviour` patterns
- System prompt patterns that reference tools

## Agent Lifecycle

```text
1. Create basic agent (relevance_upsert_agent)
        |
2. Get agent to see ID (relevance_get_agent)
        |
3. Add tools/config (relevance_save_agent_draft)
        |
4. Publish (relevance_publish_agent)
        |
5. Test (relevance_trigger_agent)
        |
6. Add triggers if needed (relevance_create_trigger)
```

## Model Options

| Model                       | Use Case                  |
| --------------------------- | ------------------------- |
| `openai-gpt-4o`             | Fast, good quality        |
| `openai-gpt-4o-mini`        | Fast, cheaper             |
| `anthropic-claude-sonnet-4` | Best quality/cost balance |
| `anthropic-claude-opus-4`   | Highest quality           |

## Common Patterns

### Search and Summarize Agent

```typescript
{
  name: "Research Assistant",
  system_prompt: `You help research topics.

When asked about something:
1. Search for information using Google Search
2. Read relevant pages with the scraper
3. Synthesize and summarize findings`,
  actions: [
    { chain_id: "google-search", action_behaviour: "never-ask", project: "...", region: "..." },
    { chain_id: "web-scraper", action_behaviour: "never-ask", project: "...", region: "..." }
  ]
}
```

### Data Enrichment Agent

```typescript
{
  name: "Lead Enricher",
  system_prompt: `You enrich lead data.

Given a company or person:
1. Search for their website
2. Extract key information
3. Find contact details`,
  actions: [
    { chain_id: "google-search", project: "...", region: "..." },
    { chain_id: "contact-finder", project: "...", region: "..." },
    { chain_id: "linkedin-scraper", project: "...", region: "..." }
  ]
}
```

### Event-Driven Agent

```typescript
{
  name: "Meeting Prep Assistant",
  system_prompt: `You prepare meeting briefings.

When triggered by a calendar event:
1. Extract attendee information
2. Research their company
3. Prepare talking points`
  // Triggered via google_calendar trigger
}
```

## Testing

After creating an agent, test it with `relevance_trigger_agent` to verify it works as expected. For production agents, see the `relevance-evals` skill for setting up formal evaluation suites.

---

## Quality Checklist

- [ ] Clear, specific name and description
- [ ] System prompt defines role and tool usage
- [ ] All necessary tools attached
- [ ] All actions have project and region fields
- [ ] Correct action_behaviour for each tool
- [ ] Model appropriate for task complexity
- [ ] Each tool individually validated with `relevance_run_tool`
- [ ] Agent tested with `relevance_trigger_agent`
- [ ] Triggers configured (if needed)
