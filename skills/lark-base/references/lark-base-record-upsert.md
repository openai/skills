# base +record-upsert

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

创建记录，或在带 `--record-id` 时更新记录。

## 推荐命令

```bash
# 创建记录
lark-cli base +record-upsert --base-token <base_token> --table-id <table_id> \
  --json '{"项目名称":"Apollo","状态":"进行中"}'

# 更新记录
lark-cli base +record-upsert --base-token <base_token> --table-id <table_id> --record-id <record_id> \
  --json '{"项目名称":"Apollo","状态":"完成","完成时间":"2026-03-24 10:00:00"}'
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-token <token>` | 是 | Base Token |
| `--table-id <id_or_name>` | 是 | 表 ID 或表名 |
| `--record-id <id>` | 否 | 传入时走更新，不传时走创建 |
| `--json <body>` | 是 | 字段写入对象，类型 `Map<FieldNameOrID, CellValue>` |

## API

- 创建：`POST /open-apis/base/v3/bases/:base_token/tables/:table_id/records`
- 更新：带 `--record-id` 时改走 `PATCH /records/:record_id`

## `--json` 结构

- `--json` 必须是 **JSON object map**，形状是 `Map<FieldNameOrID, CellValue>`。
- key 是字段名或字段 ID；value 是该字段的 `CellValue`。
- 一次请求里同一字段只用一种标识，避免重复写入冲突。
- 写入前先 `+field-list` 确认字段类型和字段名/ID。
- CellValue 统一看 [lark-base-cell-value.md](lark-base-cell-value.md)。

```json
{
  "项目名称": "Apollo",
  "状态": "进行中",
  "完成时间": "2026-03-24 10:00:00"
}
```

## 返回重点

- 创建时返回 `record` 和 `created: true`。
- 更新时返回 `record` 和 `updated: true`。
- 如果写入了 `formula / lookup / created_at / updated_at / created_by / updated_by` 等只读字段，返回里可能出现 `ignored_fields`，这些字段不会被更新。

## 坑点

- 有 `--record-id` 就一定更新；不传就一定创建，不会自动查重或按业务键 upsert。
- select 写入未知选项时平台可能自动新增选项；如果不是要新增选项，先用 `+field-list` / `+field-search-options` 确认真实选项名。
- 这是写入操作，执行前必须确认目标表和字段。

## 参考

- [lark-base-record.md](lark-base-record.md) — record 索引页
- [lark-base-cell-value.md](lark-base-cell-value.md) — CellValue 格式规范
