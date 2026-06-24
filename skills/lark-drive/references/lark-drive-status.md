
# drive +status

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

按 **精确 SHA-256**（默认）或 **快速 modified_time**（`--quick`）比较本地目录与飞书云空间文件夹，输出四类差异：

| 字段 | 含义 |
|------|------|
| `new_local` | 仅本地存在 |
| `new_remote` | 仅云端存在 |
| `modified` | 双端都存在且本次检测判定为已变更：`detection=exact` 时表示 hash 不一致；`detection=quick` 时表示本地 mtime 与远端 `modified_time` 不一致，或远端时间戳不可可信 |
| `unchanged` | 双端都存在且本次检测判定为未变更：`detection=exact` 时表示 hash 一致；`detection=quick` 时表示本地 mtime 与远端 `modified_time` 相等 |

只读命令：

- 默认 `detection=exact`：双端都有的文件会从云端拉一份字节流过来在内存里算 hash，不下载落盘，但大目录 / 大文件会有可观的网络流量。
- 传 `--quick` 后 `detection=quick`：只比较本地 mtime 与远端 `modified_time`，**不下载远端文件内容**，适合先做快速预检查；它是 best-effort，不等同于严格内容一致性判断。

## 远端同名文件冲突

如果 Drive 中多个条目映射到同一个 `rel_path`，`+status` 会在下载/hash 前直接失败，返回 `error.type=duplicate_remote_path`，并在 `error.detail.duplicates_remote[]` 中列出该路径下所有冲突条目的 `file_token`、`type`、名称、大小和时间字段；其中 `created_time`、`modified_time` 缺失时会省略，`size` 在缺失或为 `0` 时都可能被省略。不要把这种情况当成普通 `modified`；它表示同步域本身有歧义，需要先整理云端结构，或在 `+pull` / `+push` 中仅对“duplicate file”场景显式选择冲突策略。

## 命令

```bash
# 基础用法 —— 两个必填参数
lark-cli drive +status \
  --local-dir ./repo \
  --folder-token fldcnxxxxxxxxx

# 快速模式 —— 只比较 modified_time，不下载远端文件内容
lark-cli drive +status \
  --local-dir ./repo \
  --folder-token fldcnxxxxxxxxx \
  --quick

# 只看判定为 modified 的项（exact=hash 不一致；quick=mtime 不一致）（结合 --jq 过滤）
lark-cli drive +status \
  --local-dir ./repo \
  --folder-token fldcnxxxxxxxxx \
  --jq '.modified'
```

## 参数

