# Agent Actions (Tools)

How to attach and configure tools for agents.

> ⚠️ **Sub-Agents are DEPRECATED**
>
> Do NOT add agents to another agent's `actions` array. This pattern is deprecated.
> Use **Workforces** instead for multi-agent orchestration.
> See [Workforce Documentation](../managing-relevance-workforces/SKILL.md) for details.

> ⚠️ **Phantom Tools: Never Add to Actions**
>
> Tools like `thinking_tool`, `add_agent_memory`, `tag_agent_conversation`, etc. are **phantom tools** — system-injected at runtime from agent settings. Never add them to `actions` manually.
> Enable them via settings instead (e.g., `thinking_tool: { enabled: true }`).
> See [phantom-tools.md](phantom-tools.md) for the full list and how to enable each one.

## Action Structure

```typescript
interface AgentAction {
  chain_id: string; // REQUIRED: Tool's studio_id (UUID, e.g., "653af72e-bee9-42ef-ad82-ca8c54715f85")
  project: string; // REQUIRED: Project ID
  region: string; // REQUIRED: Region code (e.g., "bcbe5a")
  action_id?: string; // Generated hex ID for system prompt references
  title?: string; // Display title
  description?: string; // What the tool does
  emoji?: string; // Tool icon
  action_behaviour?: 'never-ask' | 'ask-first' | 'always-ask';
  disabled?: boolean;
}
```

## CRITICAL: Finding the Correct Tool Region

The `region` in actions must match **where the tool exists**, NOT your project's region.

**Why this happens:** Relevance AI has multiple regions:

- **API region** (e.g., `bcbe5a`): Where your MCP server connects
- **Tools region** (e.g., `f1db6c`): Where tools/studios are stored

Your project's API region may differ from where tools are stored.

### How to Find Tool Region (Recommended Pattern)

```typescript
// BEST: Find region from an existing working agent with tools
const agents = await relevance_list_agents({ pageSize: 10 });
const agentWithTools = agents.results.find((a) => a.actions?.length > 0);
const correctRegion = agentWithTools.actions[0].region;

// Use verified region when attaching tools
const actions = toolIds.map((id) => ({
  chain_id: id,
  project: projectId,
  region: correctRegion, // Use verified region
  action_behaviour: 'never-ask',
}));
```

Alternative methods:

```typescript
// Option 2: Get specific agent you know works
const { agent } = await relevance_get_agent({ agentId: 'working-agent-id' });
const region = agent.actions[0].region;

// Option 3: Check tool metadata (less reliable)
const tool = await relevance_get_tool({ studioId: 'tool-id' });
// Look for tool.studio.metadata.source_marketplace_listing.entity_region
```

### Common Mistake

```typescript
// WRONG - using project/API region
{
  chain_id: "tool-id",
  region: "bcbe5a",  // Your API region - MAY BE WRONG
  project: "your-project-id"
}

// CORRECT - using tool's actual region
{
  chain_id: "tool-id",
  region: "f1db6c",  // Region from working agent
  project: "your-project-id"
}
```

### Symptoms of Wrong Region

- `relevance_get_agent_tools` returns empty `chains: []` and `actionIdMap: {}`
- Agent config shows tools in `actions` array but they don't appear in UI
- Agent appears configured but tools don't execute
- **No error message - just silent failure**

### Verification After Attaching Tools

**Always verify tools are linked after publishing:**

After publishing, call `relevance_get_agent_tools({ agentId })` to confirm tools are linked:

- If `chains` is empty and `actionIdMap` is `{}` → region mismatch. Find the correct region from a working agent.
- If `chains` has entries → tools are linked correctly. Use `actionIdMap` for system prompt references.

## Required Fields

Every action **MUST** include `project` and `region` fields. Missing these causes:

- Agent cloning failures
- Tool execution errors
- Agent deployment issues

```typescript
// CORRECT
const action = {
  chain_id: 'my-tool-id',
  project: config.project, // REQUIRED
  region: config.region, // REQUIRED
  title: 'My Tool',
  description: 'What it does',
  action_behaviour: 'never-ask',
};

// WRONG - missing project/region
const action = {
  chain_id: 'my-tool-id',
  title: 'My Tool',
};
```

## Action Behaviours

| Behaviour    | Description                          | Use When             |
| ------------ | ------------------------------------ | -------------------- |
| `never-ask`  | Tool executes automatically          | Default, most tools  |
| `ask-first`  | Agent asks user before first use     | Sensitive operations |
| `always-ask` | Requires explicit approval each time | Destructive actions  |

## Adding Actions to an Agent

