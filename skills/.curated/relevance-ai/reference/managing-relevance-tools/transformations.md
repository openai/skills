# Transformations Reference

Complete reference for transformation types and their outputs.

## LLM / Text Processing

### prompt_completion

Text generation with LLM.

```typescript
{
  name: "analyze",
  transformation: "prompt_completion",
  params: {
    prompt: "Analyze this: {{input}}",
    model: "openai-gpt-5.1"
  },
  output: {
    result: "{{answer}}"  // NOT {{text}}!
  }
}
```

**Output:** `{{answer}}`

**Models:**

- `openai-gpt-5.1` - Fast, good quality
- `openai-gpt-4o-mini` - Fast, cheaper
- `anthropic-claude-sonnet-4` - Best quality/cost balance
- `anthropic-claude-opus-4` - Highest quality
- `relevance-cost-optimized` - Auto-select cheapest
- `relevance-performance-optimized` - Auto-select best

### prompt_completion_vision

Image analysis with LLM.

```typescript
{
  name: "analyze_image",
  transformation: "prompt_completion_vision",
  params: {
    prompt: "Describe this image",
    model: "openai-gpt-5.1",
    image: "{{image_url}}"
  },
  output: {
    description: "{{answer}}"
  }
}
```

## Web Scraping & Search

### browserless_scrape

Scrape webpage content.

```typescript
{
  name: "scrape",
  transformation: "browserless_scrape",
  params: {
    website_url: "{{url}}",
    method: "Text"
  },
  output: {
    content: "{{output.page}}"  // NOT {{content}}!
  }
}
```

**Output:** `{{output.page}}`

### serper_google_search

Google web search.

```typescript
{
  name: "search",
  transformation: "serper_google_search",
  params: {
    search_query: "{{query}}",
    num: 10
  },
  output: {
    results: "{{organic}}"
  }
}
```

**Output:** `{{organic}}`, `{{knowledge_graph}}`

### jina_reader

Clean web content for LLM.

```typescript
{
  name: "clean",
  transformation: "jina_reader_-_jina_reader-convert-to-llm-friendly-input",
  params: {
    url: "{{url}}"
  },
  output: {
    text: "{{text}}"
  }
}
```

## Apify Actors

### run_apify_dynamic

Run any Apify actor (2000+ scrapers).

```typescript
{
  name: "scrape_maps",
  transformation: "run_apify_dynamic",
  params: {
    actor_id: "compass/crawler-google-places",
    inputs: {
      searchStringsArray: ["{{query}}"],
      maxCrawledPlaces: 20
    }
  },
  output: {
    places: "{{items}}"
  }
}
```

**Output:** `{{items}}`

**Popular actors:**

- `compass/crawler-google-places` - Google Maps
- `apify/google-search-scraper` - Deep Google search
- `apify/instagram-scraper` - Instagram data
- `apify/linkedin-scraper` - LinkedIn profiles
- `apify/website-content-crawler` - Full website crawl
- `apify/contact-info-scraper` - Find emails/phones

## API Calls

### api_call

Make HTTP requests to **external** APIs. No auth injection — you must pass headers manually.

```typescript
{
  name: "fetch_data",
  transformation: "api_call",
  params: {
    url: "https://api.example.com/data",
    method: "GET",
    headers: { "Authorization": "Bearer {{api_key}}" }
  },
  output: {
    result: "{{response_body}}"
  }
}
```

**Output:** `{{response_body}}`, `{{status}}`

### relevance_api_call

Make HTTP requests to **Relevance platform** APIs. **Auth is auto-injected** from the caller's context — no API keys needed. This is critical for marketplace tools: cloners get their own auth automatically.

```typescript
{
  name: "fetch_collections",
  transformation: "relevance_api_call",
  params: {
    path: "/replicate/collections",   // Relative path (not full URL)
    method: "GET"                      // GET, POST, or PUT only
  },
  output: {
    collections: "{{response_body.collections}}"
  }
}
```

**Output:** `{{response_body}}`, `{{status}}`, `{{url}}`, `{{body}}`, `{{response_headers}}`

**Parameters:**

| Param                           | Type          | Required | Description                                                                                  |
| ------------------------------- | ------------- | -------- | -------------------------------------------------------------------------------------------- |
| `path`                          | string        | Yes      | Relative API path (e.g., `/replicate/collections`, `/knowledge/list`). Leading `/` optional. |
| `method`                        | string (enum) | Yes      | `"GET"`, `"POST"`, or `"PUT"` (no DELETE/PATCH)                                              |
| `body`                          | object        | No       | JSON body for POST/PUT requests. Ignored for GET.                                            |
| `raise_error_on_error_response` | boolean       | No       | If `true`, step fails on non-2xx. Default `false` (returns error in `response_body`).        |

