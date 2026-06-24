# okr +progress-update

> **前置条件：** 先阅读 [`lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新指定 ID 的 OKR 进展记录内容。

## 推荐命令

```bash
# 更新进展记录内容
lark-cli okr +progress-update \
  --progress-id 1234567890123456789 \
  --content '{"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[{"paragraph_element_type":"textRun","text_run":{"text":"更新后的进展内容"}}]}}]}'

# 更新进展记录内容并同时更新进度
lark-cli okr +progress-update \
  --progress-id 1234567890123456789 \
  --content '{"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[{"paragraph_element_type":"textRun","text_run":{"text":"进度已更新至 90%"}}]}}]}' \
  --progress-percent 90 \
  --progress-status normal

# 从文件读取 content（适用于较长的进展内容）
lark-cli okr +progress-update \
  --progress-id 1234567890123456789 \
  --content @updated_progress.json

# 预览 API 调用而不实际执行
lark-cli okr +progress-update \
  --progress-id 1234567890123456789 \
  --content '{"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[{"paragraph_element_type":"textRun","text_run":{"text":"test"}}]}}]}' \
  --dry-run
```

## 参数

| 参数                   | 必填 | 默认值       | 说明                                                                                                             |
|----------------------|----|-----------|----------------------------------------------------------------------------------------------------------------|
| `--progress-id`      | 是  | —         | 进展记录 ID（int64 类型，正整数）                                                                                          |
| `--content`          | 是  | —         | 进展内容，ContentBlock JSON 格式。支持 `@文件路径` 从文件读取。请参考 [ContentBlock 格式](lark-okr-contentblock.md)。                    |
| `--progress-percent` | 否  | —         | 进度百分比(-99999999999 - 99999999999)。百分比的取值通常在 0-100，但允许超过此范围，以表示超额完成或负增长等情况。挂载的目标或关键结果的量化指标不使用百分比单位时，以这个字段更新当前值。系统内最多保留两位小数 |
| `--progress-status`  | 否  | —         | 进度状态：`normal`（正常） \| `overdue`（逾期） \| `done`（已完成）。仅在指定 `--progress-percent` 时生效。                               |
| `--user-id-type`     | 否  | `open_id` | 用户 ID 类型：`open_id` \| `union_id` \| `user_id`                                                                  |
| `--dry-run`          | 否  | —         | 预览 API 调用而不实际执行。                                                                                               |
| `--format`           | 否  | `json`    | 输出格式。                                                                                                          |

## 工作流程

1. 使用 `+progress-get` 获取要更新的进展记录的 ID 和当前内容。
2. 修改 ContentBlock JSON 格式的进展内容。请参考 [ContentBlock 格式](lark-okr-contentblock.md)。
3. 执行 `lark-cli okr +progress-update --progress-id "..." --content "..."`。
4. 报告结果：更新后的进展记录 ID、修改时间、进度百分比等。

## 输出

返回 JSON：

```json
{
  "progress": {
    "progress_id": "1234567890123456789",
    "modify_time": "2025-01-15 14:30:00",
    "content": "{...}",
    "progress_rate": {
      "percent": 90.0,
      "status": "normal"
    }
  }
}
```

其中：

- `content` 字段是 JSON 字符串，为 OKR ContentBlock
  富文本格式。请参考 [lark-okr-contentblock.md](lark-okr-contentblock.md) 了解详细信息。
- `progress_rate.status` 返回可读字符串：`normal`（正常）、`overdue`（逾期）、`done`（已完成）。

## 参考

- [lark-okr](../SKILL.md) -- 所有 OKR 命令(shortcut 和 API 接口)
- [ContentBlock 格式](lark-okr-contentblock.md) -- 进展内容使用的富文本格式
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
