# Relevance AI MCP Setup

## Prerequisites

- A Relevance AI account at [app.relevanceai.com](https://app.relevanceai.com)

## Configuration

The Relevance AI MCP server connects via Streamable HTTP transport. Authentication is handled via OAuth.

### Remote MCP Server

```
https://mcp.relevanceai.com/
```

No local installation is required.

### Setup steps

1. Add the Relevance AI MCP:
   - `codex mcp add relevance-ai --url https://mcp.relevanceai.com/`
2. Enable remote MCP client:
   - Set `[features] rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in with OAuth:
   - `codex mcp login relevance-ai`
4. Restart Codex after successful login.

## Verification

After setup, verify the connection works:

1. Run `relevance-ai:relevance_list_agents` — should return your project's agents (or an empty list for new projects).
2. Run `relevance-ai:relevance_list_tools` — should return your project's tools.

If either call fails with an authentication error, re-run `codex mcp login relevance-ai` and restart Codex.
