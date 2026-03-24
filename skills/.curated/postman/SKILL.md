---
name: "postman"
description: "Use when the user needs to work with Postman from Codex, including MCP setup, workspace and collection discovery, spec and collection sync, test runs, mocks, documentation, security audits, one-off requests, local Postman CLI workflows, or API agent-readiness analysis."
metadata:
  short-description: "Use Postman MCP and CLI workflows from Codex"
---

# Postman

Use this as the umbrella Postman skill. It handles setup, MCP verification, workspace discovery, and routing to the right focused Postman skill.

For MCP setup and verification details, read `references/setup-and-mcp.md`.

## Skill boundaries

- Use this skill when the user broadly says "Postman" or needs setup, API key guidance, workspace verification, or help picking the right Postman workflow.
- If the task clearly maps to a focused workflow, switch to the matching sibling skill instead of keeping all logic here.
- Do not send users to `postman-setup`, `postman-cli`, or `postman-knowledge`. Those are folded into this umbrella skill and the focused siblings.

## Routing

Use these focused skills when the intent is specific:

| Intent | Skill |
|---|---|
| Set up Postman MCP or verify workspace access | stay in `postman` |
| Search Postman workspaces, sync specs and collections, or generate client code | [postman-build](../postman-build/SKILL.md) |
| Run Postman cloud tests, create mocks, or audit API security | [postman-validate](../postman-validate/SKILL.md) |
| Generate or publish API docs | [postman-docs](../postman-docs/SKILL.md) |
| Send one-off requests, run local collections, or generate and lint specs | [postman-local](../postman-local/SKILL.md) |
| Evaluate API agent-readiness | [postman-readiness](../postman-readiness/SKILL.md) |

## Setup flow

1. Verify the Postman MCP server with `getAuthenticatedUser`.
2. If it fails, guide the user to set `POSTMAN_API_KEY`.
3. Re-check connectivity, then list workspaces, collections, and specs.
4. Route to the focused skill that best matches the task.

## Operating rules

- Prefer a focused sibling skill over ad hoc MCP or CLI usage.
- Use Postman MCP for remote workspace, collection, spec, test, mock, docs, and search workflows.
- Use the Postman CLI for one-off requests, local collection runs, and spec linting.
- If MCP is unavailable, only continue with local static analysis when the workflow still makes sense without remote Postman access.
- Never print raw API keys or secrets.
