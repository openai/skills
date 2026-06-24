# task +set-ancestor

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.

Set a parent task for a task, or clear the parent to make it independent.

## Recommended Commands

```bash
# Set a parent task
lark-cli task +set-ancestor --task-id "guid_1" --ancestor-id "guid_2"

# Clear the parent task
lark-cli task +set-ancestor --task-id "guid_1"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to update. |
| `--ancestor-id <guid>` | No | The parent task GUID. Omit it to clear the ancestor. |

## Workflow

1. Confirm the child task and, if applicable, the ancestor task.
2. Execute `lark-cli task +set-ancestor ...`
3. Report the updated task GUID and whether the ancestor was set or cleared.

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.

