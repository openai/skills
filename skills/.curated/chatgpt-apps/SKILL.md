---
name: chatgpt-apps
description: Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply Apps SDK metadata or CSP or domain settings, or produce a docs-aligned project scaffold. Prefer a docs-first workflow by invoking the openai-docs skill or OpenAI developer docs MCP tools before generating code.
---

# ChatGPT Apps

## Overview

Scaffold ChatGPT Apps SDK implementations with a docs-first, example-first workflow, then generate code that follows current Apps SDK and MCP Apps bridge patterns.

Use this skill to produce:

- A primary app-archetype classification and repo-shape decision
- A tool plan (names, schemas, annotations, outputs)
- An upstream starting-point recommendation (official example, ext-apps example, or local fallback scaffold)
- An MCP server scaffold (resource registration, tool handlers, metadata)
- A widget scaffold (MCP Apps bridge first, `window.openai` compatibility/extensions second)
- A reusable Node + `@modelcontextprotocol/ext-apps` starter scaffold for low-dependency fallbacks
- A validation report against the minimum working repo contract
- Local dev and connector setup steps
- A short stakeholder summary of what the app does (when requested)

## Mandatory Docs-First Workflow

Use `$openai-docs` first whenever building or changing a ChatGPT Apps SDK app.

1. Invoke `$openai-docs` (preferred) or call the OpenAI docs MCP server directly.
2. Fetch current Apps SDK docs before writing code, especially (baseline pages):
   - `apps-sdk/build/mcp-server`
   - `apps-sdk/build/chatgpt-ui`
   - `apps-sdk/build/examples`
   - `apps-sdk/plan/tools`
   - `apps-sdk/reference`
3. Fetch `apps-sdk/quickstart` when scaffolding a new app or generating a first-pass implementation, and check the official examples repo/page before inventing a scaffold from scratch.
4. Fetch deployment/submission docs when the task includes local ChatGPT testing, hosting, or public launch:
   - `apps-sdk/deploy`
   - `apps-sdk/deploy/submission`
   - `apps-sdk/app-submission-guidelines`
5. Cite the docs URLs you used when explaining design choices or generated scaffolds.
6. Prefer current docs guidance over older repo patterns when they differ, and call out compatibility aliases explicitly.
7. If doc search times out or returns poor matches, fetch the canonical Apps SDK pages directly by URL and continue; do not let search failure block scaffolding.

If `$openai-docs` is unavailable, use:

- `mcp__openaiDeveloperDocs__search_openai_docs`
- `mcp__openaiDeveloperDocs__fetch_openai_doc`

Read `references/apps-sdk-docs-workflow.md` for suggested doc queries and a compact checklist.
Read `references/app-archetypes.md` to classify the request into a small number of supported app shapes before choosing examples or scaffolds.
Read `references/repo-contract-and-validation.md` when generating or reviewing a repo so the output stays inside a stable “working app” contract.
Read `references/search-fetch-standard.md` when the app is connector-like, data-only, sync-oriented, or meant to work well with company knowledge or deep research.
Read `references/upstream-example-workflow.md` when starting a greenfield app or when deciding whether to adapt an upstream example or use the local fallback scaffold.
Read `references/window-openai-patterns.md` when the task needs ChatGPT-specific widget behavior or when translating repo examples that use wrapper-specific `app.*` helpers.

## Prompt Guidance

Use prompts that explicitly pair this skill with `$openai-docs` so the resulting scaffold is grounded in current docs.

Preferred prompt patterns:

- `Use $chatgpt-apps with $openai-docs to scaffold a ChatGPT app for <use case> with a <TS/Python> MCP server and <React/vanilla> widget.`
- `Use $chatgpt-apps with $openai-docs to adapt the closest official Apps SDK example into a ChatGPT app for <use case>.`
- `Use $chatgpt-apps and $openai-docs to refactor this Apps SDK demo into a production-ready structure with tool annotations, CSP, and URI versioning.`
- `Use $chatgpt-apps with $openai-docs to plan tools first, then generate the MCP server and widget code.`

When responding, ask for or infer these inputs before coding:

- Use case and primary user flows
- Read-only vs mutating tools
- Demo vs production target
- Private/internal use vs public directory submission
- Backend language and UI stack
- Auth requirements
- External API domains for CSP allowlists
- Hosting target and local dev approach
- Org ownership/verification readiness (for submission tasks)

## Classify The App Before Choosing Code