**POST example with body:**

```typescript
{
  name: "update_metadata",
  transformation: "relevance_api_call",
  params: {
    path: "/knowledge/sets/{{conversation_id}}/update_metadata",
    method: "POST",
    body: {
      updates: { conversation: { tags: "{{tags}}" } }
    }
  },
  output: {
    result: "{{response_body}}"
  }
}
```

**Key differences from `api_call`:**

| Feature          | `relevance_api_call`                  | `api_call`                      |
| ---------------- | ------------------------------------- | ------------------------------- |
| Target           | Relevance platform APIs only          | Any external URL                |
| Auth             | **Auto-injected** from caller context | Manual (via `headers` param)    |
| URL param        | `path` (relative, e.g., `/auth/info`) | `url` (full URL)                |
| Methods          | GET, POST, PUT only                   | GET, POST, PUT, DELETE, PATCH   |
| Marketplace-safe | Yes — cloners use their own auth      | Depends on how auth is provided |

**When to use `relevance_api_call`:**

- Calling platform proxy endpoints (`/replicate/*`, `/knowledge/*`, `/agents/*`)
- Any internal platform operation from within a tool step
- Tools that need to work for marketplace cloners (no hardcoded keys)

**When to use `api_call`:**

- Calling external third-party APIs (not Relevance platform)
- Endpoints that need DELETE or PATCH methods
- When you need custom headers or query params

## Code Execution

### js_code_transformation

JavaScript code with native access to `steps` object.

```typescript
{
  name: "process",
  transformation: "js_code_transformation",
  params: {
    code: `
const data = steps.api_step.output.response_body;
const filtered = data.results.filter(item => item.score > 0.5);
return { filtered };
`
  }
}
```

**Output:** `{{transformed.field}}` - Same as Python, wrapped in `.transformed`

**Key feature:** `steps.stepName.output` gives you native JavaScript objects - no parsing needed.

**Use JavaScript when:** Processing JSON from previous steps, simple filtering/mapping, no special library requirements.

### python_code_transformation

Custom Python logic with template substitution.

```typescript
{
  name: "process",
  transformation: "python_code_transformation",
  params: {
    code: `
import json

# For simple values, direct substitution works:
value = "{{steps.previous.output.simple_field}}"

# For objects/arrays, template substitution also works:
data = {{steps.previous.output.response_body}}
processed = [item for item in data if item['score'] > 0.5]
return {"filtered": processed}
`
  },
  output: {
    result: "{{transformed.filtered}}"  // Note: wrapped in .transformed
  }
}
```

**Output:** `{{transformed.field}}` - Python returns are wrapped in `.transformed`

**Access pattern:**

```typescript
// Python returns: {"my_data": [...]}
// Next step uses: {{python_step.transformed.my_data}}
```

**Use Python when:** You need pandas, complex datetime manipulation, numpy, or other Python-specific libraries.

**Template substitution limitation:** `{{...}}` inserts raw text into the code string. This can cause syntax errors with JSON containing unescaped quotes or special characters. For complex JSON, JavaScript's native `steps` access may be simpler.

### Python: Accessing Tool Input Parameters

**`steps['params']` does NOT exist.** To access tool input parameters in Python, you MUST use template substitution (`'{{param_name}}'`). The `steps` dict only contains outputs from previous transformation steps, not the tool's input params.

```python
# WRONG - KeyError: 'params'
url = steps['params']['website_url']

# CORRECT - template substitution for input params
url = '{{website_url}}'
```

**Use direct dict access** (`steps['...']`) for previous step outputs — it's cleaner and avoids JSON parsing issues.

**Use template substitution** (`{{...}}`) for tool input params and when injecting values into string literals (e.g., SQL queries, URLs).

## Loop Transformation

### loop

Iterate over arrays.

```typescript
{
  name: "process_urls",
  transformation: "loop",
  params: {
    items: "{{urls}}",  // MUST be actual array, not JSON string
    execution_mode: "parallel",
    error_handling: "continue",
    steps: [
      {
        name: "scrape",
        transformation: "browserless_scrape",
        params: {
          website_url: "{{item}}"  // Current item
        }
      }
    ]
  },
  output: {
    all_content: "{{results}}"
  }
}
```

**Output:** `{{results}}` - Array of `{inner_step: {outputs}}`

**Critical:** Loop requires actual array, not JSON string. Parse with Python first if needed.

## File Processing

### file_to_text_llm_friendly

Convert files to text.

```typescript
{
  name: "extract",
  transformation: "file_to_text_llm_friendly",
  params: {
    file: "{{file_url}}"
  },
  output: {
    content: "{{text}}"
  }
}
```

