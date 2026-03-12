# API Reference

Additional API details for operations not covered by dedicated MCP tools.

## Discovering Transformations

There are 8000+ transformations available. Use MCP tools to find them:

```
relevance_list_transformations({ query: "google search", page_size: 10 })
```

To get full details of a specific transformation:

```
relevance_get_transformation({ transformationId: "serper_google_search" })
```

## Conversation Jobs

Get tool execution jobs within an agent conversation:

```
relevance_api_request({
  method: "POST",
  endpoint: "/agents/{agentId}/tasks/{taskId}/jobs/list",
  body: { page_size: 50 }
})
```

## OAuth Providers List

Get available OAuth providers and permission types:

```
relevance_api_request({
  method: "GET",
  endpoint: "/auth/oauth/options/list"
})
```

## Raw API Usage

For any operation not covered by dedicated MCP tools, use `relevance_api_request`:

```
relevance_api_request({
  method: "POST",
  endpoint: "/your/endpoint",
  body: { ... }
})
```

The `endpoint` must be a relative path (e.g., `/agents/list`). The base URL is added automatically.
