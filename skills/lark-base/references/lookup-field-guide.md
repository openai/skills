# Base Lookup Field Configuration Guide

## Mandatory Read Acknowledgement

When creating or updating a lookup field with `lark-cli base +field-create/+field-update --json ...` and `type` is `lookup`, you should read this guide first and only then add `--i-have-read-guide` to the command.

Do **not** proactively add `--i-have-read-guide` before reading this guide. Without it, the CLI will fail fast and direct you back to this guide.

## Default strategy

**Use Formula fields by default for cross-table references and aggregations.** Only use Lookup fields when the user explicitly requests a Lookup field. Formula is a strict superset of Lookup — anything Lookup can do, Formula can do with a single expression.

## Usage

When creating a lookup field, the Agent should:

1. Get all table names: `lark-cli base +table-list --base-token <base>` — returns `items[].table_name`
2. Get table structure: `lark-cli base +table-get --base-token <base> --table-id <table>` — returns `fields[]`
3. If the lookup references other tables, also get those tables' structures
4. Determine the four elements: from (source table), select (source field), where (filter), aggregate (aggregation)
5. Construct the Lookup field JSON and submit it to create or update the field

**Key constraints**:

- Table names and field names must **exactly match** those returned by `+table-list` / `+table-get`
- The `from` table must be in the same Base

---

## Section 1: Core Concepts — Four-Element Model

A Lookup field is defined by five fields:

| Field | Meaning | JSON key | Required |
|-------|---------|----------|----------|
| **type** | Must be `"lookup"` | `type` | Yes |
| **from** | Source table to pull data from | `from` | Yes |
| **select** | Field in the source table to retrieve | `select` | Yes |
| **where** | Filter conditions on the source table | `where` | Yes (at least one condition) |
| **aggregate** | How to aggregate multiple matching records | `aggregate` | No (default: `raw_value`) |

**SQL analogy**:

```
SELECT  [select field]
FROM    [from table]
WHERE   [filter conditions]
GROUP BY [aggregate function]
```

**Row-level matching (most important concept)**:

A Lookup field is computed row-by-row — for each row in the current table, it filters the source table to find "related" records. **The filter defines what "related" means.**

```
Current table row 1 → filter source table → matching records → select field → aggregate → result
Current table row 2 → filter source table → matching records → select field → aggregate → result
...
```

**Rule: Whenever the current table and the source table have a row-level correspondence (matching by some field value), you must specify a filter.**

---

## Section 2: Lookup vs Link vs Formula

Lookup and Link serve **different purposes**. Creating a Lookup does NOT require a Link field to exist first.

| Dimension | Link | Lookup | Formula |
|-----------|------|--------|---------|
| Purpose | Establish record relationships (read-write) | Pull and aggregate data from another table (read-only) | Compute values from expressions (read-only) |
| When to use | "link" / "associate" / "bind" two tables | "look up" / "reference" / "aggregate" / "count" from another table | Calculations, text manipulation, conditional logic |

**Common mistake**: Creating a Link field just to create a Lookup. If two tables share a matching text/number field, Lookup can match directly — no Link required.

**Selection decision tree**:

```
What does the user need?
├─ "Link"/"associate"/"bind" records between tables → Link
├─ "Look up"/"reference"/"aggregate"/"count" from another table → Lookup
│   ├─ Needs aggregation (sum/count/average)? → Lookup + aggregate
│   └─ Just reference a value? → Lookup (aggregate = null)
├─ Calculations/text manipulation within current table → Formula
└─ Access linked record's field → Prefer Lookup (more intuitive), or Formula chain access
```

---

## Section 3: Filter Condition Rules

**You must provide a `where` with at least one condition.** Improper conditions cause every row to pull all records from the source table.

### The Iron Rule: field belongs to source table

```
filter condition:
  field   → must be a field in the FROM table (source table)
  value   → constant or reference to a field in the CURRENT table
```

### How to find the matching field pair

**With a Link field (most common)**: The match is between the **Link field** and the **target table's primary field**.

```
Link is in the source table   → source.linkField matches current.primaryField
Link is in the current table  → source.primaryField matches current.linkField
```

**Without a Link field**: Two tables share a field with the same meaning — match directly.

### Where condition structure

Each condition is a **tuple** (array) of 2 or 3 elements: `[field, operator, value?]`

```json
{
  "logic": "and",
  "conditions": [
    ["<source table field>", "<operator>", { "type": "constant", "value": "<val>" }]
  ]
}
```

For `empty` / `non_empty`, the value can be omitted (2-element tuple):

