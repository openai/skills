# Conductor REST API Reference

## Authentication

Include one of these headers with every request:

```
X-Authorization: {token}
Content-Type: application/json
```

## Base URL

All paths below are relative to the server base URL (e.g. `http://localhost:8080/api`).

## Workflow metadata endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/metadata/workflow` | List all workflow definitions |
| GET | `/metadata/workflow/{name}?version={v}` | Get workflow definition |
| GET | `/metadata/workflow/names-and-versions` | List names and versions only |
| GET | `/metadata/workflow/latest-versions` | Get latest version of all workflows |
| POST | `/metadata/workflow` | Create a workflow definition |
| POST | `/metadata/workflow/validate` | Validate a workflow definition |
| PUT | `/metadata/workflow` | Update workflow definitions (array) |
| DELETE | `/metadata/workflow/{name}/{version}` | Delete a workflow definition |

## Workflow execution endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/workflow` | Start workflow (body: StartWorkflowRequest) |
| POST | `/workflow/{name}` | Start workflow by name (body: input map) |
| POST | `/workflow/execute/{name}/{version}` | Execute synchronously |
| GET | `/workflow/{workflowId}?includeTasks=true` | Get execution status |
| GET | `/workflow/{workflowId}/tasks` | Get execution tasks (paginated) |
| GET | `/workflow/running/{name}?version={v}` | List running workflow IDs |
| GET | `/workflow/search?query={q}&start={s}&size={n}` | Search executions |
| GET | `/workflow/{name}/correlated/{correlationId}` | Get by correlation ID |
| PUT | `/workflow/{workflowId}/pause` | Pause workflow |
| PUT | `/workflow/{workflowId}/resume` | Resume workflow |
| DELETE | `/workflow/{workflowId}?reason={r}` | Terminate workflow |
| POST | `/workflow/{workflowId}/restart` | Restart completed workflow |
| POST | `/workflow/{workflowId}/retry` | Retry last failed task |
| POST | `/workflow/{workflowId}/rerun` | Rerun from specific task |
| PUT | `/workflow/{workflowId}/skiptask/{taskRef}` | Skip a task |
| PUT | `/workflow/decide/{workflowId}` | Trigger decide |
| DELETE | `/workflow/{workflowId}/remove` | Remove from system |
| POST | `/workflow/test` | Test with mock data |

## Task endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tasks/poll/{tasktype}` | Poll for a single task |
| GET | `/tasks/poll/batch/{tasktype}?count={n}` | Batch poll for tasks |
| POST | `/tasks` | Update a task (body: TaskResult) |
| POST | `/tasks/{workflowId}/{taskRefName}/{status}` | Update task by ref (async) |
| POST | `/tasks/{workflowId}/{taskRefName}/{status}/sync` | Update task by ref (returns workflow) |
| GET | `/tasks/{taskId}` | Get task by ID |
| POST | `/tasks/{taskId}/log` | Log task execution details |
| GET | `/tasks/{taskId}/log` | Get task execution logs |
| GET | `/tasks/queue/size?taskType={t}` | Get queue size |
| GET | `/tasks/queue/all` | Get all queue details |
| GET | `/tasks/search?query={q}` | Search tasks |

## Task definition endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/metadata/taskdefs` | List all task definitions |
| GET | `/metadata/taskdefs/{tasktype}` | Get task definition |
| POST | `/metadata/taskdefs` | Create task definitions (array) |
| PUT | `/metadata/taskdefs` | Update a task definition |
| DELETE | `/metadata/taskdefs/{tasktype}` | Delete task definition |

## Event endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/event` | List all event handlers |
| GET | `/event/{event}?activeOnly=true` | Get handlers for event |
| POST | `/event` | Create event handler |
| PUT | `/event` | Update event handler |
| DELETE | `/event/{name}` | Delete event handler |

## Search query syntax

The `query` parameter supports field-based filtering:

- `status=RUNNING`
- `workflowType=my_workflow`
- `startTime>[epoch_ms]`
- `startTime<[epoch_ms]`

Combine with AND: `status=RUNNING AND workflowType=my_workflow`

The `sort` parameter: `sort=startTime:DESC`

## Response codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 204 | Success, no content |
| 400 | Bad request (invalid input) |
| 401 | Unauthorized (missing/invalid token) |
| 404 | Resource not found |
| 409 | Conflict (already exists) |
| 500 | Server error |
