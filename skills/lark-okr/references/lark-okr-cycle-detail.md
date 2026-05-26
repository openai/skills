# okr +cycle-detail

> **前置条件：** 先阅读 [`lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

列出指定 OKR 周期下的所有目标及其关键结果。

## 推荐命令

```bash
# 列出指定周期的目标和关键结果
lark-cli okr +cycle-detail --cycle-id 1234567890123456789

# 预览 API 调用而不实际执行
lark-cli okr +cycle-detail --cycle-id 1234567890123456789 --dry-run
```

## 参数

| 参数           | 必填 | 默认值    | 说明                                      |
|--------------|----|--------|-----------------------------------------|
| `--cycle-id` | 是  | —      | OKR 周期 ID（int64 类型）。从 `+cycle-list` 获取。 |
| `--dry-run`  | 否  | —      | 预览 API 调用而不实际执行。                        |
| `--format`   | 否  | `json` | 输出格式。                                   |

## 工作流程

1. 使用 `lark-cli okr +cycle-list` 获取 OKR 周期 ID。
2. 执行 `lark-cli okr +cycle-detail --cycle-id "123456"`。
3. 报告结果：找到的目标数量、每个目标的 ID、分数、权重及其关键结果。

## 输出

返回 JSON：

```json
{
  "cycle_id": "1234567890123456789",
  "objectives": [
    {
      "id": "2345678901234567890",
      "create_time": "2025-01-01 00:00:00",
      "update_time": "2025-01-15 12:00:00",
      "owner": {
        "owner_type": "user",
        "user_id": "ou_xxx"
      },
      "cycle_id": "1234567890123456789",
      "position": 0,
      "score": 0.75,
      "weight": 1.0,
      "deadline": "2025-06-30 23:59:59",
      "category_id": "cat_456",
      "content": "{...}",
      "notes": "{...}",
      "key_results": [
        {
          "id": "3456789012345678901",
          "create_time": "2025-01-01 00:00:00",
          "update_time": "2025-01-15 12:00:00",
          "owner": {
            "owner_type": "user",
            "user_id": "ou_xxx"
          },
          "objective_id": "2345678901234567890",
          "position": 0,
          "score": 0.8,
          "weight": 0.5,
          "deadline": "2025-06-30 23:59:59",
          "content": "{...}"
        }
      ]
    }
  ],
  "total": 1
}
```

其中，content 和 notes 字段是 JSON 字符串，为 OKR ContentBlock
富文本格式。请参考 [lark-okr-contentblock.md](lark-okr-contentblock.md) 了解详细信息。

## 参考

- [lark-okr](../SKILL.md) -- 所有 OKR 命令(shortcut 和 API 接口)
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
