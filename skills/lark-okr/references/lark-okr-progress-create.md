# okr +progress-create

> **前置条件：** 先阅读 [`lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

为目标（Objective）或关键结果（Key Result）创建一条 OKR 进展记录。

## 推荐命令

```bash
# 为目标创建进展记录
lark-cli okr +progress-create \
  --content '{"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[{"paragraph_element_type":"textRun","text_run":{"text":"本周完成了核心模块开发"}}]}}]}' \
  --target-id 1234567890123456789 \
  --target-type objective

# 为关键结果创建进展记录（带进度百分比和状态）
lark-cli okr +progress-create \
  --content '{"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[{"paragraph_element_type":"textRun","text_run":{"text":"指标已达到 80%"}}]}}]}' \
  --target-id 2345678901234567891 \
  --target-type key_result \
  --progress-percent 80 \
  --progress-status done

# 从文件读取 content（适用于较长的进展内容）
lark-cli okr +progress-create \
  --content @progress_content.json \
  --target-id 1234567890123456789 \
  --target-type objective
```

## 参数

| 参数                   | 必填 | 默认值                   | 说明                                                                                                                                   |
|----------------------|----|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `--content`          | 是  | —                     | 进展内容，ContentBlock JSON 格式。支持 `@文件路径` 从文件读取。请参考 [ContentBlock 格式](lark-okr-contentblock.md)。                                          |
| `--target-id`        | 是  | —                     | 目标 ID 或关键结果 ID（int64 类型，正整数）                                                                                                         |
| `--target-type`      | 是  | —                     | 目标类型：`objective` \| `key_result`                                                                                                     |
| `--progress-percent` | 否  | —                     | 进度百分比(-99999999999 - 99999999999)。百分比的取值通常在 0-100，但允许超过此范围，以表示超额完成或负增长等情况。挂载的目标或关键结果的量化指标不使用百分比单位时，以这个字段更新当前值。系统内最多保留两位小数            |
| `--progress-status`  | 否  | —                     | 进度状态：`normal`（正常） \| `overdue`（逾期） \| `done`（已完成）。仅在指定 `--progress-percent` 时生效。                                                     |
| `--source-title`     | 否  | `created by lark-cli` | 来源标题，用于在 OKR 界面中显示进展来源                                                                                                               |
| `--source-url`       | 否  | 根据品牌自动生成              | 来源 URL，用于在 OKR 界面中显示进展来源链接，通常可以填写 OKR 编写信息来源的文档链接等。飞书品牌默认为 `https://open.feishu.cn/app`, Lark 品牌默认为 `https://open.larksuite.com/app` |
| `--user-id-type`     | 否  | `open_id`             | 用户 ID 类型：`open_id` \| `union_id` \| `user_id`                                                                                        |
| `--dry-run`          | 否  | —                     | 预览 API 调用而不实际执行。                                                                                                                     |
| `--format`           | 否  | `json`                | 输出格式。                                                                                                                                |

## 工作流程

1. 使用 `+cycle-list` 和 `+cycle-detail` 获取目标或关键结果的 ID。
2. 构造 ContentBlock JSON 格式的进展内容。请参考 [ContentBlock 格式](lark-okr-contentblock.md)。
3. 执行 `lark-cli okr +progress-create --content "..." --target-id "..." --target-type objective`。
4. 报告结果：新创建的进展记录 ID、修改时间等。

## 输出

返回 JSON：

```json
{
  "progress": {
    "progress_id": "1234567890123456789",
    "modify_time": "2025-01-15 10:30:00",
    "content": "{...}",
    "progress_rate": {
      "percent": 80.0,
      "status": "done"
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