| 标志 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--local-dir` | 是 | path | 本地根目录（**必须是 cwd 的相对路径**；绝对路径或逃逸到 cwd 外的相对路径会被 CLI 直接拒绝） |
| `--folder-token` | 是 | string | Drive 文件夹 token |
| `--quick` | 否 | bool | 快速模式：只比较本地 mtime 与远端 `modified_time`，跳过远端下载和 SHA-256 计算；输出里的 `detection` 会变成 `quick` |

## 输出 schema

成功时：

```json
{
  "detection":  "exact",
  "new_local":  [{"rel_path": "..."}],
  "new_remote": [{"rel_path": "...", "file_token": "..."}],
  "modified":   [{"rel_path": "...", "file_token": "..."}],
  "unchanged":  [{"rel_path": "...", "file_token": "..."}]
}
```

其中：

- `detection=exact`：默认模式，双端都有的文件会下载远端字节流并做 SHA-256 比较。
- `detection=quick`：`--quick` 模式，只按本地 mtime 与远端 `modified_time` 做 best-effort 判断。

`rel_path` 始终用 `/` 作为分隔符（跨平台一致），相对于 `--local-dir` 或 `--folder-token` 的根。仅本地存在时没有 `file_token` 字段。

远端同名文件冲突时：

```json
{
  "ok": false,
  "error": {
    "type": "duplicate_remote_path",
    "message": "multiple Drive entries map to the same rel_path",
    "detail": {
      "duplicates_remote": [
        {
          "rel_path": "dup.txt",
          "entries": [
            {"file_token": "<full_file_token>", "type": "file", "name": "dup.txt", "size": 5, "created_time": "1730000000", "modified_time": "1730000000"},
            {"file_token": "<folder_token>", "type": "folder", "name": "dup.txt", "created_time": "1730000060", "modified_time": "1730000060"}
          ]
        }
      ]
    }
  }
}
```

## 比较范围

- **只比对 Drive `type=file` 的二进制文件**。在线文档（`docx` / `sheet` / `bitable` / `mindnote` / `slides`）和快捷方式（`shortcut`）都被跳过 —— 它们没有等价的本地二进制可对齐，否则会在 `new_remote` 里产生大量误报。
- 子文件夹会递归遍历；rel_path 形如 `sub1/sub2/file.txt`。
- 多个远端条目映射到同一个 rel_path 时不做隐式选择，默认失败。
- 本地侧只比对常规文件（regular file）；符号链接、设备文件等被忽略。
- `--quick` 模式下，双端都有的文件只在 **远端时间精度** 下比较 `modified_time` / 本地 mtime：相等才记为 `unchanged`，否则记为 `modified`；远端时间戳缺失或非法时，走保守路径记为 `modified`，不会盲判 `unchanged`。

## 范围限制

`+status` 的本地侧只接受 cwd 下的相对路径。如果用户想比对的目录在 cwd 之外，**不要 agent 自己 `cd` 绕过**；让用户在合适的祖先目录重新启动 agent 后再跑。注意：把目标软链接到 cwd 内**也不行**——路径校验会先 `EvalSymlinks` 再判定是否越界，链接最终指向的真实目录如果在 cwd 之外，仍然会被 `unsafe file path` 拒掉。CLI 会在路径越界时直接报错，无需在 skill 这一层提前手动校验。

## 典型用法

把 +status 当作"先看差异、再决定怎么同步"的只读探针。常见接驳场景：

- 想知道云端有什么本地没有的内容 → 看 `new_remote`，按需选择性拉取（`drive +download --file-token <token>`）。
- 想把本地新增的内容推到云端 → 看 `new_local`，再 `drive +upload --file <path> --folder-token <parent>`（注意 +upload 不接受 0 字节文件）。
- 想知道哪些文件在云端被同事改过 → 看 `modified`，逐个 `drive +download` 查内容差异。

## 性能注意

- 默认 `detection=exact` 下，`unchanged` + `modified` 的总字节数 = 本次需从云端下载的流量。100GB 的双端共享内容意味着 100GB 网络往返。
- `--quick` / `detection=quick` 下，不会下载双端共有文件的远端内容，执行时间更接近 `O(文件数量)`，而不是 `O(总文件大小)`。
- 仅一侧存在的文件不会被下载。
- 默认模式的 hash 计算在内存里流式做（io.Copy → sha256.New），不会把云端文件落到磁盘。

## 所需 scope

| 操作 | scope |
|------|-------|
| 列出文件夹 / 子目录 | `drive:drive.metadata:readonly` |
| 下载并 hash 文件 | `drive:file:download` |

默认会先要求 `drive:drive.metadata:readonly`。在 `detection=exact` 路径（默认，不传 `--quick`）下，CLI 还会额外要求 `drive:file:download`；传 `--quick` 时不会要求下载 scope。如果当前 token 缺本次执行路径需要的 scope，命令会报 `missing_scope` 并提示重新登录。`drive:drive` 在部分企业被策略禁用，所以 +status 故意只依赖上面这些细粒度 scope。

## 参考

- [lark-drive](../SKILL.md) —— 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) —— 认证和全局参数
- [lark-drive-upload](lark-drive-upload.md) / [lark-drive-download](lark-drive-download.md) —— 把 +status 输出接到推/拉动作上
