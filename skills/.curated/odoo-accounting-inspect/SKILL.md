---
name: odoo-accounting-inspect
description: "Inspect Odoo accounting: invoices, bills, payments, journal entries, aged receivables. READ-ONLY. WHEN: invoice, bill, payment, overdue, unpaid, posted, draft invoice, receivable, payable, journal entry, aged, account.move. DO NOT USE WHEN: posting invoices, creating payments, or reconciling — use the write tier."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: read
---

# Odoo Accounting Inspect (read-only)

> **READ-ONLY.** This skill never calls mutating tools.

## Key field names (Odoo 17+)

| Model | Wrong name | Correct name |
|---|---|---|
| `account.move` | `type` | `move_type` (renamed in Odoo 16) |
| `account.move` | `post_date`, `posted_date` | `invoice_date` (for invoice date) or `date` (for accounting date) |
| `account.move` | `invoice_due_date` | verify via `odoo_get_fields(model='account.move')` |
| `account.payment` | `payment_date` | `date` |

## Recipes

### Customer invoices (posted, recent)

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("account.move", "search_read", ...)`

```
cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

odoo_search_read(model="account.move",
  domain=[
    ["move_type","=","out_invoice"],
    ["state","=","posted"],
    ["invoice_date",">",cutoff]
  ],
  fields=["name","partner_id","invoice_date","amount_total","amount_residual","state","payment_state"],
  limit=200, order="invoice_date desc")
```

> The field is `move_type` — NEVER use `type`. Values: `out_invoice` (customer invoice), `in_invoice` (vendor bill), `out_refund`, `in_refund`, `entry` (journal entry).
> NEVER use `%(date)s` or `now()` in domains — compute dates in Python first.

### Unpaid / overdue invoices

```
odoo_search_read(model="account.move",
  domain=[
    ["move_type","in",["out_invoice","out_refund"]],
    ["state","=","posted"],
    ["payment_state","in",["not_paid","partial"]]
  ],
  fields=["name","partner_id","invoice_date","invoice_date_due","amount_total","amount_residual"],
  limit=200, order="invoice_date_due asc")
```

> `payment_state` values: `not_paid`, `partial`, `paid`, `in_payment`, `reversed`.
> `amount_residual` = the amount still owed.
> To check "overdue": compare `invoice_date_due` < today (compute today's date in Python).

### Vendor bills

```
odoo_search_read(model="account.move",
  domain=[["move_type","=","in_invoice"],["state","=","draft"]],
  fields=["name","partner_id","invoice_date","amount_total","ref"],
  limit=100, order="invoice_date desc")
```

### Payments

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("account.payment", "search_read", ...)`

```
odoo_search_read(model="account.payment",
  domain=[["state","=","posted"]],
  fields=["name","partner_id","amount","date","payment_type","journal_id"],
  limit=100, order="date desc")
```

> The date field is `date` — NEVER use `payment_date`.
> `payment_type`: `inbound` (customer payment), `outbound` (vendor payment).

### Invoice counts by state

**MCP tool:** `odoo_search_count` (multiple calls)
**Raw RPC:** `execute("account.move", "search_count", ...)`

```
# Count by move_type × state
for move_type in ["out_invoice", "in_invoice", "entry"]:
    for state in ["draft", "posted", "cancel"]:
        odoo_search_count(
          model="account.move",
          domain=[["move_type","=",move_type],["state","=",state]])
```
