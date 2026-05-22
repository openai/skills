---
name: fastmcp
description: Build, test, inspect, package, or deploy Python MCP servers with FastMCP. Use when creating MCP tools/resources/prompts, wrapping an API or database as an MCP server, debugging stdio/HTTP MCP transport, generating clients from server schemas, or preparing an MCP server for Codex, ChatGPT Apps, Claude Desktop, or other MCP clients.
---

# FastMCP

Use this skill for Python MCP servers built with FastMCP. Prefer the current project conventions when an MCP server already exists; otherwise create a small, explicit server module that can run locally before adding deployment or client configuration.

## Validated Version Evidence

This guidance was checked against mined repositories using `fastmcp` 2.12.5, 3.2.0, 3.2.4, and 3.3.0, plus `mcp` 1.12.4 through 1.27.0. The CLI and transport surface changes across those versions, so capture installed versions before relying on a specific command:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["fastmcp", "mcp"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to leave the user with a working MCP server or a precise compatibility diagnosis. A complete run produces:

- The installed `fastmcp`/`mcp` versions and chosen transport.
- A minimal server entrypoint or a patch to the repo's existing server.
- A list of discoverable tools/resources/prompts from an MCP client or inspector.
- At least one read-only tool call result, and one write/action call result when the server exposes side effects.
- Client configuration notes for Codex, ChatGPT Apps, Claude Desktop, or the target runtime.

## Standalone Quick Start

If the project has no server yet, create the smallest server that proves FastMCP works:

```python
from fastmcp import FastMCP

mcp = FastMCP("demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

Run it locally, then inspect it with the MCP client or inspector available in that FastMCP version. If the project already has a server, do not replace it; add one narrow tool/resource and verify discovery.

## Workflow

1. Inspect the repo for existing MCP code, package tooling, and runtime entrypoints.
2. Identify the client target: Codex, ChatGPT Apps, Claude Desktop, a web service, or a custom MCP client.
3. Choose transport deliberately:
   - `stdio` for local desktop/client integrations.
   - `streamable-http` or HTTP/SSE for hosted or multi-client access.
4. Define a narrow capability surface: tools for actions, resources for readable state, prompts for reusable task templates.
5. Add input validation and clear error messages before wiring external APIs or databases.
6. Run the server locally and inspect the exposed tools/resources before declaring it complete.

## Client Configuration Checklist

- `stdio`: record the command, working directory, and required environment variables.
- HTTP/streamable HTTP: record host, port, auth method, CORS/origin requirements, and health endpoint if present.
- Desktop clients: provide the exact server config block only after confirming the entrypoint command works.
- Hosted clients: state how secrets are injected and which tools have side effects.

## References

Open `references/workflows.md` for detailed server design, client configuration, testing, auth, transport, deployment, and review workflows.

Open `references/mastery.md` for MCP design principles, primitive selection, schema quality, transport tradeoffs, security boundaries, and review standards.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in mined/source repository evidence.

## Implementation Guidance

- Keep tool names stable, verb-oriented, and specific.
- Use typed function signatures and docstrings; MCP clients use these as interface documentation.
- Return structured JSON-compatible data for tools unless the client specifically expects text.
- Avoid hidden writes. Tool names and descriptions should make side effects obvious.
- For network or filesystem actions, document required environment variables and permissions in the server code or project docs.
- Keep authentication outside the prompt surface: read tokens from environment variables, keychains, or the hosting platform secret store.

## Local Checks

Use the package manager already present in the repository. Typical checks:

```bash
python -m pytest
python <server-file>
```

Before testing through a client, verify the server module imports cleanly and registers its decorators:

```bash
python - <<'PY'
import importlib.util

path = "<server-file>"
spec = importlib.util.spec_from_file_location("mcp_server_under_test", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(f"loaded {path}")
PY
```

Replace `<server-file>` with the actual entrypoint discovered in the repository. Then run the server and use the project-supported MCP client, SDK, `fastmcp dev`, or MCP Inspector to list tools/resources and call one read-only tool. Prefer capability discovery from the client protocol over assuming a command exists in every FastMCP version.

## Debugging

- If a client sees no tools, verify the server process starts cleanly and that tool decorators execute at import time.
- If calls hang, check whether a synchronous tool is doing blocking network or subprocess work without timeouts.
- If JSON schema generation fails, simplify annotations to standard Python types or Pydantic models.
- If hosted auth fails, confirm the server can read the same environment variables in the deployed runtime.

## Done Criteria

- The server starts from a documented command.
- Tools/resources/prompts are discoverable by an MCP client or inspector.
- At least one read-only call and one representative write/action call are tested when applicable.
- Required secrets, network access, and side effects are explicit.
- The final notes include the client config or the exact reason it cannot be produced.
