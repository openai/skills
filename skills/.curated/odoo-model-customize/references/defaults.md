# Setting Field Defaults

> **Odoo 18 & 19:** the `ir.default` schema is **identical in both versions** — same columns (`field_id`, `user_id`, `company_id`, `condition`, `json_value`), same `set()` API, same JSON encoding. `ir.default` has **no `model_id` or `model` column** in either version, so to filter defaults by model you must traverse the `field_id` Many2one: `[["field_id.model_id.model","=",model_name]]` or the shorter `[["field_id.model","=",model_name]]` (the latter works because `ir.model.fields.model` is a stored Char in both versions).

## Using odoo_set_default

The safest and simplest way to set defaults. Handles JSON encoding and field lookup automatically.

### Set a global default

```
odoo_set_default(model="product.template", field_name="invoice_policy", value="delivery")
```

### Set a user-specific default

```
odoo_set_default(model="sale.order", field_name="warehouse_id", value=2, user_id=5)
```

### Set a company-specific default

```
odoo_set_default(model="sale.order", field_name="warehouse_id", value=3, company_id=1)
```

### Remove a default

```
odoo_set_default(model="product.template", field_name="invoice_policy", value=null)
```

## How it Works Internally

The tool:
1. Finds the `field_id` in `ir.model.fields` (validates the field exists)
2. JSON-encodes the value with `json.dumps()`
3. Searches `ir.default` for an existing default matching the field + user + company
4. Creates or updates the `ir.default` record
5. Returns before/after values for confirmation

## Value Types

| Field type | Example value | JSON stored as |
|-----------|---------------|----------------|
| Char/Text | `"hello"` | `"\"hello\""` |
| Integer | `42` | `"42"` |
| Float | `3.14` | `"3.14"` |
| Boolean | `true` | `"true"` |
| Selection | `"delivery"` | `"\"delivery\""` |
| Many2one | `5` | `"5"` (the record ID) |
| Date | `"2024-01-15"` | `"\"2024-01-15\""` |

## Common Pitfalls

- **Wrong field name**: Use `odoo_model_info` first to confirm the exact field name
- **Selection values**: Must match the technical key, not the label (e.g., `"delivery"` not `"Based on Delivered Quantity"`)
- **Many2one**: Pass the integer ID, not a name string
- **Existing default**: The tool handles update vs create automatically — no need to delete first


## Learned from Experience

Add section on reading current defaults before modification

**Location:** After "## Using odoo_set_default" header, before "### Set a global default"

**Add:**
```markdown
### Check current defaults first

Always inspect existing defaults before setting new ones:

```
odoo_model_info(model="sale.order")
// Returns "defaults": [{"field": "warehouse_id", "value": "2"}]

odoo_search_read("ir.default", 
  [["field_id.model", "=", "sale.order"]], 
  ["field_id.name", "json_value", "user_id", "company_id"])
```

This prevents accidentally overwriting user-specific or company-specific defaults with global ones.
```

**Rationale:** Agent episodes show successful default queries using `odoo_search_read` on `ir.default` with field traversal (`field_id.model`). The current documentation jumps straight to setting without mentioning discovery, which can lead to unintended overwrites.

---

##


## Learned from Experience

Add explicit note about field type constraints for defaults

**Location:** After "## How it Works Internally" section

**Add:**
```markdown

## Field Type Constraints

Not all field types support defaults via `ir.default`:
- **Supported:** char, text, integer, float, boolean, selection, date, datetime, many2one, many2many (as list of IDs)
- **Not supported:** One2many, computed fields, binary fields
- **Relational fields:** Pass the database ID (integer) as the value, not a record object

Example:
```
# ✓ Correct: many2one default uses ID
odoo_set_default(model="sale.order", field_name="warehouse_id", value=2)

# ✗ Wrong: passing a record object
odoo_set_default(model="sale.order", field_name="warehouse_id", value={"id": 2})
```
```

**Rationale:** Prevents type-mismatch errors when setting defaults on relational fields, which was an implicit failure mode in the episodes.
