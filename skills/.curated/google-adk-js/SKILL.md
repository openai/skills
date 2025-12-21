---
name: adk-js
description: Build, configure, and update Agent Development Kit (ADK) agents in TypeScript using `@google/adk` and `@google/adk-devtools`. Use when a user asks to scaffold a brand-new ADK TS project, define agents (LlmAgent, workflow agents, custom BaseAgent), add tools (FunctionTool, AgentTool, built-ins like GOOGLE_SEARCH), design multi-agent orchestration, configure models/auth (Gemini API key or Vertex AI), run via devtools, or adapt patterns from ADK JS docs/samples.
---

# ADK JS

## Overview
Build and iterate on ADK TypeScript agents with the official SDK, devtools, and docs-driven patterns. Prefer official docs and samples for API details and compatibility.

## Quick Decision Guide
- **New project or first agent:** Open `references/quickstart.md`.
- **Running or debugging:** Open `references/devtools.md`.
- **Adding tools:** Open `references/tools.md`.
- **Model/auth setup:** Open `references/models.md`.
- **LLM agent configuration (schemas, output keys, context):** Open `references/llm-agents.md`.
- **Callbacks/guardrails:** Open `references/callbacks.md`.
- **Example patterns:** Open `references/samples.md`.

## Core Workflow
1. **Clarify scope:** Identify whether the user needs a new agent, an update, or a specific feature (tools, multi-agent, model/auth).
2. **Bootstrap or edit:** For brand-new projects, follow `references/quickstart.md` exactly; otherwise edit existing `agent.ts` and configs.
3. **Design architecture:** Use a root LLM orchestrator plus deterministic agents (Sequential/Parallel/Loop) instead of hardcoded intent rules. See `references/architecture.md`.
4. **Add capabilities:** Implement tools or multi-agent orchestration as needed.
5. **Run and verify:** Use devtools for local run or web UI.

## Agent Construction Guidelines
- Export a `rootAgent` when the user intends to run with ADK devtools.
- Use `outputKey` to persist agent output into session state for downstream steps.
- Prefer `LlmAgent` for reasoning, `SequentialAgent`/`ParallelAgent`/`LoopAgent` for deterministic workflows.
- Keep tools on `LlmAgent.tools`, not `generateContentConfig.tools` (ADK throws if tools are set in config).
- If `inputSchema` is set, the incoming user message must be a JSON string matching the schema.
- If `outputSchema` is set, the agent must return JSON matching the schema and tool use is not effective.
- For new projects, default to a Gemini 3 preview model string and document access + region requirements.

## Multi-Agent Patterns
- Use `subAgents` to form a hierarchy for delegation and workflow orchestration.
- Use `AgentTool` when you want the parent agent to stay in control and summarize a tool-agent's output.
- Distinguish **sub-agent transfer** vs **agent-as-tool** based on whether control should move to the child agent.
 
## Architecture Best Practices
- Use a root LLM agent as the conversational front door and delegate work to deterministic agents.
- Avoid hardcoded intent checks; let the orchestrator decide whether to ask clarifying questions or transfer to a workflow.
- Prefer `AgentTool` for isolation in loops (fresh context each iteration) when state bleed is a risk.
- Store tool outputs in session state for downstream agents to read and compile.
- Use `subAgents` for LLM-driven delegation (`transfer_to_agent`) and keep agent names/roles explicit.
- Sequential agents share the same invocation context; parallel agents share state but run on branch contexts; loops stop on `maxIterations` or `escalate=true`.

See `references/architecture.md` for a minimal “orchestrator + pipeline” blueprint.

## Human-in-the-Loop (TypeScript)
- TypeScript recommends using `SecurityPlugin` + a custom `BasePolicyEngine` to require user confirmation before tool calls.
- Treat this as the default pattern for approvals rather than hardcoding user prompts.

See `references/architecture.md` and `references/callbacks.md` for a lightweight HITL sketch.

