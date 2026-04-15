# Model Discovery Guide

## Step 1: Get the Full Picture

Always start with `odoo_model_info(model)` before making any changes. This returns:

```json
{
  "model": "sale.order",
  "name": "Sales Order",
  "default_order": "date_order desc, id desc",
  "rec_name": "name",
  "field_count": 148,
  "fields_by_type": {"many2one": 25, "char": 18, "float": 12, ...},
  "custom_fields": [{"name": "x_notes", "type": "text", "label": "Internal Notes"}],
  "relational_fields": [{"name": "partner_id", "type": "many2one", "target": "res.partner"}],
  "required_fields": [{"name": "partner_id", "type": "many2one", "label": "Customer"}],
  "views": [{"id": 944, "name": "sale.order.form", "type": "form", "priority": 16}],
  "actions": [{"id": 312, "name": "Quotations", "domain": "...", "context": "..."}],
  "defaults": [{"field": "invoice_policy", "value": "\"order\""}]
}
```

## Step 2: Understand What You're Working With

| Field in response | What it tells you |
|-------------------|-------------------|
| `default_order` | Current `_order` — **cannot change at runtime** |
| `rec_name` | Field used for display name in dropdowns |
| `custom_fields` | Existing x_ fields already on the model |
| `required_fields` | Fields that are required at model level |
| `views` | Base views — use their IDs for `inherit_id` |
| `actions` | Window actions — use their IDs for `odoo_modify_action` |
| `defaults` | Current ir.default values (JSON-encoded) |

## Step 3: Get View Details (when modifying views)

```
odoo_get_view(model="sale.order", view_type="form")
```

Returns the **merged** XML after all inheritance. Use this to:
- Find the field names used in the view
- Identify where to insert new fields (XPath targets)
- See what's already visible/hidden

## Step 4: Get Field Details (when adding/querying fields)

```
odoo_get_fields(model="sale.order")
```

Returns all field definitions with type, required, readonly, help text. Use this to:
- Find the exact field name (not the label)
- Check field type before setting a default
- Identify relational field targets

## Odoo 18 / 19 Notes for Discovery

| Item | Odoo 18 | Odoo 19 |
|---|---|---|
| `ir.model.order` (stored mirror of `_order`) | Available — safe to read | Available — safe to read |
| `ir.model.rec_name` | **Does not exist** — never request it | **Does not exist** — never request it |
| `ir.model.abstract` | Does not exist — querying it errors | Available |
| `ir.model.fold_name` | Does not exist — querying it errors | Available |

**Safe `ir.model` query that works on BOTH versions:**

```python
odoo_search_read(
    model="ir.model",
    domain=[["model", "=", target_model]],
    fields=["name", "model", "order", "state", "transient"],
    limit=1,
)
```

**To get `_rec_name`** (since it isn't stored anywhere queryable), inspect `ir.model.fields` for the model and pick `"name"` if it exists, otherwise `"x_name"`, otherwise `"id"`. This is exactly what Odoo itself does.


## Learned from Experience

Add Step 3.5 for action discovery before modification

**Location:** After "Step 3: Get View Details" section header (currently incomplete)

**Add:**
```markdown
## Step 3.5: Get Action Details (when modifying sort/filter/context)

Before calling `odoo_modify_action()`, always retrieve the action ID:

```json
odoo_model_info(model)  // Returns "actions" array with IDs
```

Use the returned `actions[].id` to target the specific menu entry. If multiple actions exist for the same model, verify you're modifying the correct one by checking the `name` field (e.g., "Quotations" vs "All Sales Orders").

**Example:**
```
// From odoo_model_info("sale.order"), you get:
// "actions": [{"id": 312, "name": "Quotations", ...}, {"id": 313, "name": "All Orders", ...}]

// Modify only the "Quotations" action:
odoo_modify_action(action_id=312, order="date_order desc")
```
```

**Rationale:** Agent episodes show that `odoo_modify_action(model=...)` without an action_id can be ambiguous when multiple actions exist. Explicit action_id targeting is safer and more predictable.

---

##


## Learned from Experience

Expand Step 3 with view-specific discovery guidance

**Location:** After "## Step 3: Get View Details (when modifying views)" (currently incomplete)

**Replace incomplete section with:**
```markdown
## Step 3: Get View Details (when modifying views)

`odoo_get_view(view_id)` returns the full XML definition. **Always call this before creating an inherited view.**

```json
{
  "id": 944,
  "name": "sale.order.form",
  "type": "form",
  "priority": 16,
  "arch": "<form>...</form>",
  "fields": {
    "name": {"type": "char", "string": "Order Reference"},
    "partner_id": {"type": "many2one", "relation": "res.partner"}
  }
}
```

**Critical:** Tree views expose only a subset of model fields. Check the `fields` dict in the response — if a field is not listed, it **cannot be added to that tree view** even via inheritance. Use `odoo_model_info()` to see all fields, then cross-reference with `odoo_get_view()` to see which are available in the specific view type.
```

**Rationale:** The tree view failure shows agents didn't understand that view-level field availability differs from model-level availability. This bridges that gap with concrete discovery steps.

---

##
