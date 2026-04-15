# Modifying Views at Runtime (Inherited Views + XPath)

> **Odoo 18 & 19:** XPath inheritance via `ir.ui.view` records is stable across both versions. Available `position` values (`after`, `before`, `inside`, `replace`, `attributes`) are identical. The one historical wrinkle: in Odoo 17 list views became `<list>` in addition to the legacy `<tree>` tag — both 18 and 19 accept either name in inherited views, but generated XML defaults to `<list>`. When writing XPath, target the tag the parent view actually uses (read it via `odoo_get_view` first).

## How it Works

Odoo views can be extended by creating **inherited views** — new `ir.ui.view` records that point to a parent view via `inherit_id` and use XPath expressions to insert, replace, or remove elements. This is how Odoo Studio modifies views. No custom module needed.

## Step 1: Find the Base View

```
odoo_get_view(model="res.partner", view_type="form")
# Returns: {"view_id": 127, "arch": "<form>...", "fields_in_view": ["name", "phone", ...]}
```

The `view_id` (127) is what you'll use as `inherit_id`.

## Step 2: Create an Inherited View

### Add a field after another field

```
odoo_create(model="ir.ui.view", values={
    "name": "res.partner.form.custom.notes",
    "model": "res.partner",
    "inherit_id": 127,
    "priority": 99,
    "arch": "<data><xpath expr=\"//field[@name='phone']\" position=\"after\"><field name=\"x_internal_notes\"/></xpath></data>"
})
```

### Add a field before another field

```
"arch": "<data><xpath expr=\"//field[@name='email']\" position=\"before\"><field name=\"x_priority_level\"/></xpath></data>"
```

### Replace a field's attributes

```
"arch": "<data><xpath expr=\"//field[@name='phone']\" position=\"attributes\"><attribute name=\"required\">1</attribute></xpath></data>"
```

### Hide a field

```
"arch": "<data><xpath expr=\"//field[@name='function']\" position=\"attributes\"><attribute name=\"invisible\">1</attribute></xpath></data>"
```

### Add a new group/section

```
"arch": "<data><xpath expr=\"//group[@name='address']\" position=\"after\"><group string=\"Custom Info\"><field name=\"x_priority_level\"/><field name=\"x_internal_notes\"/></group></xpath></data>"
```

### Modify a tree/list view

```
# First get the tree view ID
odoo_get_view(model="sale.order", view_type="tree")
# Returns: {"view_id": 938, ...}

# Add a column
odoo_create(model="ir.ui.view", values={
    "name": "sale.order.tree.custom",
    "model": "sale.order",
    "inherit_id": 938,
    "priority": 99,
    "arch": "<data><xpath expr=\"//field[@name='name']\" position=\"after\"><field name=\"amount_untaxed\" optional=\"show\"/></xpath></data>"
})
```

## XPath Reference

| Expression | Matches |
|-----------|---------|
| `//field[@name='phone']` | The `<field name="phone"/>` element |
| `//group[@name='address']` | The `<group name="address">` element |
| `//page[@name='internal_notes']` | A notebook page |
| `//sheet` | The main form sheet |
| `//div[@class='oe_title']` | Title area |
| `//button[@name='action_confirm']` | A specific button |

| Position | Effect |
|----------|--------|
| `after` | Insert after the matched element |
| `before` | Insert before the matched element |
| `inside` | Insert as last child of the matched element |
| `replace` | Replace the matched element entirely |
| `attributes` | Modify attributes of the matched element |

## Rules

- **Always set priority=99** (or higher) — ensures your view loads after core views
- **Use `odoo_get_view` first** — you need the exact field names and structure
- **Name your views clearly** — e.g., `res.partner.form.custom.notes`
- **Never modify base views directly** — always create inherited views
- **XPath must match exactly one element** — if ambiguous, use a more specific path

## Removing a Custom View

```
# Find your custom view
odoo_search_read(model="ir.ui.view", domain=[["name","=","res.partner.form.custom.notes"]], fields=["id"], limit=1)

# Delete it
odoo_delete(model="ir.ui.view", ids=[VIEW_ID])
```
