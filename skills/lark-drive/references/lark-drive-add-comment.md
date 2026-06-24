
# drive +add-comment

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

给文档、电子表格或飞书幻灯片添加评论。底层统一走 `/open-apis/drive/v1/files/:file_token/new_comments`（`create_v2`）接口；未指定位置时省略 `anchor` 创建全文评论，指定 `--block-id` 时传入 `anchor.block_id` 创建局部评论。支持直接传 docx URL/token、旧版 doc URL（仅全文评论）、sheet URL、slides URL，也支持传最终可解析为 doc/docx/sheet/slides 的 wiki URL。

## 命令

```bash
# 默认：未指定位置时添加全文评论
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/docx/<DOC_ID>" \
  --content '[{"type":"text","text":"请补充发布说明"}]'

# 也可以显式指定为全文评论；旧版 doc URL 仅支持全文评论
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/doc/<DOC_ID>" \
  --full-comment \
  --content '[{"type":"text","text":"请补充旧版文档的背景信息"}]'

# wiki 链接也可以，shortcut 会先解析到真实 doc/docx token
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/wiki/<WIKI_TOKEN>" \
  --content '[{"type":"text","text":"这里需要一段全文评论"}]'

# 给 docx 文档的指定 block 添加局部评论（block_id 可通过 docs +fetch --api-version v2 --detail with-ids 获取）
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/docx/<DOC_ID>" \
  --block-id "<BLOCK_ID>" \
  --content '[{"type":"text","text":"请补充流程说明"}]'

# wiki 链接也支持局部评论，但解析结果必须是 docx
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/wiki/<WIKI_TOKEN>" \
  --block-id "<BLOCK_ID>" \
  --content '[{"type":"text","text":"请补充更细的开发步骤"}]'

# 组合文本、@用户、链接元素
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/docx/<DOC_ID>" \
  --block-id "<BLOCK_ID>" \
  --content '[{"type":"text","text":"请 "},{"type":"mention_user","text":"ou_xxx"},{"type":"text","text":" 处理，参考 "},{"type":"link","text":"https://example.com"}]'

# 给电子表格单元格添加评论（--block-id 格式为 <sheetId>!<cell>）
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/sheets/<SHEET_TOKEN>" \
  --block-id "<SHEET_ID>!D6" \
  --content '[{"type":"text","text":"请检查此单元格数据"}]'

# wiki 链接指向的 sheet 也支持
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/wiki/<WIKI_TOKEN>" \
  --block-id "<SHEET_ID>!A1" \
  --content '[{"type":"text","text":"请 "},{"type":"mention_user","text":"ou_xxx"},{"type":"text","text":" 确认"}]'

# 给幻灯片元素添加评论（--block-id 格式为 <slide-block-type>!<xml-id>）
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/slides/<PRESENTATION_ID>" \
  --block-id "<SLIDE_BLOCK_TYPE>!<XML_ELEMENT_ID>" \
  --content '[{"type":"text","text":"请调整这个元素的位置"}]'

# 例如：给整页 slide 添加评论
# <slide id="pkk"> ... </slide>  =>  --block-id slide!pkk
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/slides/<PRESENTATION_ID>" \
  --block-id "slide!pkk" \
  --content '[{"type":"text","text":"这一页需要补充过渡说明"}]'

# 例如：给图片元素添加评论
# <img id="bPk" ... />  =>  --block-id img!bPk
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/slides/<PRESENTATION_ID>" \
  --block-id "img!bPk" \
  --content '[{"type":"text","text":"这张图片建议换成更清晰的版本"}]'

# 例如：给文本 shape 添加评论
# <shape type="text" id="bPq"> ... </shape>  =>  --block-id shape!bPq
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/slides/<PRESENTATION_ID>" \
  --block-id "shape!bPq" \
  --content '[{"type":"text","text":"这段文案可以再精简"}]'

# wiki 链接指向的 slides 也支持
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/wiki/<WIKI_TOKEN>" \
  --block-id "<SLIDE_BLOCK_TYPE>!<XML_ELEMENT_ID>" \
  --content '[{"type":"text","text":"这里需要补充说明"}]'

# 传裸 token 时需要 --type 指定文档类型
lark-cli drive +add-comment \
  --doc "<SHEET_TOKEN>" --type sheet \
  --block-id "<SHEET_ID>!D6" \
  --content '[{"type":"text","text":"请检查"}]'

lark-cli drive +add-comment \
  --doc "<DOCX_TOKEN>" --type docx \
  --content '[{"type":"text","text":"全文评论"}]'

# 裸 token + 已知 block_id 的局部评论
lark-cli drive +add-comment \
  --doc "<PRESENTATION_ID>" --type slides \
  --block-id "<SLIDE_BLOCK_TYPE>!<XML_ELEMENT_ID>" \
  --content '[{"type":"text","text":"slide block comment"}]'

# 裸 token + 已知 block_id 的局部评论
lark-cli drive +add-comment \
  --doc "<DOCX_TOKEN>" --type docx \
  --block-id "<BLOCK_ID>" \
  --content '[{"type":"text","text":"请 "},{"type":"mention_user","text":"ou_xxx"},{"type":"text","text":" 处理，参考 "},{"type":"link","text":"https://example.com"}]'

# 如果需要更底层的原生 API，也可以直接调用 V2 协议
lark-cli schema drive.file.comments.create_v2

lark-cli drive file.comments create_v2 \
  --params '{"file_token":"<DOC_TOKEN>"}' \
  --data '{"file_type":"docx","reply_elements":[{"type":"text","text":"全文评论内容"}]}'

# 预览底层调用链
lark-cli drive +add-comment \
  --doc "https://example.larksuite.com/docx/<DOC_ID>" \
  --block-id "<BLOCK_ID>" \
  --content '[{"type":"text","text":"请补充流程说明"}]' \
  --dry-run
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--doc` | 是 | 文档 URL / token、sheet / slides URL，或可解析到 `doc`/`docx`/`sheet`/`slides` 的 wiki URL |
| `--type` | 裸 token 时必填 | 文档类型：`doc`、`docx`、`sheet`、`slides`。URL 输入时自动识别，无需传 |
| `--content` | 是 | `reply_elements` JSON 数组字符串。示例：`'[{"type":"text","text":"文本"},{"type":"mention_user","text":"ou_xxx"},{"type":"link","text":"https://example.com"}]'` |
| `--full-comment` | 否 | 显式指定创建全文评论；未传 `--block-id` 时也会默认走全文评论（不适用于 sheet） |
| `--block-id` | 局部评论时必填 | 目标块 ID，可通过 `docs +fetch --api-version v2 --detail with-ids` 获取。**Sheet 评论**：格式为 `<sheetId>!<cell>`（如 `a281f9!D6`） |

