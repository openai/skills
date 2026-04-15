---
name: odoo-model-inspect
description: "General Odoo model inspection: field definitions, view XML, record counts, model structure. READ-ONLY. WHEN: what fields, model structure, view XML, count records, list models, get fields, general query. DO NOT USE WHEN: the question is about a specific domain — use odoo-system-inspect (modules/cron/logs), odoo-stock-inspect (inventory/moves), odoo-mrp-inspect (manufacturing/BoMs), or odoo-accounting-inspect (invoices/payments) instead."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: read
---

# Odoo Model Inspect (read-only)

> **READ-ONLY.** This skill never calls mutating tools. If the user asks for changes, refer them to the write tier (`odoo-model-customize`).

## When to use this vs a domain skill

| Question is about... | Use this skill | Use instead |
|---|---|---|
| Model structure, fields, views | Yes | — |
| General "how many X?" counts | Yes | — |
| Modules, cron jobs, error logs, users | — | `odoo-system-inspect` |
| Stock levels, moves, transfers, reorder rules | — | `odoo-stock-inspect` |
| Manufacturing orders, BoMs, components | — | `odoo-mrp-inspect` |
| Invoices, payments, journal entries | — | `odoo-accounting-inspect` |

## Compatibility — Odoo 18 and Odoo 19

Verified on both. The read API is stable across versions.

| Field | Odoo 18 | Odoo 19 |
|---|---|---|
| `ir.model.order` (mirrors `_order`) | Available | Available |
| `ir.model.rec_name` | Does not exist | Does not exist |
| `ir.model.abstract`, `ir.model.fold_name` | Do not exist | Available |

## Allowed Tools (READ ONLY)

**If using MCP server (`odoo-simple-mcp`):**

| MCP tool | Purpose |
|------|---------|
| `odoo_model_info` | Comprehensive model metadata in one call |
| `odoo_get_fields` | Field definitions for a model |
| `odoo_get_view` | Fully merged view XML after inheritance |
| `odoo_search_read` | Read records matching a domain |
| `odoo_search_count` | Count records matching a domain |
| `odoo_list_models` | List installed models, optional keyword filter |
| `odoo_doctor` | Run health diagnostics |

**If using raw JSON-RPC (no MCP):**

| RPC call | Equivalent |
|---|---|
| `execute(model, "fields_get", [], {"attributes": [...]})` | `odoo_get_fields` |
| `execute(model, "search_read", domain, fields=..., limit=...)` | `odoo_search_read` |
| `execute(model, "search_count", domain)` | `odoo_search_count` |
| `execute(model, "get_views", [[False, view_type]])` | `odoo_get_view` |

## Rules

1. **Count before fetching.** Use `search_count` first. If count is huge, narrow the domain.
2. **Project only needed fields.** List field names explicitly — never ask for all fields.
3. **Confirm model existence.** Call `odoo_list_models(keyword=...)` before querying models that may not be installed (`crm.lead`, `helpdesk.ticket`, `mrp.production`).
4. **Default limit=50.** Bump to 200 only for full listings.

## Generic domain rules

These apply to ALL models, in every domain skill:

> NEVER use `now()`, `%(today)s`, `%(date_start)s`, or any placeholder in domain filters. Compute dates in Python first, pass literal ISO strings like `"2024-01-15"`.

> NEVER pass bare list values in domains. Use proper tuple syntax: `[("state","in",["draft","posted"])]`.

> NEVER assume you can filter on related fields across non-Many2one relations. If the error says "is not a Many2one", query the related model separately.

## Recipes

### "What fields are on this model?"

**MCP:** `odoo_model_info(model="sale.order")`
**Raw RPC:** `execute("ir.model", "search_read", ...)` + `execute("ir.model.fields", "search_read", ...)`

Returns field count, types, custom fields, required fields, relational fields.

### "How many X are there?"

**MCP:** `odoo_search_count(model="sale.order", domain=[["state","=","sale"]])`
**Raw RPC:** `execute("sale.order", "search_count", [["state","=","sale"]])`

### "Show defaults set for a model"

```
odoo_search_read(model="ir.default",
  domain=[["field_id.model_id.model","=","sale.order"]],
  fields=["field_id","user_id","company_id","json_value"],
  limit=100)
```

> `ir.default` has no `model_id` or `model` column. Traverse via `field_id.model_id.model`.

### "Get the rendered form view"

**MCP:** `odoo_get_view(model="res.partner", view_type="form")`
**Raw RPC:** `execute("res.partner", "get_views", [[False, "form"]])`

Returns merged XML after all inheritance — what the user actually sees.

## Reporting

