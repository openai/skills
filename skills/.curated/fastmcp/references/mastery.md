# FastMCP Mastery Notes

## Mental Model

An MCP server is a capability boundary between an AI client and external state. The server must make capabilities discoverable, typed, safe, and testable.

## Primitive Selection

- Use **tools** for operations the model invokes.
- Use **resources** for readable state the model can inspect.
- Use **prompts** for reusable task templates.

Do not expose a write operation as a resource. Do not hide side effects behind vague names like `run` or `process`.

## Schema Quality

Good tool schemas:

- use typed parameters
- describe required fields
- avoid arbitrary string blobs when structured inputs are possible
- return stable JSON-compatible fields
- include actionable errors

## Transport Decisions

Use stdio for local desktop/client workflows. Use HTTP/streamable HTTP for hosted, multi-client, or remotely managed servers. Record timeout, auth, and lifecycle expectations.

## Safety Boundaries

Before adding a tool, classify it:

```text
read-only
write/action
networked
filesystem
secret-dependent
destructive
```

Destructive tools need explicit names, narrow inputs, and confirmation handled outside prompt text when possible.

## Review Standard

A complete FastMCP change proves:

- server starts
- capabilities are discoverable
- schema descriptions are useful
- at least one read-only call works
- side effects are documented
- secrets are not accepted through prompt text
- client config is provided or blocker is explicit