Before choosing examples, repo shape, or scaffolds, classify the request into one primary archetype and state it.

- `tool-only`
- `vanilla-widget`
- `react-widget`
- `interactive-decoupled`
- `submission-ready`

Infer the archetype unless a missing detail is truly blocking. Use the archetype to choose:

- whether a UI is needed at all
- whether to preserve a split `server/` + `web/` layout
- whether to prefer official OpenAI examples, ext-apps examples, or the local fallback scaffold
- which validation checks matter most
- whether `search` and `fetch` should be the default read-only tool surface

Read `references/app-archetypes.md` for the decision rubric.

## Default Starting-Point Order

For greenfield apps, prefer these starting points in order:

1. **Official OpenAI examples** when a close example already matches the requested stack or interaction pattern.
2. **Version-matched `@modelcontextprotocol/ext-apps` examples** when the user needs a lower-level or more portable MCP Apps baseline.
3. **`scripts/scaffold_node_ext_apps.mjs`** only when no close example fits, the user wants a tiny Node + vanilla starter, or network access/example retrieval is undesirable.

Do not generate a large custom scaffold from scratch if a close upstream example already exists.
Copy the smallest matching example, remove unrelated demo code, then patch it to the current docs and the user request.

## Build Workflow

### 0. Classify The App Archetype

Pick one primary archetype before planning tools or choosing a starting point.

- Prefer a single primary archetype instead of mixing several.
- If the request is broad, infer the smallest archetype that can still satisfy it.
- Escalate to `submission-ready` only when the user asks for public launch, directory submission, or review-ready deployment.
- Call out the chosen archetype in your response so the user can correct it early if needed.

### 1. Plan Tools Before Code

Define the tool surface area from user intents.

- Use one job per tool.
- Write tool descriptions that start with "Use this when..." behavior cues.
- Make inputs explicit and machine-friendly (enums, required fields, bounds).
- Decide whether each tool is data-only, render-only, or both.
- Set annotations accurately (`readOnlyHint`, `destructiveHint`, `openWorldHint`; add `idempotentHint` when true).
- If the app is connector-like, data-only, sync-oriented, or intended for company knowledge or deep research, default to the standard `search` and `fetch` tools instead of inventing custom read-only equivalents.
- For educational/demo apps, prefer one concept per tool so the model can pick the right example cleanly.
- Group demo tools by learning objective: data into the widget, widget actions back into the conversation or tools, host/layout environment signals, and lifecycle/streaming behavior.

Read `references/search-fetch-standard.md` when `search` and `fetch` may be relevant.

### 2. Choose an App Architecture

Choose the simplest structure that fits the goal.

- Use a **minimal demo pattern** for quick prototypes, workshops, or proofs of concept.
- Use a **decoupled data/render pattern** for production UX so the widget does not re-render on every tool call.

Prefer the decoupled pattern for non-trivial apps:

- Data tools return reusable `structuredContent`.
- Render tools attach `_meta.ui.resourceUri` and optional `_meta["openai/outputTemplate"]`.
- Render tool descriptions state prerequisites (for example, "Call `search` first").

### 2a. Start From An Upstream Example When One Fits

Default to upstream examples for greenfield work when they are close to the requested app.

- Check the official OpenAI examples first for ChatGPT-facing apps, polished UI patterns, React components, file upload flows, modal flows, or apps that resemble the docs examples.
- Use `@modelcontextprotocol/ext-apps` examples when the request is closer to raw MCP Apps bridge/server wiring, or when version-matched package patterns matter more than ChatGPT-specific polish.
- Pick the smallest matching example and copy only the relevant files; do not transplant an entire showcase app unchanged.
- After copying, reconcile the example with the current docs you fetched: tool names/descriptions, annotations, `_meta.ui.*`, CSP, URI versioning, and local run instructions.
- State which example you chose and why in one sentence.

Read `references/upstream-example-workflow.md` for the selection and adaptation rubric.

### 2b. Use the Starter Script When a Low-Dependency Fallback Helps

Use `scripts/scaffold_node_ext_apps.mjs` only when the user wants a quick, greenfield Node starter and a vanilla HTML widget is acceptable, and no upstream example is a better starting point.

