# Common Tool Patterns

Reusable patterns for building Relevance AI tools.

## Search + LLM Analysis

Search for information and analyze results.

```typescript
{
  studio_id: "search-analyze",
  title: "Search and Analyze",
  params_schema: {
    type: "object",
    properties: {
      query: { type: "string", title: "Query" }
    },
    required: ["query"]
  },
  transformations: {
    steps: [
      {
        name: "search",
        transformation: "serper_google_search",
        params: { search_query: "{{query}}" },
        output: { results: "{{organic}}" }
      },
      {
        name: "analyze",
        transformation: "prompt_completion",
        params: {
          prompt: "Analyze these search results about {{query}}:\n\n{{search.results}}",
          model: "openai-gpt-4o"
        },
        output: { analysis: "{{answer}}" }
      }
    ]
  }
}
```

## Scrape + Extract

Scrape webpage and extract structured data.

```typescript
{
  studio_id: "scrape-extract",
  title: "Scrape and Extract",
  params_schema: {
    type: "object",
    properties: {
      url: { type: "string", title: "URL" }
    },
    required: ["url"]
  },
  transformations: {
    steps: [
      {
        name: "scrape",
        transformation: "browserless_scrape",
        params: {
          website_url: "{{url}}",
          method: "Text"
        },
        output: { content: "{{output.page}}" }
      },
      {
        name: "extract",
        transformation: "prompt_completion",
        params: {
          prompt: `Extract key information from this webpage:

{{scrape.content}}

Return JSON with: title, main_points, contact_info`,
          model: "openai-gpt-4o"
        },
        output: { data: "{{answer}}" }
      }
    ]
  }
}
```

## Multi-Query Loop

Generate multiple queries and search each.

```typescript
{
  studio_id: "multi-search",
  title: "Multi-Query Search",
  params_schema: {
    type: "object",
    properties: {
      topic: { type: "string", title: "Topic" }
    },
    required: ["topic"]
  },
  transformations: {
    steps: [
      // Generate queries as JSON
      {
        name: "generate_queries",
        transformation: "prompt_completion",
        params: {
          prompt: `Generate 5 search queries for: {{topic}}
Output ONLY a JSON array of strings:
["query 1", "query 2", ...]`,
          model: "openai-gpt-4o"
        },
        output: { queries_json: "{{answer}}" }
      },
      // Parse JSON to array
      {
        name: "parse_queries",
        transformation: "python_code_transformation",
        params: {
          code: `
import json
json_str = """{{generate_queries.queries_json}}"""
json_str = json_str.strip()
if json_str.startswith("\`\`\`"):
    json_str = json_str.split("\\n", 1)[1]
if json_str.endswith("\`\`\`"):
    json_str = json_str[:-3]
return {"queries": json.loads(json_str.strip())}
`
        }
      },
      // Loop through queries
      {
        name: "search_loop",
        transformation: "loop",
        params: {
          items: "{{parse_queries.transformed.queries}}",
          execution_mode: "parallel",
          steps: [
            {
              name: "search",
              transformation: "serper_google_search",
              params: {
                search_query: "{{item}}",
                num: 5
              },
              output: { results: "{{organic}}" }
            }
          ]
        },
        output: { all_results: "{{results}}" }
      },
      // Synthesize all results
      {
        name: "synthesize",
        transformation: "prompt_completion",
        params: {
          prompt: `Synthesize findings about {{topic}} from these search results:

{{search_loop.all_results}}

Provide a comprehensive summary.`,
          model: "openai-gpt-4o"
        },
        output: { summary: "{{answer}}" }
      }
    ]
  }
}
```

## URL List Processing

Process a list of URLs in parallel.

