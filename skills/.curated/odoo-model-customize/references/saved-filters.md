# Saved Filters (ir.filters)

> **Odoo 18 & 19:** the `ir.filters` schema is identical in both versions. `model_id` accepts the technical model name as a string (it's effectively a Char/reference, not a Many2one to `ir.model`). `domain`, `context`, and `sort` are stored as Python-syntax strings — same in both.

## What They Are

Saved filters appear in the search bar's "Favorites" section. They store a domain filter, optional groupby, and sort order. Users can create them via the UI, or you can create them programmatically.

## Creating a Saved Filter

### Shared filter (visible to all users)

```
odoo_create(model="ir.filters", values={
    "name": "Confirmed Orders This Month",
    "model_id": "sale.order",
    "domain": "[['state','=','sale'],['date_order','>=','2024-01-01']]",
    "user_id": false,
    "is_default": false
})
```

### Personal filter (one user only)

```
odoo_create(model="ir.filters", values={
    "name": "My Open Tasks",
    "model_id": "project.task",
    "domain": "[['user_ids','in',[USER_ID]],['stage_id.fold','=',false]]",
    "user_id": USER_ID,
    "is_default": false
})
```

### Filter with groupby and sort

```
odoo_create(model="ir.filters", values={
    "name": "Invoices by Customer",
    "model_id": "account.move",
    "domain": "[['move_type','=','out_invoice'],['state','=','posted']]",
    "context": "{'group_by': 'partner_id'}",
    "sort": "['amount_total desc']",
    "user_id": false,
    "is_default": false
})
```

### Default filter (auto-applied on page load)

```
odoo_create(model="ir.filters", values={
    "name": "Active Products",
    "model_id": "product.template",
    "domain": "[['active','=',true],['sale_ok','=',true]]",
    "user_id": false,
    "is_default": true
})
```

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name in Favorites |
| `model_id` | string | Technical model name (e.g., "sale.order") |
| `domain` | string | Filter domain (Python list syntax) |
| `context` | string | Optional context with group_by |
| `sort` | string | Sort order as Python list |
| `user_id` | int/false | False = shared, int = personal |
| `is_default` | bool | Auto-apply when loading the view |

## Listing Existing Filters

```
odoo_search_read(model="ir.filters", domain=[["model_id","=","sale.order"]], fields=["name","domain","context","sort","user_id","is_default"])
```
