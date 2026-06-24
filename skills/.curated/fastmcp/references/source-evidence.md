# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. It is not a replacement for the workflows and mastery references; it explains which real repository patterns the skill is expected to cover.

## Retrieved Sources

- `OpenHands/OpenHands`: dependency evidence for `fastmcp>=3.2,<4`, `mcp>=1.25`, and lock evidence for `fastmcp` 3.2.4.
- `pydantic/pydantic-ai`: optional MCP extras, `fastmcp` dependency paths, and lock evidence for `fastmcp` 3.3.0 / `fastmcp-slim` 3.3.0.
- `modelcontextprotocol/python-sdk`: source package using `mcp[cli,ws]` and the Python SDK entrypoint model.
- `lastmile-ai/mcp-agent`: agent runtime dependency evidence for `mcp>=1.20.0`.

## Workflows Reflected In The Skill

### Server Capability Design

The skill must teach an agent to design a server around MCP primitives, not just import `FastMCP`. Evidence from source repos shows MCP used as an integration boundary for agents and applications, so the skill covers:

- Choosing tools for actions, resources for readable state, and prompts for reusable task templates.
- Keeping tool names stable and side-effect descriptions explicit.
- Returning structured, JSON-compatible outputs rather than unstructured prose when clients need to compose results.

### Version And Transport Diagnosis

The mined repos include FastMCP 2.x and 3.x era packages plus MCP SDK 1.20+ through 1.27. Because CLI and transport names can move, the skill requires version capture before recommending a command. It also requires choosing transport by client target:

- `stdio` for desktop and local agent clients.
- HTTP/SSE/streamable HTTP for hosted, multi-client, or web deployments.
- Explicit client configuration only after the server entrypoint has been run locally.

### Inspection And Client Compatibility

The source repos use MCP to connect server capabilities to clients, so the skill requires protocol-level discovery:

- List exposed tools/resources/prompts from an MCP client or inspector.
- Call at least one read-only tool before claiming success.
- Call a side-effecting tool only when the server exposes one and the test environment is safe.
- Diagnose empty discovery by checking import-time registration, process startup, and transport mismatch.

### Deployment And Security

MCP servers frequently bridge local secrets, remote APIs, and filesystem/network access. The skill therefore requires:

- Environment-variable or secret-store based credentials.
- Clear permission notes for filesystem, network, and write actions.
- Hosted deployment notes for auth, CORS/origin handling, and health checks.

## Remaining Review Questions

When reviewing this skill, reject changes that make it a library summary. It must leave a fresh agent able to produce a runnable server, inspect it through MCP, diagnose transport/version problems, and produce client configuration grounded in a verified entrypoint.
