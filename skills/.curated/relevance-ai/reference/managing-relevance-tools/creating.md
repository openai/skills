# Creating Tools

Complete workflow for creating Relevance AI tools (studios).

## Creating New Tools

### Option 1: Direct Creation with `relevance_upsert_tool`

Omit `studio_id` to create a new tool with auto-generated UUID:

```typescript
relevance_upsert_tool({
  title: "My New Tool",           // REQUIRED for new tools
  description: "What it does",
  prompt_description: "When AI should use this",
  params_schema: { ... },
  transformations: { steps: [...] },
  state_mapping: { ... }
})
// Returns { studio_id: "auto-generated-uuid", version_id: "...", created: true }
```

### Option 2: Create from Transformation

Fastest way - auto-generates params_schema, state_mapping, and bindings:

```typescript
relevance_create_tool_from_transformation({
  transformationId: 'serper_google_search',
  title: 'Google Search', // optional custom title
  description: 'Search the web', // optional custom description
});
// Searches existing tools first to avoid duplicates
// Returns { studio_id, tool, wasExisting: boolean }

// Force create even if duplicate exists:
relevance_create_tool_from_transformation({
  transformationId: 'serper_google_search',
  forceCreate: true,
});
```

> **⚠️ Auto-generated tools often have broken output configs.** The tool may have empty step output mappings (`"output": {}`) and invalid final output references. This means the tool executes but **returns empty results**. Always validate with `relevance_run_tool` after creation. See [Fixing Auto-Generated Tool Outputs](#fixing-auto-generated-tool-outputs) below.

## Updating Existing Tools

Provide `studio_id` to update - MCP auto-fetches and merges:

```typescript
relevance_upsert_tool({
  studio_id: 'existing-tool-id',
  emoji: '🔍', // Only this changes, everything else preserved
});
```

## Tool Structure

```typescript
interface Tool {
  studio_id: string; // Unique identifier (slug or UUID)
  title: string; // Display name
  description?: string; // What the tool does
  prompt_description: string; // Instructions for AI on when to use
  emoji?: string; // Icon

  params_schema: JSONSchema; // Input parameters
  output_schema?: JSONSchema; // Output structure

  transformations: {
    steps: TransformationStep[]; // Sequential steps to execute
  };

  state_mapping?: Record<string, string>; // How data flows
}
```

## Transformation Step Structure

```typescript
interface TransformationStep {
  name: string; // Unique identifier for this step
  transformation: string; // Transformation type ID
  params: Record<string, string>; // Input params (use {{variable}} templating)
  output?: Record<string, string>; // Output mapping

  // Optional control flow
  foreach?: { iterator: string; item_key: string };
  if?: string;
}
```

## Creating a Basic Tool

```typescript
relevance_upsert_tool({
  studio_id: 'my-tool',
  title: 'My Tool',
  description: 'What this tool does',
  prompt_description: 'Instructions for AI on when to use this tool',
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
    ],
  },
});
```

## Variable Templating

### Input Parameters

Reference tool inputs with `{{param_name}}`:

```typescript
params: {
  search_query: "{{query}}",      // From params_schema
  num_results: "{{count}}"
}
```

### Previous Step Outputs

Reference previous step outputs with `{{step_name.field}}`:

```typescript
// Step 1 output: { results: "..." }
// Step 2 access:
params: {
  text: '{{search.results}}';
}
```

### Loop Items

Inside loops, use `{{foreach.item}}` or just `{{item}}`:

```typescript
params: {
  url: '{{foreach.item.url}}';
}
```

## Multi-Step Example

```typescript
{
  studio_id: "search-and-summarize",
  title: "Search and Summarize",
  params_schema: {
    type: "object",
    properties: {
      topic: { type: "string", title: "Topic" }
    },
    required: ["topic"]
  },
  transformations: {
    steps: [
      {
        name: "search",
        transformation: "serper_google_search",
        params: { search_query: "{{topic}}" },
        output: { results: "{{organic}}" }
      },
      {
        name: "summarize",
        transformation: "prompt_completion",
        params: {
          prompt: "Summarize these results about {{topic}}:\n\n{{search.results}}",
          model: "openai-gpt-4o"
        },
        output: { summary: "{{answer}}" }
      }
    ]
  },
  state_mapping: {
    topic: "params.topic",
    search: "steps.search.output",
    summarize: "steps.summarize.output"
  }
}
```

## Parameter Schema Types

### String Parameter

```typescript
{
  query: {
    type: "string",
    title: "Search Query",
    description: "What to search for"
  }
}
```

### Number Parameter

```typescript
{
  count: {
    type: "number",
    title: "Result Count",
    default: 10
  }
}
```

### Boolean Parameter

```typescript
{
  include_images: {
    type: "boolean",
    title: "Include Images",
    default: false
  }
}
```

### Enum Parameter

```typescript
{
  format: {
    type: "string",
    title: "Output Format",
    enum: ["json", "markdown", "text"]
  }
}
```

### Array Parameter

```typescript
{
  urls: {
    type: "array",
    title: "URLs to Process",
    items: { type: "string" }
  }
}
```

## Conditional Steps

Run steps conditionally:

```typescript
{
  name: "optional_step",
  transformation: "prompt_completion",
  if: "{{include_analysis}}",  // Only run if truthy
  params: { ... }
}
```

## Emoji Formats

Tools support these emoji formats:

| Format           | Example                              | Use Case                     |
| ---------------- | ------------------------------------ | ---------------------------- |
| Unicode emoji    | `"🔍"`                               | Default, simplest option     |
| CDN URL          | `"https://cdn.example.com/icon.svg"` | Brand icons, custom graphics |
| Agent avatar URL | `"https://..."`                      | Match agent branding         |

## Testing After Creation

```typescript
// Sync execution
relevance_run_tool({
  studioId: 'my-tool',
  params: { query: 'test query' },
});
```

## Publishing

After creation, the tool is in draft. To make it active:

```typescript
relevance_publish_tool({ toolId: 'my-tool' });
```

---

## `transformations` is Replaced, Not Deep-Merged

The MCP auto-merge preserves top-level fields you omit (e.g., providing only `emoji` keeps your existing `transformations`). But if you DO provide `transformations`, the entire object — including the `steps` array — is replaced wholesale. To update a single step in a multi-step tool, you must get the tool first, modify the specific step, then upsert with ALL steps:

```typescript
// WRONG — replaces ALL steps with just this one
relevance_upsert_tool({
  studio_id: 'x',
  transformations: { steps: [modified_step_2_only] },
});

// CORRECT — preserves all other steps
const { studio } = await relevance_get_tool({ studioId: 'x' });
studio.transformations.steps[1].params.code = newCode;
relevance_upsert_tool({
  studio_id: 'x',
  transformations: studio.transformations,
});
```

---

## `state_mapping` is REQUIRED

**This is the #1 cause of "missing required property" errors when tools are called by agents.**

Every tool MUST have a `state_mapping` field that maps input params to template variables. Without this, `{{search_query}}` won't resolve even when the agent passes the parameter.

```json
{
  "params_schema": {
    "properties": { "search_query": { "type": "string" } }
  },
  "state_mapping": {
    "search_query": "params.search_query"
  },
  "transformations": {
    "steps": [
      {
        "transformation": "serper_google_search",
        "params": { "search_query": "{{search_query}}" }
      }
    ]
  }
}
```

**CRITICAL:** Do NOT use curly braces in state_mapping values!

```json
// WRONG - curly braces cause params to not resolve
"state_mapping": { "name": "{{params.name}}" }

// CORRECT - no curly braces
"state_mapping": { "name": "params.name" }
```

## Fixing Auto-Generated Tool Outputs

Tools created by `relevance_create_tool_from_transformation` often return empty `{}` because output fields aren't mapped. To fix:

1. **Check the transformation's `output_schema`** to find available fields
2. **Add explicit output mappings** to the step
3. **Fix the final output reference** to point to the correct step output

```typescript
// BROKEN (auto-generated):
{ name: "my_step", transformation: "some_transformation", output: {} }

// FIXED (explicit mapping — check output_schema for actual field names):
{ name: "my_step", transformation: "some_transformation",
  output: { results: "{{results}}", metadata: "{{metadata}}" } }
```

| Config           | Broken (auto-generated)         | Working (fixed)                         |
| ---------------- | ------------------------------- | --------------------------------------- |
| Step output      | `"output": {}`                  | `"output": {"field": "{{field}}", ...}` |
| Final output ref | `"answer": "{{stepname.data}}"` | `"answer": "{{stepname.actual_field}}"` |
| State mapping    | Missing step entries            | `"stepname": "steps.stepname.output"`   |

**Tip:** When in doubt, find a working tool in the project that uses the same transformation and copy its output pattern.

## Discover Transformation Outputs via `output_schema`

**Don't guess output fields - check the transformation's `output_schema` first!**

```typescript
const t = await relevance_get_transformation({
  transformationId: 'browserless_scrape',
});
// t.output_schema.properties.output.properties.page  → use {{output.page}}
// t.output_schema.properties.credits_cost            → use {{credits_cost}}
```

## Using Secrets in Code Steps

Secrets are accessed via **template syntax** `{{secrets.secret_name}}`, NOT as JavaScript/Python objects.

```javascript
// WRONG - secrets is not a defined JS object
const apiKey = secrets.my_api_key; // Error: secrets is not defined

// CORRECT - template substitution (resolved before code runs)
const apiKey = '{{secrets.my_api_key}}';
```

**Secret names MUST start with `chains_` prefix.** If you reference `{{secrets.my_key}}`, the secret must be named `chains_my_key` in the project.

**Alternative:** Pass credentials as tool input parameters with hidden defaults to avoid the `chains_` prefix:

```json
{
  "params_schema": {
    "properties": {
      "_api_key": { "type": "string", "default": "sk-...", "hidden": true }
    }
  }
}
```

Then use template substitution: `api_key = '{{_api_key}}'`

**For API calls**, prefer transformations with built-in `authorization_config` (e.g., `hubspot_api_call`) which handle auth automatically.

---

## Best Practices

1. **Use descriptive step names** - Makes debugging easier
2. **Map outputs explicitly** - Don't rely on implicit variable names
3. **Test incrementally** - Add one step at a time
4. **Document with prompt_description** - Help AI know when to use the tool
5. **Handle errors in Python steps** - Add try/catch for robustness
6. **Validate every tool before attaching to agents** - Test with `relevance_run_tool` to catch empty output issues
