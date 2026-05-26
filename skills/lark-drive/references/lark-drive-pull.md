
# drive +pull

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

把飞书云空间的某个文件夹**单向、文件级**镜像到本地目录（Drive → 本地）。命令递归列出 `--folder-token` 下所有 `type=file` 的文件，逐一下载到 `--local-dir` 对应的相对路径，子文件夹自动复刻为本地目录。

> ⚠️ **不是 directory-level mirror**：`--delete-local` 只删除本地"多余"的常规文件，不删除空目录。如果云端把整个子文件夹删了，对应的本地子目录会留空（里面的文件被清掉，目录本身保留）；想精确同步目录结构请自己 `rmdir` 处理空壳。

输出按"动作"分类：

| 字段 | 含义 |
|------|------|
| `summary.downloaded` | 成功下载的文件数 |
| `summary.skipped` | 因 `--if-exists=skip` 或 `--if-exists=smart` 命中“无需下载”而跳过的文件数 |
| `summary.failed` | 下载或写盘失败的文件数 |
| `summary.deleted_local` | 启用 `--delete-local --yes` 时删除的本地文件数 |
| `items[]` | 每个文件的明细（`rel_path` / `file_token` / `source_id` / `action` / 失败时的 `error`） |

`summary.failed > 0` 时命令以 **非零状态码**（`exit=1`，`error.type=partial_failure`）退出，且同一份 `summary + items` 会在 `error.detail` 里返回；脚本/agent 直接通过 exit code 判断成败即可，不需要再去解 `summary.failed`。

## 远端同名文件冲突

如果 Drive 中多个条目映射到同一个 `rel_path`，默认直接失败（`error.type=duplicate_remote_path`），且不会下载、覆盖或删除任何本地文件。只有“多个 `type=file` 同名”的场景支持显式策略；`file-folder` 这类异构冲突始终直接失败。

| 策略 | 行为 |
|------|------|
| `fail` | 默认。返回所有冲突条目的完整信息，不写盘 |
| `rename` | 仅适用于 duplicate file。下载全部重复文件；第一个保留原名，后续文件使用稳定 hash 后缀生成唯一文件名；若短后缀目标已被占用，会自动升级到更强后缀 |
| `newest` | 只下载 `modified_time` 最新的远端文件 |
| `oldest` | 只下载 `created_time` 最早的远端文件 |

`rename` 命名规则稳定且可追溯：`report.pdf` 的后续重复项会落盘为 `report__lark_<hash>.pdf`，例如 `report__lark_3a2f4c5d6e7f.pdf`。如果这个短 hash 目标名已经被同目录下的其他远端对象占用，CLI 会自动改用更长的稳定 hash，必要时再追加序号后缀，直到目标名唯一。此模式下 `items[]` 不再返回可直接复用的 Drive `file_token`；CLI 会在 `source_id` 中返回稳定 hash 标识符，供日志、比对和人工排查使用。

## 命令

```bash
# 基础用法 —— 把云端 fldcXXX 镜像到 ./repo
lark-cli drive +pull --local-dir ./repo --folder-token fldcnxxxxxxxxx

# 推荐的重复同步用法：smart 会按 modified_time 跳过已经对齐的本地文件
lark-cli drive +pull --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --if-exists smart

# 已存在的本地文件保持不动
lark-cli drive +pull --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --if-exists skip

# 云端有多个同名二进制文件时，显式下载全部并用稳定 hash 后缀改名
lark-cli drive +pull --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --on-duplicate-remote rename

# 文件级镜像：下载新文件 + 删除云端没有的本地文件（不删空目录）
# （--delete-local 必须搭配 --yes，否则会被 Validate 直接拒绝）
lark-cli drive +pull --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --delete-local --yes
```

## 参数

