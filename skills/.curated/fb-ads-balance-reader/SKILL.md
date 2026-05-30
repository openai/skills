---
name: fb-ads-balance-reader
description: Read Facebook/Meta Ads account billing balances safely through Computer Use. Use when the user asks to inspect ad account balance, current balance, credit line, spending limit remaining amount, billing status, or balances for all accounts under a BM/business portfolio.
---

# FB Ads Balance Reader

## Purpose

Use this skill to read Meta Ads Billing & payments data only. It can navigate to billing pages, pass already-authorized browser 2FA, switch accounts, and record displayed balances. It must not pay bills, reset limits, add payment methods, change credit lines, or edit ads.

When the user says BM, business portfolio, all accounts, or does not clearly restrict the request to the current ad account, check every ad account under the current BM. Do not treat the currently selected account as the whole BM.

## Balance Fields

Record both billing fields when present because operators may call either one "balance":

- `current_balance`: value under `Current balance`, usually shown as `$X + any applicable fees`. This is the current amount due/accrued in Billing.
- `spending_limit_remaining`: value under `Account spending limit` / `Remaining amount`.
- `spending_limit`: the limit shown in the detail text, for example `$66.53 spent | $100.01 spending limit`.
- `spend_against_limit`: the spent value shown beside the spending limit.
- `payment_method_summary`: high-level method text only, such as `Credit line / Example Provider`; do not expose sensitive payment numbers.
- `billing_alerts`: read visible alerts such as `No issues detected`.

## Workflow

### Computer Use Preflight

When using Computer Use:

1. Run `get_app_state` or `list_apps` before touching Meta UI.
2. If Computer Use is unavailable, stop with `computer_use_unavailable`; do not reuse old balance readings.
3. Confirm the browser is already logged in and on Meta/Ads Manager/Billing, or navigate from the visible browser state.

### Account Scope

Use `$fb-ads-scope` when available for BM-wide requests. If working inline, use the strongest available account list:

1. Business Settings or configured inventory.
2. Ads Manager/Billing account selector when reconciled against an expected count.
3. Selector-visible accounts as fallback only; set `coverage_status: partial_ui_discovery` unless reconciled.

Each account row needs account name and ID.

### Billing Navigation

For each account, prefer a direct Billing details URL:

```text
https://business.facebook.com/billing_hub/accounts/details/?business_id=<BUSINESS_ID>&asset_id=<ACCOUNT_ID>&payment_account_id=<ACCOUNT_ID>&placement=ads_manager&entrypoint=ads_ecosystem_navigation_ads_billing_tool_plugin&payment_account_id_from_jsmodule=<ACCOUNT_ID>
```

Fallback: open Ads Manager for the account, then use the left navigation `Billing & payments`.

Wait for the page to show the target account title before reading values. The URL may briefly show a previous account while loading; trust the visible title and displayed fields after loading completes.

### 2FA and Passkey Prompts

- If Billing triggers `Two-factor authentication required`, use an existing user-authorized 2FA source only when available in the current browser/workflow. Do not reveal OTP codes in the final answer.
- If a `Create passkey`, `Next time, skip the code`, or system passkey prompt appears, do not create a passkey. Choose `Not now`, `Cancel`, or close the prompt if possible.
- If 2FA cannot be completed without user input, stop and ask the user to complete verification, then resume reading.

### Reading Values

On each account page:

1. Confirm visible account title matches the target account.
2. Read `Current balance`.
3. Read `Account spending limit` / `Remaining amount`.
4. Read the accompanying `spent | spending limit` text.
5. Read visible billing alerts.
6. Optionally record non-sensitive credit-line text. Never expand or copy hidden payment details.

If the account page stays on skeleton/loading for more than a short wait, refresh once or navigate directly again. If it still fails, record `data_status: data_unavailable` for that account and continue with the next account.

## Output

For BM-wide reads, return a coverage wrapper plus one balance object per account:

```yaml
business_id: ""
business_name: ""
scope: business_all_accounts
discovery_source: business_settings | configured_inventory | ads_manager_selector | billing_selector
coverage_status: complete | partial_ui_discovery | incomplete
account_count: 0
balances: []
limitations: []
```

Each balance object:

```yaml
account_id: "act_..."
account_name: ""
data_source: billing_ui
data_status: available | data_unavailable | auth_required
current_balance: "$0.00"
current_balance_note: "+ any applicable fees"
spending_limit_remaining: "$0.00"
spend_against_limit: "$0.00"
spending_limit: "$0.00"
billing_alerts: []
payment_method_summary: ""
checked_at: ""
limitations: []
```

For a user-facing table, include at minimum:

```text
Account | Account ID | Current balance | Spending limit remaining
```

If both fields are present, make clear which one is `Current balance` and which is spending-limit remaining amount.

## Guardrails

- Do not click `Pay Now`.
- Do not click `Reset now`.
- Do not click `Add payment method`.
- Do not edit credit lines, billing settings, account spending limits, campaigns, budgets, delivery toggles, or payment methods.
- Do not create passkeys or change account security settings.
- Do not expose OTP codes, full payment details, or sensitive card/bank identifiers.
- Disabled buttons are safe to observe but do not use them as actions.
- If UI state is unclear, stop and mark `data_unavailable` instead of guessing.
