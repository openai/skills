---
name: fb-ads-guard
description: Orchestrate safe Facebook/Meta Ads Manager guardrail workflows after an operator is already logged in. Use when the user asks for BM-wide ad monitoring, read-only spend checks, pause recommendations, semi-auto ad set pauses, emergency shutdown planning, permission gates, audit output, or a minimal scaffold for FB ads spend guards. For detailed account scope, metrics reading, rule evaluation, delivery closure, and reporting, coordinate with fb-ads-scope, fb-ads-metrics-reader, fb-ads-rules, fb-ads-delivery-closer, and fb-ads-report.
---

# FB Ads Guard

## Role

Use this skill as the top-level coordinator for FB Ads Manager safety workflows. It decides which sub-skills are needed, keeps the action boundary safe, and produces an operator-ready outcome.

Login and 2FA are out of scope unless the user explicitly asks. Prefer Meta Marketing API when available. When the user specifically asks for Computer Use, use it as the page operator while keeping scope, decisions, permissions, and audit outside the browser UI.

## Sub-Skills

- `$fb-ads-scope`: enumerate BM/business portfolio accounts and prove coverage.
- `$fb-ads-metrics-reader`: collect Ads Manager metrics by CSV/copy/UI without changing delivery.
- `$fb-ads-rules`: evaluate spend, CPA, conversion, recovery, and anomaly rules.
- `$fb-ads-delivery-closer`: execute explicitly authorized pause/turn-off operations with Computer Use verification and audit evidence.
- `$fb-ads-report`: format the final coverage, recommendations, limitations, and audit.
- `$feishu-report`: send the final report when the user asks for Feishu delivery.

If a sub-skill is unavailable in the current session, follow the same boundaries manually and say which part is being handled inline.

## Operating Principles

- Default to read-only unless the user explicitly authorizes actions.
- Control normal spend risk at the Ad Set level.
- Use Campaign-level pause only with explicit confirmation.
- Pause only by default; do not auto-resume or increase budgets.
- Use CSV export or copied table data before UI reading; avoid screenshot OCR as the primary data source.
- Never hide recovery data. First select recovery fields through Ads Manager custom columns and re-export. Only after that attempt fails may recovery be marked `custom_column_failed` or `external_recovery_required`.
- Never pause based on missing recovery, missing CPA, inferred budgets, or ambiguous object identity.
- Treat BM/business scope as all accounts under that BM, not just the accounts visible in the current Ads Manager selector; include every requested/discovered account in reports.
- Screenshot before and after every operation that changes delivery.
- Any delivery change must be delegated to `$fb-ads-delivery-closer`; this guard skill may prepare inputs and permission decisions, but must not inline toggle delivery.
- Stop rather than guessing when search results are ambiguous, names do not match, or the UI state is unclear.

## Preflight

Before any workflow that depends on Computer Use:

- Run one harmless Computer Use check such as `get_app_state` or `list_apps` against the target browser/session.
- If Computer Use returns an app-server, MCP, connection, timeout, or unavailable error, stop immediately with `computer_use_unavailable`.
- Do not read old CSV files, do not infer fresh data from previous runs, and do not send a normal Feishu data report when preflight fails.
- Send a Feishu failure notice only when the user explicitly asks to notify in the current turn; do not send repeated identical failure reports.
- Include the exact preflight error, time, and required operator action in the blocker summary.

## Main Workflows

### Read-Only BM Check

Use when the user says "只读", "检查", "生成建议", "不要关闭", or asks to send a report.

```text
fb-ads-guard
  -> fb-ads-scope
  -> fb-ads-metrics-reader
  -> fb-ads-rules
  -> fb-ads-report
  -> feishu-report, when requested
```

Rules:

- Do not pause, close, edit, publish, resume, or change budget.
- It is allowed to navigate, switch accounts, set date ranges, export CSV, save files, and read page totals.
- It is allowed and expected to open `Columns` / `Columns: Custom` to select recovery fields before export. This is read-only and should be done per account when recovery columns are not visible.
- Account discovery must prefer Business Settings/API/configured inventory; selector-visible accounts alone are partial discovery unless reconciled.
- Final report must include quiet/empty accounts as checked rows.

