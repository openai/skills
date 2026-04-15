# Changing List Sort Order

> **Odoo 18 & 19:** the `default_order` mechanism on `ir.actions.act_window` works identically in both versions. `_order` remains a Python class attribute on the model in both — runtime override is via the window action only. Both versions also expose the model's `_order` value as the stored `order` Char on `ir.model`, so you can read it (you just can't write to it meaningfully).

## The Problem

Odoo's default sort order is defined by the `_order` attribute on the Python model class. For example, `sale.order` has `_order = "date_order desc, id desc"`. **This cannot be changed at runtime via RPC.**

## The Solution: Window Action `default_order`

Every menu item in Odoo points to a window action (`ir.actions.act_window`). You can set a `default_order` in the action's context, which overrides `_order` for that specific menu entry.

### Using odoo_modify_action

```
# List all window actions for a model
odoo_modify_action(model="sale.order")

# Change the sort order on a specific action
odoo_modify_action(action_id=312, order="name asc")

# Change sort on the first action for the model
odoo_modify_action(model="sale.order", order="amount_total desc")
```

### What happens internally

The tool sets `context['default_order']` on the `ir.actions.act_window` record. When Odoo loads the list view via this action, it uses `default_order` instead of the model's `_order`.

### Multiple actions, different sorts

A model can have multiple window actions (e.g., "Quotations" and "Sales Orders" for sale.order). Each can have a different default_order:

```
# Quotations: newest first
odoo_modify_action(action_id=312, order="create_date desc")

# Sales Orders: by amount
odoo_modify_action(action_id=313, order="amount_total desc, date_order desc")
```

## When the user asks to change _order

Explain:
1. `_order` is a Python class attribute — it can't be changed at runtime
2. The window action `default_order` achieves the same visible effect
3. If they truly need `_order` changed (affects all dropdowns and API calls), they need a custom module with `_inherit`

## Sort syntax

Same as Odoo's order syntax:
- `"name asc"` — ascending by name
- `"date_order desc, id desc"` — descending by date, then by ID
- `"partner_id, amount_total desc"` — ascending by partner, descending by amount


## Learned from Experience

Complete the truncated example and add multi-field sort guidance

**Location:** After "# Change sort" (line appears cut off)

**Replace incomplete section with:**
```markdown
### Using odoo_modify_action

```
# List all window actions for a model
odoo_model_info(model="sale.order")

# Change the sort order on a specific action
odoo_modify_action(action_id=312, order="date_order desc")

# Multi-field sort (evaluated left-to-right)
odoo_modify_action(action_id=312, order="state asc, date_order desc, id desc")
```

### Important: Field Names in `order`

- Use the **database field name** (e.g., `date_order`, not "Date Order")
- For related fields, use dot notation: `partner_id.name asc`
- Direction is optional; defaults to `asc` if omitted
- Separate multiple fields with commas and spaces
```

**Rationale:** Agent episodes show successful multi-field sorts (e.g., "state asc, date_order desc") but the current documentation cuts off mid-example. Agents need explicit guidance on field name syntax and related field sorting.

---

##


## Learned from Experience

Add warning about tree view sort order limitations

**Location:** After "## The Solution: Window Action `default_order`" heading, before the code example

**Add:**
```markdown

### Important: Tree View Sort Limitations

Tree views in Odoo have stricter sort field requirements than form views. A field must be:
- Present in the tree view's `<field>` elements
- Not a computed/non-stored field
- Not a One2many or Many2many relation

If `odoo_modify_action(order="field_name asc")` fails silently on a tree view action, verify the field exists in the tree view XML via `odoo_get_view(view_id)` before troubleshooting further.
```

**Rationale:** Prevents agents from debugging sort order issues on tree views without first checking field availability in the view definition.

---

##