```json
["<source table field>", "empty"]
```

### Two value formats

**Constant value** — for fixed conditions (e.g., "status is completed"):

```json
["状态", "==", { "type": "constant", "value": "已完成" }]
```

**Field reference** — for dynamic per-row matching (e.g., "match current row's project"):

```json
["项目名", "==", { "type": "field_ref", "field": "项目名" }]
```

**Decision guide**: Fixed condition (e.g., "status is completed") → `constant`. Dynamic condition (e.g., "match current record's project ID") → `field_ref`.

### Constant value format by field type

The `value` inside `{ "type": "constant", "value": ... }` varies by field type:

| Field type | Constant value format | Example |
|-----------|----------------------|---------|
| `text` | String | `"已完成"` |
| `number` | Number | `100`, `0.8` |
| `datetime` / `created_at` / `updated_at` | String | `"ExactDate(2025-01-01)"`, `"ExactDate(2025-01-01 09:30)"`, `"Today"`, `"Yesterday"`, `"Tomorrow"` |
| `select` (`multiple=false/true`) | Option name array | `["Todo"]`, `["Todo", "Done"]` |
| `link` | Record reference array | `[{ "id": "rec_xxx" }]`, `[{ "id": "rec_xxx" }, { "id": "rec_yyy" }]` |
| `user` / `created_by` / `updated_by` | User reference array | `[{ "id": "ou_xxx" }]`, `[{ "id": "ou_xxx" }, { "id": "ou_yyy" }]` |
| `checkbox` | Boolean | `true`, `false` |
| `attachment` / `location` | Only `empty` / `non_empty` | value must be `null` or omitted |
| `auto_number` | Not supported for constant comparison | Use dynamic field\_ref instead |
| `formula` / `lookup` (exact type) | Follow the underlying type rules | — |
| `formula` / `lookup` (fuzzy type) | String | `"some text"` |

**`datetime` notes**:
- Supported datetime constant values are `ExactDate(...)`, `Today`, `Yesterday`, `Tomorrow`
- Date-only fields use `ExactDate(YYYY-MM-DD)`
- Fields that include time use `ExactDate(YYYY-MM-DD HH:mm)`
- For complex or relative date filtering, consider using a Formula field instead

### Dynamic field reference — set comparison semantics

When using `{ "type": "field_ref", "field": "..." }`, values from both sides are first **converted to sets** at runtime, then compared using set operations:

- **`==`**: Sets are exactly equal (strict matching)
- **`intersects`**: Sets have a non-empty intersection (most commonly used)

**Conversion rules by field type**:

| Field type | Converted to |
|-----------|-------------|
| `text` | Single-element string set |
| `number` / `auto_number` / `datetime` | Single-element number set |
| `select` (`multiple=false/true`) | Set of option name strings |
| `user` / `created_by` / `updated_by` | Set of user name strings |
| `link` | Set of linked records' primary field string representations |
| `formula` / `lookup` | The computed value set |

**Examples**:
- User field `["name1", "name2"]` **intersects** text `"name1"` → true; **==** text `"name1"` → false (sets not equal)
- User field `["name1"]` **==** text `"name1"` → true (single-element sets are equal)
- Link field referencing records → converted to primary field strings, then compared

### Supported operators

| Operator | Meaning | Applicable field types |
|----------|---------|-----------------|
| `==` | Equal (exact match) | All types |
| `!=` | Not equal | All types |
| `>` | Greater than | `number`, `datetime` |
| `>=` | Greater than or equal | `number`, `datetime` |
| `<` | Less than | `number`, `datetime` |
| `<=` | Less than or equal | `number`, `datetime` |
| `intersects` | Has intersection (non-empty overlap) | All types (most commonly used for dynamic field\_ref) |
| `disjoint` | No intersection | All types |
| `empty` | Field is empty | All types (value must be null or omitted) |
| `non_empty` | Field is not empty | All types (value must be null or omitted) |

### Constraints

- **Only one level of and/or** — nesting (e.g., `{ and: [{ or: [...] }] }`) is not supported
- **At least one condition** — empty conditions array will error

---

## Section 4: Aggregate Rules

