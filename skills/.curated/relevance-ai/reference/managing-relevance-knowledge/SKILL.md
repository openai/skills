---
name: managing-relevance-knowledge
description: Manages Relevance AI knowledge tables - creating tables, adding rows, querying data, and bulk updates. Use when working with knowledge tables, CRM data, or agent data storage.
---

# Managing Relevance AI Knowledge

Skill for managing knowledge tables - CRM-like data storage for agents.

> **Full API Documentation:** If MCP tools don't cover your use case, see `https://api-{region}.stack.tryrelevance.com/latest/documentation` (replace `{region}` with your project's region)

## When to Use

- Creating knowledge tables for data storage
- Adding, updating, or deleting rows
- Querying table data
- Setting up data for agent workflows

## Overview

Knowledge tables are CRM-like data stores that agents can read from and write to. They're useful for:

- Contact lists
- Lead tracking
- Research data
- Agent memory/context

## Available MCP Tools

| Tool                                 | Description                                   |
| ------------------------------------ | --------------------------------------------- |
| `relevance_create_knowledge_table`   | Create a new knowledge table                  |
| `relevance_add_knowledge_rows`       | Add rows to a table                           |
| `relevance_list_knowledge_rows`      | List/query rows with filtering and pagination |
| `relevance_get_knowledge_row`        | Get a single row by ID                        |
| `relevance_get_knowledge_table_info` | Get table schema and metadata                 |
| `relevance_update_knowledge_rows`    | Update existing rows                          |
| `relevance_delete_knowledge_rows`    | Delete rows from a table                      |

## Quick Start

### Create a Table + Add Data

1. Create the table:

```
relevance_create_knowledge_table({
  name: "my-contacts"
})
```

2. Add rows:

```
relevance_add_knowledge_rows({
  knowledge_set: "my-contacts",
  rows: [
    { name: "John", email: "john@example.com", company: "Acme" },
    { name: "Jane", email: "jane@example.com", company: "Tech Co" }
  ]
})
```

### Query Data

```
relevance_list_knowledge_rows({
  knowledge_set: "my-contacts",
  page_size: 25,
  page: 1
})
```

**Note:** Row data is nested under the `data` field in responses: `row.data.name`, not `row.name`.

### Update Rows

```
relevance_update_knowledge_rows({
  knowledge_set: "my-contacts",
  updates: [
    { document_id: "uuid-1", data: { status: "contacted", last_contact: "2025-01-15" } }
  ]
})
```

Updates are partial — only specified fields are changed.

### Delete Rows

```
relevance_delete_knowledge_rows({
  knowledge_set: "my-contacts",
  document_ids: ["uuid-1", "uuid-2"]
})
```

## Reference Files

- [tables.md](tables.md) - Field types, filtering, response format, common patterns

## Use Cases

### Lead Management

Store and track sales leads:

```
relevance_add_knowledge_rows({
  knowledge_set: "leads",
  rows: [
    { company: "Acme", contact: "John", status: "new", score: 85 }
  ]
})
```

### Agent Memory

Store conversation context for agents:

```
relevance_add_knowledge_rows({
  knowledge_set: "agent-memory",
  rows: [
    {
      user_id: "user-123",
      preferences: { timezone: "PST", language: "en" },
      last_topic: "product pricing"
    }
  ]
})
```

### Research Results

Store research findings:

```
relevance_add_knowledge_rows({
  knowledge_set: "research",
  rows: [
    {
      query: "AI market trends",
      findings: "...",
      sources: ["url1", "url2"],
      date: "2025-01-15"
    }
  ]
})
```
