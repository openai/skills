# base CellValue 规范（lark-base-cell-value）

> 适用命令：`lark-cli base +record-upsert`、`lark-cli base +record-batch-create`、`lark-cli base +record-batch-update`

本文件定义 **shortcut 写记录** 时 `CellValue` 的推荐格式，目标是让 AI 一次写对。不同命令的外层 JSON 形状不同，但每个 cell 都以本文为 source of truth。

## 1. 顶层规则（必须遵守）

- `--json` 必须是 JSON 对象。
- `+record-upsert`：顶层直接传字段映射：`{"字段名或字段ID": CellValue}`。
- `+record-batch-create`：`rows` 是 `CellValue[][]`，列顺序由 `fields` 决定。
- `+record-batch-update`：`patch` 是 `Map<FieldNameOrID, CellValue>`，同一份 `patch` 会应用到所有 `record_id_list`。
- 一次 payload 里同一字段只用一种 key（字段名或字段 ID），不要重复。
- 写入前先 `+field-list` 获取字段 `type/style/multiple`，再构造值。
- 需要清空字段时优先传 `null`（字段允许清空时）。

## 2. 各类型 CellValue

### 2.1 text / phone / url

用字符串。URL 字段也传 URL 字符串；普通文本里可以保留 Markdown 风格链接文本，平台会按字段类型处理。

```json
{
    "标题": "Hello",
    "联系电话": "1380000000000",
    "官网": "https://example.com"
}
```

### 2.2 number

用 JSON number，不要用带单位或千分位的字符串。货币、百分比、进度、评分等数字类字段也按数字写入，展示格式由字段配置决定。

```json
{
    "工时": 12.5,
    "预算": 3000,
    "完成度": 0.65,
    "评分": 4
}
```

### 2.3 select（单选/多选）

单选用选项名字符串；多选用选项名数组。选项名建议与字段配置一致；写入未知选项时平台可能自动新增选项，因此不要把自然语言近义词当成已有选项传入。

```json
{
    "单选": "Todo",
    "多选": ["后端", "高优"]
}
```

### 2.4 datetime

优先用 `YYYY-MM-DD HH:mm:ss` 字符串，这是最稳妥的写法，也和常见 API 输出更容易对齐。不要写相对时间（如“明天上午”）。

```json
{
    "截止时间": "2026-03-24 10:00:00"
}
```

### 2.5 checkbox

用 JSON boolean：`true` 或 `false`，不要用 `"true"`、`"是"`、`1`。

```json
{
    "已完成": true
}
```

### 2.6 user / group_chat

用对象数组，元素至少包含 `id`。人员字段传用户 ID（如 `ou_xxx`），群字段传群 ID（如 `oc_xxx`）；单值/多值都统一使用数组。

> **人员字段：不要猜 ID。** 不知道 `open_id` 时，先用 `lark-contact` 查 id：`lark-cli contact +search-user --query "<姓名/邮箱/手机号>" --as user`。

> **群组字段：不要猜 ID。** 不知道 `chat_id` 时，先用 `lark-im` 搜群：`lark-cli im +chat-search --query "<群名关键词>" --as user`；取结果里的 `oc_xxx`。

```json
{
    "负责人": [
      { "id": "ou_xxx" },
      { "id": "ou_xxx2" }
    ],
    "协作群": [
      { "id": "oc_xxx" }
    ]
}
```

### 2.7 link

用对象数组，元素包含 `id`，值为目标记录的 `record_id`。不要传记录标题；先用 `+record-list` / `+record-search` 找到目标记录 ID。

```json
{
    "关联任务": [
      { "id": "<record_id>" }
    ]
}
```

### 2.8 location

用对象 `{lng, lat}`，两者都是数字；`lng` 是经度，`lat` 是纬度。

```json
{
    "坐标": {
      "lng": 116.397428,
      "lat": 39.90923
    }
}
```

### 2.9 attachment（不作为普通 CellValue 写入）

用户要把本地文件加到记录里时，必须使用 `lark-cli base +record-upload-attachment --file <path>` 上传到已有记录。不能用普通记录操作接口来上传附件。

`+record-get` 返回的附件字段单元格包含 `file_token` 和文件名，可以把 `file_token` 交给 `lark-cli docs +media-download` 进行附件下载。

## 3. 只读字段（不要写）

以下字段在写记录时应视为只读：
- `auto_number`
- `lookup`
- `formula`
- `created_at` / `updated_at`
- `created_by` / `updated_by`

写入只读字段通常不会更新数据；返回里可能出现 `ignored_fields`，reason 会说明 `READONLY`。看到这种返回时，不要重试同一 payload，应移除只读字段，只写存储字段。

## 4. 完整示例

```json
{
    "标题": "Created from shortcut",
    "状态": "Todo",
    "标签": ["高优", "外部依赖"],
    "工时": 8,
    "截止时间": "2026-03-24 10:00:00",
    "已完成": false,
    "负责人": [{ "id": "ou_123" }],
    "关联任务": [{ "id": "rec_456" }],
    "坐标": { "lng": 116.397428, "lat": 39.90923 }
}
```
