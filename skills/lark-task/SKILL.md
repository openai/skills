---
name: lark-task
version: 1.0.0
description: "飞书任务：管理任务、清单和任务智能体。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员、上传任务附件、注册或注销任务智能体、更新任务智能体的主页数据、写入智能体任务记录。当用户需要创建待办事项、查看任务列表、跟踪任务进度、管理项目清单或给他人分配任务、为任务上传附件文件、注册注销任务智能体、更新智能体主页数据、写入任务记录时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli task --help"
---

# task (v2)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

> **任务搜索技巧**：先区分用户是否**特地指定使用搜索 skill**，以及是否真的提供了**查询关键字**（例如任务名称、关键词、片段描述）。如果用户特地指定使用搜索 skill，或明确给出了任务查询关键字，则目标是**任务**时优先使用 `+search`。如果用户没有特地指定使用搜索 skill，且意图里没有查询关键字，只有范围条件（例如“今年以来”“已完成”“由我创建”“我关注的”），并且使用 `+search` 与 `+get-related-tasks` / `+get-my-tasks` 都能达到目的时，应优先使用列表型能力，而不是搜索型能力。其中，“与我相关 / 我关注的 / 由我创建”等优先考虑 `+get-related-tasks`；“我负责的 / 分配给我”的列表优先考虑 `+get-my-tasks`。不要把时间范围词（例如“今年以来”）本身误当成 `query` 去走搜索。
> **任务清单搜索技巧**：任务清单也遵循同样的判断逻辑。先区分用户是否**特地指定使用搜索 skill**，以及是否真的提供了**清单查询关键字**（例如清单名称、关键词、片段描述）。如果用户特地指定使用搜索 skill，或明确给出了清单查询关键字，则优先使用 `+tasklist-search`。如果用户没有特地指定使用搜索 skill，且意图里没有查询关键字，只有范围条件（例如“由我创建的任务清单”“今年以来创建的清单”），并且使用搜索或原生列取清单都能达到目的时，应优先使用原生 `tasklists.list` 接口列取清单（先 `schema task.tasklists.list`，再 `lark-cli task tasklists list --as user ...`），再按 `creator`、`created_at` 等字段做本地筛选和分页控制。
> **意图区分补充**：像“搜索飞书中今年以来我关注的任务”这类表达，虽然字面带有“搜索”，但如果没有真正的查询关键字，且本质是在限定“与我相关 + 时间范围”，则应优先走 `+get-related-tasks`；像“搜索飞书中由我创建的任务清单”这类表达，如果没有清单关键字，且本质是在限定“清单范围 + 创建者”，则应优先走原生 `tasklists.list` 后筛选，而不是直接走搜索型 shortcut。
> **用户身份识别**：在用户身份（user identity）场景下，如果用户提到了“我”（例如“分配给我”、“由我创建”），请默认获取当前登录用户的 `open_id` 作为对应的参数值。
> **术语理解**：如果用户提到 “todo”（待办），应当思考其是否是指“task”（任务），并优先尝试使用本 Skill 提供的命令来处理。
> **友好输出**：在输出任务（或清单）的执行结果给用户时，建议同时提取并输出命令返回结果中的 `url` 字段（任务链接），以便用户可以直接点击跳转查看详情。

> **创建/更新注意**：
> 1. 只有在设置了 `due`（截止时间）的情况下，才能设置 `repeat_rule`（重复规则）和 `reminder`（提醒时间）。
> 2. 若同时设置了 `start`（开始时间）和 `due`（截止时间），开始时间必须小于或等于截止时间。
> 3. 使用 tenant_access_token（应用身份）时，无法跨租户添加任务成员。

> **查询注意**：
> 1. 在输出任务详情时，如果需要渲染负责人、创建人等人员字段，除了展示 `id` (例如 open_id) 外，还必须通过其他方式（例如调用通讯录技能）尝试获取并展示这个人的真实名字，以便用户更容易识别。
> 2. 在输出清单详情时，如果需要渲染 owner、member、角色成员等人员字段，也必须像任务成员展示一样，除了展示 `id` 外，尽量解析并展示对应人员的真实名字。
> 3. 在输出任务或清单详情时，如果需要渲染创建时间、截止时间等字段，需要使用本地时区来渲染（格式为2006-01-02 15:04:05）。

> **Task GUID 定义**：
> Task OpenAPI 中用于更新/操作任务的 `guid` 是任务的全局唯一标识（GUID），不是客户端展示的任务编号（例如 `t104121` / `suite_entity_num`）。
> 对于 Feishu 的任务 applink（例如 `.../client/todo/task?guid=...`），必须使用 URL query 里的 `guid` 参数作为 task guid。

## Shortcuts

