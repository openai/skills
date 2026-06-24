
# drive +push

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

把本地目录**单向、文件级**镜像到飞书云空间的某个文件夹（本地 → Drive）。命令递归列出 `--folder-token` 下的远端清单，遍历 `--local-dir` 的所有常规文件，按相对路径在 Drive 上新建、覆盖或跳过；可选地（`--delete-remote --yes`）删除云端"本地没有"的 `type=file`。

> **"文件级镜像"≠"目录镜像"。** 命令只在文件维度收敛差异：本地多了文件就上传，本地少了文件且开了 `--delete-remote --yes` 就删远端文件。**远端只有的空目录、本地已删除的目录**都不会被收敛，云端目录树的多余结构不会被清理。如果需要"目录也要保持完全一致"，得自行先 `+status` 找差异、再手动处理多余目录。

输出按"动作"分类：

| 字段 | 含义 |
|------|------|
| `summary.uploaded` | 成功新建或覆盖的文件数 |
| `summary.skipped` | 因 `--if-exists=skip` 或 `--if-exists=smart` 命中“无需传输”而跳过的文件数 |
| `summary.failed` | 上传 / 覆盖 / 建目录 / 删除失败的条目数；**只要不为 0，命令就以非零状态退出**（结构化 `items[]` 仍在 stdout 上） |
| `summary.deleted_remote` | 启用 `--delete-remote --yes` 时删除的云端文件数 |
| `items[]` | 每个条目的明细（`rel_path` / `file_token` / `action` / 覆盖时的 `version` / `size_bytes` / 失败时的 `error`） |

`items[].action` 取值：`uploaded` / `overwritten` / `skipped` / `folder_created` / `deleted_remote` / `failed` / `delete_failed`。

> 本地目录（包括空目录）会被镜像到 Drive；新建的子目录会以 `action: "folder_created"` 出现在 `items[]` 里，但**不计入** `summary.uploaded`（该字段只数文件）。已存在的远端目录复用其 token，不会重复 `create_folder`，也不会出现在 `items[]` 里。

## 远端同名文件冲突

如果 Drive 中多个条目映射到同一个 `rel_path`，默认直接失败（`error.type=duplicate_remote_path`），且不会上传、覆盖或进入 `--delete-remote` 删除阶段。只有“多个 `type=file` 同名”的场景支持显式策略；`file-folder` 这类异构冲突始终直接失败。

| 策略 | 行为 |
|------|------|
| `fail` | 默认。返回所有冲突条目的完整信息，不写远端 |
| `newest` | 只把本地文件与 `modified_time` 最新的远端文件对齐 |
| `oldest` | 只把本地文件与 `created_time` 最早的远端文件对齐 |

`+push` 不提供 `rename`：本地一个文件无法表达要覆盖多个远端对象。若用户想保留多个云端副本，应先显式整理云端文件，再重新 push。

## 命令

```bash
# 基础用法 —— 把本地 ./repo 推送到云端 fldcXXX
# 默认 --if-exists=skip：已经存在的远端文件保持不动，只新增、不覆盖。
lark-cli drive +push --local-dir ./repo --folder-token fldcnxxxxxxxxx

# 重复同步时可用 smart 做增量优化：它会按 modified_time 跳过已对齐的远端文件；但如果远端更旧，仍会继续走覆盖路径
lark-cli drive +push --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --if-exists smart

# 显式覆盖远端同名文件（依赖 upload_all 的灰度协议字段，详见下文"覆盖语义"）
lark-cli drive +push --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --if-exists overwrite

# 云端已有多个同名二进制文件时，显式选择一个远端目标再覆盖
lark-cli drive +push --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --if-exists overwrite --on-duplicate-remote newest

# 文件级镜像同步：上传 / 覆盖 + 删除本地不存在的远端文件
# （--delete-remote 必须搭配 --yes，否则会被 Validate 直接拒绝；
#   且 Validate 阶段会动态检查 space:document:delete scope，缺权限会立刻失败，
#   不会出现"上传成功了但是后面删除阶段挂了"的半同步状态）
lark-cli drive +push --local-dir ./repo --folder-token fldcnxxxxxxxxx \
  --if-exists overwrite --delete-remote --yes
```

## 参数

