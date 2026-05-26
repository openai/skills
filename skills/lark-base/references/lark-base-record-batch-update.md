# base +record-batch-update (batch update)

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

批量更新记录（将同一份 `patch` 批量应用到一批 `record_id_list`）。

## 推荐命令

```bash
lark-cli base +record-batch-update --base-token <base_token> --table-id <table_id> \
  --json '{"record_id_list":["<record_id>"],"patch":{"状态":"完成"}}'

lark-cli base +record-batch-update --base-token <base_token> --table-id <table_id> --json @batch-update.json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-token <token>` | 是 | Base Token |
| `--table-id <id_or_name>` | 是 | 表 ID 或表名 |
| `--json <body>` | 是 | 批量更新请求体，必须是 JSON 对象。支持直接传 JSON 字符串，或 `@<file_path>` 从文件读取 |

## API

`POST /open-apis/base/v3/bases/:base_token/tables/:table_id/records/batch_update`

## `--json` 结构

本节只说明 `+record-batch-update` 的外层 JSON 形状；CellValue 统一看 [lark-base-cell-value.md](lark-base-cell-value.md)。

对象形态：`{"record_id_list":[...],"patch":{...}}`。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `record_id_list` | `string[]` | 是 | 要更新的记录 ID 列表（单次最多 200 条） |
| `patch` | `Map<FieldNameOrID, CellValue>` | 是 | 字段更新对象；key 是字段名或字段 ID，value 是 `CellValue`；同一份 `patch` 会应用到 `record_id_list` 内所有记录 |

## 返回重点

返回 `record_id_list`、`update`，可选返回 `ignored_fields`；`update` 可能为空对象。

## 坑点

- 这是“同值批量更新”：所有 `record_id_list` 都应用同一份 `patch`。
- `record_id_list` 最大 200 条，超过会被接口校验拒绝。
- 命令不会自动做字段/行映射转换，传什么就发什么。
- 如果 `patch` 包含只读字段，返回里可能出现 `ignored_fields`；这些字段不会被更新。

## 参考

- [lark-base-record.md](lark-base-record.md) — record 索引页
- [lark-base-cell-value.md](lark-base-cell-value.md) — CellValue 格式规范
