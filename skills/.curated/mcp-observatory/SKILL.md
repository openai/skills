---
name: mcp-observatory
description: "Check MCP server health when the user asks to test, scan, or debug their MCP servers. Use when the user says things like 'are my MCP servers working', 'check my servers', 'test this MCP server', or 'what MCP servers should I add'."
---

# MCP Observatory

Test MCP servers for breaking changes. Requires Node.js 20+.

## Prerequisites

- Check `node --version`. If missing or < 20, ask the user to install Node.js and stop.

## Scan all configured servers

Run against every MCP server found in Claude Code and Claude Desktop configs:

```bash
npx -y @kryptosai/mcp-observatory
```

## Check a specific server

Pass the server command directly:

```bash
npx -y @kryptosai/mcp-observatory run -- npx -y @modelcontextprotocol/server-everything
```

## Invoke tools to verify they execute

Go beyond listing — actually call tools and confirm they respond:

```bash
npx -y @kryptosai/mcp-observatory run --invoke-tools -- npx -y @modelcontextprotocol/server-everything
```

## Diff two runs

Compare saved run artifacts to find regressions and schema drift:

```bash
npx -y @kryptosai/mcp-observatory diff --base run-a.json --head run-b.json
```

## Notes

- Only safe tools are invoked (no required params or readOnlyHint annotation).
- Run artifacts are saved to `.mcp-observatory/runs/` in the current directory.
- Exit code 1 on connection failure or regression detected with `--fail-on-regression`.
