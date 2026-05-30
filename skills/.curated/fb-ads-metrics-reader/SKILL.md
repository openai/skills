---
name: fb-ads-metrics-reader
description: Read Facebook Ads Manager metrics safely without changing delivery. Use when the user asks to inspect Ads Manager data, export CSV, read spend/results/budget/impressions/delivery, collect ad set metrics, gather read-only inputs for FB ads guard reports, or query metrics for all ad accounts under the current BM/business portfolio.
---

# FB Ads Metrics Reader

## Purpose

Use this skill to collect Ads Manager data only. It can discover accounts under the current BM, navigate, switch accounts, choose object level, set date ranges, export CSV, copy table data, and read UI totals. It must not decide whether to pause or change any campaign, ad set, or ad.

When the user says BM, business portfolio, all accounts, or does not clearly restrict the request to the current ad account, query metrics for every ad account under the current BM. Do not treat the currently selected ad account as the whole BM.

## Preferred Data Sources

1. Ads Manager CSV export.
2. Copied table data.
3. UI totals and visible rows.
4. Screenshot reading only as a last resort, and never as the primary source when export/copy is available.

## Data Correctness Requirements

Treat every exported file as untrusted until it passes validation. Never reuse an existing CSV just because the filename looks close.

Before parsing any CSV, verify and record:

- `account_id` and account name match the account currently being checked.
- `level` matches the requested object level. If the request is Ad sets, do not substitute Campaigns unless explicitly marked as a fallback and explained.
- `date_range` in the CSV rows matches the requested range or the explicitly recorded applied range when Meta normalizes a relative date selector.
- `date_range` shown by the UI after applying the selector matches the intended range. Meta may normalize relative ranges such as "last 30 days" to completed dates; record the UI-displayed dates and use them in the final output.
- `export_time` is from the current run, or the file was intentionally selected by the user.
- Required metric columns exist: `Amount spent`, `Results`, `Budget`, `Impressions`.
- Recovery columns were explicitly selected or attempted through `Columns: Custom` before export. Do not accept a CSV without recovery columns as final until one custom-column retry has been attempted.
- Final recovery status is explicit: `available`, `custom_column_failed`, or `external_recovery_required`.

Cross-check after parsing:

- Compare parsed spend/results/impressions/recovery against the visible UI row or total whenever the UI exposes those values.
- If CSV totals and UI-visible totals differ materially, stop and mark `data_conflict` instead of reporting the number.
- If the only available file is stale, partial, missing required columns, or has a different level/date/account, do not use it for totals. Export again or mark `export_failed`.
- Keep stale/invalid file paths in `limitations` so the operator can see what was rejected.

## Workflow

### Computer Use Preflight

When the collection path uses Computer Use:

- Run one harmless `get_app_state` or `list_apps` check before touching Ads Manager.
- If the check fails with an app-server, MCP, connection, timeout, or unavailable error, stop with `computer_use_unavailable`.
- Do not parse stale downloads, do not reuse prior CSVs, and do not report totals from previous runs after a preflight failure.
- Record the exact error in `limitations` and require the operator to restart/reconnect Codex Computer Use before retrying.

### Account Discovery

Before reading metrics, determine account scope:

- `current_account`: only when the user explicitly says current account or one selected account.
- `business_all_accounts`: default when the user says BM/business/all accounts, or when current BM context is implied.

For `business_all_accounts`, use `$fb-ads-scope` when available. If working inline, build the account list from the strongest available source:

1. Meta Marketing API or configured account inventory, when available.
2. Business Settings > Ad accounts for the current BM.
3. Ads Manager account selector only as fallback.

If only selector-visible accounts are available and they are not reconciled against an expected count, configured inventory, API, or Business Settings, set `coverage_status: partial_ui_discovery`.

### Metric Collection

For each discovered account:

1. Open Ads Manager for the account.
2. Switch to the requested level: Campaigns, Ad sets, or Ads.
3. Set the requested date range, defaulting to Today only when the user asks for current monitoring. After the page refreshes, read the date button or CSV `Reporting starts` / `Reporting ends` fields and record the actual applied range. If the requested range and applied range differ, report both and use the applied range for totals.
4. Use stable metric columns:
   - Delivery
   - Results
   - Cost per result
   - Budget
   - Amount spent
   - Impressions
   - Reach
   - Schedule / Starts / Ends
   - Attribution setting
