# Agent Team Protocol Adapter

Use this adapter when `ralph-wiggum-loop` is running as `Builder` under the agent team protocol.

## Role Boundaries

- Keep Ralph scoped to bounded implementation work only.
- Do not let Ralph self-approve completion.
- Route acceptance through external review before terminal completion.

## Required Handoff Fields

Emit these fields after each Ralph iteration so protocol coordinators can route work deterministically:

- `task_id`
- `state`
- `owner_role`
- `handoff_id`
- `project`
- `iteration`
- `changed_files`
- `verification_status`
- `failure_domain`
- `next_action`

## Review Gating

- Enforce reviewer separation: builder identity must differ from final reviewer identity.
- On conflicting reviewer outcomes, escalate and stop rather than retrying in-loop.
- Mark completion only after review gate returns an explicit accept decision.

## Contract Preservation

Keep Ralph's strict loop contract unchanged:

- exactly one planned change-set per iteration
- exactly one verification pass per iteration
- persistent iteration state in `.ralph/`
