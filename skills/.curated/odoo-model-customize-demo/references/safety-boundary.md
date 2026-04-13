# Safety Boundary: Runtime-Safe vs Module-Required

> **Verified on Odoo 18.0 and Odoo 19.0.** The runtime-safe and module-required boundaries below apply identically to both versions — no model-customization operations were added or removed between 18 and 19. The only schema additions on `ir.model` in 19 (`abstract`, `fold_name`) are read-only and don't change what you can or can't customize at runtime.

## Runtime-Safe Operations (via RPC — no module needed)

| What | How | Model |
|------|-----|-------|
| Set field defaults | `odoo_set_default(model, field, value)` | ir.default |
| Change list sort order | `odoo_modify_action(model, order="field desc")` | ir.actions.act_window |
| Add default domain filter | `odoo_modify_action(model, domain="[...]")` | ir.actions.act_window |
| Add default groupby | `odoo_modify_action(model, context="{'group_by':'field'}")` | ir.actions.act_window |
| Change page size | `odoo_modify_action(model, limit=200)` | ir.actions.act_window |
| Create custom fields | `odoo_create("ir.model.fields", {name: "x_...", ...})` | ir.model.fields |
| Add field to form/tree view | Create inherited ir.ui.view with XPath | ir.ui.view |
| Hide/show fields in views | Inherited view with `invisible="1"` | ir.ui.view |
| Make field visually required | Inherited view with `required="1"` | ir.ui.view |
| Create saved search filters | `odoo_create("ir.filters", {...})` | ir.filters |
| Automated actions | `odoo_create("base.automation", {...})` | base.automation |
| Server actions | `odoo_create("ir.actions.server", {...})` | ir.actions.server |
| Record access rules | `odoo_create("ir.rule", {...})` | ir.rule |

## Module-Required Operations (need Python code)

| What | Why it can't be done via RPC |
|------|------------------------------|
| Change `_order` | Python class attribute set at class definition time. Not a DB field. |
| Override `create()`, `write()`, `unlink()` | Requires Python method override via `_inherit` |
| Override `name_get()` / `_compute_display_name()` | Python method on the model class |
| Add stored computed fields | Needs `compute="method_name"` + `store=True` in Python |
| Add `@api.constrains` | Python decorator, runs server-side validation |
| Add `@api.onchange` | Python decorator, runs in form view on field change |
| Change field `type` | Field type is set at module install, altering it corrupts data |
| Make a standard field `required` at model level | Python class attribute, not just a view attribute |
| Add SQL constraints | `models.Constraint(...)` in Python class |

## Decision Flow

```
User wants to customize something
    │
    ├── Default value? → odoo_set_default (SAFE)
    ├── Sort order? → odoo_modify_action with order (SAFE)
    ├── Filter/groupby? → odoo_modify_action with domain/context (SAFE)
    ├── Add a field? → x_ field via ir.model.fields (SAFE)
    ├── Show/hide field in view? → inherited ir.ui.view (SAFE)
    ├── Trigger on record change? → base.automation (SAFE)
    ├── Change _order? → NEEDS MODULE (suggest window action instead)
    ├── Override create/write? → NEEDS MODULE
    ├── Stored computed field? → NEEDS MODULE (suggest x_ + automation)
    └── Add constraint? → NEEDS MODULE (suggest automation for soft check)
```


## Learned from Experience

Complete the truncated "Module-Required Operations" section and add clarification about when RPC truly cannot work.

```markdown
## Module-Required Operations (need Python code)

| What | Why it can't be done via RPC |
|------|------------------------------| 
| Change `_order` | Python class attribute set at class definition time. Not stored in database—only readable via `default_order` override on actions. |
| Add computed fields | Requires `@api.depends()` decorator and Python method. Cannot be created via RPC. |
| Add relational field constraints | Requires `_sql_constraints` or domain logic in Python. |
| Override model methods | Requires Python inheritance (`_inherit`). |
| Add field validation logic | Requires `@api.constrains()` or `@api.onchange()` decorators. |
| Change field `compute` function | Requires Python method definition. |

**Key principle**: If it requires Python decorators, class attributes, or method definitions, it needs a module. Use RPC only for data-layer changes (records, views, actions, rules).
```

---

##


## Learned from Experience

Add missing entries to the Module-Required Operations table with specific examples

```markdown
## Module-Required Operations (need Python code)

| What | Why it can't be done via RPC |
|------|------------------------------|
| Change `_order` | Python class attribute set at class definition time. Not stored in database. |
| Add computed fields | Requires `@api.depends()` decorator and Python method definition. |
| Add relational fields (one2many, many2many) | Requires reverse relation setup and Python class attributes. |
| Change field type | Field type is immutable after creation; would require database migration. |
| Add field constraints | `_sql_constraints` and `@api.constrains()` are Python-only. |
| Override model methods | Methods like `create()`, `write()`, `unlink()` must be defined in Python. |
| Add field dependencies | `@api.depends()` decorators cannot be added via RPC. |
| Change model inheritance | `_inherit` is a class attribute set at module load time. |
```

---

##
