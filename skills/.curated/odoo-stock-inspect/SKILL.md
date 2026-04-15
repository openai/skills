---
name: odoo-stock-inspect
description: "Inspect Odoo inventory: stock levels, moves, transfers, quants, reordering rules, warehouse locations. READ-ONLY. WHEN: stock level, inventory, warehouse, quant, picking, transfer, reorder, negative stock, overdue delivery, stock move, reserved quantity. DO NOT USE WHEN: the user wants to create or modify stock records — use the write tier."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: read
---

# Odoo Stock Inspect (read-only)

> **READ-ONLY.** This skill never calls mutating tools.

## Recipes

### Current stock levels (by product)

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("stock.quant", "search_read", ...)`

```
odoo_search_read(model="stock.quant",
  domain=[["product_id","=",PRODUCT_ID],["location_id.usage","=","internal"]],
  fields=["product_id","location_id","quantity","reserved_quantity"],
  limit=200)
```

> `stock.quant` uses `quantity` and `reserved_quantity`. There is no `qty_available` field on `stock.quant` — that field lives on `product.product`.
> `product.product.qty_available` IS filterable in domains (it has a custom `_search` method), but `product.product.virtual_available` and `free_qty` may not be.

### Stock moves (recent activity)

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("stock.move", "search_read", ...)`

```
# Compute cutoff first
cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

odoo_search_read(model="stock.move",
  domain=[["product_id","=",PRODUCT_ID],["date",">",cutoff]],
  fields=["product_id","product_uom_qty","quantity","state","location_id","location_dest_id","reference"],
  limit=200, order="date desc")
```

> ON `stock.move`, the quantity field is `quantity` — NEVER use `quantity_done` (renamed in Odoo 17+).
> NEVER read `name` on `stock.move` for identification — use `reference` or `id`.
> NEVER use `now()` in domain filters — compute the date in Python first.

### Reordering rules (orderpoints)

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("stock.warehouse.orderpoint", "search_read", ...)`

```
odoo_search_read(model="stock.warehouse.orderpoint",
  domain=[["product_id","=",PRODUCT_ID]],
  fields=["name","product_id","product_min_qty","product_max_qty","qty_to_order","warehouse_id"],
  limit=50)
```

> The fields are `product_min_qty` and `product_max_qty` — NEVER use `qty_min` or `qty_max` (those don't exist).
> If you need the current on-hand qty to compare against the rule, read it from `product.product` or `stock.quant` separately.

### Overdue transfers

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("stock.picking", "search_read", ...)`

```
cutoff = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

odoo_search_read(model="stock.picking",
  domain=[["state","not in",["done","cancel"]],["scheduled_date","<",cutoff]],
  fields=["name","partner_id","scheduled_date","state","picking_type_id"],
  limit=100, order="scheduled_date asc")
```

### Stock move lines (lot/serial level)

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("stock.move.line", "search_read", ...)`

> NEVER use `qty_done` on `stock.move.line` in domain filters — verify the correct field via `odoo_get_fields(model='stock.move.line')`.

### Products with negative stock

```
odoo_search_read(model="stock.quant",
  domain=[["quantity","<",0],["location_id.usage","=","internal"]],
  fields=["product_id","location_id","quantity"],
  limit=100)
```

### Reconciliation pattern

When the user says "quant says X but I think we consumed more":

```
1. Read current quant level for the product + location
2. Read recent stock.move records for same product (last 30d)
3. Sum the `quantity` field by state (done vs assigned vs draft)
4. Compare totals — mismatches indicate unreserved or phantom moves
```