Supports: PDF, Word, CSV, Excel

## Quick Reference Table

| Transformation               | Key Output            | Access Pattern                                |
| ---------------------------- | --------------------- | --------------------------------------------- |
| `prompt_completion`          | `{{answer}}`          | `{{step.answer}}`                             |
| `python_code_transformation` | `return {"key": val}` | `{{step.transformed.key}}`                    |
| `browserless_scrape`         | `{{output.page}}`     | `{{step.content}}` (via output mapping)       |
| `serper_google_search`       | `{{organic}}`         | `{{step.results}}`                            |
| `loop`                       | `{{results}}`         | Array of `{inner_step: {outputs}}`            |
| `run_apify_dynamic`          | `{{items}}`           | `{{step.items}}`                              |
| `api_call`                   | `{{response_body}}`   | `{{step.response_body}}`                      |
| `relevance_api_call`         | `{{response_body}}`   | `{{step.response_body}}` (auth auto-injected) |

## Common Gotchas

### 1. prompt_completion uses `{{answer}}` NOT `{{text}}`

```yaml
# WRONG
output:
  result: "{{text}}"

# CORRECT
output:
  result: "{{answer}}"
```

### 2. Python outputs are wrapped in `.transformed`

```yaml
# Python returns: {"items": [...]}
# Access via:
{{python_step.transformed.items}}    # CORRECT
{{python_step.items}}                 # WRONG
```

### 3. Loop requires actual array, not JSON string

```yaml
# If LLM generates JSON string, parse first:
- name: parse
  transformation: python_code_transformation
  params:
    code: |
      import json
      return {"items": json.loads("""{{llm_step.json_str}}""")}

- name: loop_step
  transformation: loop
  params:
    items: '{{parse.transformed.items}}' # Now an actual array
```

### 4. Handle markdown code blocks from LLMs

````python
json_str = """{{step.json_output}}"""
json_str = json_str.strip()
if json_str.startswith("```"):
    json_str = json_str.split("\n", 1)[1]
if json_str.endswith("```"):
    json_str = json_str[:-3]
data = json.loads(json_str.strip())
````

### 5. Python: Handle undefined/empty template values

**Problem:** Template variables resolve to literal strings like `'undefined'` or `'null'` when the parameter isn't provided.

```python
# WRONG - This will be truthy even when contact_id is "undefined"
if '{{contact_id}}':
    do_something('{{contact_id}}')

# CORRECT - Explicitly check for invalid values
contact_id = '{{contact_id}}'
if contact_id and contact_id not in ['', 'undefined', 'null', 'None']:
    do_something(contact_id)

# For numeric IDs (like HubSpot), also check .isdigit()
if contact_id and contact_id not in ['', 'undefined', 'null', 'None'] and contact_id.isdigit():
    associations.append({'to': {'id': contact_id}})
```

**Common invalid values to check:**

- `''` (empty string)
- `'undefined'` (JavaScript undefined)
- `'null'` (JavaScript null)
- `'None'` (Python None as string)

### 6. Validate IDs before API calls

**Problem:** Passing undefined IDs to external APIs causes confusing errors.

**Symptom:** "Object not found. objectId are usually numeric" with `"id":["undefined"]`

```python
# Add validation step before API call
deal_id = '{{deal_id}}'
if not deal_id or deal_id in ['', 'undefined', 'null', 'None'] or not deal_id.isdigit():
    raise ValueError(f'Invalid deal_id: {deal_id}. Must be a valid numeric ID.')
return deal_id
```

### 7. Don't access array[0] on potentially empty results

**Problem:** Search returns empty array, accessing `results[0]` causes error.

**Symptom:** "Failed to extract output: Error: Value of search.results[0] is null"

```yaml
# WRONG
output:
  contact: "{{search.results[0]}}"

# CORRECT - return the whole results, let caller check if empty
output:
  found: "{{search.total > 0}}"
  total: "{{search.total}}"
  results: "{{search.results}}"
```

### 8. Use Python for timestamps, not {{now()}}

**Problem:** `{{now()}}` template function doesn't work in some API call bodies.

```yaml
# WRONG
- name: create_note
  transformation: hubspot_api_call
  params:
    body:
      properties:
        hs_timestamp: '{{now()}}' # May not work

# CORRECT - Use Python step first
- name: get_timestamp
  transformation: python_code_transformation
  params:
    code: |
      import datetime
      return int(datetime.datetime.now().timestamp() * 1000)
  output:
    timestamp: '{{transformed}}'

- name: create_note
  transformation: hubspot_api_call
  params:
    body:
      properties:
        hs_timestamp: '{{get_timestamp.timestamp}}'
```
