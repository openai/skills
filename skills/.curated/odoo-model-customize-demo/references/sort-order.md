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

Add a section on discovering which action to modify and handling multiple actions.

```markdown
## Finding the Right Action to Modify

A model may have multiple window actions. Use `odoo_model_info` to list them:

```json
"actions": [
  {"id": 312, "name": "Quotations", "domain": "[('state','=','draft')]"},
  {"id": 313, "name": "Sales Orders", "domain": "[]"}
]
```

Each action can have its own sort order. **Modify the specific action ID**, not the model:

```
# Wrong: affects only the first action
odoo_modify_action(model="sale.order", order="amount_total desc")

# Right: affects the specific action
odoo_modify_action(action_id=312, order="amount_total desc")
```

### Verify the change took effect

```
odoo_model_info(model="sale.order")
# Check the "actions" array — the modified action should now show your new order
```

## Limitations

- `default_order` only affects **list views** opened via that action
- Form views, kanban views, and other view types ignore `default_order`
- If a user manually sorts the list, their choice overrides `default_order` for that session
```

---

##


## Learned from Experience

Add section on discovering which action to modify and clarify the relationship between multiple actions

```markdown
## Finding the Right Action to Modify

Use `odoo_model_info(model)` to list all window actions:

```json
"actions": [
  {"id": 312, "name": "Quotations", "domain": "[('state','in',['draft','sent'])]"},
  {"id": 313, "name": "Sales Orders", "domain": "[]"},
  {"id": 314, "name": "All Orders", "domain": "[]"}
]
```

Each action corresponds to a menu item. Modify the specific action ID for the menu you want to change:

```
# Change sort only for the "Quotations" menu
odoo_modify_action(action_id=312, order="date_order asc")

# Change sort for the first/default action
odoo_modify_action(model="sale.order", order="amount_total desc")
```

## Important: Action-Specific Changes

- Changes via `odoo_modify_action` only affect that specific menu/action
- The model's `_order` remains unchanged (still visible in `odoo_model_info`)
- Different menu items can have different sort orders
- If no action is specified, the first action for the model is modified
```