## Model + Auth Notes
- Use `GOOGLE_GENAI_API_KEY` or `GEMINI_API_KEY` for Gemini API mode; ADK does not read `GOOGLE_API_KEY`.
- Use Vertex by setting `GOOGLE_GENAI_USE_VERTEXAI=true` plus `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`.
- Do not expect API keys to work with Vertex. Use ADC or service account JSON/credentials.
- For Gemini 3 preview on Vertex, set `GOOGLE_CLOUD_LOCATION=global` and confirm model access.
- Use `ADK_MODEL` to override the model string; default to `gemini-3-flash-preview` and fall back to `gemini-2.5-flash` if preview access is not enabled.
- If `GOOGLE_SERVICE_ACCOUNT_JSON` is provided (single-line JSON), write it to a temp file and set `GOOGLE_APPLICATION_CREDENTIALS` at runtime. Escape newlines in `private_key` with `\\n`.

## Common Failure Modes
- **"Invalid JSON payload... ~standard/def" for tools**: Pin `zod` to v3. ADK tool schema conversion is not compatible with zod v4 output.
- **"Must include at least one parts field"**: Ensure request contents contain at least one `parts` entry (use a `beforeModelCallback` guard).
- **Vertex auth errors with API key**: Remove API key env vars or disable Vertex (`GOOGLE_GENAI_USE_VERTEXAI=false`).
- **"Session not found"**: Create a session in your API route before calling `runner.runAsync` (InMemoryRunner does not auto-create).
- **"Publisher Model ... was not found"**: For `gemini-3-flash-preview`, set `GOOGLE_CLOUD_LOCATION=global`. Otherwise use `gemini-2.5-flash` in regional locations.
- **Empty reply after tool call**: If the final event contains only `functionResponse` parts, surface the tool response directly in the UI/API (this is expected when `skipSummarization` is set or the model emits tool-only output).
- **Tool results missing in UI**: If you only read `event.content.parts[].text` (e.g., via `stringifyContent`), tool outputs will be dropped. Read `functionResponse.response` when no text is present.

## Field Notes (Next.js Chat Integration)
- Use a singleton `InMemoryRunner` (e.g., on `globalThis`) to avoid reinitializing sessions during hot reloads.
- Default to `LoggingPlugin` in dev to log tool calls + events (`new InMemoryRunner({ plugins: [new LoggingPlugin()] })`); keep prod quiet unless debugging.
- Create sessions explicitly on each request if missing: `sessionService.getSession` then `createSession`.
- Surface `event.errorMessage` / `event.errorCode` when no reply is returned to avoid silent failures.
- For preview models on Vertex: `GOOGLE_CLOUD_LOCATION=global` + `ADK_MODEL=gemini-3-flash-preview`.
- Streaming (SSE): pass `runConfig: { streamingMode: StreamingMode.SSE }` to `runner.runAsync`, then stream `event.partial` deltas from `event.content.parts[].text`. Avoid emitting the full final text if you already streamed deltas (otherwise you'll double‑append). For UI drip‑feed, buffer the delta string and emit small chunks on a timer.
- If Vertex returns `must include at least one parts field` during streaming, add a `beforeModelCallback` that prunes empty `request.contents` and reuses `context.userContent` if needed.
- Avoid heuristic pre-routing (regex checks for math/search); let the LLM agent decide which tools to call.
- If tool calls succeed but no text is returned, read `event.content.parts[].functionResponse.response` and display it when no text is present (avoid regex pre-routing; let the LLM decide tool use).
- For SSE, don’t stop on empty “final” events; keep reading the generator to allow tool responses and the post‑tool LLM pass to arrive.

## Notes and Constraints
- Treat the ADK web UI as development-only.
- Check the tools limitations doc before mixing tools.
- Confirm TypeScript support for evaluation features before implementing them.

## References
- `references/quickstart.md`: Project scaffolding and minimal agent setup.
- `references/devtools.md`: CLI/web devtools usage.
- `references/tools.md`: Built-ins, FunctionTool, AgentTool.
- `references/models.md`: Model selection and authentication.
- `references/llm-agents.md`: Input/output schema, outputKey, includeContents, instruction templating.
- `references/callbacks.md`: Agent/tool callbacks for validation and guardrails.
- `references/samples.md`: Sample repository layout and usage.
- `references/architecture.md`: Orchestrator + workflow patterns and state isolation.
