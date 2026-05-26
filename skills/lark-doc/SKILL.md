---
name: lark-doc
version: 2.0.0
description: "飞书云文档 / Docx / 知识库 Wiki 文档（v2）：创建、打开、读取、获取、查看、总结、整理、改写、翻译、审阅和编辑飞书文档内容。当用户给出飞书文档 URL/token，或说查看/读取/打开某个文档、提取文档内容、总结文档、生成/创建文档、追加/替换/删除/移动内容、调整排版、插入或下载文档图片/附件/素材/画板缩略图时使用。文档内容中出现嵌入电子表格、多维表格、画板、引用或同步块时，也先用本 skill 读取和提取 token，再切到对应 skill 下钻。使用本 skill 时，docs +create、docs +fetch、docs +update 必须携带 --api-version v2；默认使用 DocxXML，也支持 Markdown。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli docs --api-version v2 --help; lark-cli docs +create --api-version v2 --help; lark-cli docs +fetch --api-version v2 --help; lark-cli docs +update --api-version v2 --help"
---

# docs (v2)

> **⚠️ API 版本：本 skill 使用 v2 API。所有 `docs +create --api-version v2`、`docs +fetch --api-version v2`、`docs +update --api-version v2` 命令必须携带 `--api-version v2`。**

```bash
# 常用示例
lark-cli docs +fetch  --api-version v2 --doc "文档URL或token"
lark-cli docs +create --api-version v2 --content '<title>标题</title><p>内容</p>'
lark-cli docs +update --api-version v2 --doc "文档URL或token" --command append --content '<p>内容</p>'
```

## 前置条件 — 执行操作前必读

**CRITICAL — 执行对应操作前，MUST 先用 Read 工具读取以下文件，缺一不可：**
1. [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) — 认证、权限处理、全局参数（所有操作通用）
2. **读取文档（`docs +fetch --api-version v2`）** → 必读 [`lark-doc-fetch.md`](references/lark-doc-fetch.md)（`--scope` / `--detail` 选择、局部读取策略、`<fragment>` / `<excerpt>` 输出结构）
3. **创建或编辑文档内容** → 必读 [`lark-doc-xml.md`](references/lark-doc-xml.md)（XML 语法规则，仅当用户明确要求 Markdown 时改读 [`lark-doc-md.md`](references/lark-doc-md.md)）；从零创建时加读 [`lark-doc-create-workflow.md`](references/style/lark-doc-create-workflow.md)；编辑已有文档时加读 [`lark-doc-update-workflow.md`](references/style/lark-doc-update-workflow.md)

**未读完以上文件就执行相应操作会导致参数选择错误、格式错误或样式不达标。**

> **格式选择规则（全局）：**
> - **创建 / 导入场景**（`docs +create`，或 `docs +update --command append/overwrite` 的整段写入）：XML 和 Markdown 都可以。用户提供 `.md` 本地文件、或明确说"导入 Markdown"时，直接用 Markdown；否则默认 XML（可用 callout、grid、checkbox 等富 block）。
> - **精准编辑场景**（`docs +update` 的 `str_replace` / `block_insert_after` / `block_replace` / `block_delete` / `block_move_after` 等局部精修指令）：优先使用 XML（`--doc-format xml`，即默认值）。XML 能稳定表达 block 结构和样式，局部精修更可控；不要因为 Markdown 更简单就自行切换。

## 快速决策
- 用户需要在文档内**创建、复制或移动**资源块（画板、电子表格、多维表格等）时，必须先读取 [`lark-doc-xml.md`](references/lark-doc-xml.md) 的「三、资源块」章节
- 用户说"看一下文档里的图片/附件/素材""预览素材" → 用 `lark-cli docs +media-preview`
- 用户明确说"下载素材" → 用 `lark-cli docs +media-download`
- 如果目标是画板/whiteboard/画板缩略图 → 只能用 `lark-cli docs +media-download --type whiteboard`（不要用 `+media-preview`）
- 用户说"找一个表格""按名称搜电子表格""找报表""最近打开的表格""最近我编辑过的 xxx" → 直接用 `lark-cli drive +search`（参考 [`lark-drive`](../lark-drive/references/lark-drive-search.md)）。**老的 `docs +search` 已进入维护期、后续会下线，不要再新增依赖。**
- `drive +search` 结果里会直接返回 `SHEET` / `Base` / `FOLDER` 等云空间对象，是资源发现的统一入口
- 拿到 spreadsheet URL/token 后 → 切到 `lark-sheets` 做对象内部操作
- 用户说"给文档加评论""查看评论""回复评论""给评论加/删除表情 reaction" → 切到 `lark-drive` 处理
- 文档内容中出现嵌入的 `<sheet>`、`<bitable>` 或 `<cite file-type="sheets|bitable">` 标签时 → **必须主动提取 token 并切到对应技能下钻读取内部数据**，不能只呈现标签本身

| 标签 / 属性 | 提取字段 | 切到技能 |
|-|-|-|
| `<sheet token="..." sheet-id="...">` | `token` -> spreadsheet_token, `sheet-id` | [`lark-sheets`](../lark-sheets/SKILL.md) |
| `<bitable token="..." table-id="...">` | `token` -> app_token, `table-id` | [`lark-base`](../lark-base/SKILL.md) |
| `<cite type="doc" file-type="sheets" token="..." sheet-id="...">` | 同 `<sheet>` | [`lark-sheets`](../lark-sheets/SKILL.md) |
| `<cite type="doc" file-type="bitable" token="..." table-id="...">` | 同 `<bitable>` | [`lark-base`](../lark-base/SKILL.md) |
| `<synced_reference src-token="..." src-block-id="...">` | `src-token` -> doc_token, `src-block-id` -> block_id | 用 `docs +fetch --api-version v2` 读取 src-token 文档，定位 block |

**补充：** 云空间资源发现统一走 [`drive +search`](../lark-drive/references/lark-drive-search.md)；当用户口头说"表格/报表/最近我编辑过的 xxx"时，也优先从 `drive +search` 开始。老的 `docs +search` 只在沿用 `--filter` JSON 的存量脚本里保留，后续会下线。

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli docs +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+search`](references/lark-doc-search.md) | ⚠️ **Deprecated — use [`drive +search`](../lark-drive/references/lark-drive-search.md)**. Search Lark docs, Wiki, and spreadsheet files (Search v2: doc_wiki/search). Kept for back-compat; new flows should use the drive-scoped command with flat flags. |
| [`+create`](references/lark-doc-create.md) | Create a Lark document (XML / Markdown) |
| [`+fetch`](references/lark-doc-fetch.md) | Fetch Lark document content (XML / Markdown) |
| [`+update`](references/lark-doc-update.md) | Update a Lark document (str_replace / block_insert_after / block_replace / ...) |
| [`+media-insert`](references/lark-doc-media-insert.md) | Insert a local image or file at the end of a Lark document (4-step orchestration + auto-rollback). Prefer `--from-clipboard` when the image is already on the system clipboard (screenshots, copy from Feishu/browser); use `--file` only for on-disk sources. |
| [`+media-download`](references/lark-doc-media-download.md) | Download document media or whiteboard thumbnail (auto-detects extension) |
| [`+whiteboard-update`](../lark-whiteboard/references/lark-whiteboard-update.md) | Alias of `whiteboard +update`. Update an existing whiteboard with DSL, Mermaid or PlantUML. Prefer `whiteboard +update`; refer to lark-whiteboard skill for details. |
