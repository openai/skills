---
name: odoo-model-customize-demo
description: "Sandboxed Odoo model customization for learning, prototyping, and demos. Same operations as odoo-model-customize (set defaults, create custom fields, modify views, build automations, save filters) BUT every artifact is tagged as demo data so it can be cleanly rolled back. WHEN: try, demo, prototype, experiment, sandbox, learn, walk me through, test out, see how it works. DO NOT USE WHEN: the user is operating on a production database and wants real persistent changes — switch to odoo-model-customize."
license: MIT
metadata:
  author: oconsole
  version: "1.0.0"
  tier: demo
---

# Odoo Model Customize — Demo Mode

> **DEMO TAGGING IS MANDATORY.** Every record this skill creates or mutates MUST be identifiable as demo data so it can be found and removed. The `[DEMO]` prefix on names, the `x_demo_` prefix on custom fields, and the `.demo.` infix on views are non-negotiable. If you cannot tag the artifact, do not create it.

> **WHEN IN DOUBT, REFUSE.** This skill is for sandbox / demo / prototyping work. If the user is on a production database and wants permanent changes, stop and tell them to install the `odoo-skills-write` plugin and use the `odoo-model-customize` skill instead.

## Triggers

Activate this skill when the user wants to:
- Try out Odoo customization features without committing to anything
- See a demo of how custom fields, views, automations, or filters work
- Prototype an idea on a sandbox/demo Odoo instance
- Walk through what's possible at runtime without writing a module
- Experiment safely before promoting changes to production

## Compatibility — Odoo 18 and Odoo 19

Verified on **Odoo 18.0** and **Odoo 19.0**. The runtime customization API is identical between the two versions; the demo guardrails below apply equally to both. See `references/safety-boundary.md` for the version-by-version field reference.

---

## Demo Tagging Conventions

Every artifact you create gets a discriminator that makes it trivially findable later. Use these exact prefixes:

| Artifact | Convention | Example |
|---|---|---|
| Custom field on a model | `x_demo_<purpose>` (NOT `x_<purpose>`) | `x_demo_priority`, `x_demo_notes` |
| Inherited view | `<model>.<viewtype>.demo.<purpose>` | `res.partner.form.demo.priority_field` |
| Saved filter (`ir.filters`) | `[DEMO] <name>` | `[DEMO] Active Customers` |
| Automation (`base.automation`) | `[DEMO] <name>` | `[DEMO] Auto-tag VIPs` |
| Server action (`ir.actions.server`) | `[DEMO] <name>` | `[DEMO] Set priority high` |
| `ir.default` value | scope to a demo user or company if possible | `user_id=<demo_user>` |
| Window action mods | NEVER modify global window actions in demo mode — duplicate first or skip |

If a user asks to modify a global window action (`ir.actions.act_window`) in demo mode, REFUSE. Window actions are global UI state; mutating them in a demo session leaks into production. Direct them to the write tier or suggest creating a saved filter instead, which is per-user/scoped.

---

## Allowed vs Restricted Operations

| Operation | Demo mode? | How |
|---|---|---|
| Set field defaults via `ir.default` | ALLOWED, scope to a demo `user_id` if available | `odoo_set_default(model, field, value, user_id=<demo_user_id>)` |
| Create custom field on a model | ALLOWED with `x_demo_` prefix | `odoo_create("ir.model.fields", {name: "x_demo_priority", state: "manual", ...})` |
| Inherit a view to add a field | ALLOWED with `.demo.` infix in name | `odoo_create("ir.ui.view", {name: "res.partner.form.demo.priority", ...})` |
| Create a saved filter | ALLOWED with `[DEMO]` prefix | `odoo_create("ir.filters", {name: "[DEMO] Active VIPs", ...})` |
| Create an automated action | ALLOWED with `[DEMO]` prefix on both action and trigger | `odoo_create("base.automation", {name: "[DEMO] ...", ...})` |
| Modify a shared `ir.actions.act_window` | **REFUSED** — too global for demo mode | Suggest a saved filter instead |
| Delete production records | **REFUSED** | Demo mode never deletes user data |
| Change field types or rename fields | **REFUSED** — destructive and irreversible | — |

## Rules

