# task +tasklist-task-add

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.

Add existing tasks to a tasklist.

## Recommended Commands

```bash
# Add a single task to a tasklist
lark-cli task +tasklist-task-add --tasklist-id "<tasklist_guid>" --task-id "<task_guid>"

# Add multiple tasks to a tasklist
lark-cli task +tasklist-task-add --tasklist-id "<tasklist_guid>" --task-id "<task_guid>,<another_task_guid>,<third_task_guid>"

# Add a task to a specific section in the tasklist
lark-cli task +tasklist-task-add \
  --tasklist-id "<tasklist_guid>" \
  --task-id "<task_guid>" \
  --section-guid "<section_guid>"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--tasklist-id <guid>` | Yes | The GUID of the tasklist, or a full AppLink URL. |
| `--task-id <guids>` | Yes | Comma-separated list of task GUIDs to add to the tasklist. For Feishu task applinks, use each task's `guid` query parameter, not the `suite_entity_num` / display task ID like `t104121`. |
| `--section-guid <guid>` | No | The GUID of the custom section to add the tasks to. If omitted, tasks will be added to the default section. |

## Workflow

1. Confirm the tasklist and the tasks to add.
2. Execute the command `lark-cli task +tasklist-task-add ...`.
3. Report the result (successful vs failed tasks).

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.
