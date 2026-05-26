# okr +cycle-list

> **前置条件：** 先阅读 [`lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

列出指定用户的 OKR 周期，支持可选的时间范围过滤。

## 推荐命令

```bash
# 列出用户的所有周期
lark-cli okr +cycle-list --user-id "ou_xxx"

# 使用特定的用户 ID 类型列出周期
lark-cli okr +cycle-list --user-id "xxx" --user-id-type user_id

# 列出时间范围内的周期（例如 2025-01 到 2025-06）
lark-cli okr +cycle-list --user-id "ou_xxx" --time-range "2025-01--2025-06"

# 预览 API 调用而不实际执行
lark-cli okr +cycle-list --user-id "ou_xxx" --dry-run
```

## 参数

| 参数               | 必填 | 默认值       | 说明                                                               |
|------------------|----|-----------|------------------------------------------------------------------|
| `--user-id`      | 是  | —         | OKR 所有者的用户 ID                                                    |
| `--user-id-type` | 否  | `open_id` | 用户 ID 类型：`open_id` \| `union_id` \| `user_id`                    |
| `--time-range`   | 否  | —         | 按时间范围过滤周期。格式：`YYYY-MM--YYYY-MM`（例如 `2025-01--2025-06`）。留空获取所有周期。 |
| `--dry-run`      | 否  | —         | 预览 API 调用而不实际执行。                                                 |
| `--format`       | 否  | `json`    | 输出格式。                                                            |

## 工作流程

1. 获取目标用户的 `open_id`（或其他 ID 类型）。如果用户说"我的 OKR 周期"，先通过 `lark-cli contact +get-user` 获取当前用户的
   ID。
2. 执行 `lark-cli okr +cycle-list --user-id "ou_xxx"`，可选择使用 `--time-range`。
3. 报告结果：找到的周期数量、每个周期的 ID、开始/结束时间和状态。

## 输出

返回 JSON：

```json
{
  "cycles": [
    {
      "id": "1234567890123456789",
      "create_time": "2025-01-01 00:00:00",
      "update_time": "2025-01-01 00:00:00",
      "tenant_cycle_id": "789",
      "owner": {
        "owner_type": "user",
        "user_id": "ou_xxx"
      },
      "start_time": "2025-01-01 00:00:00",
      "end_time": "2025-06-30 00:00:00",
      "cycle_status": "normal",
      "score": 0
    }
  ],
  "total": 1
}
```

在这个周期信息中，这些字段值得关注：

- `id` 是这个周期的 ID，你通常需要用它在之后使用 `okr +cycle-detail` 获取 OKR 内容详情
- `start_time` `end_time` 是周期的起止时间，总是从某个月1日开始，直到此月或之后某月的最后一日结束。
    - 在 OKR 系统中，我们只关注这个时间的年月部分，如 “2025-01-01开始，2025-06-30结束” 的周期被称作 “2025 年 1-6 月” 周期，而
      “2025-01-01开始，2025-01-31结束” 的周期被称作 “2025 年 1 月”周期。
    - 如果一个周期从某年1月1日开始，某年12月31日结束，则它是这一年的年度周期，如 “2025-01-01开始，2025-12-31结束” 的周期就是
      “2025 年” 的年度周期
- `cycle_status` 为周期状态值，参见下文。

### 周期状态值

| 值         | 说明       |
|-----------|----------|
| `default` | 默认状态 (0) |
| `normal`  | 生效 (1)   |
| `invalid` | 失效 (2)   |
| `hidden`  | 隐藏 (3)   |

在 OKR 系统中，default/normal 状态下的周期当前正常生效，invalid 状态下的周期已失效但通常仍然可以填写，hidden 状态下的周期隐藏不可见。

## 参考

- [lark-okr](../SKILL.md) -- 所有 OKR 命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
