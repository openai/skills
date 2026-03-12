# Relevance AI MCP Setup

## Prerequisites

- A Relevance AI account at [app.relevanceai.com](https://app.relevanceai.com)
- Your project credentials: **Region code**, **Project ID**, and **API key** (starts with `sk-`)

These can be found in your Relevance AI project settings.

## Configuration

The Relevance AI MCP server connects via Streamable HTTP transport. After adding the MCP dependency, authenticate with your project credentials when prompted.

### Remote MCP Server

The hosted MCP server is available at:

```
https://mcp.relevanceai.com/
```

No local installation is required. The server handles authentication via your API key passed as part of the MCP connection.

## Verification

After setup, verify the connection works:

1. Run `relevance-ai:relevance_list_agents` — should return your project's agents (or an empty list for new projects).
2. Run `relevance-ai:relevance_list_tools` — should return your project's tools.

If either call fails with an authentication error, verify your API key and project ID are correct.

## Multi-project support

The MCP server supports switching between multiple Relevance AI projects without reconnecting:

- `relevance-ai:relevance_list_projects` — list configured projects
- `relevance-ai:relevance_switch_project` — switch to a different project
- `relevance-ai:relevance_get_active_project` — check which project is active

This is useful when managing staging and production environments or multiple client projects.
