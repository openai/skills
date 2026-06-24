# Callbacks (TypeScript ADK)

## Available callback types
- **Before/after agent:** `beforeAgentCallback`, `afterAgentCallback`
- **Before/after model:** `beforeModelCallback`, `afterModelCallback`
- **Before/after tool:** `beforeToolCallback`, `afterToolCallback`

Callbacks can observe, modify, or short-circuit execution depending on return value.

## Common uses
- Guardrails and validation (block a request before the model call).
- Ensure model requests always include `parts` in `contents`.
- Post-process tool results or redact sensitive data.
- Logging and tracing without touching agent logic.
For security guardrails, prefer ADK plugins when possible.

## Short-circuit rules (high level)
- Returning a `Content` from a `beforeAgentCallback` skips agent execution.
- Returning an `LlmResponse` from a `beforeModelCallback` skips the model call.
- Returning an object from a `beforeToolCallback` skips tool execution and becomes the tool result.
- Returning a value from an `after*` callback replaces the upstream result.

## Source
- https://google.github.io/adk-docs/callbacks/
- https://google.github.io/adk-docs/callbacks/types-of-callbacks/
