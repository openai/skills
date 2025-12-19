# Advanced Search Techniques

## Search Filtering

### By Date Range

Use `created_date_range` to find recent content:

```
filters: {
  created_date_range: {
    start_date: "2024-01-01",
    end_date: "2025-01-01"
  }
}
```

**When to use**:
- Finding recent updates on a topic
- Focusing on current information
- Excluding outdated content

### By Creator

Use `created_by_user_ids` to find content from specific people:

```
filters: {
  created_by_user_ids: ["user-id-1", "user-id-2"]
}
```

**When to use**:
- Research from subject matter experts
- Team-specific information
- Attribution tracking

### Combined Filters

Stack filters for precision:

```
filters: {
  created_date_range: {
    start_date: "2024-10-01"
  },
  created_by_user_ids: ["expert-user-id"]
}
```

## Scoped Searches

### Teamspace Scoping

Restrict search to specific teamspace:

```
teamspace_id: "teamspace-uuid"
```

**When to use**:
- Project-specific research
- Department-focused information
- Reducing noise from irrelevant results

### Page Scoping

Search within a specific page and its subpages:

```
page_url: "https://notion.so/workspace/Page-Title-uuid"
```

**When to use**:
- Research within a project hierarchy
- Documentation updates
- Focused investigation

### Database Scoping

Search within a database's content:

```
data_source_url: "collection://data-source-uuid"
```

**When to use**:
- Task/project database research
- Structured data investigation
- Finding specific entries

## Search Strategies

### Broad to Narrow

1. Start with general search term
2. Review results for relevant teamspaces/pages
3. Re-search with scope filters
4. Fetch detailed content from top results

**Example**:
```
Search 1: query="API integration" → 50 results across workspace
Search 2: query="API integration", teamspace_id="engineering" → 12 results
Fetch: Top 3-5 most relevant pages
```

### Multi-Query Approach

Run parallel searches with related terms:

```
Query 1: "API integration"
Query 2: "API authentication"
Query 3: "API documentation"
```

Combine results to build comprehensive picture.

### Temporal Research

Search across time periods to track evolution:

```
Search 1: created_date_range 2023 → Historical context
Search 2: created_date_range 2024 → Recent developments
Search 3: created_date_range 2025 → Current state
```

## Result Processing

### Identifying Relevant Results

Look for:
- **High semantic match**: Result summary closely matches query intent
- **Recent updates**: Last-edited date is recent
- **Authoritative sources**: Created by known experts or in official locations
- **Comprehensive content**: Result summary suggests detailed information

### Prioritizing Fetches

Fetch pages in order of relevance:

1. **Primary sources**: Direct documentation, official pages
2. **Recent updates**: Newly edited content
3. **Related context**: Supporting information
4. **Historical reference**: Background and context

Don't fetch everything - be selective based on research needs.

### Handling Too Many Results

If search returns 20+ results:

1. **Add filters**: Narrow by date, creator, or teamspace
2. **Refine query**: Use more specific terms
3. **Use page scoping**: Search within relevant parent page
4. **Sample strategically**: Fetch diverse results (recent, popular, authoritative)

### Handling Too Few Results

If search returns < 3 results:

1. **Broaden query**: Use more general terms
2. **Remove filters**: Search full workspace
3. **Try synonyms**: Alternative terminology
4. **Search in related areas**: Adjacent teamspaces or pages

## Search Quality

### Effective Search Queries

**Good queries** (specific, semantic):
- "Q4 product roadmap"
- "authentication implementation guide"
- "customer feedback themes"

**Weak queries** (too vague):
- "roadmap"
- "guide"
- "feedback"

**Over-specific queries** (too narrow):
- "Q4 2024 product roadmap for mobile app version 3.2 feature X"

### User Context

Always use available user context:
- Query should match their terminology
- Scope to their relevant teamspaces
- Consider their role/department
- Reference their recent pages

## Connected Sources

### Notion Integrations

Search extends beyond Notion pages to:
- Slack messages (if connected)
- Google Drive documents (if connected)
- GitHub issues/PRs (if connected)
- Jira tickets (if connected)

Be aware results may come from these sources.

### Source Attribution

When citing results from connected sources:
- Note the source type in documentation
- Use appropriate mention format
- Verify user has access to the source system

