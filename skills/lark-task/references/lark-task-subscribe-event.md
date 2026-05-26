# task +subscribe-event

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
>
> **⚠️ Note:** This API supports both `user` and `bot` identities. Use `user` to subscribe the current user's accessible tasks; use `bot` to subscribe tasks the **application is responsible for**.

Subscribe task update events with the current identity.

This shortcut is different from `event +subscribe`:
- `task +subscribe-event` registers task-event access for the **current identity**
- with `--as user`, it subscribes the **current user** to task events for tasks they created, are responsible for, or follow
- with `--as bot`, it subscribes using the **application identity** for tasks the application is responsible for

The task event type is:

```text
task.task.update_user_access_v2
```

Within this event, task changes are represented by commit types (string values). Deduped list:

```text
task_assignees_update
task_completed_update
task_create
task_deleted
task_desc_update
task_followers_update
task_reminders_update
task_start_due_update
task_summary_update
```

Event payload shape (example):

```json
{
  "event_id": "evt_xxx",
  "event_types": ["task_summary_update"],
  "task_guid": "task_guid_xxx",
  "timestamp": "1775793266152",
  "type": "task.task.update_user_access_v2"
}
```

- `type`: event type, should be `task.task.update_user_access_v2`
- `event_id`: unique event id (useful for dedup)
- `event_types`: list of commit types (see the deduped list above)
- `task_guid`: the task GUID that changed
- `timestamp`: event timestamp (ms)

In practice, this means:
- with `--as user`, the subscribed user can receive updates for tasks visible to them through authorship, assignment, or following
- with `--as bot`, the subscription covers tasks the application is responsible for

To actually receive the subscribed events, use the standard event WebSocket receiver:

```bash
lark-cli event +subscribe --event-types task.task.update_user_access_v2 --compact --quiet
```

The full flow is:
1. Register the subscription with `lark-cli task +subscribe-event [--as user|bot]`
2. Receive those events with `lark-cli event +subscribe --event-types task.task.update_user_access_v2 ...`

## Recommended Commands

```bash
lark-cli task +subscribe-event
```
# Subscribe with app identity
lark-cli task +subscribe-event --as bot


## Parameters

This shortcut has no additional parameters.

## Workflow

1. Confirm whether the user wants to subscribe with `user` identity or `bot` identity.
2. Execute `lark-cli task +subscribe-event`
3. Report whether the subscription succeeded, and clarify which identity the subscription applies to.

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.