```typescript
// 1. Get current agent config
const { agent } = await relevance_get_agent({ agentId: 'xxx' });

// 2. Add actions to config
relevance_save_agent_draft({
  agentId: 'xxx',
  agentConfig: {
    ...agent, // CRITICAL: preserve all existing fields
    actions: [
      {
        chain_id: '653af72e-bee9-42ef-ad82-ca8c54715f85', // UUID from relevance_upsert_tool
        project: config.project,
        region: config.region,
        title: 'Search Google',
        description: 'Search the web for information',
        action_behaviour: 'never-ask',
      },
      {
        chain_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', // UUID from relevance_upsert_tool
        project: config.project,
        region: config.region,
        title: 'Scrape Webpage',
        description: 'Extract content from a URL',
        action_behaviour: 'never-ask',
      },
    ],
  },
});

// 3. Publish
relevance_publish_agent({ agentId: 'xxx' });
```

## CRITICAL: Action IDs vs Studio IDs

**STOP CONFUSING THESE!**

| ID Type                  | Format      | Example                                | Where Used                            |
| ------------------------ | ----------- | -------------------------------------- | ------------------------------------- |
| `studio_id` / `chain_id` | UUID v4     | `653af72e-bee9-42ef-ad82-ca8c54715f85` | Tool identifier, `actions[].chain_id` |
| `action_id`              | 16-char hex | `3261d8205a334a99`                     | System prompt `{{_actions.xxx}}`      |

### Wrong vs Correct

```typescript
// WRONG - using tool's studio_id as action reference
system_prompt: `Use {{_actions.653af72e-bee9-42ef-ad82-ca8c54715f85}} to create contacts.`;

// CORRECT - using backend-generated hex action_id
system_prompt: `Use {{_actions.3261d8205a334a99}} to create contacts.`;
```

### Getting Action IDs

Backend-generated action IDs are required for system prompt references.

```typescript
const tools = await relevance_get_agent_tools({ agentId: '...' });
// Returns:
// {
//   chains: [
//     { studio_id: "653af72e-bee9-42ef-ad82-ca8c54715f85", action_id: "3261d8205a334a99" }
//   ],
//   actionIdMap: { "653af72e-bee9-42ef-ad82-ca8c54715f85": "3261d8205a334a99" }
// }
```

### Workflow to Use Correct Action IDs

**⚠️ Two-Pass Required:** Action IDs are backend-generated and only exist after first publish. If your system prompt uses `{{_actions.*}}`, you need two publish cycles.

See [actions.md - Action IDs vs Studio IDs](#critical-action-ids-vs-studio-ids) for the full reference.

Use these IDs in system prompts: `{{_actions.3261d8205a334a99}}`

## OAuth-Enabled Tools

Some tools require OAuth accounts. Add the OAuth parameter to tool params:

```typescript
{
  chain_id: "b2c3d4e5-f6a7-8901-bcde-f12345678901",  // UUID of your email tool
  project: config.project,
  region: config.region,
  title: "Send Email",
  action_behaviour: "ask-first"
}
```

The user selects their OAuth account when using the tool.

For the full list of OAuth providers and permission types, see [OAuth Guide](../managing-relevance-tools/oauth.md).

## Three-Layer Default Values (OAuth Credentials)

When passing agent variables to tools (especially OAuth credentials), configure defaults in THREE places for reliable operation:

```
LAYER 1: Agent params_schema → Sets the agent-level variable default
LAYER 2: Agent actions[].default_values → Maps agent variable to tool input at call time
LAYER 3: Tool params_schema → Fallback if agent doesn't pass value
```

**All three layers are needed.**

```typescript
// 1. Get OAuth account ID
const accounts = await relevance_list_oauth_accounts();
const oauthAccountId = accounts.results.find(
  (a) => a.provider === 'linkedin'
).account_id;

// 2. Update tool with default (Layer 3)
await relevance_upsert_tool({
  studio_id: 'my-linkedin-tool',
  params_schema: {
    properties: {
      linkedin_account_id: {
        type: 'string',
        title: 'LinkedIn Account ID',
        default: oauthAccountId, // LAYER 3: Tool fallback default
      },
    },
  },
});

// 3. Configure agent with variable and action mapping (Layers 1 & 2)
const { agent } = await relevance_get_agent({ agentId: 'my-agent' });
await relevance_save_agent_draft({
  agentId: agent.agent_id,
  agentConfig: {
    ...agent,
    params_schema: {
      type: 'object',
      properties: {
        linkedin_account_id: {
          type: 'string',
          title: 'LinkedIn Account ID',
          default: oauthAccountId, // LAYER 1: Agent variable default
        },
      },
    },
    actions: agent.actions.map((action) => ({
      ...action,
      default_values: needsOAuth(action.chain_id)
        ? { linkedin_account_id: '{{linkedin_account_id}}' } // LAYER 2: Maps variable to tool
        : action.default_values,
    })),
  },
});
await relevance_publish_agent({ agentId: agent.agent_id });
```

## Listing Available OAuth Accounts

```typescript
// List all connected OAuth accounts
relevance_list_oauth_accounts();
```
