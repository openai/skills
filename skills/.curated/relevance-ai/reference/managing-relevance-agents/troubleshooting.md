# Troubleshooting Agents

Common issues and fixes for Relevance AI agents.

## Critical Issues

### Agent Config Wiped After Update

**Symptom:** Agent lost system prompt, tools, or other config after saving.

**Cause:** `relevance_save_agent_draft` does NOT support partial updates.

**Fix:**

```typescript
// WRONG - wipes everything not included
relevance_save_agent_draft({
  agentId: 'xxx',
  agentConfig: { emoji: 'new' },
});

// CORRECT - get first, merge, save all
const { agent } = await relevance_get_agent({ agentId: 'xxx' });
relevance_save_agent_draft({
  agentId: 'xxx',
  agentConfig: { ...agent, emoji: 'new' },
});
```

### Agent Says "I'll Run the Tool" But Nothing Happens

**Symptom:** Agent announces it will use a tool but never actually executes it.

**Cause:** `action_behaviour` is set to `"always-ask"`, which requires user approval before each tool call.

**Fix:**

```typescript
{
  action_behaviour: "never-ask",  // At agent level
  actions: [
    {
      chain_id: "my-tool",
      action_behaviour: "never-ask"  // Per-tool level
    }
  ]
}
```

### Agent Runs Tool Then Silently Stops

**Symptom:** Tool executes successfully but agent ends conversation without providing results.

**Cause:** `autonomy_limit_behaviour: "terminate-conversation"` causes the agent to silently end instead of responding after reaching its limit.

**Fix:**

```typescript
{
  autonomy_limit: 25,
  autonomy_limit_behaviour: "ask-for-approval"  // NOT "terminate-conversation"
}
```

With `"ask-for-approval"`, the agent will pause and ask to continue rather than silently stopping.

### Tools Not Executing

**Symptom:** Agent acknowledges tools but doesn't use them, or tool calls fail.

**Cause 1:** Missing `project` and `region` in action config.

**Fix:**

```typescript
{
  chain_id: "my-tool",
  project: config.project,    // REQUIRED
  region: config.region,      // REQUIRED
  title: "My Tool",
  action_behaviour: "never-ask"
}
```

**Cause 2:** Tool is disabled.

**Fix:** Check `disabled: false` in action config.

**Cause 3:** `action_behaviour: "always-ask"` blocking execution (see above).

### System Prompt Tool References Not Working

**Symptom:** `{{_actions.xxx}}` not resolving in system prompt.

**Cause:** Using wrong action ID.

**Fix:** Use backend-generated IDs, not your custom IDs:

```typescript
// Get the real action IDs
const tools = await relevance_get_agent_tools({ agentId: '...' });
// Use actionIdMap values in system prompt
```

### Agent Cloning Fails with "additional properties" Error

**Symptom:** Error like `must NOT have additional properties {"additionalProperty":"studio_id"}` when cloning or running in a workforce.

**Cause:** Phantom tools (e.g., `thinking_tool`, `add_agent_memory`) leaked into the agent's `actions` array, bringing invalid fields like `studio_id`, `transformations`, `action_config`.

**Fix:** Re-save the agent using `relevance_save_agent_draft` — the MCP automatically strips phantom tools on save. See [phantom-tools.md](phantom-tools.md) for details.

### Agent Cloning Fails (Missing Fields)

**Symptom:** Clone link doesn't work or cloned agent is broken.

**Cause:** Actions missing `project`/`region` fields.

**Fix:** Ensure all actions have these fields populated.

### Tools Not Attaching to Agent (Empty chains)

**Symptom:** `relevance_get_agent_tools` returns `{ chains: [], actionIdMap: {} }` even after adding actions.

**Cause:** Wrong `region` in action config. The region must match where the tool exists, not your project's region.

**Diagnosis:**

```typescript
// Check if tools attached
const tools = await relevance_get_agent_tools({ agentId: '...' });
if (tools.chains.length === 0) {
  // Tools not attached - likely region mismatch
}
```

**Fix:**

1. Find correct region from a working agent or tool:

```typescript
// Option 1: Check a working agent that uses the same tool
const agents = await relevance_list_agents({ pageSize: 5 });
// Look at actions[].region in agents that work

// Option 2: The tool metadata often shows source region
const tool = await relevance_get_tool({ studioId: 'tool-id' });
// Check tool.studio.metadata.source_marketplace_listing.entity_region
```

