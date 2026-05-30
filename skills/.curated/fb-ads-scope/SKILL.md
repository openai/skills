---
name: fb-ads-scope
description: Enumerate and reconcile Facebook Ads Manager business portfolio/BM account scope. Use when the user asks to check all accounts under a BM, verify coverage, list ad accounts, identify inaccessible/disabled/empty accounts, or prepare account coverage before FB ads monitoring.
---

# FB Ads Scope

## Purpose

Use this skill before reading metrics whenever the user scope is a BM, business portfolio, multiple accounts, or "all accounts". Its job is account coverage only: identify all accounts under the current BM, not merely accounts visible in the current Ads Manager selector, and prove each account was checked or explicitly skipped.

Do not evaluate performance rules, generate pause decisions, or execute delivery changes here.

## Inputs

```yaml
business:
  business_id: ""
  name: ""
expected_account_count: null
known_accounts: []
requested_scope: current_account | selected_accounts | business_all_accounts
```

## Workflow

1. Confirm requested account scope from the user request.
2. If scope is BM/business/all accounts, build the account list from the strongest available source:
   - Meta Marketing API or configured account inventory, when available.
   - Business Settings > Ad accounts for the current BM.
   - Ads Manager account selector only as a fallback discovery source.
3. Capture account name and account ID for every BM account found.
4. Build a coverage list before metric collection; do not treat selector visibility as complete BM coverage by itself.
5. For each account, set one status:
   - `enabled`
   - `disabled_account`
   - `inaccessible_account`
   - `excluded_account`
   - `unknown_visibility`
6. Reconcile actual accounts against `expected_account_count` or known accounts when provided.
7. Return a coverage table for downstream metric reading and final reports.

## Output

```yaml
business_id: ""
business_name: ""
requested_scope: business_all_accounts
expected_accounts: 5
discovered_accounts: 5
discovery_source: business_settings | api | configured_inventory | ads_manager_selector
coverage_status: complete
accounts:
  - account_id: "act_..."
    account_name: ""
    status: enabled
    skipped_reason: null
```

## Rules

- Do not claim BM-wide coverage after checking only the selected account or only the accounts currently visible in the selector.
- Include quiet, empty, disabled, and inaccessible accounts in the output.
- If the only source is a partial UI list, set `coverage_status: partial_ui_discovery` unless it is reconciled against an expected count, configured inventory, or Business Settings/API source.
- If fewer accounts are discovered than expected, set `coverage_status: incomplete` and list the missing count or names when known.
- Account IDs should keep the `act_` prefix in structured output when possible; display tables may omit it for readability.
