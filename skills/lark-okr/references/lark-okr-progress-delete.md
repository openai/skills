# okr +progress-delete

> **前置条件：** 先阅读 [`lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

根据 ID 删除一条 OKR 进展记录。此操作为高风险操作，删除后不可恢复。

## 推荐命令

```bash
# 删除指定 ID 的进展记录
lark-cli okr +progress-delete --progress-id 1234567890123456789

# 预览 API 调用而不实际执行
lark-cli okr +progress-delete --progress-id 1234567890123456789 --dry-run
```

## 参数

| 参数              | 必填 | 默认值    | 说明                    |
|-----------------|----|--------|-----------------------|
| `--progress-id` | 是  | —      | 进展记录 ID（int64 类型，正整数） |
| `--dry-run`     | 否  | —      | 预览 API 调用而不实际执行。      |
| `--format`      | 否  | `json` | 输出格式。                 |

## 工作流程

1. 使用 `+progress-get` 确认要删除的进展记录 ID 和内容。
2. 执行 `lark-cli okr +progress-delete --progress-id "1234567890123456789"`。
3. 报告结果：已删除的进展记录 ID。

> **注意**：此操作不可恢复，建议在删除前先用 `+progress-get` 确认记录内容。

## 输出

返回 JSON：

```json
{
  "deleted": true,
  "progress_id": "1234567890123456789"
}
```

## 参考

- [lark-okr](../SKILL.md) -- 所有 OKR 命令(shortcut 和 API 接口)
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
