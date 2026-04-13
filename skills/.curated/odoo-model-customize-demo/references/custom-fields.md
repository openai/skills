# Creating Custom Fields at Runtime

> **Odoo 18 & 19:** `ir.model.fields` accepts identical create payloads in both versions. The `state="manual"` + `x_` prefix rules are unchanged. Selection field creation via `selection_ids` (a One2many to `ir.model.fields.selection`) works the same in both. The supported `ttype` values are identical.

## How it Works

Odoo allows creating "manual" fields at runtime by writing to `ir.model.fields`. These fields:
- **Must** have names starting with `x_`
- **Must** have `state = "manual"`
- Are immediately available for use in views and searches
- Survive module upgrades (they're stored in the database, not in Python code)
- This is exactly how Odoo Studio creates fields

## Creating a Custom Field

### Simple text field

```
# First, get the model's ir.model ID
odoo_search_read(model="ir.model", domain=[["model","=","res.partner"]], fields=["id"], limit=1)
# Returns: {"records": [{"id": 42}]}

# Create the field
odoo_create(model="ir.model.fields", values={
    "model_id": 42,
    "name": "x_internal_notes",
    "field_description": "Internal Notes",
    "ttype": "text",
    "state": "manual"
})
```

### Selection field

```
odoo_create(model="ir.model.fields", values={
    "model_id": 42,
    "name": "x_priority_level",
    "field_description": "Priority Level",
    "ttype": "selection",
    "state": "manual",
    "selection_ids": [
        [0, 0, {"value": "low", "name": "Low", "sequence": 1}],
        [0, 0, {"value": "medium", "name": "Medium", "sequence": 2}],
        [0, 0, {"value": "high", "name": "High", "sequence": 3}]
    ]
})
```

### Many2one (relational) field

```
odoo_create(model="ir.model.fields", values={
    "model_id": 42,
    "name": "x_project_id",
    "field_description": "Related Project",
    "ttype": "many2one",
    "relation": "project.project",
    "state": "manual"
})
```

## Supported Field Types

| ttype | Description | Extra params |
|-------|-------------|-------------|
| `char` | Short text | `size` (optional max length) |
| `text` | Long text | — |
| `integer` | Whole number | — |
| `float` | Decimal number | `digits` (optional precision) |
| `boolean` | True/False | — |
| `date` | Date only | — |
| `datetime` | Date + time | — |
| `selection` | Dropdown | `selection_ids` (required) |
| `many2one` | Link to another record | `relation` (target model name) |
| `many2many` | Multiple links | `relation` (target model name) |
| `binary` | File upload | — |
| `html` | Rich text | — |

## After Creating the Field

The field exists in the database but is **not visible in any view** until you add it. See [View Inheritance Guide](view-inheritance.md) to add it to a form or tree view.

## Deleting a Custom Field

```
# Find the field
odoo_search_read(model="ir.model.fields", domain=[["model","=","res.partner"],["name","=","x_internal_notes"]], fields=["id"], limit=1)

# Delete it (WARNING: destroys all data in that field)
odoo_delete(model="ir.model.fields", ids=[FIELD_ID])
```

## Rules

- **Always use x_ prefix** — fields without it are rejected
- **Always set state='manual'** — this marks it as user-created
- **Verify the model_id** — use odoo_model_info to get the correct ir.model ID
- **Selection values must have both value and name** — value is the technical key, name is the display label
