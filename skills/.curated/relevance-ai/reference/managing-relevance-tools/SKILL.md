---
name: managing-relevance-tools
description: Manages Relevance AI tools (studios) - creating transformation workflows, configuring OAuth, running tools, and recovering versions. Use when building tools, adding steps, debugging transformations, or restoring previous versions.
---

# Managing Relevance AI Tools

Skill for creating, configuring, running, and debugging Relevance AI tools (studios).

> **📚 Full API Documentation:** If MCP tools don't cover your use case, see `https://api-{region}.stack.tryrelevance.com/latest/documentation` (replace `{region}` with your project's region)

## When to Use

- Creating new tools with transformation workflows
- Adding or editing transformation steps
- Configuring OAuth for integrations
- Running and testing tools
- Recovering from accidental changes via versions
- Debugging transformation issues

## MCP Tools

| Tool                                        | Description                                                 |
| ------------------------------------------- | ----------------------------------------------------------- |
| `relevance_list_tools`                      | List all tools in project                                   |
| `relevance_get_tool`                        | Get full tool config                                        |
| `relevance_upsert_tool`                     | Create or update a tool (auto-generates UUID for new tools) |
| `relevance_create_tool_from_transformation` | Create tool from transformation with auto-generated config  |
| `relevance_publish_tool`                    | Publish tool draft                                          |
| `relevance_run_tool`                        | Execute tool synchronously                                  |
| `relevance_trigger_tool_async`              | Execute tool asynchronously                                 |
| `relevance_poll_tool_result`                | Poll async job status                                       |
| `relevance_get_latest_tool_run`             | Get latest run ID                                           |
| `relevance_list_tool_versions`              | List version history for a tool                             |
| `relevance_get_tool_version`                | Get a specific version's config                             |
| `relevance_restore_tool_version`            | Restore a tool to a previous version                        |
| `relevance_search_public_tools`             | Search community/public tools                               |
| `relevance_clone_public_tool`               | Clone a public tool into your project                       |
| `relevance_api_request`                     | Raw API fallback for uncovered endpoints                    |

## Finding the Right Tool: Search Order

When looking for tools to accomplish a task, follow this search order:

1. **Search project tools** — `relevance_list_tools({ query: "..." })` — Already built and configured
2. **Search public/community tools** — `relevance_search_public_tools({ query: "..." })` — Pre-built, sorted by popularity
3. **Search marketplace listings** — `relevance_search_marketplace_listings({ query: "...", entityType: "tool" })` — Complete solutions (agent + tools bundled)
4. **Search transformations** — `relevance_list_transformations({ query: "..." })` — 8000+ integrations, use `relevance_create_tool_from_transformation` to wrap

**Tip:** Use multiple diverse search queries per tier (e.g., "scrape", "extract", "crawl" rather than just one term).

## Critical Rules

### Underlying API: NO PARTIAL UPDATES

The Relevance API does NOT support partial updates - any field you omit will be WIPED. However, the MCP tools handle this automatically:

- **Creating new tools (no `studio_id`)**: Just provide your fields, MCP adds defaults
- **Updating existing tools (with `studio_id`)**: MCP auto-fetches existing config and merges your changes

```typescript
// Creating new tool - just provide what you need
relevance_upsert_tool({
  title: "My Tool",  // REQUIRED for new tools
  transformations: { steps: [...] }
})
// Returns { studio_id: "auto-uuid", created: true }

// Updating existing tool - MCP auto-merges
relevance_upsert_tool({
  studio_id: "my-tool",
  emoji: "new-emoji"  // Only this changes, rest preserved
})
```

### Creating Tools from Transformations

Fastest way to create a tool - auto-generates params_schema, state_mapping, and bindings:

```typescript
relevance_create_tool_from_transformation({
  transformationId: 'serper_google_search',
  title: 'Google Search', // optional
});
// Searches existing tools first to avoid duplicates
// Returns { studio_id, tool, wasExisting: boolean }
```

See [creating.md](creating.md) for full workflow.

### Key Output Patterns

| Transformation               | Output Variable                                          |
| ---------------------------- | -------------------------------------------------------- |
| `prompt_completion`          | `{{answer}}` (NOT `{{text}}`)                            |
| `python_code_transformation` | `{{step.transformed.field}}` (wrapped in `.transformed`) |
| `browserless_scrape`         | `{{output.page}}`                                        |
| `serper_google_search`       | `{{organic}}`                                            |
| `loop`                       | `{{results}}`                                            |

### Loop Requires Actual Arrays

Loop transformation needs parsed arrays, not JSON strings:

```typescript
// LLM generates JSON string → parse with Python first
items: '{{parse_step.transformed.items}}'; // Parsed array
items: '{{llm_step.answer}}'; // WRONG - string
```

## Quick Start: Create Tool

```typescript
relevance_upsert_tool({
  studio_id: 'my-search-tool',
  title: 'Search and Summarize',
  description: 'Search web and summarize results',
  prompt_description: 'Use this to search for information',
  params_schema: {
    type: 'object',
    properties: {
      query: { type: 'string', title: 'Search Query' },
    },
    required: ['query'],
  },
  transformations: {
    steps: [
      {
        name: 'search',
        transformation: 'serper_google_search',
        params: { search_query: '{{query}}' },
        output: { results: '{{organic}}' },
      },
      {
        name: 'summarize',
        transformation: 'prompt_completion',
        params: {
          prompt: 'Summarize: {{search.results}}',
          model: 'openai-gpt-5.1',
        },
        output: { summary: '{{answer}}' },
      },
    ],
  },
});
```

## Reference Files

- [creating.md](creating.md) - Full creation workflow
- [transformations-catalog.md](transformations-catalog.md) - Quick lookup of popular transformations by category
- [transformations.md](transformations.md) - Implementation details, output patterns, and gotchas
- [patterns.md](patterns.md) - Common patterns (search+analyze, loops)
- [oauth.md](oauth.md) - OAuth account configuration
- [running.md](running.md) - Running and testing tools
- [versions.md](versions.md) - Version history and recovery
- [reference.md](reference.md) - API auth, base URLs, discovering transformations

## URL Patterns

```
# Tool editor (notebook)
https://app.relevanceai.com/notebook/{region}/{project}/{studioId}

# Clone link
https://app.relevanceai.com/form/{region}/{project}/clone/tool/{studioId}
```

## Emergency Version Recovery

If you accidentally wipe a tool:

1. `relevance_list_tool_versions({ toolId: "my-tool" })` — Find a version with transformations intact
2. `relevance_restore_tool_version({ versionId: "working-version-uuid" })` — Creates a new draft from that version
3. `relevance_publish_tool({ toolId: "my-tool" })` — Publish the restored draft

See [versions.md](versions.md) for full details.
