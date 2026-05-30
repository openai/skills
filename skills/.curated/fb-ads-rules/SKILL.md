---
name: fb-ads-rules
description: Evaluate Facebook ad spend, CPA, conversion, ROAS, recovery, and anomaly rules from collected metrics. Use when the user asks for pause recommendations, abnormal spend detection, zero-conversion burn checks, high CPA checks, low recovery checks, or watch/no-pause decisions.
---

# FB Ads Rules

## Purpose

Use this skill after `$fb-ads-metrics-reader` has collected account metrics. It evaluates rules and returns decisions. It does not operate the browser and does not execute pauses.

## Decision Values

```text
pause_recommended
manual_confirm_required
watch
no_pause
no_active_delivery
no_today_spend
skipped
```

## Required Inputs

```yaml
mode: read_only | semi_auto | emergency
level: adset
metrics: []
policy:
  min_spend_to_act: 20
  target_cpa: null
  daily_cap: null
  min_roas: null
  min_payback: null
  min_spend_for_recovery_check: 30
```

## Rules

### Fast Spend

- Pace spike: `today_spend > daily_cap * elapsed_day_ratio * pace_multiplier` and spend is at least `min_spend_to_act`.
- Short-window burn: short-window spend delta exceeds the configured share of daily cap.
- Hard cap: `today_spend >= daily_cap`.

If daily cap is missing, mark `daily_cap_missing` and do not use pace or hard-cap rules.

### Conversion Efficiency

- Zero conversion burn: `today_spend > target_cpa * 2` and results are `0`.
- High CPA: results are at least `3` and CPA is greater than `target_cpa * 1.5`.

If target CPA is missing, mark `target_cpa_missing` and do not use zero-burn or high-CPA rules.

### Recovery

- Low recovery: spend is at least `min_spend_for_recovery_check` and ROAS/payback/revenue recovery is below target.
- Missing recovery data never triggers pause by itself. Mark `recovery_missing`.

## Conservative Defaults

- In `read_only` mode, never return an executable action; return recommendations only.
- Never recommend pause based only on missing recovery, missing CPA, inferred budget, or screenshot-only data.
- Prefer `watch` when spend exists but required thresholds are missing.
- Use `pause_recommended` only when an explicit threshold is present and violated.
- Use `manual_confirm_required` when the rule is plausible but object identity, account scope, or input completeness is not strong enough.

## Output

```yaml
account_id: "act_..."
object_level: adset
object_id: null
object_name: ""
decision: watch
triggered_rules: []
missing_inputs:
  - target_cpa
  - recovery
reason: ""
recommended_action: none | pause_adset | pause_ad | pause_campaign
executable: false
```