```typescript
{
  studio_id: "process-urls",
  title: "Process URL List",
  params_schema: {
    type: "object",
    properties: {
      urls: {
        type: "array",
        title: "URLs",
        items: { type: "string" }
      }
    },
    required: ["urls"]
  },
  transformations: {
    steps: [
      {
        name: "scrape_all",
        transformation: "loop",
        params: {
          items: "{{urls}}",
          execution_mode: "parallel",
          error_handling: "continue",
          steps: [
            {
              name: "scrape",
              transformation: "browserless_scrape",
              params: {
                website_url: "{{item}}",
                method: "Text"
              },
              output: { content: "{{output.page}}" }
            }
          ]
        },
        output: { pages: "{{results}}" }
      }
    ]
  }
}
```

## Data Enrichment

Enrich data with external lookups.

```typescript
{
  studio_id: "enrich-company",
  title: "Enrich Company Data",
  params_schema: {
    type: "object",
    properties: {
      company_name: { type: "string", title: "Company Name" },
      domain: { type: "string", title: "Domain (optional)" }
    },
    required: ["company_name"]
  },
  transformations: {
    steps: [
      // Search for company info
      {
        name: "search_company",
        transformation: "serper_google_search",
        params: {
          search_query: "{{company_name}} company overview",
          num: 5
        },
        output: { results: "{{organic}}" }
      },
      // Scrape website if domain provided
      {
        name: "scrape_site",
        transformation: "browserless_scrape",
        if: "{{domain}}",
        params: {
          website_url: "https://{{domain}}",
          method: "Text"
        },
        output: { website_content: "{{output.page}}" }
      },
      // Extract structured data
      {
        name: "extract_info",
        transformation: "prompt_completion",
        params: {
          prompt: `Extract company information:

Company: {{company_name}}
Search results: {{search_company.results}}
Website content: {{scrape_site.website_content}}

Return JSON:
{
  "name": "",
  "description": "",
  "industry": "",
  "size": "",
  "headquarters": "",
  "website": "",
  "social_links": []
}`,
          model: "openai-gpt-4o"
        },
        output: { company_data: "{{answer}}" }
      }
    ]
  }
}
```

## Error Handling Pattern

Robust error handling with Python.

```typescript
{
  name: "safe_parse",
  transformation: "python_code_transformation",
  params: {
    code: `
import json

try:
    json_str = """{{previous_step.output}}"""
    json_str = json_str.strip()

    # Handle markdown code blocks
    if json_str.startswith("\`\`\`"):
        json_str = json_str.split("\\n", 1)[1]
    if json_str.endswith("\`\`\`"):
        json_str = json_str[:-3]

    data = json.loads(json_str.strip())
    return {"data": data, "success": True, "error": None}

except Exception as e:
    return {"data": None, "success": False, "error": str(e)}
`
  }
}
```

## Conditional Branching

Different actions based on input.

```typescript
{
  studio_id: "conditional-process",
  transformations: {
    steps: [
      {
        name: "determine_type",
        transformation: "prompt_completion",
        params: {
          prompt: "Is '{{input}}' a URL, email, or other? Reply with just: url, email, or other",
          model: "openai-gpt-4o-mini"
        },
        output: { type: "{{answer}}" }
      },
      {
        name: "process_url",
        transformation: "browserless_scrape",
        if: "{{determine_type.type == 'url'}}",
        params: {
          website_url: "{{input}}"
        }
      },
      {
        name: "process_email",
        transformation: "prompt_completion",
        if: "{{determine_type.type == 'email'}}",
        params: {
          prompt: "Extract info from email: {{input}}"
        }
      }
    ]
  }
}
```

## Pagination Pattern

Handle paginated data sources.

```typescript
{
  name: "fetch_all_pages",
  transformation: "python_code_transformation",
  params: {
    code: `
import requests

all_items = []
page = 1
has_more = True

while has_more and page <= 10:  # Max 10 pages safety
    response = requests.get(
        "{{api_url}}",
        params={"page": page, "per_page": 100}
    )
    data = response.json()
    all_items.extend(data.get("items", []))
    has_more = data.get("has_more", False)
    page += 1

return {"items": all_items, "total_pages": page - 1}
`
  }
}
```
