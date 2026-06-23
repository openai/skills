# Simple Language Development

Development skill for the [Simple Language](https://github.com/ormastes/simple) compiler and toolchain.

## What it does

Provides 68 MCP tools for Simple Language projects:
- **Code intelligence** — diagnostics, completions, hover, go-to-definition for `.spl`/`.shs` files
- **Debugging** — DAP integration, breakpoints, step execution, variable inspection
- **Build** — compile, native-build, release, cross-compilation
- **Test** — run specs, SSpec BDD framework, test isolation
- **VCS** — jj (Jujutsu) operations, commit, push, rebase
- **Analysis** — code search, symbol lookup, documentation coverage

## Setup

Install the MCP server:

```bash
npx @simple-lang/mcp-server
```

Or add to your Codex config (`.codex/config.toml`):

```toml
[mcp.simple-mcp]
command = "npx"
args = ["-y", "@simple-lang/mcp-server"]
```

## Links

- **Repository:** https://github.com/ormastes/simple
- **npm:** https://www.npmjs.com/package/@simple-lang/mcp-server
- **MCP Registry:** https://registry.modelcontextprotocol.io/servers/io.github.ormastes/simple-mcp-server