| 标志 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--local-dir` | 是 | path | 本地根目录（**必须是 cwd 的相对路径**；绝对路径或逃出 cwd 的相对路径会被 CLI 直接拒绝） |
| `--folder-token` | 是 | string | 目标 Drive 文件夹 token |
| `--if-exists` | 否 | enum | 远端文件已存在时的策略：`skip`（**默认**，安全）/ `smart`（用于重复增量同步；当远端 `modified_time` 已匹配或更新时跳过上传，否则继续走覆盖路径）/ `overwrite`（依赖灰度后端协议，详见"覆盖语义"） |
| `--on-duplicate-remote` | 否 | enum | 云端多个条目映射到同一个 `rel_path` 时的策略：`fail`（默认）；如果冲突全是 `type=file`，还可选 `newest` / `oldest` |
| `--delete-remote` | 否 | bool | 删除云端本地不存在的文件（文件级镜像；**不会**清理远端只有的目录）；**必须配合 `--yes`**，且 Validate 阶段会动态检查 `space:document:delete` scope |
| `--yes` | 否 | bool | 确认 `--delete-remote`；不传时该破坏性操作在 Validate 阶段被拒绝 |

## 上传与目录复刻范围

- **只上传 / 覆盖 / 删除 Drive `type=file`**。在线文档（`docx` / `sheet` / `bitable` / `mindnote` / `slides`）和快捷方式（`shortcut`）即使在同一 rel_path 下出现，也不会被覆盖或删除 —— 它们没有等价的本地二进制。
- **本地目录结构整体被镜像**：所有子目录（含**空目录**）会按需在 Drive 上 `create_folder`；同名远端目录复用其 token，不重建。空目录不计入 `summary.uploaded`，但会在 `items[]` 里以 `folder_created` 形式留痕。
- 已存在的远端文件按 `--if-exists` 决定 `overwrite` / `smart` / `skip`。其中 `smart` 是**增量优化模式**：只要远端 `modified_time` 在同等时间精度下已经等于或晚于本地 mtime，就跳过上传；时间戳缺失/非法时会退回安全路径继续上传，不会盲跳。**但如果远端更旧，`smart` 会继续走和 `overwrite` 相同的覆盖路径，因此也继承同样的 rollout / version 返回 caveat。** 想做 `keep-both` 这类的仍需自行改名再 push。
- 云端同名冲突默认失败；只有“冲突全是 `type=file`”且传了 `--on-duplicate-remote newest|oldest` 时才会选择一个远端文件继续。启用 `--delete-remote` 时，未被选中的 duplicate sibling 也会被删除，最终远端只保留一个被选中的文件副本；只有在 `--if-exists=overwrite` 成功时，才能保证该副本内容与本地对齐。

## 覆盖语义

`--if-exists=overwrite` 走 `POST /open-apis/drive/v1/files/upload_all`，并在 form 中带上现有文件的 `file_token`，由后端原地更新内容并返回新版本号。`items[].version` 字段会回填该版本号。

`--if-exists=smart` 是给“重复跑同步”的场景增加的增量优化：当远端 `modified_time` 在同等时间精度下已经等于或晚于本地 mtime 时，命令会把该文件计为 `skipped`；时间戳缺失、非法或更旧时，则继续走正常上传/覆盖路径。**也就是说，只要 smart 判定“远端不够新”，它就会进入与 `--if-exists=overwrite` 相同的覆盖实现，因此在未 rollout version 字段的 tenant 上仍可能非零失败。**

> **为什么默认是 `skip` 而不是 `overwrite`：** `upload_all` 接受 `file_token` 字段、并在响应里返回 `version` 是设计文档（Drive 同步盘）规定的协议；此后端尚在灰度发布。在还未开通该字段的 tenant 上，`--if-exists=overwrite` 会因"无 version 返回"而把对应文件标成 `failed`，整次 `+push` 也会因此非零退出。所以默认值故意定为 `skip`：第一次往一个已经有内容的目录里 push，不会因为协议没到位就把整次运行打挂；要真的覆盖远端，必须显式带 `--if-exists overwrite`。新建上传不依赖该字段，不受影响。

大文件（>20MB）会自动切到三段式 `upload_prepare` / `upload_part` / `upload_finish`；该路径下 `version` 暂未在响应中返回，覆盖结果中 `items[].version` 会留空，但 `file_token` 与 `action: overwritten` 仍会正确产出。

## --delete-remote 的安全行为

`--delete-remote` 是命令里**唯一的破坏性 flag**，会按"远端有但本地没有"逐个 `DELETE /open-apis/drive/v1/files/<token>?type=file` 清理云端副本。设计上把它跟 `--yes` 强绑定：

- `--delete-remote`（无 `--yes`）→ Validate 直接报错：`--delete-remote requires --yes`，不会发起任何列表 / 上传 / 删除请求。
- `--delete-remote --yes` → Validate 阶段还会**动态做一次** `space:document:delete` 的 scope 预检：缺这条 scope 时整次运行立刻失败、不发任何上传请求，避免出现"上传都成功了，但删除阶段才报 missing_scope"的半同步状态。
- `--delete-remote --yes`（且 scope 已授权）→ 正常执行：先把本地文件 push 上去，再扫一遍远端 `type=file` 列表，把不在本地清单里的逐个删除。**任何上传 / 覆盖 / 建目录失败时，整段 `--delete-remote` 阶段会被跳过**（stderr 上有提示），命令以非零状态退出，远端不会被破坏。
- 远端同名冲突且使用默认 `fail`，或冲突里混有 folder / 其他非 `type=file` 对象 → 在上传阶段前失败，删除阶段不会运行。
- 不传 `--delete-remote` → `summary.deleted_remote` 永远是 0；命令对远端"多余"文件视而不见。
- 在线文档（docx / sheet / bitable / ...）和快捷方式即使本地完全没有同名文件，也**不会**进入删除候选，因为它们从来不进 `summary.uploaded` 的对齐域。
- **远端只有的空目录、本地已删除的目录**也不会被清理 —— 这是"文件级镜像"的语义边界，命令不会对目录结构做主动收敛。

第 6 章里把 `+push --delete-remote` 标了 `high-risk-write`，CLI 这边的实现等价于"未传 `--yes` 时拒绝执行 + 动态 scope 预检"，符合该约束的精神。

## 输出 schema

```json
{
  "summary": {
    "uploaded": 0,
    "skipped": 0,
    "failed": 0,
    "deleted_remote": 0
  },
  "items": [
    {"rel_path": "...", "file_token": "...", "action": "folder_created"},
    {"rel_path": "...", "file_token": "...", "action": "uploaded",       "size_bytes": 0},
    {"rel_path": "...", "file_token": "...", "action": "overwritten",    "version": "...", "size_bytes": 0},
    {"rel_path": "...", "file_token": "...", "action": "skipped",        "size_bytes": 0},
    {"rel_path": "...",                       "action": "failed",        "size_bytes": 0, "error": "..."},
    {"rel_path": "...", "file_token": "...", "action": "deleted_remote"},
    {"rel_path": "...", "file_token": "...", "action": "delete_failed",  "error": "..."}
  ]
}
```

`rel_path` 始终用 `/` 作为分隔符（跨平台一致）。

## 性能注意

- 默认 `skip` 下，已存在的远端文件一律不碰；`overwrite` 下，重复跑会重传所有命中的同名文件；`smart` 下会按 `modified_time` 跳过已对齐的远端文件，但对“远端更旧”的文件仍会进入覆盖路径，因此它减少的是**不必要的重传**，不是把覆盖风险完全拿掉。
- 想更精细地控制传输量，可以先 `+status` 找出 `new_local` 和 `modified`，再只对这些文件单独上传 / 覆盖；或者直接在整目录同步时使用 `--if-exists smart`。
- 大文件会用三段式分片上传（不会把整个 body 读进内存），但本地磁盘和上行带宽需要够。

## 所需 scope

| 操作 | scope | 是否在命令上预声明 |
|------|-------|-------------------|
| 列出文件夹 / 子目录 | `drive:drive.metadata:readonly` | ✅ 预声明 |
| 上传 / 覆盖文件 | `drive:file:upload` | ✅ 预声明 |
| 新建子目录（`create_folder`） | `space:folder:create` | ✅ 预声明 |
| 删除文件（仅 `--delete-remote --yes`） | `space:document:delete` | ⚙️ 不在命令默认 Scopes 里，但在 `--delete-remote --yes` 时由 Validate 动态预检 |

`drive:drive` 在部分企业被策略禁用，所以 +push 故意只声明上面这几条细粒度 scope。

> **关于 `space:document:delete`：** 框架的 scope 预检（`runner.go: checkShortcutScopes`）会在 `Validate` 和 `--dry-run` 之前就把命令上声明的 scope 全检查一遍；如果把删除 scope 也预声明，**普通上传或 dry-run** 都会因为没授权删除权限而被拦下来。所以这一项不放在命令的默认 Scopes 里，而是在 Validate 中**条件触发**：只有 `--delete-remote --yes` 同时打开时才会调用 `runtime.EnsureScopes([]string{"space:document:delete"})` 做一次动态前置校验。这样既保留了"普通上传不需要删除权限"的便利，又能在真要做镜像删除前把 scope 缺失暴露出来，避免出现"上传成功 → 删除阶段才挂"的半同步状态。
>
> 想一次性把权限补齐：`lark-cli auth login --scope "drive:drive.metadata:readonly drive:file:upload space:folder:create space:document:delete"`。

## 范围限制

`--local-dir` 只接受 cwd 内的相对路径。CLI 会先 `EvalSymlinks` 整条路径，再判断它是否仍落在 cwd 内 —— **指向 cwd 外的符号链接也会被拒**，"在 cwd 内放一条软链指向外面" 这条捷径走不通，会直接撞上 `unsafe file path`。

如果用户想 push cwd 之外的目录，**不要 agent 自己 `cd` 绕过**。可以选：让用户在外部把 agent 工作目录切换到目标的祖先后重启会话；或者把目标整体物理移动 / 拷贝到 cwd 内（不是软链）；或者直接放弃这次同步，改用别的方式。

## 参考

- [lark-drive](../SKILL.md) —— 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) —— 认证和全局参数
- [lark-drive-status](lark-drive-status.md) —— 上传前先看差异（避免全量回写）
- [lark-drive-pull](lark-drive-pull.md) —— Drive → 本地的对称命令
- [lark-drive-upload](lark-drive-upload.md) —— 单文件按需上传
