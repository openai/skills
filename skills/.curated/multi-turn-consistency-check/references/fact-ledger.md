# Fact Ledger

Use a compact internal ledger before any substantive answer that depends on earlier turns.

By default this ledger is ephemeral. It is a thinking aid, not a required markdown artifact on disk.

## Template

- User-stated facts:
- Verified local facts:
- Verified external facts:
- Bounded inferences:
- Unresolved items:

## Rules

- Keep each item atomic.
- Prefer the latest explicit user instruction when user-stated facts conflict.
- Prefer fresh file reads, command outputs, and tool results over remembered repo state.
- Tag unstable external facts with the verification date when the timing matters.
- Never promote an inference into a fact without fresh evidence.
- If an unresolved item blocks a safe answer, ask one short question instead of guessing.
- Do not write the ledger to a file unless the user explicitly asks for a persistent summary, handoff note, or working record.

## Example

- User-stated facts: "Use PostgreSQL, not MySQL." (latest user turn)
- Verified local facts: `docker-compose.yml` still starts a `mysql` container.
- Verified external facts: The package release being discussed was published on 2026-03-20.
- Bounded inferences: The migration work is not finished yet.
- Unresolved items: Whether production already uses PostgreSQL.