2. Update actions with correct region:

```typescript
actions: [{
  chain_id: "tool-id",
  region: "f1db6c",  // Correct region from above
  project: "your-project-id",
  ...
}]
```

3. Re-save and publish the agent.

## Trigger Issues

### Trigger Not Firing

| Cause                    | Fix                               |
| ------------------------ | --------------------------------- |
| OAuth expired            | Reconnect OAuth account           |
| Wrong account ID         | Verify `oauth_account_id` matches |
| Missing provider_user_id | Add for Unipile triggers          |
| Agent not published      | Publish the agent                 |

### LinkedIn Trigger Not Responding

**Checklist:**

1. OAuth account connected and valid
2. `provider_user_id` is correct LinkedIn ID
3. `is_outreach_reply_only` setting matches intent
4. Agent is published (not draft)

### Email Trigger Missing Messages

**Check:**

- OAuth has correct permissions (`email-read-write`)
- No email filters blocking messages
- Agent system prompt handles email format

## Conversation Issues

### Agent Gives Wrong/Generic Response

| Cause               | Fix                             |
| ------------------- | ------------------------------- |
| Vague system prompt | Add specific instructions       |
| Too many tools      | Remove unused tools             |
| Wrong model         | Try higher-capability model     |
| Missing context     | Include relevant info in prompt |

### Agent Stuck/Not Responding

1. Check task view for errors
2. Look for tool timeouts
3. Verify tool inputs are valid
4. Check model availability

### Tool Output Not Used

**Symptom:** Agent calls tool but ignores results.

**Fixes:**

- Add instructions to use tool output in system prompt
- Verify tool actually returns expected data
- Check tool output format matches prompt expectations

## Configuration Issues

### Fields That Get Wiped If Not Included

When using `relevance_save_agent_draft`, these are wiped if omitted:

- `system_prompt`
- `actions`
- `emoji`
- `model`
- `temperature`
- `params_schema`
- `description`

**Always fetch and merge before saving.**

### Model Not Available

**Symptom:** Error about model not found.

**Valid models:**

- `openai-gpt-4o`
- `openai-gpt-4o-mini`
- `anthropic-claude-sonnet-4`
- `anthropic-claude-opus-4`

## Debugging Steps

### 1. Check Agent Config

Inspect the full agent config returned by `relevance_get_agent({ agentId: "..." })`.

Verify:

- `system_prompt` is set
- `actions` array has tools
- Each action has `project` and `region`

### 2. Check Agent Tools

```typescript
const tools = await relevance_get_agent_tools({ agentId: '...' });
```

Verify:

- Tools are attached
- Action IDs are generated

### 3. Check Conversation

```typescript
const task = await relevance_get_task_view({
  agentId: '...',
  taskId: '...',
  fullMode: true,
});
```

Look for:

- Error messages
- Failed tool calls
- Unexpected tool outputs

### 4. Check Triggers

```typescript
const triggers = await relevance_list_agent_triggers({ agentId: '...' });
```

Verify:

- Trigger exists
- OAuth account is valid
- Configuration is correct

## Tool/Transformation Errors

### "must NOT have additional properties"

**Symptom:** Error like `Studio transformation python_code_transformation input validation error: must NOT have additional properties {"additionalProperty":"variables"}`

**Cause:** Using a parameter that doesn't exist in the transformation schema.

**Fix:** Check the transformation schema before using parameters:

```typescript
// Find the transformation schema
const transform = await relevance_get_transformation({
  transformationId: 'python_code_transformation',
});
// Check transform.params_schema for valid parameters
```

**Common invalid parameters:**

- `variables` in `python_code_transformation` - doesn't exist
- Custom params that aren't in the schema

### Tool Syntax Errors with Template Substitution

**Symptom:** Python code fails with syntax errors when processing data from previous steps.

**Cause:** Template substitution (`{{steps.x.output}}`) inserts raw text that may contain characters breaking the code.

**Options:**

1. Use `js_code_transformation` which has native `steps` object access
2. For simple values in Python, use string quotes: `value = "{{steps.x.output.field}}"`
3. Check for special characters in the data being substituted

## Getting Help

1. Use `relevance_get_agent` to dump full config
2. Check conversation with `relevance_get_task_view`
3. Test tools independently with `relevance_run_tool`
4. Review OAuth with `relevance_list_oauth_accounts`
5. Check transformation schemas with `relevance_get_transformation`