| 标志 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--local-dir` | 是 | path | 本地根目录（**必须是 cwd 的相对路径**；绝对路径或逃出 cwd 的相对路径会被 CLI 直接拒绝） |
| `--folder-token` | 是 | string | 源 Drive 文件夹 token |
| `--if-exists` | 否 | enum | 本地文件已存在时的策略：`overwrite`（**默认**，Drive 作为权威源时使用）/ `smart`（**推荐用于重复增量同步**；当本地 mtime 已与远端 `modified_time` 匹配或更新时跳过下载）/ `skip` |
| `--on-duplicate-remote` | 否 | enum | 云端多个条目映射到同一个 `rel_path` 时的策略：`fail`（默认）；如果冲突全是 `type=file`，还可选 `rename` / `newest` / `oldest` |
| `--delete-local` | 否 | bool | 删除本地"云端没有的常规文件"（**不删空目录**，因此是 file-level mirror）；**必须配合 `--yes`** |
| `--yes` | 否 | bool | 确认 `--delete-local`；不传时该破坏性操作在 Validate 阶段被拒绝 |

## 比较与下载范围

- **只下载 Drive `type=file` 的二进制文件**。在线文档（`docx` / `sheet` / `bitable` / `mindnote` / `slides`）和快捷方式（`shortcut`）会被跳过 —— 它们没有等价的本地二进制可写盘，否则会变成产生噪声的"假"下载。
- 子文件夹会递归遍历；rel_path 形如 `sub1/sub2/file.txt`，本地缺失的父目录会被自动创建。
- 已存在的本地文件按 `--if-exists` 决定 `overwrite` / `smart` / `skip`。其中 **`smart` 是推荐的重复同步模式**：只要本地 mtime 在远端时间精度下已经等于或晚于远端 `modified_time`，就跳过下载；时间戳缺失/非法时会退回安全路径继续下载，不会盲跳。想做 `keep-both` 这类的仍需自己改名再 pull。
- 云端同名冲突默认失败；只有“冲突全是 `type=file`”且传了 `--on-duplicate-remote rename|newest|oldest` 时才会继续。

## --delete-local 的安全行为

`--delete-local` 是命令里**唯一的破坏性 flag**，会按"本地有但云端没有"清理本地常规文件。设计上把它跟 `--yes` 强绑定，且与下载阶段的失败联动：

- `--delete-local`（无 `--yes`）→ Validate 直接报错：`--delete-local requires --yes`，没有任何下载、列表请求或删除发生。
- `--delete-local --yes`，**且下载阶段全部成功** → 扫一遍 `--local-dir` 下所有常规文件，把不在云端清单里的逐个 `os.Remove`。**只删常规文件，不删目录**：远端文件夹被删除后，对应本地目录会保留空壳。
- `--delete-local --yes`，**但下载阶段有任何条目失败** → **跳过整个删除阶段**，命令以 `partial_failure` 非零退出。设计意图：避免出现"前面下载失败、后面继续删本地文件"的半同步状态；操作者修好下载错误后再重跑即可。
- 远端同名文件冲突且使用默认 `fail` → 在下载阶段前失败，删除阶段不会运行。
- 不传 `--delete-local` → `summary.deleted_local` 永远是 0；命令对本地"多余"文件视而不见。

第 6 章里把 `+pull --delete-local` 标了 `high-risk-write`，CLI 这边的实现等价于"未传 `--yes` 时拒绝执行"，符合该约束的精神。

## 输出 schema

```json
{
  "summary": {
    "downloaded": 0,
    "skipped": 0,
    "failed": 0,
    "deleted_local": 0
  },
  "items": [
    {"rel_path": "...", "file_token": "...", "action": "downloaded"},
    {"rel_path": "...", "source_id": "hash_3a2f4c5d6e7f", "action": "downloaded"},
    {"rel_path": "...", "source_id": "hash_3a2f4c5d6e7f", "action": "failed", "error": "..."},
    {"rel_path": "...", "action": "deleted_local"},
    {"rel_path": "...", "action": "delete_failed", "error": "..."}
  ]
}
```

`rel_path` 始终用 `/` 作为分隔符（跨平台一致）。删除条目（`deleted_local` / `delete_failed`）没有 `file_token`。`rename` 模式下，duplicate 文件条目会返回 `source_id` 而不是可调用 API 的真实 `file_token`；其余模式仍返回真实 `file_token`。

## 性能注意

- 默认 `overwrite` 下，重复跑会重新下载所有命中的同名文件；`skip` 下则完全不碰已存在文件；**`smart` 下才会按 `modified_time` 跳过已经对齐的本地文件**，适合重复增量同步。
- 想更精细地控制下载量，可以先 `+status` 找出 `new_remote` 和 `modified`，再只对这些文件单独 `+download`；或者直接在整目录同步时使用 `--if-exists smart`。
- 大文件会用 SDK 的流式下载（不会把整个 body 读进内存），但本地磁盘空间需要够。

## 所需 scope

| 操作 | scope |
|------|-------|
| 列出文件夹 / 子目录 | `drive:drive.metadata:readonly` |
| 下载文件 | `drive:file:download` |

如果当前 token 缺这些 scope，命令会直接报 `missing_scope` 并提示重新登录。`drive:drive` 在部分企业被策略禁用，所以 +pull 故意只声明上面这两个细粒度 scope。

## 范围限制

`--local-dir` 只接受 cwd 内的相对路径。CLI 会先 `EvalSymlinks` 整条路径，再判断它是否仍落在 cwd 内 —— **指向 cwd 外的符号链接也会被拒**，"在 cwd 内放一条软链指向外面" 这条捷径走不通，会直接撞上 `unsafe file path`。

如果用户想 pull 到 cwd 之外的目录，**不要 agent 自己 `cd` 绕过**。可以选：让用户在外部把 agent 工作目录切换到目标的祖先后重启会话；或者把目标整体物理移动 / 拷贝到 cwd 内（不是软链）；或者直接放弃这次同步，改用别的方式。

## 参考

- [lark-drive](../SKILL.md) —— 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) —— 认证和全局参数
- [lark-drive-status](lark-drive-status.md) —— 下载前先看差异
- [lark-drive-download](lark-drive-download.md) —— 单文件按需拉取
