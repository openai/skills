---
name: fb-ads-delivery-closer
description: Close or pause Facebook/Meta Ads delivery through Computer Use after explicit operator authorization. Use when the user asks to shut down, close, pause, turn off, or stop campaigns, ad sets, or ads in Ads Manager, especially BM-wide or multi-account execution, with audit evidence and optional Feishu reporting.
---

# FB Ads Delivery Closer

## Purpose

Use this skill to execute delivery shutdowns in Facebook/Meta Ads Manager through Computer Use. It changes delivery state, so it is not a read-only skill.

Only use it after the operator explicitly authorizes closing/pausing in the current turn. If authorization, scope, level, or object identity is unclear, stop and produce a manual confirmation report.

## Safety Boundary

Allowed:

- Navigate Ads Manager.
- Switch BM/ad accounts.
- Filter/search rows.
- Select rows.
- Turn off delivery toggles for explicitly authorized Campaigns, Ad sets, or Ads.
- Confirm pause/turn-off dialogs when they exactly match the authorized operation.
- Capture before/after screenshots and write audit reports.

Forbidden:

- Create, duplicate, edit, publish, resume, increase budgets, change bids, change schedules, or change targeting.
- Close objects outside the authorized scope.
- Act on screenshot-only identity when names/IDs are ambiguous.
- Use bulk shutdown when Computer Use cannot read stable UI state.
- Continue after an unexpected dialog, review/publish flow, account switch mismatch, or row count mismatch.

## Required Inputs

```yaml
mode: semi_auto | emergency
business_id: ""
scope: current_account | selected_accounts | business_all_accounts
account_ids: []
level: campaign | adset | ad
selection:
  type: all_active | all_today_spend | ids | names | rule_recommended
  ids: []
  names: []
source_metrics: []
reason: ""
report_destination: chat | file | feishu
```

If the user says "关闭所有广告" without a level, treat `level: ad` as unsafe. Ask for explicit level unless the surrounding context clearly means Ad sets. For spend-control workflows, prefer `level: adset`.

## Preflight

Before changing anything:

1. Confirm current-turn authorization includes an executable phrase such as "关闭", "暂停", "turn off", or "pause".
2. Resolve account scope using `$fb-ads-scope` or a configured BM inventory. Do not rely on the currently selected account as the full BM.
3. Load metrics from `$fb-ads-metrics-reader` when rule-based selection is requested.
4. Load decisions from `$fb-ads-rules` when the user asks to close recommended or abnormal objects.
5. Build an execution plan:
   - accounts to visit
   - level to operate
   - expected object count per account
   - exact matching method
6. If expected count is missing for a bulk operation, first inspect the table and report the count. Do not close until count is stable.
7. Take a screenshot or record UI state before each account-level operation.

## Computer Use Procedure

For each account:

1. Open Ads Manager URL with `act=<account_id>`, `business_id=<business_id>`, requested level, and date range when relevant.
2. Verify:
   - account selector shows the expected account ID/name
   - selected tab matches `Campaigns`, `Ad sets`, or `Ads`
   - table is loaded and not in a login/error/interstitial state
3. Apply filters only when needed:
   - active delivery for `all_active`
   - today spend for `all_today_spend`
   - search exact IDs/names for targeted closure
4. Verify rows:
   - record visible row count and total result count
   - for targeted rows, match object ID when available; otherwise exact name plus account/level
   - for bulk rows, verify the selected filter and total count
5. Select only authorized rows.
6. Turn off delivery using the safest visible control:
   - prefer bulk Off/On toggle/action for selected rows when the selected count is exact
   - otherwise toggle individual authorized rows one by one
7. Confirm only dialogs that clearly say the selected objects will be turned off/paused.
8. Wait for table update.
9. Verify after-state:
   - delivery/off status changed for every intended object
   - no unintended selected rows remain
   - review/publish is not pending unless Meta requires a publish confirmation for the exact pause
10. Capture after screenshot/state.

## Stop Conditions

Stop immediately and do not change delivery if any of these happen:

- Ads Manager asks for login, 2FA, captcha, account verification, or permission upgrade.
- Account selector does not match the target account.
- UI tree/screenshot is unreadable and the action would require coordinate guessing.
- Row identity is ambiguous.
- Bulk selected count differs from expected count.
- A dialog mentions create/edit/publish/budget/audience instead of turning off delivery.
- Any pause action appears to target a different level than requested.

## Audit Output

Return one audit row per account and per changed object when possible:

```yaml
event_time: ""
business_id: ""
account_id: ""
account_name: ""
level: adset
object_id: ""
object_name: ""
requested_action: pause
before_delivery: active
after_delivery: off
selection_method: all_active | all_today_spend | id | name | rule_recommended
reason: ""
result: changed | skipped | failed | manual_confirm_required
evidence:
  before_screenshot: ""
  after_screenshot: ""
limitations: []
```

For bulk operations where per-object rows cannot be exported safely, include account-level audit:

```yaml
account_id: ""
level: adset
requested_count: 0
changed_count: 0
skipped_count: 0
result: changed | partial | failed | manual_confirm_required
```

## Reporting

If `$feishu-report` is requested, send only the final audit summary after execution or stop. Include:

- authorization phrase
- scope
- level
- accounts attempted
- changed count
- skipped/failed count
- stop reason, if any
- confirmation that no budgets, bids, creates, duplicates, or resumes were performed

Do not include webhook URLs.