- Run it only after fetching current docs, then reconcile the generated files with the docs you fetched.
- If you choose the script instead of an upstream example, say why the fallback is better for that request.
- Skip it when a close official example exists, when the user already has an existing app structure, when they need a non-Node stack, when they explicitly want React first, or when they only want a plan/review instead of code.
- The script generates a minimal `@modelcontextprotocol/ext-apps` server plus a vanilla HTML widget that uses the MCP Apps bridge by default.
- The generated widget keeps follow-up messaging on the standard `ui/message` bridge and only uses `window.openai` for optional host signals/extensions.
- After running it, patch the generated output to match the current docs and the user request: adjust tool names/descriptions, annotations, resource metadata, URI versioning, and README/run instructions.

### 3. Scaffold the MCP Server

Generate a server that:

- Registers a widget resource/template with the MCP Apps UI MIME type (`text/html;profile=mcp-app`) or the SDK constant (`RESOURCE_MIME_TYPE`) when using `@modelcontextprotocol/ext-apps/server`
- Registers tools with clear names, schemas, titles, and descriptions
- Returns `structuredContent` (model + widget), `content` (model narration), and `_meta` (widget-only data) intentionally
- Keeps handlers idempotent or documents non-idempotent behavior explicitly
- Includes tool status strings (`openai/toolInvocation/*`) when helpful in ChatGPT

Keep `structuredContent` concise. Move large or sensitive widget-only payloads to `_meta`.

### 4. Scaffold the Widget UI

Use the MCP Apps bridge first for portability, then add ChatGPT-specific `window.openai` APIs when they materially improve UX.

- Listen for `ui/notifications/tool-result` (JSON-RPC over `postMessage`)
- Render from `structuredContent`
- Use `tools/call` for component-initiated tool calls
- Use `ui/update-model-context` only when UI state should change what the model sees

Use `window.openai` for compatibility and extensions (file upload, modal, display mode, etc.), not as the only integration path for new apps.

#### API Surface Guardrails

- Some examples wrap the bridge with an `app` object (for example, `@modelcontextprotocol/ext-apps/react`) and expose helper names like `app.sendMessage()`, `app.callServerTool()`, `app.openLink()`, or host getter methods.
- Treat those wrappers as implementation details or convenience layers, not the canonical public API to teach by default.
- For ChatGPT-facing guidance, prefer the current documented surface: `window.openai.callTool(...)`, `window.openai.sendFollowUpMessage(...)`, `window.openai.openExternal(...)`, `window.openai.requestDisplayMode(...)`, and direct globals like `window.openai.theme`, `window.openai.locale`, `window.openai.displayMode`, `window.openai.toolInput`, `window.openai.toolOutput`, `window.openai.toolResponseMetadata`, and `window.openai.widgetState`.
- If you reference wrapper helpers from repo examples, map them back to the documented `window.openai` or MCP Apps bridge primitives and call out that the wrapper is not the normative API surface.
- Use `references/window-openai-patterns.md` for the wrapper-to-canonical mapping and for React helper extraction patterns.

### 5. Add Resource Metadata and Security

Set resource metadata deliberately on the widget resource/template:

- `_meta.ui.csp` with exact `connectDomains` and `resourceDomains`
- `_meta.ui.domain` for app submission-ready deployments
- `_meta.ui.prefersBorder` (or OpenAI compatibility alias when needed)
- Optional `openai/widgetDescription` to reduce redundant narration

Avoid `frameDomains` unless iframe embeds are core to the product.

### 5a. Enforce A Minimum Working Repo Contract

Every generated repo should satisfy a small, stable contract before you consider it done.

- The repo shape matches the chosen archetype.
- The MCP server and tools are wired to a reachable `/mcp` endpoint.
- Tools have clear descriptions, accurate annotations, and UI metadata where needed.
- Connector-like, data-only, sync-oriented, and company-knowledge-style apps use the standard `search` and `fetch` tool shapes when relevant.
- The widget uses the MCP Apps bridge correctly when a UI exists.
- The repo includes enough scripts or commands for a user to run and check it locally.
- The response explicitly says what validation was run and what was not run.

Read `references/repo-contract-and-validation.md` for the detailed checklist and validation ladder.

### 6. Validate the Local Loop

Validate against the minimum working repo contract, not just “did files get created.”

- Run the lowest-cost checks first:
  - static contract review
  - syntax or compile checks when feasible
  - local `/mcp` health check when feasible
- Then move up to runtime checks:
  - verify tool descriptors and widget rendering in MCP Inspector
  - test the app in ChatGPT developer mode through HTTPS tunneling
  - exercise retries and repeated tool calls to confirm idempotent behavior
  - check widget updates after host events and follow-up tool calls
