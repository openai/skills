# Automated Actions (base.automation)

> **Odoo 18 & 19:** `base.automation` and `ir.actions.server` schemas are identical in both versions. Trigger types (`on_create`, `on_write`, `on_create_or_write`, `on_unlink`, `on_time`) are unchanged. `ir.actions.server.state` values (`object_write`, `email`, `followers`, `next_activity`, `code`, `multi`) are the same. The `code` action requires admin in both. Trigger field linkage uses the same `[[6, 0, [...]]]` Many2many command syntax in both.

## What They Are

Automated actions trigger server actions when records are created, updated, deleted, or based on a time condition. They're stored in `base.automation` and don't require a custom module.

## Prerequisites

The `base_automation` module must be installed. Check with:

```
odoo_search_read(model="ir.module.module", domain=[["name","=","base_automation"],["state","=","installed"]], fields=["name","state"], limit=1)
```

## Creating an Automated Action

### Step 1: Create a Server Action

The server action defines what happens when triggered.

```
# Get the model ID first
odoo_search_read(model="ir.model", domain=[["model","=","res.partner"]], fields=["id"], limit=1)
# Returns: {"records": [{"id": 42}]}

# Create a server action that updates a field
odoo_create(model="ir.actions.server", values={
    "name": "Set Priority to High for Large Companies",
    "model_id": 42,
    "state": "object_write",
    "update_field_id": FIELD_ID_OF_X_PRIORITY,
    "update_m2m_operation": "set",
    "value": "high"
})
```

### Step 2: Create the Automation Trigger

```
# Trigger when partner is created
odoo_create(model="base.automation", values={
    "name": "Auto-set priority for new partners",
    "model_id": 42,
    "trigger": "on_create",
    "action_server_ids": [[6, 0, [SERVER_ACTION_ID]]]
})

# Trigger when email field changes
odoo_create(model="base.automation", values={
    "name": "Log email changes",
    "model_id": 42,
    "trigger": "on_write",
    "trigger_field_ids": [[6, 0, [EMAIL_FIELD_ID]]],
    "action_server_ids": [[6, 0, [SERVER_ACTION_ID]]]
})
```

## Trigger Types

| Trigger | When it fires |
|---------|---------------|
| `on_create` | When a new record is created |
| `on_write` | When specified fields are modified |
| `on_create_or_write` | On both create and write |
| `on_unlink` | When a record is deleted |
| `on_time` | Based on a date field + interval |

## Server Action Types

| state | What it does |
|-------|-------------|
| `object_write` | Update field values on the record |
| `email` | Send an email |
| `followers` | Add/remove followers |
| `next_activity` | Schedule an activity |
| `code` | Execute Python code (requires admin) |
| `multi` | Run multiple actions in sequence |

## Common Use Cases

- **Auto-tag new records** — on_create → set a field value
- **Notify on changes** — on_write → send email
- **Escalation** — on_time (e.g., 3 days after create_date) → send email or update field
- **Data validation** — on_create_or_write → code action that checks conditions

## Listing Existing Automations

```
odoo_search_read(model="base.automation", domain=[], fields=["name","model_id","trigger","active"], limit=50)
```
