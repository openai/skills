
# docs +update（更新飞书云文档）

> **前置条件（MUST READ）：** 生成文档内容前，必须先用 Read 工具读取以下文件，缺一不可：
> 1. [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) — 认证、全局参数和安全规则
> 2. [`lark-doc-xml.md`](lark-doc-xml.md) — XML 语法规则（使用 Markdown 格式时改读 [`lark-doc-md.md`](lark-doc-md.md)）
> 3. [`lark-doc-style.md`](style/lark-doc-style.md) — 排版指南（元素选择、丰富度规则、颜色语义）
> 4. [`lark-doc-update-workflow.md`](style/lark-doc-update-workflow.md) — 改写增强工作流（Code-Act Loop、并行执行策略）
>
> **未读完以上文件就生成内容会导致格式错误或样式不达标。**

通过八种指令精确更新飞书云文档。支持字符串级别和 block 级别的操作。

> **⚠️ 格式选择规则：**
> - **局部精修**（`str_replace` / `block_insert_after` / `block_replace` / `block_delete` / `block_move_after`）：优先使用 XML（默认）。XML 能稳定表达 block 结构和样式，精准编辑更可控；不要因为 Markdown 写起来更简单就自行切换。
> - **整段写入**（`append` / `overwrite`）：XML 和 Markdown 都可以。用户提供 `.md` 本地文件或明确要求 Markdown 时直接用 Markdown；否则默认 XML。
>
> **Markdown 局限 & block ID 前提：** Markdown 不携带 block ID，也无样式（颜色、对齐、callout 等）。需要按 block ID 定位（`block_*` 指令的 `--block-id`）时，先 `docs +fetch --api-version v2 --detail with-ids` **配合 `--scope`（`outline` / `range` / `keyword` / `section`）局部获取**目标段落，不要全量 fetch。拿到 block ID 后 `--content` 仍可用 Markdown，只是写入内容不带样式。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--api-version` | 是 | 固定传 `v2` |
| `--doc` | 是 | 文档 URL 或 token |
| `--command` | 是 | 操作指令（见下方指令速查表） |
| `--doc-format` | 否 | 内容格式：`xml`（默认，始终优先使用）\| `markdown`（仅用户明确要求时） |
| `--content` | 视指令 | 写入内容（`str_replace` 传空字符串可实现删除） |
| `--pattern` | 视指令 | 匹配文本（str_replace） |
| `--block-id` | 视指令 | 目标 block ID（block_* 操作）,-1 表示末尾 |
| `--src-block-ids` | 视指令 | 源 block ID（逗号分隔），用于 block_copy_insert_after / block_move_after |
| `--revision-id` | 否 | 基准版本号，-1 = 最新（默认 `-1`） |

## 指令速查表

| 指令 | 说明 | 必需参数 |
|------|------|----------|
| `str_replace` | 全文文本查找替换（replacement 支持富文本标签；`--content` 传空字符串即为删除） | `--pattern` `--content` |
| `block_insert_after` | 在指定 block 之后插入新内容 | `--block-id` `--content` |
| `block_copy_insert_after` | 复制源 block 并插入到锚点之后（源块不变） | `--block-id` `--src-block-ids` |
| `block_replace` | 替换指定 block（同一 block 仅限一次） | `--block-id` `--content` |
| `block_delete` | 删除指定 block（逗号分隔可批量） | `--block-id` |
| `overwrite` | ⚠️ 清空文档后全文重写（可能丢失图片、评论） | `--content` |
| `append` | 在文档末尾追加内容（等价于 `block_insert_after --block-id -1`） | `--content` |
| `block_move_after` | 移动已有 block 到指定位置 | `--block-id` + (`--content` 或 `--src-block-ids`) |

## 指令示例

### str_replace — 全文文本替换

> **匹配范围：**
> - **XML 模式（默认）**：`--pattern` 只支持**行内匹配**，不能跨 block / 跨段落匹配。涉及整段或多 block 的改动，请改用 `block_replace`。
> - **Markdown 模式**（`--doc-format markdown`）：`--pattern` 同时支持**行内和跨行匹配**，可以用多行字符串匹配并替换一整段内容。
>   - 还支持**`前缀...后缀` 省略号语法**：用 `...`（三个英文句点）串联起始与结束片段，匹配从前缀到后缀之间的全部内容（含中间被省略部分）。适合一段很长、但首尾特征明显的文本，避免把整段都塞进 `--pattern`。
>   - 前缀、后缀本身仍遵循 Markdown 转义规则；省略号中间的内容**会被替换**为 `--content` 的完整文本，不会被保留。

```bash
# 简单文本替换
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --pattern "张三" --content "李四"

