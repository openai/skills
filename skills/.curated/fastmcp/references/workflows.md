# FastMCP Workflows

Use these workflows to produce a complete MCP server change rather than a decorator summary.

## Contents

- [Server Design](#server-design)
- [Local Server Verification](#local-server-verification)
- [Client Configuration](#client-configuration)
- [Auth and Secrets](#auth-and-secrets)
- [Deployment Review](#deployment-review)
- [Final Artifact](#final-artifact)

## Server Design

1. Name the server for the domain, not the implementation.
2. List user tasks, then map them to MCP primitives:
   - Tools: actions or computations.
   - Resources: readable state or documents.
   - Prompts: reusable task templates.
3. Mark every side effect in the tool name, docstring, and final notes.
4. Keep inputs typed and JSON-compatible.
5. Return structured results with stable fields.

Tool contract template:

```text
tool:
purpose:
inputs:
side effects:
auth/env:
success response:
failure modes:
read-only test:
```

## Local Server Verification

Run these before client configuration:

```bash
python -m pytest
python - <<'PY'
import importlib.util
path = "server.py"
spec = importlib.util.spec_from_file_location("server_under_test", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print("loaded", path)
PY
python server.py
```

Then use the MCP client, SDK, `fastmcp dev`, or MCP Inspector supported by the installed version to list tools/resources and call at least one read-only tool.

## Client Configuration

For stdio clients, produce:

```json
{
  "command": "python",
  "args": ["server.py"],
  "cwd": "<repo root>",
  "env": {
    "SERVICE_API_KEY": "set outside config when possible"
  }
}
```

For HTTP deployments, record:

```text
url:
transport:
auth:
headers:
health check:
allowed origins:
timeout:
```

## Auth and Secrets

- Read secrets from environment, keychain, or hosting secret store.
- Do not accept secrets as prompt text or tool arguments unless the task is explicitly secret management.
- Add startup checks for required environment variables.
- Return actionable errors when auth is missing.

## Deployment Review

Before shipping:

- Confirm process manager or hosting command.
- Confirm logs do not print secrets.
- Confirm side-effect tools have names that make writes obvious.
- Confirm client discovery shows descriptions and schemas.
- Confirm one representative failure response is useful.

## Final Artifact

Final notes should include:

```text
server entrypoint:
transport:
client config:
versions:
tools/resources/prompts discovered:
tested calls:
required secrets:
known side effects:
```
