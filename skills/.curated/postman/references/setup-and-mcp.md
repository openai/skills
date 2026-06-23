# Setup And MCP

Use this reference when the task starts with setup, authentication, or workspace verification.

## MCP configuration

Use this MCP server configuration as the baseline:

```json
{
  "mcpServers": {
    "postman": {
      "type": "http",
      "url": "https://mcp.postman.com/mcp",
      "headers": {
        "Authorization": "Bearer ${POSTMAN_API_KEY}",
        "X-Source": "codex-plugin"
      }
    }
  }
}
```

## API key setup

Ask the user to set `POSTMAN_API_KEY` to a key that starts with `PMAK-`.

```bash
export POSTMAN_API_KEY=PMAK-your-key-here
```

If they want it persisted, suggest adding it to `~/.zshrc` or `~/.bashrc`.

## Verification flow

1. Verify MCP connectivity with `getAuthenticatedUser`.
2. If successful, list workspaces with `getWorkspaces`.
3. For the chosen workspace, inspect collections with `getCollections`.
4. Inspect specs with `getAllSpecs`.
5. Summarize the authenticated user, visible workspaces, collection counts, and spec counts.

Example result shape:

```text
Connected as: <user name>

Workspaces:
  - My Workspace — 12 collections, 3 specs
  - Team APIs — 8 collections, 5 specs
```

## Failure handling

- MCP unavailable: explain that the Postman MCP server is not loaded or configured.
- `401`: tell the user the API key was rejected and suggest checking for whitespace or generating a new key.
- Timeout: suggest checking network access and `https://status.postman.com`.

## Next-step routing

- Collections exist: move to search, tests, codegen, docs, or mocks.
- Specs exist but collections do not: move to sync.
- Workspace is empty: start from a local OpenAPI spec and sync it into Postman.