5. Always include recovery columns before reading, copying, or exporting. If the visible table does not already show recovery, purchase value, conversion value, or ROAS columns, first open `Columns` / `Columns: Custom`, search/select the recovery fields, apply the column view, wait for the table to refresh, and only then read, copy, or export the table. Prefer a saved/custom column view that contains:
   - Purchase conversion value
   - Purchases conversion value
   - Website purchase ROAS
   - Purchase ROAS (return on ad spend)
   - ROAS
   - Conversion value
   - Results value
   - Direct website purchases conversion value
   - Purchases
6. Custom-column selection is part of the normal read flow, not an error path. Do this for every BM/account because column presets can differ by account.
7. Export CSV only after the recovery fields are selected and the table visibly shows recovery headers, or a custom-column attempt has clearly failed.
8. Parse recovery fields from CSV headers using tolerant aliases:
   - `Purchase conversion value`
   - `Purchases conversion value`
   - `Website purchase ROAS`
   - `Purchase ROAS (return on ad spend)`
   - `ROAS`
   - `Conversion value`
   - `Results value`
   - `Direct website purchases conversion value`
   - `Purchases`
9. Interpret recovery fields explicitly:
   - `Results value`, purchase conversion value, or direct website purchase value are revenue/value fields.
   - `Purchase ROAS`, `Website purchase ROAS`, `Results ROAS`, or generic `ROAS` are ROAS fields.
   - `Purchases` is count, not revenue.
10. If recovery columns are still not present after the custom-column retry, set `recovery.status: custom_column_failed` and keep `revenue` / `roas` as `not_available`. Do not treat this as a normal zero value.
11. If the operator has a separate backend recovery source, mark `recovery.status: external_recovery_required` and do not report FB recovery as the business recovery number.
12. Validate the CSV using the data correctness requirements above before using it in totals.
13. If export fails or stalls, read page totals and mark `data_source: ui_total`; only use UI totals for recovery if the recovery columns are visibly present in the table and not clipped off-screen.
14. Record no-data states as first-class rows.
15. Continue until every discovered BM account has either metrics or a skipped/no-data status.

### Export Validation Checklist

For each exported file:

1. Confirm the file modified time is from the current run.
2. Confirm the account name and ID match the UI account selector or exported filename.
3. Confirm `Reporting starts` and `Reporting ends` match the applied UI date range.
4. Confirm the level from the filename/table context matches the requested level.
5. Confirm required columns exist, including spend, results, budget, impressions, and at least one recovery alias after the custom-column attempt.
6. Confirm parsed totals match visible UI totals for spend, results, and impressions when visible.
7. If a file fails any check, add it to `rejected_sources` and export again or mark the account as `export_failed`.

## No-Data Statuses

```text
no_active_delivery
no_today_spend
scheduled_only
data_unavailable
export_failed
ui_total_only
data_conflict
```

## Output

For multi-account BM reads, return a coverage wrapper plus one metrics object per account:

```yaml
business_id: ""
business_name: ""
scope: business_all_accounts
discovery_source: business_settings | api | configured_inventory | ads_manager_selector
coverage_status: complete | partial_ui_discovery | incomplete
account_count: 0
metrics: []
limitations: []
```

Each account metric object:

```yaml
account_id: "act_..."
account_name: ""
level: adset
date_range: "2026-05-20_2026-05-20"
data_source: csv | copied_table | ui_total | unavailable
csv_path: null
csv_validated: false
export_time: ""
row_count: 0
active_rows: 0
spend: 0.0
today_spend: null
results: 0
impressions: 0
recovery:
  status: available | custom_column_failed | external_recovery_required | not_applicable
  revenue: not_available
  roas: not_available
  purchases: not_available
rows: []
limitations: []
rejected_sources: []
```

## Guardrails

- Do not click delivery toggles.
- Do not edit, duplicate, publish, pause, resume, or change budgets.
- Exporting or saving CSV files is allowed.
- For BM requests, do not stop after the currently selected account; every discovered BM account needs a result row.
- If UI state is unclear, stop and mark `data_unavailable` instead of guessing.
- Preserve the data source and limitations so `$fb-ads-rules` can avoid unsafe decisions.