# 替换为富文本（加粗 + 链接）
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --pattern "旧链接" --content '<b>新链接</b> <a href="https://example.com">点击查看</a>'

# 仅当用户明确要求时才使用 Markdown
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --doc-format markdown --pattern "旧内容" --content "新内容"

# Markdown 模式下支持跨行匹配（--pattern 与 --content 都需要真实换行；"..."/'...' 里的 \n 是字面量）
# 多行内容推荐 heredoc 或 --content @file.md，避免 shell 转义踩坑
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --doc-format markdown \
  --pattern "$(printf '## 旧标题\n\n第一段原文\n\n第二段原文')" \
  --content - <<'EOF'
## 新标题

改写后的第一段

改写后的第二段
EOF

# Markdown 模式下使用 `前缀...后缀` 省略号匹配首尾特征明显的大段内容
# 下例会把「## 旧标题」到「结束语。」之间的所有内容整体替换
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --doc-format markdown \
  --pattern "## 旧标题...结束语。" \
  --content - <<'EOF'
## 新标题

重写后的正文...

新的结束语。
EOF

# 删除文本：--content 传空字符串即可
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --pattern "废弃的内容" --content ""
```

### block_insert_after — 在指定 block 之后插入

```bash
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_insert_after \
  --block-id "目标 block_id" \
  --content '<h2>新章节</h2><ul><li>要点 1</li><li>要点 2</li></ul>'
```

### block_replace — 替换指定 block

```bash
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_replace \
  --block-id "目标 block_id" \
  --content '<p>替换后的段落内容</p>'
```

### block_delete — 删除指定 block

```bash
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_delete \
  --block-id "目标 block_id"
```

### overwrite — 全文覆盖

```bash
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command overwrite \
  --content '<title>全新文档</title><h1>概述</h1><p>新的内容</p>'
```

> ⚠️ 会清空文档后重写，可能丢失图片、评论等。仅在需要完全重建文档时使用。

### append — 在文档末尾追加

```bash
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command append \
  --content '<h2>新增章节</h2><p>追加的内容</p>'
```

> 等价于 `block_insert_after --block-id -1`，无需先获取 block ID。

### block_copy_insert_after — 复制块并插入

将一个或多个源块复制到锚点块之后，源块保持不变。`--src-block-ids` 为逗号分隔的源块 ID，按顺序依次插入到锚点之后。

```bash
# 复制多个块（按顺序插入：anchor → a → b → c）
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_copy_insert_after \
  --block-id "锚点 block_id" \
  --src-block-ids "block_a,block_b,block_c"
```

### block_move_after — 移动已有 block

将文档中已有的 block 移动到指定锚点之后。使用 `--src-block-ids` 指定要移动的块 ID，无需 `--content`。

```bash
# 移动到页面末尾
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_move_after \
  --block-id "-1表示末尾，page_id表示开头，blk" \
  --src-block-ids "block_a,block_b"
