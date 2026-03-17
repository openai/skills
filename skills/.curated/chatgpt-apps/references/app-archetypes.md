# App Archetypes

Load this reference before choosing a starting point for a new ChatGPT app. The goal is to keep the skill inside a small number of supported app shapes instead of inventing a custom structure for every prompt.

## Rule

Choose one primary archetype per request and state it.

Do not combine several archetypes unless the user explicitly asks for a hybrid app and the extra complexity is necessary.

## Archetypes

### `tool-only`

Use when:

- The user does not need an in-ChatGPT UI
- The task is mainly search, fetch, retrieval, or background actions

Default shape:

- MCP server only

Best starting point:

- Official docs and MCP server examples

Validation emphasis:

- `/mcp` route works
- tool schemas and annotations are correct
- no unnecessary UI resource is registered
- if the app is connector-like or sync-oriented, `search` and `fetch` should be the default read-only tools

### `vanilla-widget`

Use when:

- The user wants a small demo, workshop starter, or simple inline widget
- A single HTML widget is enough
- The user wants the fastest path to a working repo

Default shape:

- Root-level server plus `public/` widget assets

Best starting point:

- Apps SDK quickstart first
- Local fallback scaffold if the quickstart is not a good fit

Validation emphasis:

- bridge initialization
- `ui/notifications/tool-result`
- `tools/call` only when the widget is interactive

### `react-widget`

Use when:

- The user wants a polished UI
- The UI is clearly component-based
- The user mentions React, TypeScript frontend tooling, or richer design requirements

Default shape:

- Split `server/` + `web/` layout when the example already uses it

Best starting point:

- Official OpenAI examples

Validation emphasis:

- build output is wired into the server correctly
- bundle references resolve
- widget renders from `structuredContent`

### `interactive-decoupled`

Use when:

- The app has repeated user interaction
- The widget should stay mounted while tools are called repeatedly
- The app is a board, map, editor, game, dashboard, or other stateful experience

Default shape:

- Split `server/` + `web/`
- data tools plus render tools

Best starting point:

- Official OpenAI examples plus `references/interactive-state-sync-patterns.md`

Validation emphasis:

- tool retries are safe
- widget does not remount unnecessarily
- state sync is intentional
- UI tool calls work independently of model reruns

### `submission-ready`

Use when:

- The user asks for public launch, review readiness, or directory submission

Default shape:

- Smallest viable repo that still includes deployment and review requirements

Best starting point:

- Closest official example that matches the requested stack

Validation emphasis:

- `_meta.ui.domain`
- accurate CSP
- auth and review-safe flows
- submission prerequisites and artifacts

## Selection Heuristic

- If the prompt does not mention a UI, choose `tool-only`.
- If the prompt is about a knowledge source, sync app, connector-like integration, or deep research, strongly prefer `tool-only` plus the standard `search` and `fetch` tools unless the user clearly needs a widget.
- If the prompt asks for a simple demo or starter, choose `vanilla-widget`.
- If the prompt asks for a polished UI or React, choose `react-widget`.
- If the prompt implies long-lived client state or repeated interaction, choose `interactive-decoupled`.
- Only choose `submission-ready` when the user explicitly asks for launch or review-readiness work.
