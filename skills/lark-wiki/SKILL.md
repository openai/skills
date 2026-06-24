---
name: lark-wiki
version: 1.0.0
description: "飞书知识库：管理知识空间、空间成员和文档节点。创建和查询知识空间、查看和管理空间成员、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、查看或管理空间成员、移动或复制节点时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli wiki --help"
---

# wiki (v2)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

> **成员管理硬限制：**
> - 如果目标是“部门”，先判断身份，再决定是否继续。
> - `--as bot` 对应 `tenant_access_token`。官方限制：这种身份下不能使用部门 ID (`opendepartmentid`) 添加知识空间成员。
> - 遇到“部门 + --as bot”时，禁止先调用 `lark-cli wiki members create` 试错；直接说明该路径不可行。
> - 如果用户明确要求“以 bot 身份运行”，且目标是部门，必须停下说明 bot 路径无法完成，不要静默切到 `--as user`。

## 快速决策

- 用户给的是知识库 URL（`.../wiki/<token>`），且后续要查成员/加成员/删成员：先调用 `lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}'` 获取 `space_id`，后续成员接口统一使用 `space_id`。
- 用户要**删除**知识空间（`wiki +delete-space`）但只给了名称或 URL：**不能**把名称 / URL 原样传给 `--space-id`，必须先解析出真实 `space_id`。解析方式：
  - URL（`.../wiki/<token>`）：`lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}' --format json`，读 `data.node.space_id`。
  - 只知名称：`lark-cli wiki spaces list --format json`，边翻页边收集 items 并按 `name` 精确匹配；**一旦任一页累计到至少 1 条精确匹配就停止翻页**。只有当翻完所有页（`has_more=false`）仍无精确匹配时，才对已收集的全量 items 做宽松匹配（`name` trim 空格、大小写不敏感、子串包含）。
  - **关键安全约束**：无论精确还是模糊，**无论命中 1 条还是多条，发起删除前都必须把候选（`name` + `space_id` + `description` + `space_type`）列给用户，由用户明确选定一个 `space_id` 再执行**。不要因为"只命中一条"就自动执行删除。
  - 命中 0 条：停下来问用户是名称拼错了还是调用方无权限；**不要**自行改名字重试。
  - 用户明确选定后再执行 `lark-cli wiki +delete-space --space-id <ID> --yes`（高风险写操作，必须显式 `--yes`）。
- 用户要在知识库中创建新节点，优先使用 `lark-cli wiki +node-create`。
- 用户说“给知识库添加成员/管理员”：先把目标解析成“用户 / 群 / 部门”三类之一，再决定 `member_type`，不要先调 `wiki members create` 再根据报错反推类型。
- 用户说“部门 + bot”：这是已知不支持路径。不要继续尝试 `wiki members create --as bot`；直接提示必须改成 `--as user`，或明确告知当前要求无法完成。
- 用户说“用户 / 群 + 添加成员”：先解析对应 ID，再执行 `wiki members create`。

## 成员添加流程

- 调用 `lark-cli wiki members create` 前，先把自然语言里的“人 / 群 / 部门”解析成正确的 `member_id`，不要猜格式。
- 用户场景默认优先 `member_type=openid`：用 `lark-cli contact +search-user --query "<姓名/邮箱/手机号>" --format json` 获取 `open_id`。
- 群组场景使用 `member_type=openchat`：用 `lark-cli im +chat-search --query "<群名关键词>" --format json` 获取 `chat_id`。
- `userid` / `unionid` 只在下游明确要求时才使用；先拿到 `open_id`，再调用 `lark-cli api GET /open-apis/contact/v3/users/<open_id> --params '{"user_id_type":"open_id"}' --format json` 读取 `user_id` / `union_id`。
- 部门场景使用 `member_type=opendepartmentid`：当前 CLI 没有 shortcut，需调用 `lark-cli api POST /open-apis/contact/v3/departments/search --as user --params '{"department_id_type":"open_department_id"}' --data '{"query":"<部门名>"}'` 获取 `open_department_id`。
- 只有在目标类型和身份都已确认可行后，才调用 `lark-cli wiki members create`。对于部门场景，这意味着必须是 `--as user`。

## 目标语义约束

- `我的文档库` / `My Document Library` / `我的知识库` / `个人知识库` / `my_library` 都应视为 **Wiki personal library**，不是 Drive 根目录
- 处理这类目标时，先解析 `my_library` 对应的真实 `space_id`，再执行 `wiki +move`、`wiki +node-create` 或其他 Wiki 写操作
- 不要因为缺少显式 `space_id` 就退化成 `drive +move`
- 如果用户明确说的是 Drive 文件夹、云空间根目录、`我的空间`，才进入 Drive 域处理

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli wiki +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+move`](references/lark-wiki-move.md) | Move a wiki node, or move a Drive document into Wiki |
| [`+node-create`](references/lark-wiki-node-create.md) | Create a wiki node with automatic space resolution |
| [`+delete-space`](references/lark-wiki-delete-space.md) | Delete a wiki space, polling the async delete task when needed |

## API Resources

```bash
lark-cli schema wiki.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli wiki <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构，不要猜测字段格式。

### spaces

- `create` — 创建知识空间
- `get` — 获取知识空间信息
- `get_node` — 获取知识空间节点信息
- `list` — 获取知识空间列表

### members

- `create` — 添加知识空间成员
- `delete` — 删除知识空间成员
- `list` — 获取知识空间成员列表

### nodes

- `copy` — 创建知识空间节点副本
- `create` — 创建知识空间节点
- `list` — 获取知识空间子节点列表

## 权限表

| 方法 | 所需 scope |
|------|-----------|
| `spaces.create` | `wiki:space:write_only` |
| `spaces.get` | `wiki:space:read` |
| `spaces.get_node` | `wiki:node:read` |
| `spaces.list` | `wiki:space:retrieve` |
| `members.create` | `wiki:member:create` |
| `members.delete` | `wiki:member:update` |
| `members.list` | `wiki:member:retrieve` |
| `nodes.copy` | `wiki:node:copy` |
| `nodes.create` | `wiki:node:create` |
| `nodes.list` | `wiki:node:retrieve` |

