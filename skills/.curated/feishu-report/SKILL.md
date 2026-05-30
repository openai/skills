---
name: feishu-report
description: Send structured reports to a configured Feishu custom bot webhook. Use when the user asks to push FB Ads guard results, execution summaries, monitoring reports, or pause suggestions to Feishu without involving business application projects.
---

# Feishu Report

## Purpose

Use this skill to send concise report text to the configured Feishu bot.

This skill is standalone. Do not call AutoArk, app backends, or project-local Feishu integrations.

## Workflow

1. Read config from `.env` in this skill directory.
2. Include `FEISHU_KEYWORD` in the message when configured.
3. Before sending user, account, campaign, ad set, or spend data, confirm the destination unless the user explicitly asked to send or test in the current turn.
4. For FB Ads Guard / FB Ads Manager reports, normalize the content with the Feishu template below before sending.
5. Send with `scripts/send_feishu.py`.
6. Report only whether Feishu accepted the message; do not print the full webhook URL.

## FB Ads Guard Feishu Template

Use this fixed layout for FB Ads Guard, FB Ads Manager metrics, pause suggestions, closure summaries, or BM monitoring reports. Keep it compact and readable in Feishu.

```text
FB投放风控 | 数据检查
时间：
BM：
范围：
模式：只读 / 执行关闭 / 执行暂停
操作：未执行关闭/暂停/编辑/发布

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
- 只列有问题的账号：数据冲突、回收列自定义失败、后台回收待合并、导出失败、覆盖不完整、疑似旧文件。

四、数据来源
- 每个账号列出 CSV 文件名或 UI total。
- 明确写出被拒绝的旧文件/错层级文件。

五、操作审计
- 只读：未执行关闭/暂停/编辑/发布。
- 执行模式：列出已操作账号、层级、对象数量、结果。
```

Rules for FB Ads messages:

- The top summary must fit in the first screen of Feishu.
- If Computer Use preflight fails, send only a blocker report when the user explicitly requested Feishu notification in the current turn; do not send a normal data report or repeated duplicate failure notices.
- Always include `回收` as its own column. If unavailable after custom-column retry, write `待复核`; do not leave it blank.
- Always include `数据状态`: `CSV已校验`, `UI读取`, `回收列自定义失败`, `后台回收待合并`, `数据冲突`, `导出失败`, or `覆盖不完整`.
- Do not mark recovery missing before trying Ads Manager custom columns. First select recovery fields, re-export, and only then use `回收列自定义失败` if the export still lacks recovery.
- Do not send raw row dumps unless the user explicitly asks for full details.
- Do not mix old CSV, wrong account, wrong date, or wrong level data into totals.
- If a source was rejected, include it under `四、数据来源`.
- In read-only runs, explicitly write `未执行关闭/暂停/编辑/发布`.
- In execution runs, include an operation audit; never imply an action happened without listing the object count and result.

## Commands

Send direct text:

```bash
python3 /Users/niqiao/.codex/skills/feishu-report/scripts/send_feishu.py --title "FB投放风控 汇报" --text "..."
```

Send a report file:

```bash
python3 /Users/niqiao/.codex/skills/feishu-report/scripts/send_feishu.py --file report.md
```

## Config

`.env` supports:

```bash
FEISHU_WEBHOOK_URL=...
FEISHU_KEYWORD=FB投放风控
```