Present results in the format that matches the question:

- **Structure question** → field table or JSON snippet
- **Audit / health check** → grouped by severity (Critical / Warning / OK)
- **Listing** → table with most informative columns first
- **Comparison** → side-by-side table

---

## Common Pitfalls (auto-curated by RL)

_Maintained automatically by the SkillRL self-edit loop. Each bullet is a prescriptive rule learned from a real failed episode._

<!-- AUTO-CURATED-START -->
- NEVER use `now()` in domain expressions for `ir.cron` date fields — use `fields.Datetime.now()` or verify correct syntax via `odoo_get_fields(model='ir.cron')`.
- NEVER query `numbercall` on `ir.cron` — verify the correct field via `odoo_get_fields(model='ir.cron')`.
- NEVER filter on `ir.module.module.dependency.state` — it is not a stored field; query `ir.module.module.state` instead.
- NEVER query `version` on `ir.module.module` — it is not a stored field; verify the correct field via `odoo_get_fields(model='ir.module.module')`.
- NEVER query `category` on `ir.module.module` — it is not a stored field; verify the correct field via `odoo_get_fields(model='ir.module.module')`.
- NEVER query `depend_id` on `ir.module.module.dependency` — it is not a stored field; verify the correct field via `odoo_get_fields(model='ir.module.module.dependency')`.
- NEVER query `qty_available` on `product.product` — it is not a stored field; verify the correct field via `odoo_get_fields(model='product.product')`.
- NEVER query `name` on `stock.move` — it is not a stored field; verify the correct field via `odoo_get_fields(model='stock.move')`.
- NEVER query `quantity_done` on `stock.move` — it is not a stored field; verify the correct field via `odoo_get_fields(model='stock.move')`.
- NEVER query `qty_done` on `stock.move.line` — it is not a stored field; verify the correct field via `odoo_get_fields(model='stock.move.line')`.
- NEVER query `type` on `account.move` — it is not a stored field; verify the correct field via `odoo_get_fields(model='account.move')`.
- NEVER query `post_date` on `account.move` — it is not a stored field; verify the correct field via `odoo_get_fields(model='account.move')`.
- NEVER use `%(today)s` in domain expressions — use `fields.Date.today()` or verify correct syntax via `odoo_get_fields(model='account.move')`.
- WHEN building domains for `odoo_search_count`, ensure the domain argument is a list of tuples, not a string or malformed structure.
- NEVER query `last_login` on `res.users` — it is not a stored field; verify the correct field via `odoo_get_fields(model='res.users')`.
- NEVER query `groups_id` on `res.users` — it is not a stored field; verify the correct field via `odoo_get_fields(model='res.users')`.
- WHEN passing a domain to `odoo_search_count`, ensure it is a list of tuples, not a nested list or other structure — unhashable type errors indicate malformed domain syntax.
- NEVER query `last_call` on `ir.cron` — it is not a stored field; verify the correct field via `odoo_get_fields(model='ir.cron')`.
- NEVER query `timestamp` on `res.users.log` — it is not a stored field; verify the correct field via `odoo_get_fields(model='res.users.log')`.
- NEVER query `name` on `privacy.log` — it is not a stored field; verify the correct field via `odoo_get_fields(model='privacy.log')`.
- NEVER query `name` on `res.device.log` — it is not a stored field; verify the correct field via `odoo_get_fields(model='res.device.log')`.
- NEVER attempt to query `auth.totp.rate.limit.log` without verifying group permissions — access may be restricted to administrators only.
- NEVER use `now()` in domain expressions for date fields — use `fields.Datetime.now()` or `fields.Date.today()` instead.
- NEVER query `reserved_uom_qty` on `stock.move.line` — it is not a stored field; verify the correct field via `odoo_get_fields(model='stock.move.line')`.
- NEVER use `today()` in domain expressions — use `fields.Date.today()` or `fields.Datetime.now()` instead.
- NEVER query `description` on `account.move.line` — it is not a stored field; verify the correct field via `odoo_get_fields(model='account.move.line')`.
- NEVER query `payment_date` on `account.payment` — it is not a stored field; verify the correct field via `odoo_get_fields(model='account.payment')`.
- NEVER query `credit_exposure` on `res.partner` — it is not a stored field; verify the correct field via `odoo_get_fields(model='res.partner')`.
- NEVER query `invoice_due_date` on `account.move` — it is not a stored field; verify the correct field via `odoo_get_fields(model='account.move')`.
- NEVER query `doall` on `ir.cron` — it is not a stored field; verify the correct field via `odoo_get_fields(model='ir.cron')`.
<!-- AUTO-CURATED-END -->
