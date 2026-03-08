# Interactive State Sync Patterns

Use this reference when building ChatGPT apps with long-lived widget state, repeated interactions, or component-initiated tool calls (for example: games, boards, maps, dashboards, editors, or realtime-ish UIs).

Do not load this file for simple read-only render apps unless state sync behavior is part of the task.

## When This Reference Helps

Read this file when the app needs one or more of these patterns:

- Repeated actions that may return similar data (retry, refresh, reset, reroll)
- UI controls that trigger tool calls after the initial render
- Local widget behavior that should also work outside ChatGPT during development
- Multiple tool calls updating one mounted widget over time
- Clear separation between model-visible state and widget-only state

## Reusable Patterns

### 1. Snapshot + Event Token

Return a stable state snapshot in `structuredContent` and add a monotonic event token for repeated actions that may not change other fields.

Examples:

- `stateVersion`
- `refreshCount`
- `resetCount`
- `lastMutationId`

Use this when the widget must detect "same shape, new event" updates reliably.

### 2. Intent-Focused Tool Surface

Prefer small, explicit tools that map to user-visible actions or data operations.

- Keep names action-oriented
- Use enums and bounded schemas where possible
- Avoid kitchen-sink tools that mix unrelated reads and writes

This improves model tool selection and reduces malformed calls.

### 3. Idempotent Handlers (or Explicitly Non-Idempotent)

Design handlers to tolerate retries. If a tool is not idempotent, make the side effect explicit and confirm intent in the flow.

- Reads and pure transforms should usually be idempotent
- Writes should include clear impact hints and current-turn confirmation where needed
- Repeated calls with the same input should not corrupt widget state

### 4. `structuredContent` / `_meta` Partitioning

Partition payloads intentionally:

- `structuredContent`: concise model-visible state the widget also uses
- `content`: short narration/status text
- `_meta`: large maps, caches, or sensitive widget-only hydration data

Keep `structuredContent` small enough for follow-up reasoning and chaining.

### 5. MCP Apps Bridge First, `window.openai` Second

For new scaffolds:

- Prefer MCP Apps bridge notifications and `tools/call` (portable across hosts)
- Use `window.openai` as a compatibility layer plus optional ChatGPT extensions

This keeps the app portable while still enabling ChatGPT-specific capabilities when helpful.

### 6. Component-Initiated Tool Calls Without Remounting

For interactive widgets, allow the UI to call data/action tools directly and update the existing widget state instead of forcing a full re-render/remount every time.

This is especially useful for:

- Refresh
- Retry
- Rerun
- Toggle/filter actions
- Incremental interactions inside one widget session

### 7. Standalone / No-Host Fallback Mode

When feasible, make the widget usable without ChatGPT during development:

- If host APIs are unavailable, apply local state directly
- Preserve basic interactions in a normal browser

This speeds up front-end iteration and reduces dependence on connector setup for every UI tweak.

### 8. Decouple Data Tools from Render Tools (When Complexity Grows)

Use separate data and render tools when the app has multi-step reasoning or frequent updates.

- Data tools fetch/compute/mutate and return reusable `structuredContent`
- Render tools attach the widget template and focus on presentation

This reduces unnecessary remounts and gives the model a chance to refine data before rendering.

## Common Anti-Patterns

- Putting large widget-only blobs into `structuredContent`
- Attaching a widget template to every tool when only one render tool needs it
- Using hidden client-side state as the source of truth for critical actions
- Depending only on `window.openai` APIs for baseline app behavior
- Using ambiguous tool names that do not match user intent

## Example App Types That Benefit From These Patterns

- Multiplayer or turn-based games
- Collaborative boards / task views
- Maps with filters and repeated searches
- Dashboards with refresh and drill-down actions
- Editors or builders with iterative tool calls