## 行为说明

- **局部评论需要先获取 block ID**：先调用 `docs +fetch --api-version v2 --doc <TOKEN> --detail with-ids` 获取带有 block ID 的文档内容，然后使用 `--block-id` 指定目标块。
- 未传 `--block-id` 时，shortcut 默认创建**全文评论**；也可以显式传 `--full-comment`。全文评论支持 `docx`、旧版 `doc` URL，以及最终可解析为 `doc`/`docx` 的 wiki URL。
- 传 `--block-id` 时，shortcut 创建**局部评论（划词评论）**；该模式支持 `docx`、`slides`，以及最终可解析为这些类型的 wiki URL。
- **Sheet 评论**：当 `--doc` 为 sheet URL 或 wiki 解析为 sheet 时，使用 `--block-id "<sheetId>!<cell>"` 指定单元格（如 `a281f9!D6`）；sheet 没有全文评论，`--full-comment` 不可用。
- **Slide 评论**：当 `--doc` 为 slides URL、`--type slides`，或 wiki 解析为 slides 时，必须传 `--block-id "<SLIDE_BLOCK_TYPE>!<XML_ELEMENT_ID>"`。CLI 会将其拆分映射到 `anchor.block_id` / `anchor.slide_block_type`。此时 `--full-comment` 和 `--selection-with-ellipsis` 不可用。
- **Slide 参数映射示例**：`--block-id` 由 PPT XML 元素类型和元素 `id` 组成。例如：
    - `<slide id="pkk">` 对应 `--block-id slide!pkk`，表示给整页评论。
    - `<img id="bPk" ... />` 对应 `--block-id img!bPk`，表示给图片元素评论。
    - `<shape type="text" id="bPq">...</shape>` 对应 `--block-id shape!bPq`，表示给文本 shape 评论。

- `--content` 接收结构化评论元素数组；`type` 支持 `text`、`mention_user`、`link`。为便于书写，`mention_user` / `link` 元素可以直接把用户 ID 或链接地址放在 `text` 字段中，shortcut 会转换成 OpenAPI 所需字段。
- `type=text` 的评论文本不能直接包含 `<`、`>`；应优先传 `&lt;`、`&gt;`。shortcut 在发送前也会自动将 `<`、`>` 转义为 `&lt;`、`&gt;` 作为兜底。
- **所有 `type=text` 元素的字符总和 ≤ 10000**（按字符算，中英文 / 符号一视同仁）。超过会被 shortcut 在发送前拒绝，并指出累计超长的元素。**拆成多个 text element 不能绕过这个上限**——上限是总额，不是每元素。需要更长内容就缩短或拆成多条评论。
- 长度限制只对 `type=text` 生效，`mention_user` / `link` 不计入。
- 局部评论走 `locate-doc` 时，内部固定使用 `limit=10`。
- 当 `locate-doc` 命中多处时，shortcut 会中止并提示用户继续收窄 `--selection-with-ellipsis`，不支持手动指定匹配序号。
- 写入评论前会自动生成符合 OpenAPI 定义的请求体：
  - 统一接口：`POST /new_comments`
  - 统一字段：`file_type` + `reply_elements`
  - 全文评论：省略 `anchor`
  - 局部评论：传入 `anchor.block_id`
- `--dry-run` 仅预览调用链和请求体，不会实际写入。
- 如果需要更底层的控制，仍可改用 `lark-cli schema drive.file.comments.create_v2` + `lark-cli drive file.comments create_v2`。

> [!CAUTION]
> 这是**写入操作** —— 执行前必须确认用户意图。

## 参考

- [lark-drive](../SKILL.md) -- 云空间全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
