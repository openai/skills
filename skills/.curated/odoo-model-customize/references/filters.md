# Default Filters and Grouping

> **Odoo 18 & 19:** `ir.actions.act_window.context` and `domain` are stored as Python-dict / Python-list **strings** in both versions (NOT JSON). `search_default_<filter_name>` and `group_by` context keys behave identically. The set of accepted context keys is the same in both versions.

## Via Window Actions (odoo_modify_action)

Window actions control what the user sees when they click a menu item. You can set:
- **domain** — default filter (which records to show)
- **context** — default groupby, search defaults, field defaults
- **limit** — records per page

### Add a default domain filter

Show only confirmed sale orders by default:

```
odoo_modify_action(model="sale.order", domain="[['state','=','sale']]")
```

### Add a default groupby

Group invoices by partner by default:

```
odoo_modify_action(model="account.move", context="{'group_by': 'partner_id'}")
```

### Add a search default

Auto-activate a search filter named "posted":

```
odoo_modify_action(model="account.move", context="{'search_default_posted': 1}")
```

### Combine multiple context keys

```
odoo_modify_action(
    model="sale.order",
    context="{'group_by': 'partner_id', 'search_default_my_sale_orders': 1, 'default_type': 'out_invoice'}"
)
```

### Change page size

```
odoo_modify_action(model="stock.picking", limit=200)
```

## Context Key Reference

| Key pattern | Effect |
|-------------|--------|
| `group_by` | Default grouping in list view |
| `search_default_FILTERNAME` | Auto-activate a search filter |
| `default_FIELDNAME` | Pre-fill a field when creating new records |
| `default_order` | Override the sort order |
| `active_id` / `active_ids` | Pass selected record context |

## Important Notes

- **Multiple actions per model**: A model can have several window actions (e.g., "Quotations" and "Sales Orders"). Each can have different filters.
- **List actions first**: Run `odoo_modify_action(model="sale.order")` with no changes to see all actions and pick the right one.
- **Context is a Python dict string**: Must be valid Python dict syntax, not JSON.
