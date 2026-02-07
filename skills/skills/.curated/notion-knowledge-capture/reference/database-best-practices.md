# Database Best Practices

General guidance for creating and maintaining knowledge capture databases.

## Core Principles

### 1. Keep It Simple
- Start with core properties
- Add more only when needed
- Don't over-engineer

### 2. Use Consistent Naming
- Title property for main identifier
- Status for lifecycle tracking
- Tags for flexible categorization
- Owner for accountability

### 3. Include Metadata
- Created/Updated timestamps
- Owner or maintainer
- Last reviewed dates
- Status indicators

### 4. Enable Discovery
- Use tags liberally
- Create helpful views
- Link related content
- Use clear titles

### 5. Plan for Scale
- Consider filters early
- Use relations for connections
- Think about search
- Organize with categories

## Creating a Database

### Using `Notion:notion-create-database`

Example for documentation database:

```javascript
{
  "parent": {"page_id": "wiki-page-id"},
  "title": [{"text": {"content": "Team Documentation"}}],
  "properties": {
    "Type": {
      "select": {
        "options": [
          {"name": "How-To", "color": "blue"},
          {"name": "Concept", "color": "green"},
          {"name": "Reference", "color": "gray"},
          {"name": "FAQ", "color": "yellow"}
        ]
      }
    },
    "Category": {
      "select": {
        "options": [
          {"name": "Engineering", "color": "red"},
          {"name": "Product", "color": "purple"},
          {"name": "Design", "color": "pink"}
        ]
      }
    },
    "Tags": {"multi_select": {"options": []}},
    "Owner": {"people": {}},
    "Status": {
      "select": {
        "options": [
          {"name": "Draft", "color": "gray"},
          {"name": "Final", "color": "green"},
          {"name": "Deprecated", "color": "red"}
        ]
      }
    }
  }
}
```

### Fetching Database Schema

Before creating pages, always fetch database to get schema:

```
Notion:notion-fetch
id: "database-url-or-id"
```

This returns the exact property names and types to use.

## Database Selection Guide

| Need | Use This Database |
|------|-------------------|
| General documentation | [Documentation Database](documentation-database.md) |
| Track decisions | [Decision Log](decision-log-database.md) |
| Q&A knowledge base | [FAQ Database](faq-database.md) |
| Team-specific content | [Team Wiki](team-wiki-database.md) |
| Step-by-step guides | [How-To Guide Database](how-to-guide-database.md) |
| Incident/project learnings | [Learning Database](learning-database.md) |

## Tips

1. **Start with general documentation database** - most flexible
2. **Add specialized databases** as needs emerge (FAQ, Decisions)
3. **Use relations** to connect related docs
4. **Create views** for common use cases
5. **Review properties** quarterly - remove unused ones
6. **Document the schema** in database description
7. **Train team** on property usage and conventions

