---
name: fb-ads-report
description: Format Facebook ads guard outputs into concise operator reports. Use when the user asks for FB Ads Guard reports, BM coverage summaries, pause suggestions, watch lists, data limitations, Feishu-ready markdown, or account-level monitoring summaries.
---

# FB Ads Report

## Purpose

Use this skill after scope, metrics, and rule evaluation. It creates concise operator-facing reports. It does not collect browser data, evaluate new rules, send Feishu messages, or execute delivery changes.

Use `$feishu-report` only after this skill has produced the report text or file.

## Required Sections

1. Header:
   - check time
   - BM/business name and ID
   - account scope
   - mode: read-only, semi-auto, or emergency
   - whether actions were executed
2. Coverage summary:
   - expected accounts
   - checked accounts
   - accounts with active delivery
   - accounts with spend today
   - pause suggestions
   - watch suggestions
   - coverage status
3. Account table.
4. Pause suggestions.
5. Watch suggestions.
6. Data source and limitations.
7. Action audit when any action was executed.

## Feishu Report Layout

Use a compact, fixed order so the report is readable in Feishu:

```text
FB投放风控 | 数据检查
时间：
BM：
范围：
模式：只读 / 未执行关闭、暂停、编辑、发布

一、总览
账号：已检查/应检查
消耗：
结果：
回收：
异常：
数据状态：

二、账号汇总
日期 | 账号 | 消耗 | 结果 | 回收 | 展示 | 数据状态

三、异常/需复核
- 只列有问题的账号：数据冲突、缺回收列、导出失败、覆盖不完整、疑似旧文件。

四、数据来源
- 每个账号列出 CSV 文件名或 UI total。
- 明确写出被拒绝的旧文件/错层级文件。

五、操作审计
- 只读：未执行关闭/暂停/编辑/发布。
```

Keep the Feishu message short. Put full row-level details in an attached/linked markdown file only when needed.

If any metric is derived from a fallback source, mark it in the account table. Do not mix CSV and UI totals silently.

## Account Table

```text
Account | Account ID | Status | Row count | Active rows | Today spend | Results | Decision | Reason
```

Always include:

- `no_active_delivery`
- `no_today_spend`
- `scheduled_only`
- `disabled_account`
- `inaccessible_account`
- `data_unavailable`
- `data_conflict`

These rows prove the account was checked rather than forgotten.

## Decision Language

- `pause_recommended`: one or more explicit thresholds were violated.
- `watch`: spend exists but no safe pause rule triggered.
- `no_pause`: checked successfully and no rule triggered.
- `no_active_delivery`: no active Campaign/Ad Set/Ad rows found.
- `skipped`: account could not or should not be checked.
- `data_conflict`: source totals disagree or the export failed validation; do not make pause decisions from it.

## Feishu Style

- Keep the top summary short.
- Put counts before detail.
- Include every account in multi-account checks.
- State "未执行关闭/暂停/编辑/发布" when the run is read-only.
- Do not include full webhook URLs.
- Avoid long raw dumps. Use one summary table plus a short problem list.
- Show recovery explicitly as a column. If unavailable, write `缺失` instead of leaving it blank.

## Output

Create markdown suitable for direct chat, file storage, or `$feishu-report`.