- If you are only delivering a scaffold and are not installing dependencies, still run low-cost checks and say exactly what you did not run.

Read `references/repo-contract-and-validation.md` for the validation ladder.

### 7. Connect and Test in ChatGPT (Developer Mode)

For local development, include explicit ChatGPT setup steps (not just code/run commands).

- Run the MCP server locally on `http://localhost:<port>/mcp`
- Expose the local server with a public HTTPS tunnel (for example `ngrok http <port>`)
- Use the tunneled HTTPS URL plus `/mcp` path when connecting from ChatGPT
- In ChatGPT, enable Developer Mode under **Settings → Apps & Connectors → Advanced settings**
- In ChatGPT app settings, create a new app for the remote MCP server and paste the public MCP URL
- Tell users to refresh the app after MCP tool/metadata changes so ChatGPT reloads the latest descriptors

Note: Some docs/screenshots still use older "connector" terminology. Prefer current product wording ("app") while acknowledging both labels when giving step-by-step instructions.

### 8. Plan Production Hosting and Deployment

When the user asks to deploy or prepare for launch, generate hosting guidance for the MCP server (and widget assets if hosted separately).

- Host behind a stable public HTTPS endpoint (not a tunnel) with dependable TLS
- Preserve low-latency streaming behavior on `/mcp`
- Configure secrets outside the repo (environment variables / secret manager)
- Add logging, request latency tracking, and error visibility for tool calls
- Add basic observability (CPU, memory, request volume) and a troubleshooting path
- Re-test the hosted endpoint in ChatGPT Developer Mode before submission

### 9. Prepare Submission and Publish (Public Apps Only)

Only include these steps when the user intends a public directory listing.

- Use `apps-sdk/deploy/submission` for the submission flow and `apps-sdk/app-submission-guidelines` for review requirements
- Keep private/internal apps in Developer Mode instead of submitting
- Confirm org verification and Owner-role prerequisites before submission work
- Ensure the MCP server uses a public production endpoint (no localhost/testing URLs) and has submission-ready CSP configured
- Prepare submission artifacts: app metadata, logo/screenshots, privacy policy URL, support contact, test prompts/responses, localization info
- If auth is required, include review-safe demo credentials and test the login path end-to-end
- Submit for review in the Platform dashboard, monitor review status, and publish only after approval

## Interactive State Guidance

Read `references/interactive-state-sync-patterns.md` when the app has long-lived widget state, repeated interactions, or component-initiated tool calls (for example, games, boards, maps, dashboards, editors).

Use it to choose patterns for:

- State snapshots plus monotonic event tokens (`stateVersion`, `resetCount`, etc.)
- Idempotent retry-safe handlers
- `structuredContent` vs `_meta` partitioning
- MCP Apps bridge-first update flows with optional `window.openai` compatibility
- Decoupled data/render tool architecture for more complex interactive apps

## Output Expectations

When using this skill to scaffold code, produce output in this order unless the user asks otherwise:

- For direct scaffold requests, do not stop at the plan: give the brief plan, then create the files immediately.

1. Primary app archetype chosen and why
2. Tool plan and architecture choice (minimal vs decoupled)
3. Upstream starting point chosen (official example, ext-apps example, or local fallback scaffold) and why
4. Doc pages/URLs used from `$openai-docs`
5. File tree to create or modify
6. Implementation (server + widget)
7. Validation performed against the minimum working repo contract
8. Local run/test instructions (including tunnel + ChatGPT Developer Mode app setup)
9. Deployment/hosting guidance (if requested or implied)
10. Submission-readiness checklist (for public launch requests)
11. Risks, gaps, and follow-up improvements

## References

- `references/app-archetypes.md` for classifying requests into a small number of supported app shapes
- `references/apps-sdk-docs-workflow.md` for doc queries, page targets, and code-generation checklist
- `references/interactive-state-sync-patterns.md` for reusable patterns for stateful or highly interactive widget apps
- `references/repo-contract-and-validation.md` for the minimum working repo contract and lightweight validation ladder
- `references/search-fetch-standard.md` for when and how to default to the standard `search` and `fetch` tools
- `references/upstream-example-workflow.md` for choosing between official examples, ext-apps examples, and the local fallback scaffold
- `references/window-openai-patterns.md` for ChatGPT-specific extensions, wrapper API translation, and React helper patterns
- `scripts/scaffold_node_ext_apps.mjs` for a minimal Node + `@modelcontextprotocol/ext-apps` fallback starter scaffold
