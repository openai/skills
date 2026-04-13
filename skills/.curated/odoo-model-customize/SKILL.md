---
name: odoo-model-customize
description: "Customize Odoo models at runtime without custom modules. Set field defaults via ir.default, change list sort order via window actions, create saved filters, add custom x_ fields, create inherited views with XPath, and set up automated actions. WHEN: change default value, set default, sort order, reorder list, default filter, add custom field, customize form, add field to view, change dropdown order, groupby default, saved filter, automated action. DO NOT USE WHEN: override Python methods, change _order class attribute, add stored computed fields, modify core field constraints — those require a custom module."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: write
---

# Odoo Model Customization

> **SAFETY BOUNDARY — RUNTIME-SAFE vs MODULE-REQUIRED**
>
> This skill covers customizations that can be done **safely at runtime via RPC** without writing Python code or creating a custom module. Operations that require a custom module are explicitly flagged — do NOT attempt them via RPC.

## Triggers

Activate this skill when user wants to:
- Set or change a field's default value
- Change the sort order of a list/tree view
- Add a default filter or groupby to a menu
- Create a custom field on a model
- Add a field to a form or list view
- Create a saved search filter
- Set up an automated action (on create/write/delete)
- Understand what can be customized at runtime vs what needs a module

> **Scope**: This skill handles runtime-safe customizations only. For creating full Odoo modules with Python model inheritance, use the `odoo-19` development skill.

---

## Compatibility — Odoo 18 and Odoo 19

This skill is verified on **Odoo 18.0** and **Odoo 19.0**. The runtime customization API (`ir.default`, `ir.model.fields`, `ir.actions.act_window`, `ir.ui.view`, `base.automation`, `ir.filters`) is **stable across both versions** — the same RPC calls work on either. Always check the connected server's version first via `odoo_doctor` or by reading `version` from `/jsonrpc` `common.version` so you can apply the right notes below.

### Differences between 18 and 19

| Area | Odoo 18 | Odoo 19 | Why it matters |
|---|---|---|---|
| `ir.model` extra columns | base set only | adds `abstract`, `fold_name` | If you query `abstract` or `fold_name` on 18 you get "Invalid field". Only request them when version ≥ 19. |
| `ir.cron.interval_number.aggregator` | `None` | `'avg'` | Cosmetic; only affects read_group reporting on cron intervals. |
| RPC endpoints | `/jsonrpc` (legacy) | `/jsonrpc` AND `/api/<model>/<method>` (JSON v2 + bearer token) | On 19 you can authenticate with an API key via JSON v2 — faster and avoids passing the password. On 18, only `/jsonrpc` with login/password is available. |
| Default sort source | `ir.model.order` (stored Char mirrors `_order`) | Same — `ir.model.order` works | Both versions expose `_order` via the `order` Char on `ir.model`. Safe to read on either. |

### Fields the LLM often invents that DO NOT exist in either 18 or 19

| Wrong | What to use instead |
|---|---|
| `ir.model.rec_name` | Not a stored field. `_rec_name` is a Python class attr. Infer from `ir.model.fields`: use `"name"` if present, else `"x_name"`, else `"id"` — Odoo's own fallback. |
| `ir.module.module.version` | Use `installed_version` (computed Char). |
| `ir.cron.numbercall` | Removed in Odoo ≥16. Use `nextcall` for scheduling state. |
| `res.users.last_login` | Use `login_date` (related to `log_ids.create_date`). |
| `ir.logging.path_ids` | Use the scalar `path` (Char). |
| `ir.module.module.dependency.state` | Computed, not stored — cannot be in domain filters. Read deps and filter client-side. |
| `ir.default.model_id`, `ir.default.model` | `ir.default` has no model column. Filter via `[["field_id.model_id.model","=",model_name]]` or `[["field_id.model","=",model_name]]`. |

## Rules

1. **Always start with `odoo_model_info`** — get the full picture before making changes
2. **Runtime-safe operations only** — see [Safety Boundary](references/safety-boundary.md)
3. **Verify after every write** — re-read the record to confirm the change took effect
4. **Confirm destructive changes** — ask user before modifying window actions or views
5. **Use specialized tools** — prefer `odoo_set_default`, `odoo_modify_action`, `odoo_get_view` over raw `odoo_update`

---

## Steps

| # | Action | Reference |
|---|--------|-----------|
| 1 | **Discover** — Run `odoo_model_info(model)` to see fields, views, actions, defaults, and sort order | [Discovery Guide](references/discovery.md) |
| 2 | **Classify** — Is this runtime-safe or module-required? | [Safety Boundary](references/safety-boundary.md) |
| 3 | **Execute** — Use the appropriate method for the operation type | See operation guides below |
| 4 | **Verify** — Re-read the affected record to confirm success | — |
| 5 | **Report** — Show the user what changed (before → after) | — |

---

## Operation Guides

| Operation | Method | Reference |
|-----------|--------|-----------|
| **Set field defaults** | `odoo_set_default` → ir.default | [Defaults Guide](references/defaults.md) |
| **Change list sort order** | `odoo_modify_action` → context.default_order | [Sort Order Guide](references/sort-order.md) |
| **Add default filters/groupby** | `odoo_modify_action` → domain/context | [Filters Guide](references/filters.md) |
| **Create custom fields** | `odoo_create` → ir.model.fields (x_ prefix) | [Custom Fields Guide](references/custom-fields.md) |
| **Modify form/tree/search views** | `odoo_create` → ir.ui.view (inherited + XPath) | [View Inheritance Guide](references/view-inheritance.md) |
| **Create saved filters** | `odoo_create` → ir.filters | [Saved Filters Guide](references/saved-filters.md) |
| **Set up automated actions** | `odoo_create` → base.automation | [Automation Guide](references/automation.md) |

