---
name: odoo-mrp-inspect
description: "Inspect Odoo manufacturing: bills of materials, manufacturing orders, production status, component availability, throughput KPIs. READ-ONLY. WHEN: manufacturing order, MO, BoM, bill of materials, production, component, raw material, work center, WIP, throughput, scrap, capacity, where-used, finished goods. DO NOT USE WHEN: creating or modifying MOs, BoMs, or production records — use the write tier."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: read
---

# Odoo MRP Inspect (read-only)

> **READ-ONLY.** This skill never calls mutating tools.
> **BEFORE any MRP query**, verify the Manufacturing module is installed: `odoo_list_models(keyword='mrp')`. If `mrp.production` doesn't appear, the module is not installed — explain this to the user.

## Key field names (Odoo 17+)

| Model | Wrong name | Correct name |
|---|---|---|
| `mrp.production` | `date_planned_start` | `date_start` |
| `mrp.production` | `scheduled_start_date` | `date_start` |
| `mrp.production` | `name` in `create()` | Auto-generated — do not pass |
| `mrp.bom` | `name` | No `name` field — use `product_tmpl_id.name` or `code` |

## Recipes

### Manufacturing order status

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("mrp.production", "search_read", ...)`

```
odoo_search_read(model="mrp.production",
  domain=[["state","in",["confirmed","progress"]]],
  fields=["name","product_id","product_qty","state","date_start","date_finished","origin"],
  limit=100, order="date_start asc")
```

> The field is `date_start` — NEVER use `date_planned_start` or `scheduled_start_date`.
> States: `draft` → `confirmed` → `progress` → `to_close` → `done` / `cancel`.

### Stuck MOs (confirmed, no reservation, old)

```
cutoff = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")

odoo_search_read(model="mrp.production",
  domain=[["state","=","confirmed"],["date_start","<",cutoff]],
  fields=["name","product_id","product_qty","date_start","reservation_state"],
  limit=100, order="date_start asc")
```

> `reservation_state` shows whether components are reserved: `confirmed` (not reserved), `assigned` (ready), `waiting` (partially).

### BoM lookup

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("mrp.bom", "search_read", ...)`

```
# Find the BoM for a product
odoo_search_read(model="mrp.bom",
  domain=[["product_tmpl_id","=",TEMPLATE_ID]],
  fields=["id","product_tmpl_id","product_qty","code","type"],
  limit=5)

# Get its lines (components)
odoo_search_read(model="mrp.bom.line",
  domain=[["bom_id","=",BOM_ID]],
  fields=["product_id","product_qty"],
  limit=200)
```

> `mrp.bom` has no `name` field. Use `code` (if set) or `product_tmpl_id` for identification.
> `mrp.bom.type`: `"normal"` = manufactured, `"phantom"` = kit (explodes in SO, no MO created).

## BoM recursion playbook

### "Where is component X used?" — bottom-up

```
1. Resolve X to a product.product id
2. Find every mrp.bom.line with product_id = X:
     odoo_search_read(model="mrp.bom.line",
       domain=[["product_id","=",X_ID]],
       fields=["bom_id","product_qty"], limit=200)
3. Batch-read the parent BoMs:
     bom_ids = unique [line["bom_id"][0] for line in step 2]
     odoo_search_read(model="mrp.bom",
       domain=[["id","in",bom_ids]],
       fields=["id","product_tmpl_id","product_qty","code","type"])
4. Recurse: for each parent template, repeat from step 2.
   Stop after 4 levels or when no new BoMs found.
   Track visited template_ids to avoid cycles.
```

### "Walk the BoM for product Y" — top-down

```
1. Get the top BoM for the product template
2. Get its lines (mrp.bom.line with bom_id = BOM_ID)
3. For each line product, batch-lookup whether it has its own BoM:
     odoo_search_read(model="mrp.bom",
       domain=[["product_tmpl_id","in",line_template_ids]],
       fields=["id","product_tmpl_id","product_qty"])
4. Recurse on components that have BoMs.
   Multiply qty through each level: parent_qty × child_qty.
   Aggregate leaf totals by product_id.
```

> ALWAYS batch-fetch BoMs in step 3 — one call with `("id","in",ids)`, NOT one call per line.
> Skip `phantom` (kit) BoMs — they explode but produce no MO.

### Feasibility check ("Can we make N units?")

```
1. Walk the BoM top-down for N units (get leaf-level qtys)
2. For each leaf component, read stock.quant:
     odoo_search_read(model="stock.quant",
       domain=[["product_id","=",COMP_ID],["location_id.usage","=","internal"]],
       fields=["quantity","reserved_quantity"])
3. available = sum(quantity - reserved_quantity)
4. The gating constraint = min(available / required_qty) across all components
```

### Throughput / OTD

```
# Finished MOs in a time window
cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

odoo_search_read(model="mrp.production",
  domain=[["state","=","done"],["date_finished",">",cutoff]],
  fields=["product_id","product_qty","date_start","date_finished"],
  limit=500, order="date_finished desc")

# On-time = date_finished <= date_start + planned_duration
# Late = date_finished > planned end
```