- [`+create`](./references/lark-task-create.md) — Create a task
- [`+update`](./references/lark-task-update.md) — Update a task
- [`+comment`](./references/lark-task-comment.md) — Add a comment to a task
- [`+complete`](./references/lark-task-complete.md) — Complete a task
- [`+reopen`](./references/lark-task-reopen.md) — Reopen a task
- [`+assign`](./references/lark-task-assign.md) — Assign or remove members from a task
- [`+followers`](./references/lark-task-followers.md) — Manage task followers
- [`+reminder`](./references/lark-task-reminder.md) — Manage task reminders
- [`+get-my-tasks`](./references/lark-task-get-my-tasks.md) — List tasks assigned to me
- [`+get-related-tasks`](./references/lark-task-get-related-tasks.md) — List tasks related to me
- [`+search`](./references/lark-task-search.md) — Search tasks
- [`+subscribe-event`](./references/lark-task-subscribe-event.md) — Subscribe to task events
- [`+set-ancestor`](./references/lark-task-set-ancestor.md) — Set or clear a task ancestor
- [`+tasklist-create`](./references/lark-task-tasklist-create.md) — Create a tasklist and batch add tasks
- [`+tasklist-search`](./references/lark-task-tasklist-search.md) — Search tasklists
- [`+tasklist-task-add`](./references/lark-task-tasklist-task-add.md) — Add existing tasks to a tasklist
- [`+tasklist-members`](./references/lark-task-tasklist-members.md) — Manage tasklist members
- [`+upload-attachment`](./references/lark-task-upload-attachment.md) — Upload a file as a task attachment

## API Resources

```bash
lark-cli schema task.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli task <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构，不要猜测字段格式。

### tasks

  - `create` — 创建任务
  - `delete` — 删除任务
  - `get` — 获取任务详情
  - `list` — 列取任务列表
  - `patch` — 更新任务

### tasklists

  - `add_members` — 添加清单成员
  - `create` — 创建清单
  - `delete` — 删除清单
  - `get` — 获取清单详情
  - `list` — 获取清单列表
  - `patch` — 更新清单
  - `remove_members` — 移除清单成员
  - `tasks` — 获取清单任务列表

### subtasks

  - `create` — 创建子任务
  - `list` — 获取任务的子任务列表

### members

  - `add` — 添加任务成员
  - `remove` — 移除任务成员

### sections

  - `create` — 创建自定义分组
  - `delete` — 删除自定义分组
  - `get` — 获取自定义分组详情
  - `list` — 获取自定义分组列表
  - `patch` — 更新自定义分组
  - `tasks` — 获取自定义分组任务列表

### custom_fields

  - `create` — 创建自定义字段
  - `get` — 获取自定义字段详情
  - `patch` — 更新自定义字段
  - `list` — 获取自定义字段列表
  - `add` — 将自定义字段加入资源
  - `remove` — 将自定义字段移出资源

### custom_field_options

  - `create` — 创建自定义字段选项
  - `patch` — 更新自定义字段选项

### agent

  - `update_agent_profile` — 更新任务代理的主页内容数据。
  - `register_agent` — 注册AI 智能体

### agent_task_step_info

  - `append_task_steps` — 写入任务记录。

## 权限表

| 方法 | 所需 scope |
|------|-----------|
| `tasks.create` | `task:task:write` |
| `tasks.delete` | `task:task:write` |
| `tasks.get` | `task:task:read` |
| `tasks.list` | `task:task:read` |
| `tasks.patch` | `task:task:write` |
| `tasklists.add_members` | `task:tasklist:write` |
| `tasklists.create` | `task:tasklist:write` |
| `tasklists.delete` | `task:tasklist:write` |
| `tasklists.get` | `task:tasklist:read` |
| `tasklists.list` | `task:tasklist:read` |
| `tasklists.patch` | `task:tasklist:write` |
| `tasklists.remove_members` | `task:tasklist:write` |
| `tasklists.tasks` | `task:tasklist:read` |
| `subtasks.create` | `task:task:write` |
| `subtasks.list` | `task:task:read` |
| `members.add` | `task:task:write` |
| `members.remove` | `task:task:write` |
| `sections.create` | `task:section:write` |
| `sections.delete` | `task:section:write` |
| `sections.get` | `task:section:read` |
| `sections.list` | `task:section:read` |
| `sections.patch` | `task:section:write` |
| `sections.tasks` | `task:section:read` |
| `custom_fields.create` | `task:custom_field:write` |
| `custom_fields.get` | `task:custom_field:read` |
| `custom_fields.patch` | `task:custom_field:write` |
| `custom_fields.list` | `task:custom_field:read` |
| `custom_fields.add` | `task:custom_field:write` |
| `custom_fields.remove` | `task:custom_field:write` |
| `custom_field_options.create` | `task:custom_field:write` |
| `custom_field_options.patch` | `task:custom_field:write` |
| `agent.update_agent_profile` | `task:task:write` |
| `agent.register_agent` | `task:task:write` |
| `agent_task_step_info.append_task_steps` | `task:task:write` |
| `+upload-attachment` | `task:attachment:write` |
