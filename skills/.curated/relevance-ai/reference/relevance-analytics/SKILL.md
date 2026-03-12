---
name: relevance-analytics
description: Retrieves usage analytics for Relevance AI agents and projects. Use when asked about agent usage, most active agents, execution counts, or usage trends over time.
---

# Relevance AI Analytics

Skill for retrieving and analyzing usage data for agents and projects.

> **📚 Full API Documentation:** `https://api-{region}.stack.tryrelevance.com/latest/documentation` (replace `{region}` with your project's region)

## When to Use

- Finding most used/active agents
- Getting agent execution counts
- Analyzing usage trends over time
- Identifying idle or underutilized agents
- Tracking tasks pending approval

## No Dedicated MCP Tool

Analytics uses `relevance_api_request` since there's no dedicated MCP tool. This skill shows you how to call the endpoints correctly.

## Get Agent Analytics

### Endpoint

```http
POST /agents/analytics
```

### Calling the Endpoint

```typescript
// Get all agent analytics (no filters)
const analytics = await relevance_api_request({
  endpoint: '/agents/analytics',
  method: 'POST',
  body: { filters: {} },
});

// Filter by specific agent
const agentAnalytics = await relevance_api_request({
  endpoint: '/agents/analytics',
  method: 'POST',
  body: {
    filters: {
      agentId: { eq: 'your-agent-id' },
    },
  },
});

// Filter by date range
const rangeAnalytics = await relevance_api_request({
  endpoint: '/agents/analytics',
  method: 'POST',
  body: {
    filters: {
      insert_date_: {
        gte: '2025-01-01T00:00:00.000Z',
        lte: '2025-01-31T23:59:59.999Z',
      },
    },
  },
});
```

### Response Structure

```json
{
  "states_results": {
    "timeseries": [
      {
        "insert_date_": "2025-01-20T00:00:00.000Z",
        "source_type": "agent",
        "source_id": "<agent_id>",
        "event_type": "state-updated",
        "event_value": "running",
        "frequency": 5,
        "total": 5,
        "bucket": "weekly"
      }
    ],
    "total_change": { ... },
    "change_per_event_value": { ... }
  },
  "labels_results": { ... },
  "tasks_created_results": {
    "timeseries": [
      {
        "insert_date_": "2025-01-27T00:00:00.000Z",
        "source_type": "agent",
        "source_id": "<agent_id>",
        "frequency": 10,
        "total": 10,
        "bucket": "weekly"
      }
    ],
    "total_change": { ... }
  },
  "last_updated_at": "2025-01-23T00:00:00.000Z"
}
```

### Key Fields

| Field                             | Description                         |
| --------------------------------- | ----------------------------------- |
| `event_value: "running"`          | Agent executed a task               |
| `event_value: "idle"`             | Agent completed/stopped             |
| `event_value: "pending-approval"` | Agent waiting for human approval    |
| `frequency`                       | Count of events in that time bucket |
| `bucket`                          | Time grouping (e.g., "weekly")      |
| `source_id`                       | Agent ID                            |

## Common Queries

### Find Most Used Agents

1. Call `relevance_api_request` with `POST /agents/analytics` and `{ filters: {} }`
2. In the response, filter `states_results.timeseries` for entries where `event_value` is `"running"`
3. Group by `source_id` (agent ID) and sum `frequency` to get total runs per agent
4. Cross-reference agent IDs with `relevance_list_agents` to get agent names

### Find Idle Agents (No Runs in Last 30 Days)

1. Call analytics with a date filter: `{ filters: { insert_date_: { gte: "2025-12-01T00:00:00.000Z" } } }`
2. Collect all `source_id` values from entries where `event_value` is `"running"` — these are active agents
3. Call `relevance_list_agents` and find agents whose IDs are NOT in the active set

### Count Tasks Pending Approval

Call analytics with `{ filters: {} }` and sum the `frequency` of all entries where `event_value` is `"pending-approval"`.

### Get Usage Trend for Specific Agent

Call analytics with `{ filters: { agentId: { eq: "your-agent-id" } } }`. The `states_results.timeseries` entries with `event_value: "running"` show weekly run counts via `insert_date_` (week) and `frequency` (count).

## Related Endpoints

| Endpoint                 | Purpose                                             |
| ------------------------ | --------------------------------------------------- |
| `GET /agents/list`       | List all agents (includes `metadata.last_run_date`) |
| `GET /agents/{agentId}`  | Get agent details by ID                             |
| `POST /agents/analytics` | Get usage analytics (this skill)                    |

## Tips

1. **Pagination:** Analytics returns all data - no pagination needed
2. **Date filtering:** Use ISO 8601 format for dates
3. **Agent names:** Analytics only returns IDs - cross-reference with `relevance_list_agents`
4. **Time buckets:** Data is pre-aggregated into "weekly" buckets