| Aggregate | Common user phrasing | Select field should be | Result type |
|-----------|---------------------|----------------------|-------------|
| `sum` | "total" / "sum" / "cumulative amount" | `number` field (e.g., amount) | Number |
| `average` | "average" / "mean" | `number` field | Number |
| `max` | "maximum" / "latest" / "most recent" | `number` / `datetime` field | Same as source |
| `min` | "minimum" / "earliest" | `number` / `datetime` field | Same as source |
| `counta` | "count" / "how many" / "total number" | Any field | Number |
| `unique_counta` | "count distinct" / "how many different" | Field to deduplicate | Number |
| `unique` | "list distinct" / "which ones" / "show different" | Field to display | List |
| `raw_value` | "list all" / "show all values" (default) | Field to display | List |

**Common confusion**: `unique` returns a **deduplicated list**, `unique_counta` returns a **count**. "Which categories are involved" → `unique`; "How many categories" → `unique_counta`.

**Important**:
- Enum values are **snake_case lowercase**: `sum` not `Sum`, `average` not `Average`
- **Count is `counta`, NOT `count`** — this is the most common enum mistake

---

## Section 5: Hard Constraints

1. **Always write a filter**: The `where` field is required with at least one condition. Whenever the current table and source table have row-level correspondence, the condition should express that relationship.
2. **Lookup fields are read-only**: Cell values cannot be manually set.
3. **Create Lookup after all dependent fields exist**: The source table and referenced fields must exist before creating the Lookup field.
4. **Source table must be in the same Base**: Cross-Base lookups are not supported.
5. **Changing `from` requires changing `select`**: Updating the source table without updating the select field will error.

---

## Section 6: Decision Trees

### How to build the filter

```
Step 1: Analyze the filtering semantics in the user's request
  "Count artworks per exhibition" → filter: belongs to exhibition = current exhibition
  "Sum completed order amounts"   → filter: status = completed AND project = current project

Step 2: Find the matching field pair
  ├─ Tables have a Link relationship?
  │   ├─ Link is in source table → source.linkField matches current.primaryField
  │   └─ Link is in current table → source.primaryField matches current.linkField
  ├─ Tables share same-meaning text/number field? → source.field matches current.field
  └─ Also need constant filtering? → AND combination
```

### Which aggregate?

```
How to handle multiple matching records?
├─ Show all values as-is → raw_value (default)
├─ Show deduplicated list → unique
├─ Sum → sum
├─ Average → average
├─ Maximum / minimum → max / min
├─ Count records → counta
└─ Count distinct → unique_counta
```

---

## Section 7: Common Configuration Patterns

> Patterns are categorized by **filter matching method**. Aggregate choice is independent — see Section 4.

### Pattern 1: Aggregate from a linked table (Link is in the source table)

**Scenario**: "Count artworks per exhibition", "Sum order amounts per project"

When the source table has a Link pointing to the current table:

```
Exhibition table: ExhibitionName (primaryField) ← current table
Artwork table: ArtworkName (primaryField), ← source table (Link is here)
                  Exhibition (Link → Exhibition table)
```

```json
{
  "type": "lookup",
  "name": "Artwork Count",
  "from": "Artwork table",
  "select": "ArtworkName",
  "aggregate": "counta",
  "where": {
    "logic": "and",
    "conditions": [
      ["Exhibition", "intersects", { "type": "field_ref", "field": "ExhibitionName" }]
    ]
  }
}
```

### Pattern 2: Reference a linked record's field (Link is in the current table)

**Scenario**: "Show supplier's contact person", "Display warehouse manager"

When the current table has a Link pointing to the source table:

```
Supplier table: SupplierName (primaryField), Contact (Text) ← source table
Inventory table: ProductName (primaryField), ← current table (Link is here)
                 Supplier (Link → Supplier table)
```

```json
{
  "type": "lookup",
  "name": "Supplier Contact",
  "from": "Supplier table",
  "select": "Contact",
  "where": {
    "logic": "and",
    "conditions": [
      ["SupplierName", "intersects", { "type": "field_ref", "field": "Supplier" }]
    ]
  }
}
```

### Pattern 3: Match by same-meaning field (no Link)

**Scenario**: "Sum order amounts per project" (tables share a "ProjectName" field but no Link)

```
Project table: ProjectName (primaryField) ← current table
Order table: OrderID (primaryField), ProjectName (Text), ← source table
               Amount (Number)
```

```json
{
  "type": "lookup",
  "name": "Order Total",
  "from": "Order table",
  "select": "Amount",
  "aggregate": "sum",
  "where": {
    "logic": "and",
    "conditions": [
      ["ProjectName", "==", { "type": "field_ref", "field": "ProjectName" }]
    ]
  }
}
```

### Pattern 4: Dynamic matching + constant filtering

**Scenario**: "Only count completed orders", "Only sum approved budgets"