#### Recovery Columns Gate

Before exporting CSV for an Ads Manager metrics report that includes `回收`, verify the visible/exported columns contain a recovery source. Do not rely on the default `Performance` preset.

Required read-only sequence:

1. Open `Columns: ...`.
2. Open `Customize columns`.
3. Search/select at least one purchase recovery value field, preferring `Purchases conversion value`. If the account uses another locale or event setup, acceptable equivalents include purchase conversion value, purchase value, website purchase conversion value, or ROAS fields that clearly represent purchase return.
4. Apply the customized columns before exporting.
5. Export fresh CSV for the same account, level, and date range.
6. Parse the fresh CSV and confirm the recovery column is present before totals are reported.

If the recovery field cannot be selected or the fresh CSV still lacks recovery columns:

- Mark that account `回收列自定义失败` or `外部回收待合并`.
- Keep `回收` as `待复核`.
- List the exact account and failed step under exceptions.
- Do not send a normal "all CSV verified" Feishu report.

### Semi-Auto Pause

Use when the user authorizes pause recommendations or limited automatic pauses.

```text
fb-ads-guard
  -> fb-ads-scope
  -> fb-ads-metrics-reader
  -> fb-ads-rules
  -> permission check
  -> fb-ads-delivery-closer
  -> fb-ads-report
  -> feishu-report, when requested
```

Default permission matrix:

```text
auto_pause_adset: default false; allowed only with current-turn authorization, explicit thresholds, and exact object match
emergency_pause_ad: default false; allowed only with current-turn authorization and configured emergency package events
emergency_pause_adset: default false; allowed only with current-turn authorization and configured emergency package events
emergency_pause_campaign: confirmation required
auto_resume: forbidden
auto_increase_budget: forbidden
```

Default action limits:

```text
single_run_routine_pause_limit: 5
single_run_emergency_ad_limit: 50
cooldown: 6 hours per object
```

### Emergency Shutdown

Use for app removal, package unavailability, payment outage, landing page failure, product bugs, creative/compliance risk, or explicit operator emergency command.

Require stable mapping before automation:

```yaml
packages:
  com.example.app:
    account_ids:
      - act_xxx
    campaign_name_patterns:
      - com.example.app
    adset_name_patterns:
      - com.example.app
    ad_name_patterns:
      - com.example.app
    landing_url_patterns:
      - example.com/app
```

If package mapping is incomplete or search results are ambiguous, produce a manual-confirmation report instead of pausing.

When emergency shutdown is authorized and package mapping is stable, route the actual delivery change through `$fb-ads-delivery-closer`:

```text
fb-ads-guard
  -> fb-ads-scope
  -> fb-ads-metrics-reader, when metrics or today-spend filters are needed
  -> fb-ads-rules, when rule recommendations are needed
  -> permission gate
  -> fb-ads-delivery-closer
  -> fb-ads-report
  -> feishu-report, when requested
```

## Inputs to Clarify

Clarify only when the answer cannot be inferred safely:

```yaml
mode: read_only | semi_auto | emergency
scope: current_account | selected_accounts | business_all_accounts
level: campaign | adset | ad
date_range: today | yesterday | custom
target_cpa: null
daily_cap: null
min_roas: null
min_payback: null
recovery_source: ads_manager | external_bi | unavailable
report_destination: chat | file | feishu
```

If thresholds are missing, continue the read-only check and return `watch` rather than `pause_recommended`.

## Standard Output

Every multi-account run should end with:

```text
Expected accounts
Checked accounts
Accounts with active delivery
Accounts with spend today
Pause suggestions
Watch suggestions
Coverage status
```

Then list every account:

```text
Account | Account ID | Status | Row count | Active rows | Today spend | Results | Decision | Reason
```

For actions, add an audit row:

```text
event_time
actor/source
business_id
account_id
object_level
object_id/name
before_status
after_status
rule
reason
result
screenshots
```

## Implementation Scaffold

When the user asks for implementation shape or code scaffold, read `references/minimal_code_structure.md`.
