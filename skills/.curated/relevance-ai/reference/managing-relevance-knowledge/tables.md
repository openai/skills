# Knowledge Tables Reference

Complete reference for knowledge table operations.

## Create Table

Use `relevance_create_knowledge_table` to create a table:

```
relevance_create_knowledge_table({
  name: "my-table-name"
})
```

Table names must be lowercase alphanumeric with hyphens or underscores.

Alternatively, tables are created **implicitly** when you add the first row via `relevance_add_knowledge_rows`.

## Add Rows

### Single Row

```
relevance_add_knowledge_rows({
  knowledge_set: "my-table",
  rows: [
    { name: "John", email: "john@example.com" }
  ]
})
```

### Multiple Rows

```
relevance_add_knowledge_rows({
  knowledge_set: "my-table",
  rows: [
    { name: "John", email: "john@example.com" },
    { name: "Jane", email: "jane@example.com" },
    { name: "Bob", email: "bob@example.com" }
  ]
})
```

Each row automatically gets a `document_id` (UUID).

## List Rows

### Basic List

```
relevance_list_knowledge_rows({
  knowledge_set: "my-table",
  page_size: 25,
  page: 1
})
```

### With Filters

```
relevance_list_knowledge_rows({
  knowledge_set: "my-table",
  page_size: 25,
  page: 1,
  filters: [
    {
      field: "domain",
      filter_type: "exact_match",
      condition_value: "acme.com"
    }
  ]
})
```

### Response Format

Row data is nested under the `data` field:

```json
{
  "results": [
    {
      "document_id": "uuid-1",
      "knowledge_set": "my-table",
      "data": {
        "name": "John",
        "email": "john@example.com"
      },
      "insert_date_": "2025-01-15T10:30:00Z"
    }
  ]
}
```

**Important:** Access fields via `row.data.name`, not `row.name`.

### Pagination

Use `page` and `page_size` parameters to paginate through results. Increment `page` to get the next set of rows. If the number of results returned equals `page_size`, there may be more pages.

## Update Rows

### Single Row Update

```
relevance_update_knowledge_rows({
  knowledge_set: "my-table",
  updates: [
    {
      document_id: "uuid-1",
      data: { status: "contacted", last_contact: "2025-01-15" }
    }
  ]
})
```

### Multiple Row Update

```
relevance_update_knowledge_rows({
  knowledge_set: "my-table",
  updates: [
    { document_id: "uuid-1", data: { status: "contacted" } },
    { document_id: "uuid-2", data: { status: "qualified" } },
    { document_id: "uuid-3", data: { status: "closed" } }
  ]
})
```

Updates are partial — only specified fields are changed.

## Delete Rows

```
relevance_delete_knowledge_rows({
  knowledge_set: "my-table",
  document_ids: ["uuid-1", "uuid-2"]
})
```

## Field Types

Knowledge tables are schema-less. Common field patterns:

```
{
  // Strings
  name: "John Doe",
  email: "john@example.com",

  // Numbers
  score: 85,
  price: 99.99,

  // Booleans
  is_active: true,

  // Arrays
  tags: ["lead", "enterprise"],

  // Objects
  address: {
    city: "San Francisco",
    state: "CA"
  },

  // Dates (as strings)
  created_at: "2025-01-15T10:30:00Z"
}
```

## Common Patterns

### Upsert Pattern

To upsert (update if exists, add if not):

1. Call `relevance_list_knowledge_rows` with a filter on the unique field (e.g., `email`)
2. If results are returned, call `relevance_update_knowledge_rows` with the `document_id` from the result
3. If no results, call `relevance_add_knowledge_rows` to create the row

### Get Table Info

Use `relevance_get_knowledge_table_info` to inspect a table's schema and metadata before operating on it.

### Get Single Row

Use `relevance_get_knowledge_row` when you know the exact `document_id` of the row you need.

## Tips

1. **Use descriptive table names** — `sales-leads` not `table1`
2. **Include timestamps** — Add `created_at`, `updated_at` fields
3. **Use consistent field names** — Stick to snake_case or camelCase
4. **Store IDs as strings** — For cross-referencing tables
5. **Batch large operations** — 50 rows per batch is a safe limit
6. **Remember data nesting** — Response rows have fields under `.data`, not at top level
