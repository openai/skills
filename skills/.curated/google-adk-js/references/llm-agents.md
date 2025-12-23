# LLM Agents (TypeScript ADK)

## Identity + Instructions
- `name` is required and used for routing in multi-agent setups.
- `description` helps other agents decide when to transfer work to this agent.
- `instruction` can be a string template with state placeholders like `{trip_origin}` and `{artifact.summary}`.
- Use `{var?}` to avoid errors when state is missing.

## Tools
- Pass tools via `tools` on the `LlmAgent`.
- Tools must return an object (not a string).
- For agent-to-agent delegation inside tool calls, wrap sub-agents with `AgentTool`.

## Structured input/output
- `inputSchema` means the incoming user message must be a JSON string matching the schema.
- `outputSchema` uses `Schema` + `Type` from `@google/genai` and forces JSON output.
- Do not rely on tools when `outputSchema` is set (tool use is not effective).
- `outputKey` saves the agent's final response text into `session.state[outputKey]`.

## Context control
- `includeContents: "default"` sends prior history; `"none"` makes the agent stateless.
- For system-wide constraints, prefer a root-level global instruction (see multi-agent docs).

## GenerateContentConfig
Use `GenerateContentConfig` from `@google/genai` for temperature, maxOutputTokens, and safety.
Do not place tools inside `generateContentConfig`.

## Source
- https://google.github.io/adk-docs/agents/llm-agents/
- https://google.github.io/adk-docs/agents/multi-agents/