Combine row-level matching with fixed-value filtering using `logic: "and"`:

```json
{
  "type": "lookup",
  "name": "Completed Order Amount",
  "from": "Order table",
  "select": "Amount",
  "aggregate": "sum",
  "where": {
    "logic": "and",
    "conditions": [
      ["Manager", "==", { "type": "field_ref", "field": "EmployeeName" }],
      ["Status", "==", { "type": "constant", "value": "Completed" }]
    ]
  }
}
```

### Pattern 5: Date filtering with constant value

**Scenario**: "Look up orders created after 2025-01-01", "Sum today's sales"

```json
{
  "type": "lookup",
  "name": "Recent Orders",
  "from": "Order table",
  "select": "Amount",
  "aggregate": "sum",
  "where": {
    "logic": "and",
    "conditions": [
      ["ProjectName", "==", { "type": "field_ref", "field": "ProjectName" }],
      ["CreatedDate", ">=", { "type": "constant", "value": "ExactDate(2025-01-01)" }]
    ]
  }
}
```

---

## Section 8: Anti-Pattern Collection

### Mistake 1: Omitting where (most common)

```json
// Wrong: no where, every row pulls all records
{ "type": "lookup", "name": "Artwork Count", "from": "Artwork table", "select": "ArtworkName", "aggregate": "counta" }

// Correct: where with Link relationship
{ "type": "lookup", "name": "Artwork Count", "from": "Artwork table", "select": "ArtworkName", "aggregate": "counta",
  "where": { "logic": "and", "conditions": [
    ["Exhibition", "intersects", { "type": "field_ref", "field": "ExhibitionName" }]
  ]}}
```

### Mistake 2: Wrong value type — confusing constant vs field_ref

```json
// Wrong: using constant for a dynamic join
["ProjectName", "==", { "type": "constant", "value": "ProjectName" }]

// Correct: use field_ref for dynamic per-row matching
["ProjectName", "==", { "type": "field_ref", "field": "ProjectName" }]
```

### Mistake 3: Using `count` instead of `counta`

```json
// Wrong
{ "aggregate": "count" }

// Correct
{ "aggregate": "counta" }
```

### Mistake 4: Wrong case for aggregate values

```json
// Wrong
{ "aggregate": "SUM" }
{ "aggregate": "Sum" }

// Correct — snake_case lowercase
{ "aggregate": "sum" }
{ "aggregate": "average" }
```

### Mistake 5: Nested where conditions

```json
// Wrong: nesting not supported
{ "logic": "and", "conditions": [
  { "logic": "or", "conditions": [...] }
]}

// Correct: only one level
{ "logic": "and", "conditions": [cond1, cond2, cond3] }
```

### Mistake 6: Confusing Lookup with Link

The user says "aggregate order amounts" — use Lookup, not Link. Link establishes relationships; Lookup retrieves and aggregates data.

### Mistake 7: Using object format instead of tuple for conditions

```json
// Wrong: object format
{ "fieldRef": "Status", "operator": "is", "value": { "type": "constant", "value": "Done" } }

// Correct: tuple format [field, operator, value?]
["Status", "==", { "type": "constant", "value": "Done" }]
```

### Mistake 8: Missing `type` field

```json
// Wrong: no type field
{ "name": "Total", "from": "Orders", "select": "Amount", "aggregate": "sum", "where": { ... } }

// Correct: must include type
{ "type": "lookup", "name": "Total", "from": "Orders", "select": "Amount", "aggregate": "sum", "where": { ... } }
```

---

## Section 9: Constraint Summary

- `type` must be `"lookup"` — this field is required in the request body
- `where` is required with at least one condition — always specify a filter
- Conditions use **tuple format**: `[field, operator, value?]` — NOT object format
- Lookup fields are read-only — values cannot be manually set
- Source table and referenced fields must exist before creating the Lookup
- Condition field (first element of tuple) must reference a field in the source table, not the current table
- Where supports only one level of and/or — no nesting
- Aggregate values are snake_case lowercase: `sum`, `counta`, `unique_counta` (NOT `count`)
- Operators: `==`, `!=`, `>`, `>=`, `<`, `<=`, `intersects`, `disjoint`, `empty`, `non_empty`
- Table and field names must exactly match `+table-get` output
- `datetime` constant values use string format: `ExactDate(YYYY-MM-DD)` / `ExactDate(YYYY-MM-DD HH:mm)` / `Today` / `Yesterday` / `Tomorrow`
- `select` constant values use option names;
- `link` / `user` constant values use `{id}` object arrays
