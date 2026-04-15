---
name: odoo-system-inspect
description: "Inspect Odoo system health: modules, cron jobs, error logs, user activity. READ-ONLY. WHEN: health check, module status, cron stuck, error logs, installed modules, user login, dependencies, system diagnostics. DO NOT USE WHEN: the user wants to inspect stock, manufacturing, accounting, or model structure — use the domain-specific inspection skills instead."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: read
---

# Odoo System Inspect (read-only)

> **READ-ONLY.** This skill never calls mutating tools.

## Recipes

### Installed modules

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("ir.module.module", "search_read", [["state","=","installed"]], fields=[...], limit=500)`

```
odoo_search_read(
  model="ir.module.module",
  domain=[["state","=","installed"]],
  fields=["name","installed_version","summary"],
  limit=500)
```

> ALWAYS use `installed_version`, NEVER `version` — `version` is not a stored field on `ir.module.module`.
> NEVER filter on `installable` — use `state` instead.

### Module dependencies

**MCP tool:** `odoo_search_read` (two calls)
**Raw RPC:** `execute("ir.module.module.dependency", "search_read", ...)`

```
# Step 1: get the module id
odoo_search_read(model="ir.module.module",
  domain=[["name","=","sale"]],
  fields=["id","state","installed_version"], limit=1)

# Step 2: get its dependencies
odoo_search_read(model="ir.module.module.dependency",
  domain=[["module_id","=",MODULE_ID]],
  fields=["name","module_id"], limit=200)
```

> NEVER filter on `ir.module.module.dependency.state` — it is computed, not stored. Query the records and inspect client-side.
> NEVER wrap domain values in bare lists — use tuples: `[("state","in",["installed"])]` not `[("state","in",["installed"])]`.

### Cron job health

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("ir.cron", "search_read", ...)`

```
odoo_search_read(model="ir.cron",
  domain=[["active","=",True]],
  fields=["name","nextcall","interval_number","interval_type","state"],
  limit=200)
```

> NEVER use `numbercall` — removed in Odoo 16+. Use `nextcall` and `state`.
> NEVER use `last_call` — not a valid field. Verify via `odoo_get_fields(model='ir.cron')`.

### Recent error logs

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("ir.logging", "search_read", ...)`

```
# Compute the cutoff in Python first — NEVER use now() in domains
from datetime import datetime, timedelta
cutoff = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")

odoo_search_read(model="ir.logging",
  domain=[["level","=","ERROR"],["create_date",">",cutoff]],
  fields=["name","message","path","create_date"],
  limit=100, order="create_date desc")
```

> NEVER use `now()`, `%(today)s`, `%(date_start)s`, or any placeholder syntax in domain filters. Compute the date string in Python first, pass the literal ISO string.
> The field is `path` (Char), not `path_ids`.

### User login activity

**MCP tool:** `odoo_search_read`
**Raw RPC:** `execute("res.users", "search_read", ...)`

```
odoo_search_read(model="res.users",
  domain=[["active","=",True]],
  fields=["login","name","login_date"],
  limit=200, order="login_date desc")
```

> NEVER use `last_login` — it does not exist. The field is `login_date` (related to `log_ids.create_date`).
> NEVER filter ON `login_date` in a domain — it is a related field on a non-Many2one relation and cannot be converted to SQL. Fetch all active users and sort/filter client-side, or query `ir.logging` separately for login timestamps.