```

## 返回值

```json
{
  "ok": true,
  "identity": "user",
  "data": {
    "document": {
      "revision_id": 13,
      "new_blocks": [
        { "block_id": "blkcnXXXX", "block_type": "whiteboard", "block_token": "boardXXXX" }
      ]
    },
    "result": "success",
    "updated_blocks_count": 3,
    "warnings": []
  }
}
```

| 字段 | 说明 |
|------|------|
| `result` | `success` \| `partial_success` \| `failed` |
| `updated_blocks_count` | 实际更新的 block 数量 |
| `warnings` | 警告信息列表 |
| `document.new_blocks` | 本次操作新增的 block 列表（如画板）。`block_id` 可用于后续精确编辑；`block_token` 是资源块 token（如画板）可交给 `lark-whiteboard` 等 skill 继续操作 |

## 典型工作流

### 精确 block 级更新

1. **获取文档内容和 block ID**：
   ```bash
   lark-cli docs +fetch --api-version v2 --doc "<doc_id>" --detail with-ids
   ```

2. **定位目标 block**：从返回的 XML 中找到要修改的 block 及其 `id` 属性

3. **执行更新**：
   ```bash
   # 替换特定 block
   lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_replace \
     --block-id "blkcnXXXX" --content "<p>新内容</p>"

   # 在某 block 后插入
   lark-cli docs +update --api-version v2 --doc "<doc_id>" --command block_insert_after \
     --block-id "blkcnXXXX" --content "<h2>追加的章节</h2>"
   ```

### 简单文本替换

不需要 block ID，直接匹配替换：

```bash
lark-cli docs +update --api-version v2 --doc "<doc_id>" --command str_replace \
  --pattern "v1.0" --content "v2.0"
```

## 画板处理

> **`docs +update` 不能直接编辑已有画板的内容。** 本命令只能**新增**画板块；要修改已有画板，先用 `docs +fetch --api-version v2` 取到 `<whiteboard token="...">`，再切到 [`lark-whiteboard`](../../lark-whiteboard/SKILL.md) 用 `whiteboard +update` 写入。

画板的语法选型与插入示例见 [`lark-doc-style.md`](style/lark-doc-style.md) 的「画板语法与插入」章节。

## 最佳实践

- **精确操作优于全文覆盖**：使用 `block_replace`/`block_insert_after` 精确修改，避免 `overwrite` 全文覆盖
- **str_replace 的匹配范围取决于格式**：
  - **XML 模式（默认）**：`--pattern` 只支持**行内**匹配，不支持跨行 / 跨 block。段落、整块或容器级（列表、表格、分栏、引用块等）改动请改用 `block_replace` 指定 block_id 重建。
  - **Markdown 模式**（`--doc-format markdown`）：`--pattern` 同时支持**行内和跨行**匹配，还支持 `前缀...后缀` 省略号语法（用 `...` 串联首尾片段匹配一大段内容），可以一次替换多行文本；但仍建议优先按最小片段匹配，跨 block 容器级重写仍优先用 `block_replace`，避免副作用。
- **保护不可重建的内容**：图片、画板、电子表格等以 token 形式存储，替换时避开这些 block
- **str_replace 的 replacement 支持富文本**：可以用行内标签 `<b>`、`<a>`、`<cite>`、`<latex>` 等替换普通文本为富文本
- **同一 block 只能被 replace 一次**：多次修改同一 block 请合并为一次 block_replace
- **block_delete 支持批量**：用逗号分隔多个 block_id 一次删除
- **复杂结构重组**：将多个段落转换为 grid / table 等复杂布局时，分步操作比 overwrite 更安全：
  1. 用 `block_insert_after` 在目标位置插入新的富文本结构
  2. 用 `block_delete` 批量删除旧的 block
  3. 这样可以保留文档中其他不相关的内容（图片、评论等）
- **视觉丰富度**：插入或替换内容时，同样遵循 [`lark-doc-style.md`](style/lark-doc-style.md) 中的样式指南，主动使用结构化 block

## 参考

- [`lark-doc-update-workflow.md`](style/lark-doc-update-workflow.md) — 改写增强工作流（Code-Act Loop、并行执行策略）
- [`lark-doc-style.md`](style/lark-doc-style.md) — 文档样式指南（元素选择 + 丰富度规则 + 颜色语义）
- [`lark-doc-xml.md`](lark-doc-xml.md) — XML 语法规范
- [`lark-doc-fetch.md`](lark-doc-fetch.md) — 获取文档
- [`lark-doc-create.md`](lark-doc-create.md) — 创建文档
- [`lark-doc-media-insert.md`](lark-doc-media-insert.md) — 插入图片/文件到文档
- [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) — 认证和全局参数
