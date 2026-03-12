# Running and Testing Tools

How to execute tools, handle async operations, and debug issues.

## Synchronous Execution

For tools that complete quickly:

```typescript
relevance_run_tool({
  studioId: 'my-tool',
  params: { query: 'test input' },
});
```

Returns the tool output directly.

## Asynchronous Execution

For long-running tools:

```typescript
// 1. Start async execution
const { job_id } = await relevance_trigger_tool_async({
  studioId: 'my-tool',
  params: { query: 'test input' },
});

// 2. Poll for results
relevance_poll_tool_result({
  studioId: 'my-tool',
  jobId: job_id,
});
```

### Poll Response States

| Status      | Meaning               |
| ----------- | --------------------- |
| `pending`   | Job queued            |
| `running`   | Currently executing   |
| `completed` | Finished successfully |
| `failed`    | Execution failed      |

## Getting Latest Run

Useful for getting example task IDs:

```typescript
relevance_get_latest_tool_run({
  studioId: 'my-tool',
});
```

## Testing Workflow

### 1. Test with Minimal Input

```typescript
relevance_run_tool({
  studioId: 'my-tool',
  params: { query: 'simple test' },
});
```

### 2. Test Each Step

If a multi-step tool fails, test transformations individually by creating a minimal tool with just that step.

### 3. Check Step Outputs

Examine the full response to see what each step returned:

```json
{
  "output": {
    "search": { "results": [...] },
    "analyze": { "analysis": "..." }
  },
  "steps": {
    "search": { "status": "completed", "output": {...} },
    "analyze": { "status": "completed", "output": {...} }
  }
}
```

### 4. Debug Python Steps

For Python steps, add print statements (they appear in logs):

```python
import json
data = {{input}}
print(f"Input type: {type(data)}")
print(f"Input value: {data}")
return {"result": data}
```

## Common Issues

### Tool Returns Empty Output

1. Check transformation outputs are mapped correctly
2. Verify `{{answer}}` vs `{{text}}` for prompt_completion
3. Check `{{transformed.field}}` for Python steps

### Step Failed

1. Check the step status in response
2. Look for error messages
3. Verify input parameters are correct type

### Timeout

- Long-running tools may timeout
- Use async execution for tools > 30 seconds
- Consider breaking into smaller tools

### "Variable not found"

1. Check variable name spelling
2. Verify previous step actually outputs that variable
3. Check output mapping in previous step

## Debugging with Raw API

### Get Tool Run History

```typescript
relevance_api_request({
  method: 'GET',
  endpoint: `/studios/run_history/list?page_size=10&filters=${encodeURIComponent(
    JSON.stringify([
      {
        field: 'studio_id',
        filter_type: 'exact_match',
        condition: '==',
        condition_value: 'my-tool-id',
      },
    ])
  )}`,
});
```

### Get Specific Run Details

```typescript
relevance_api_request({
  method: 'GET',
  endpoint: `/studios/tasks/${taskId}/get`,
});
```

## URL Patterns

### Tool Editor

```
https://app.relevanceai.com/notebook/{region}/{project}/{studioId}
```

Open this to see/edit the tool visually.

### Run History

View in the Relevance AI dashboard under tool settings.

## Best Practices

1. **Start simple** - Test with basic inputs first
2. **Check each step** - Review step outputs in response
3. **Use descriptive names** - Makes debugging easier
4. **Handle errors in Python** - Add try/catch blocks
5. **Log intermediate values** - Use print() in Python for debugging
6. **Test edge cases** - Empty inputs, special characters, etc.
