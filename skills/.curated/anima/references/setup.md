# Setup: Anima MCP Connection

If any Anima MCP call fails, pause and set up the connection. There are two authentication approaches depending on your environment.

## Interactive environments (Claude Code, Cursor, Codex, etc.)

These editors support browser-based OAuth. Add the Anima MCP server using your editor's MCP configuration, pointing to:

**Server URL:** `https://public-api.animaapp.com/v1/mcp`
**Transport:** HTTP

When prompted, authenticate in the browser with your Anima account. Optionally connect your Figma account during authentication to enable Figma flows.

Each editor has its own way to add MCP servers. Check your editor's MCP documentation for the specific steps.

## Headless environments (OpenClaw, server-side agents)

These environments use an API token instead of browser login. Your MCP client handles the connection. You just need to provide:

**Server URL:** `https://public-api.animaapp.com/v1/mcp`
**Transport:** HTTP
**Authorization:** Bearer token using your Anima API key

### Getting your API key

1. Go to [dev.animaapp.com](https://dev.animaapp.com)
2. Open **Settings** (gear icon)
3. Navigate to **API Keys**
4. Choose an expiration period and click **Generate API Key**
5. Copy the key and store it securely. You won't be able to see it again.

### Connecting

Configure your MCP client (mcporter, MCP Port, or any MCP-compatible tool) with the server URL above and pass the API key as a Bearer token in the Authorization header. Refer to your MCP client's documentation for specific configuration steps.

**Important:** Set your MCP client's timeout to at least 10 minutes (600000ms). Playground generation builds full applications and typically takes 3-7 minutes. Default timeouts will fail.