1. **Discover first.** Always run `odoo_model_info(model)` before creating anything, exactly like the production skill.
2. **Tag every artifact** with the conventions above. No exceptions.
3. **Show the user the cleanup recipe** at the end of every session, so they know how to remove what you created.
4. **Confirm before deleting.** Even cleanup of demo records gets one confirmation.
5. **Never touch production-named records.** If a record matches the user's question but doesn't have a demo tag (e.g., they say "modify the Quotations action"), refuse and explain that demo mode operates on `[DEMO]`-tagged artifacts only.
6. **Verify after every write.** Re-read the record using a `[DEMO]`-anchored domain to confirm.

---

## Steps

| # | Action | Tool |
|---|--------|------|
| 1 | **Discover** — get model shape | `odoo_model_info` |
| 2 | **Plan the demo artifact** — pick a name with the demo prefix | — |
| 3 | **Create** — with the demo prefix baked in | `odoo_create` / `odoo_set_default` |
| 4 | **Verify** — re-read using a domain that matches the demo prefix | `odoo_search_read` |
| 5 | **Report** — show what was created and the cleanup recipe | — |

---

## Example: Add a "Priority" Custom Field on Demo

```
# 1. Get the model_id
odoo_model_info(model="res.partner")
# → ir.model id = 42

# 2. Create custom field with demo prefix
odoo_create(model="ir.model.fields", values={
    "model_id": 42,
    "name": "x_demo_priority",          # x_demo_, NOT x_
    "field_description": "[DEMO] Priority",
    "ttype": "selection",
    "state": "manual",
    "selection_ids": [
        [0, 0, {"value": "low",    "name": "Low",    "sequence": 1}],
        [0, 0, {"value": "medium", "name": "Medium", "sequence": 2}],
        [0, 0, {"value": "high",   "name": "High",   "sequence": 3}],
    ]
})

# 3. Add it to the form via a demo-named inherited view
odoo_create(model="ir.ui.view", values={
    "name": "res.partner.form.demo.priority",   # .demo. infix
    "model": "res.partner",
    "inherit_id": <base_partner_form_id>,
    "priority": 99,
    "arch": "<data><xpath expr=\"//field[@name='phone']\" position=\"after\"><field name=\"x_demo_priority\"/></xpath></data>"
})

# 4. Verify
odoo_search_read(model="ir.model.fields",
    domain=[["name","=","x_demo_priority"],["model","=","res.partner"]],
    fields=["name","field_description","ttype","state"],
    limit=1)
```

Then ALWAYS show the user the cleanup recipe.

---

## Cleanup Recipe (always show this at the end of a demo session)

To remove everything this demo session created, run these queries to find demo artifacts and delete them. Always confirm with the user before deleting.

```
# Custom fields with x_demo_ prefix
odoo_search_read(model="ir.model.fields",
    domain=[["name","=like","x_demo_%"],["state","=","manual"]],
    fields=["id","name","model","field_description"], limit=200)

# Inherited views with .demo. in the name
odoo_search_read(model="ir.ui.view",
    domain=[["name","like",".demo."]],
    fields=["id","name","model"], limit=200)

# Saved filters
odoo_search_read(model="ir.filters",
    domain=[["name","=like","[DEMO]%"]],
    fields=["id","name","model_id"], limit=200)

# Automations
odoo_search_read(model="base.automation",
    domain=[["name","=like","[DEMO]%"]],
    fields=["id","name","model_id"], limit=200)

# Server actions
odoo_search_read(model="ir.actions.server",
    domain=[["name","=like","[DEMO]%"]],
    fields=["id","name","model_id"], limit=200)
```

After confirming with the user, delete in this order (children first):

1. `base.automation` (depends on `ir.actions.server`)
2. `ir.actions.server`
3. `ir.ui.view` (so the field isn't referenced when deleted)
4. `ir.filters`
5. `ir.model.fields` (last — destroys the column data)

> **Cleanup of `ir.model.fields` is destructive** and removes the column from the database. Confirm explicitly with the user even in demo mode.

---

## What This Skill Does Not Cover

| Operation | Why | Where to go |
|---|---|---|
| Production model customization | Demo mode is sandbox-only | `odoo-skills-write` plugin → `odoo-model-customize` |
| Reading / inspecting / auditing data | No writes needed | `odoo-skills-read` plugin → `odoo-model-inspect` |
| Modifying global window actions | Bleeds into production state | Use a saved filter instead |
| Creating Python modules / Python inheritance | Runtime can't do this in any tier | Use the `odoo-19` development skill |
