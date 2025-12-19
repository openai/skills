# General Documentation Database

**Purpose**: Store all types of documentation in a searchable, organized database.

## Schema

| Property | Type | Options | Purpose |
|----------|------|---------|---------|
| **Title** | title | - | Document name |
| **Type** | select | How-To, Concept, Reference, FAQ, Decision, Post-Mortem | Categorize content type |
| **Category** | select | Engineering, Product, Design, Operations, General | Organize by department/topic |
| **Tags** | multi_select | - | Additional categorization (languages, tools, topics) |
| **Status** | select | Draft, In Review, Final, Deprecated | Track document lifecycle |
| **Owner** | people | - | Document maintainer |
| **Created** | created_time | - | Auto-populated creation date |
| **Last Updated** | last_edited_time | - | Auto-populated last edit |
| **Last Reviewed** | date | - | Manual review tracking |

## Usage

```
Create pages with properties:
{
  "Title": "How to Deploy to Production",
  "Type": "How-To",
  "Category": "Engineering",
  "Tags": "deployment, production, DevOps",
  "Status": "Final",
  "Owner": [current_user],
  "Last Reviewed": "2025-10-01"
}
```

## Views

**By Type**: Group by Type property
**By Category**: Group by Category property  
**Recent Updates**: Sort by Last Updated descending
**Needs Review**: Filter where Last Reviewed > 90 days ago
**Draft Docs**: Filter where Status = "Draft"

## Creating This Database

Use `Notion:notion-create-database`:

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

## Best Practices

1. **Start with this schema** - most flexible for general documentation
2. **Use relations** to connect related docs
3. **Create views** for common use cases
4. **Review properties** quarterly - remove unused ones
5. **Document the schema** in database description
6. **Train team** on property usage and conventions