---

## What Requires a Custom Module

These operations **cannot** be done at runtime. If the user asks for them, explain that a Python module is needed:

| Operation | Why | What to suggest instead |
|-----------|-----|------------------------|
| Change `_order` on a model | Python class attribute | Use `odoo_modify_action` to set `default_order` on the window action |
| Override methods (create, write, name_get) | Python inheritance | Suggest a custom module with `_inherit` |
| Add stored computed fields | Needs `compute=` + `store=True` | Add a non-computed x_ field + base.automation to populate it |
| Change field `required`/`readonly` at model level | Python class definition | Use inherited view with `required="1"` or `readonly="1"` (visual only) |
| Add Python constraints | `@api.constrains` decorator | Use base.automation with validation logic |
| Add onchange logic | `@api.onchange` decorator | Use base.automation triggered on write |

## MCP Tools

| Tool | Purpose |
|------|---------|
| `odoo_model_info` | Get comprehensive model metadata in one call |
| `odoo_set_default` | Set/update/clear field default values |
| `odoo_get_view` | Get fully rendered (merged) view XML |
| `odoo_modify_action` | Change window action domain/context/sort/limit |
| `odoo_search_read` | Query any Odoo model |
| `odoo_create` | Create records (ir.model.fields, ir.ui.view, ir.filters, base.automation) |
| `odoo_get_fields` | Get field definitions for a model |

---

## Common Pitfalls (auto-curated by RL)

_Maintained automatically by the SkillRL self-edit loop. Each bullet is a prescriptive rule learned from a real failed episode._

<!-- AUTO-CURATED-START -->
- ON `ir.default`, the value column is `json_value` (JSON-encoded); there is no `value` or `default_value` field. Prefer the `odoo_set_default` helper over raw writes.
- BEFORE querying `crm.lead`, verify CRM module is installed via `odoo_list_models(keyword='crm')`.
- ON `ir.model.fields`, the column is `field_description` not `label`; verify other column names via `odoo_get_fields(model='ir.model.fields')`.
- BEFORE querying `mrp.production`, verify the Manufacturing module is installed via `odoo_list_models(keyword='mrp')`.
- ON `mrp.production`, do not pass `name` to `create()` — it is auto-generated; verify required fields via `odoo_get_fields(model='mrp.production')` first.
- NEVER assume `probability` exists on `sale.order` — that field belongs to `crm.lead`. If CRM is uninstalled, score prospects via `amount_total` and `state` instead.
- NEVER assume `product_id` exists on `project.project` — projects do not link directly to products. Use `project.task` or `mrp.production` for product relationships.
- NEVER use `+` syntax in date domains; use `fields.Date.today()` + `timedelta()` to compute cutoff dates before querying.
- ON `sale.order.line`, the field is `product_uom_qty` not `product_uom`; verify via `odoo_get_fields(model='sale.order.line')`.
- ALWAYS pass domain as a list of lists `[[...]]` not a string; malformed domains cause "invalid argument type" errors.
- ON `mrp.production`, the field is `date_start` not `date_planned_start`; verify required/available fields via `odoo_get_fields()` first.
- ON `mrp.bom`, the field is `product_id` not `name`; use `product_id.name` to access the BOM's product name.
- ON `project.project`, there is no `state` field; use `project.task.state` instead for task-level status tracking.
- ON `purchase.order`, there is no `warehouse_id` field; warehouse context comes from `stock.warehouse` or purchase line locations.
- WHEN creating inherited tree views, use `<xpath position="after">` not `position="remove"` for column insertion; verify valid XPath positions via `odoo_get_view()` first.
- ON `ir.filters`, do not assume `user_id` is a valid filter field; verify filterable fields via `odoo_get_fields(model='ir.filters')`.
- NEVER call `fields_view_get()` directly on models like `sale.order`; use `odoo_get_view(model='sale.order', view_type='tree')` instead.
- BEFORE creating automated actions on `res.partner`, verify `base.automation` exists via `odoo_list_models(keyword='automation')` — the module may be uninstalled.
- ON `ir.ui.view`, the field is `inherit_id` not `module`; verify available fields via `odoo_get_fields(model='ir.ui.view')`.
- NEVER assume `total_revenue` exists on `res.partner` — verify the correct field via `odoo_get_fields(model='res.partner')`.
- ON `stock.move`, do not query or set `name` directly; verify the correct field via `odoo_get_fields(model='stock.move')`.
- ON `stock.move`, do not query or set `quantity_done` directly; verify the correct field via `odoo_get_fields(model='stock.move')`.
- ON `mrp.routing.workcenter`, do not assume `routing_id` exists; verify the correct field via `odoo_get_fields(model='mrp.routing.workcenter')`.
- NEVER use `+` syntax in date domains like `'now + 7 days'`; compute cutoff dates with `fields.Date.today()` + `timedelta()` before querying.
- ON `mrp.bom`, do not query `name` directly; use `product_id.name` to access the BOM's product name.
- NEVER assume `expected_revenue` exists on `sale.order`; verify the correct field via `odoo_get_fields(model='sale.order')`.
- WHEN creating inherited tree views, verify the parent view exists via `odoo_get_view()` before writing the `<xpath>` element.
- ON inherited `ir.ui.view` records, always set `inherit_id` to reference the parent view's database ID, not its name.
- NEVER assume `last_time_contacted` exists on `res.partner`; verify the correct field via `odoo_get_fields(model='res.partner')`.
- BEFORE querying `crm.lead`, verify CRM module is installed via `odoo_list_models(keyword='crm')` — if uninstalled, score prospects via `sale.order` fields instead.
<!-- AUTO-CURATED-END -->
