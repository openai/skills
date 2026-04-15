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

Complete the truncated "Common Pitfalls" section and add a troubleshooting guide.

```markdown
## Common Pitfalls

- **Wrong field name**: Use `odoo_model_info` first to confirm the exact field name
- **Selection values**: Must match the exact selection key (e.g., `"delivery"` not `"Delivery"`)
- **Many2one IDs**: Use the record ID, not the display name. Verify with `odoo_search_read` first
- **Date format**: Use ISO format `"YYYY-MM-DD"` for date fields
- **Null vs empty string**: `null` removes the default; `""` sets an empty string default
- **User/company context**: Defaults are scoped—a user-specific default overrides global, company-specific overrides global

## Troubleshooting

**Default not appearing in form?**
- Check if the field has a hardcoded default in the model's Python code (takes precedence)
- Verify the field name matches exactly (case-sensitive)
- Confirm the user/company context matches where you're testing

**Value looks wrong in database?**
- Use `odoo_search_read("ir.default", [["field_id.name", "=", "your_field"]])` to inspect the raw JSON
- The value is stored JSON-encoded; `"5"` (string) is correct for many2one, not `5` (integer)
```

---

##


## Learned from Experience

Complete the truncated "Common Pitfalls" section and add troubleshooting guidance

```markdown
## Common Pitfalls

- **Wrong field name**: Use `odoo_model_info` first to confirm the exact field name
- **Selection values**: Must match the exact string defined in the field's `selection` parameter. Use `odoo_get_fields(model)` to see valid options.
- **Many2one IDs**: Always use the record ID, not the display name. Verify the ID exists with `odoo_search_read`.
- **Relational fields**: Cannot set defaults for one2many or many2many fields via `ir.default`. Use server actions or automated actions instead.
- **User/company context**: If `user_id` or `company_id` is specified, the default only applies to that user/company. Omit both for a global default.

## Troubleshooting

**Default not appearing in form:**
- Check if the field is already set on the record (defaults only apply to new records)
- Verify the user/company context matches where you're testing
- Use `odoo_search_read("ir.default", domain=[("field_id.name", "=", "field_name")])` to confirm the default was created

**"Field not found" error:**
- Run `odoo_model_info(model)` and check the `custom_fields` and `fields_by_type` sections
- Ensure you're using the exact field name (case-sensitive)
- Custom fields must start with `x_`
```

---

##
