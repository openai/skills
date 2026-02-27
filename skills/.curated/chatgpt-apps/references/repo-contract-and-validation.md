# Repo Contract And Validation

Load this reference when scaffolding or reviewing a generated ChatGPT app repo.

The goal is not “files were created.” The goal is “the repo is plausibly runnable and follows a stable working-app contract.”

## Minimum Working Repo Contract

Every generated repo should satisfy the relevant parts of this contract.

### 1. Shape

- The repo shape matches the chosen archetype.
- The repo structure is simple enough that a user can identify where the server and widget live.

### 2. Server

- There is a clear MCP server entry point.
- The server exposes `/mcp`.
- The server registers tools intentionally.
- If a UI exists, the server registers a resource/template with the MCP Apps UI MIME type.

### 3. Tools

- Each tool maps to one user intent.
- Descriptions help the model choose the tool.
- Required annotations are present and accurate.
- UI-linked tools use `_meta.ui.resourceUri`.
- `_meta["openai/outputTemplate"]` is treated as optional compatibility, not the primary contract.
- When the app is connector-like, data-only, sync-oriented, or intended for company knowledge or deep research, it implements standard `search` and `fetch` tools instead of custom substitutes.

### 4. Widget

- The widget initializes the MCP Apps bridge when needed.
- The widget can receive `ui/notifications/tool-result`.
- The widget renders from `structuredContent`.
- Interactive widgets use `tools/call`.
- Baseline follow-up messaging uses `ui/message`.
- `window.openai` is optional and additive.

### 5. Local Developer Experience

- There is a clear way to start the app locally.
- There is at least one low-cost check command when the stack supports it.
- The response explains how to connect the app in ChatGPT Developer Mode when relevant.

## Validation Ladder

Run the highest level you can without overfitting to a single stack.

### Level 0: Static contract review

Check for:

- chosen archetype is sensible
- repo shape matches archetype
- `/mcp` route is present
- tool/resource/widget responsibilities are coherent
- if the app is connector-like or sync-oriented, `search` and `fetch` are present with the expected standard shape

### Level 1: Syntax or compile checks

Use the stack-appropriate cheapest check available, for example:

- Python syntax check
- TypeScript compile check
- framework-specific lint or build sanity check if already installed

### Level 2: Local runtime sanity

If feasible:

- start the server
- confirm the health route or `/mcp` endpoint responds

### Level 3: Host loop validation

If feasible:

- inspect with MCP Inspector
- test through ChatGPT Developer Mode
- confirm widget updates after tool results

## Reporting Rule

Always say which validation level was reached and what was not run.

That makes the skill more reliable because it separates:

- “repo shape looks right”
- “syntax is valid”
- “server starts”
- “host integration was actually exercised”
