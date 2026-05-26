
# drive +move

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

将文件或文件夹移动到用户云空间的其他位置。

## 与 `wiki +move` 的区别

- `drive +move` 只处理 **Drive 文件夹树内部** 的位置调整，目标位置用 `--folder-token` 表示
- `wiki +move` 处理的是 **Wiki 知识空间 / 页面层级**：要么移动已有 Wiki 节点，要么把 Drive 文档迁入 Wiki
- 如果用户说“移动到某个文件夹”“移动到我的空间根目录”，应使用 `drive +move`
- 如果用户说“移动到某个知识库 / 页面下”“迁入 Wiki / 知识空间”，应使用 `wiki +move`
- 如果用户说“移动到我的文档库 / 我的知识库 / 个人知识库 / my_library”，不要使用 `drive +move`；先按 Wiki 目标处理
- `我的文档库` 不是 Drive root folder，也不是 `--folder-token` 省略后的默认目的地
- `drive +move` 不支持 wiki 文档；如果目标是 Wiki，不要尝试用 `drive +move` 代替

## 不要误用到 `我的文档库`

下面几种说法都**不应该**触发 `drive +move`：

- `移动到我的文档库`
- `放到我的知识库`
- `迁入个人知识库`
- `move to My Document Library`

这些目标都应该先走 Wiki 解析流程：

```bash
lark-cli wiki spaces get --params '{"space_id":"my_library"}'
```

拿到真实 `space_id` 后，再改用 `wiki +move`。不要因为 `drive +move` 可以省略 `--folder-token` 就把它当作“我的文档库”的近似目标。

## 命令

```bash
# 移动文件到指定文件夹
lark-cli drive +move \
  --file-token <FILE_TOKEN> \
  --type file \
  --folder-token <TARGET_FOLDER_TOKEN>

# 移动文档到指定文件夹
lark-cli drive +move \
  --file-token <DOCX_TOKEN> \
  --type docx \
  --folder-token <TARGET_FOLDER_TOKEN>

# 移动文件夹（异步操作，会自动有限轮询任务状态）
lark-cli drive +move \
  --file-token <FOLDER_TOKEN> \
  --type folder \
  --folder-token <TARGET_FOLDER_TOKEN>

# 移动到根文件夹（不指定 --folder-token）
lark-cli drive +move \
  --file-token <FILE_TOKEN> \
  --type file
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file-token` | 是 | 需要移动的文件或文件夹 token |
| `--type` | 是 | 文件类型，可选值：`file` (普通文件)、`docx` (新版文档)、`bitable` (多维表格)、`doc` (旧版文档)、`sheet` (电子表格)、`mindnote` (思维笔记)、`folder` (文件夹)、`slides` (幻灯片) |
| `--folder-token` | 否 | 目标文件夹 token，不指定则移动到根文件夹 |

## 文件类型说明

| 类型 | 说明 |
|------|------|
| `file` | 普通文件 |
| `docx` | 新版云文档 |
| `doc` | 旧版云文档 |
| `sheet` | 电子表格 |
| `bitable` | 多维表格 |
| `mindnote` | 思维笔记 |
| `slides` | 幻灯片 |
| `folder` | 文件夹（移动文件夹是异步操作） |

## 行为说明

- **普通文件移动**：同步操作，立即完成
- **文件夹移动**：异步操作，接口返回 `task_id`，shortcut 会先做有限轮询；如果在轮询窗口内完成，则直接返回成功结果
- **轮询超时不是失败**：文件夹移动内置最多轮询 30 次、每次间隔 2 秒；如果轮询结束任务仍未完成，会返回 `task_id`、`status`、`ready=false`、`timed_out=true` 和 `next_command`
- **继续查询**：当看到 `next_command` 时，改用 `lark-cli drive +task_result --scenario task_check --task-id <TASK_ID>` 继续查询
- **目标文件夹**：如果不指定 `--folder-token`，文件将被移动到用户的根文件夹（"我的空间"）
- **不要混淆产品概念**：这里的“根文件夹 / 我的空间”仅属于 Drive 文件夹树，不等于 Wiki 的“我的文档库”
- **权限要求**：需要被移动文件的可管理权限、被移动文件所在位置的编辑权限、目标位置的编辑权限

## 推荐续跑方式

```bash
# 第一步：先直接移动文件夹
lark-cli drive +move \
  --file-token <FOLDER_TOKEN> \
  --type folder \
  --folder-token <TARGET_FOLDER_TOKEN>

# 如果返回 ready=false / timed_out=true，再继续查
lark-cli drive +task_result \
  --scenario task_check \
  --task-id <TASK_ID>
```

## 限制

- 被移动的文件不支持 wiki 文档
- 该接口不支持并发调用
- 调用频率上限为 5 QPS 且 10000 次/天

> [!CAUTION]
> 这是**写入操作** —— 执行前必须确认用户意图。

## 参考

- [lark-drive](../SKILL.md) -- 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
