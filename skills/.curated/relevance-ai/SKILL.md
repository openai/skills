---
name: relevance-ai
description: Manage AI agents, tools & multi-agent workforces on Relevance AI. Use when the user wants to create agents, build tool workflows, orchestrate multi-agent systems, or manage knowledge tables via the Relevance AI API.
license: Apache-2.0
metadata:
  short-description: Manage AI agents, tools, and workflows on Relevance AI
---

## Overview

The Relevance AI MCP integration enables building and managing AI agent systems. Connect to your Relevance AI project to create agents, build tool workflows, orchestrate multi-agent pipelines, and manage knowledge tables — all from within Codex.

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 0: Set up Relevance AI MCP (if not already configured)

If any MCP call fails because the Relevance AI MCP is not connected, pause and set it up:

1. Add the Relevance AI MCP:
   - `codex mcp add relevance-ai --url https://mcp.relevanceai.com/`
2. Enable remote MCP client:
   - Set `[features] rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in:
   - `codex mcp login relevance-ai`

After successful login, the user will have to restart Codex. Finish your answer and tell them so — when they try again they can continue with Step 1.

### Step 1: Verify connectivity

Run `relevance-ai:relevance_list_agents` and `relevance-ai:relevance_list_tools` to confirm the MCP connection is working. If either fails, revisit Step 0.

### Step 2: Identify the goal

Clarify the user's goal — creating an agent, building a tool, setting up a workforce, or querying knowledge. Confirm scope before executing.

### Step 3: Execute the appropriate workflow

Select the matching workflow below and execute tool calls in logical batches — read first, then create or update.

### Step 4: Summarize results

Report what was created or changed, call out remaining gaps or blockers, and propose next actions.

## Available Tools

The MCP server provides 46 tools organized across six domains:

| Domain | Key tools |
|--------|-----------|
| Agents | `list_agents`, `get_agent`, `upsert_agent`, `save_agent_draft`, `attach_tools_to_agent`, `trigger_agent_sync` |
| Tools | `list_tools`, `get_tool`, `upsert_tool`, `trigger_tool`, `search_tools`, `search_transformations` |
| Workforces | `list_workforces`, `create_workforce`, `trigger_workforce`, `get_workforce_task_messages` |
| Knowledge | Via `raw_api` — add, list, update, delete rows in knowledge tables |
| Marketplace | `search_marketplace_listings`, `clone_marketplace_listing`, `search_public_tools` |
| Triggers | `list_agent_triggers`, `create_trigger`, `delete_trigger` |

## Workflows

### Creating an agent

1. **Create the agent** with `relevance-ai:relevance_upsert_agent` — provide name, description, and system prompt.
2. **Find and attach tools** — search existing tools with `relevance-ai:relevance_search_tools`, public tools with `relevance-ai:relevance_search_public_tools`, or 8000+ integrations with `relevance-ai:relevance_search_transformations`.
3. **Attach tools** using `relevance-ai:relevance_attach_tools_to_agent` — this handles fetch, merge, save, publish, and action ID retrieval in one call.
4. **Test the agent** with `relevance-ai:relevance_trigger_agent_sync` — sends a message and waits for the complete response, including tool call details.

### Building a tool

1. **Search for existing solutions** before building from scratch — check project tools, public tools, marketplace listings, and transformations in that order.
2. **Create from transformation** with `relevance-ai:relevance_create_tool_from_transformation` for the fastest path — auto-generates params, state mapping, and bindings.
3. **Or build custom** with `relevance-ai:relevance_upsert_tool` — define params_schema, transformation steps, and output configuration.
4. **Test the tool** with `relevance-ai:relevance_trigger_tool` — execute with sample parameters and verify output.

### Creating a multi-agent workforce

1. **Build individual agents** first — each agent should handle a specific part of the workflow.
2. **Create the workforce** with `relevance-ai:relevance_create_workforce` — define agents and their connections (defaults to a linear chain with forced-handover edges).
3. **Trigger the workforce** with `relevance-ai:relevance_trigger_workforce` — send a message to start the pipeline.
4. **Monitor execution** with `relevance-ai:relevance_get_workforce_task_messages` — see what each agent produced and the overall state.

### Managing knowledge tables

Use `relevance-ai:relevance_raw_api` for knowledge operations:
- **Add rows**: `POST /knowledge/add` with `knowledge_set` and `data` array
- **List rows**: `POST /knowledge/list` with `knowledge_set`
- **Update rows**: `POST /knowledge/bulk_update` with `knowledge_set` and `updates`
- **Delete rows**: `POST /knowledge/delete` with `knowledge_set` and `filters`

Tables are created implicitly when you add the first row.

## Important rules

### Agent updates require full config

Agent saves do NOT support partial updates — omitted fields are wiped. Always fetch the current config first, merge your changes, then save:

```
1. Fetch: relevance-ai:relevance_get_agent → get full agent config
2. Merge: modify only the fields you need
3. Save: relevance-ai:relevance_save_agent_draft with the complete config
```

### Use attach_tools_to_agent for adding tools

Do not manually edit the agent's `actions` array. Use `relevance-ai:relevance_attach_tools_to_agent` which handles the fetch-merge-save-publish cycle and retrieves action IDs automatically.

### Workforces replace sub-agents

Adding sub-agents to an agent's `actions` array is deprecated. Use workforces for all multi-agent orchestration.

### Tool search order

When looking for tools to accomplish a task, search in this order:
1. Project tools (`search_tools`) — already built and configured
2. Public/community tools (`search_public_tools`) — pre-built, sorted by popularity
3. Marketplace listings (`search_marketplace_listings`) — complete bundled solutions
4. Transformations (`search_transformations`) — 8000+ integrations to wrap as tools

### Test tools before attaching

Always test a tool with `relevance-ai:relevance_trigger_tool` before attaching it to an agent. Tools that return empty `{}` need their output configuration fixed.

## References

- `reference/setup.md` — MCP server configuration, authentication, and project setup
- [Relevance AI documentation](https://relevanceai.com/docs) — full platform docs
- [API documentation](https://api-f1db6c.stack.tryrelevance.com/latest/documentation) — complete API reference
