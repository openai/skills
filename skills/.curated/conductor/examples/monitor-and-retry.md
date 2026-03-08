# Example: Monitor and Retry Failed Workflows

## User Request

> "Show me all failed workflows from today and retry the ones that failed due to timeouts"

## Workflow Execution

### Step 1: Search for Failed Workflows

```bash
conductor workflow search -s FAILED --start-time-after "2024-01-15" -c 20
```

**Response:**
```
WORKFLOW ID                              NAME                   STATUS   START TIME
f1a2b3c4-d5e6-7890-abcd-111111111111    order_processing       FAILED   2024-01-15 08:12:33
f1a2b3c4-d5e6-7890-abcd-222222222222    data_pipeline          FAILED   2024-01-15 09:45:12
f1a2b3c4-d5e6-7890-abcd-333333333333    email_campaign         FAILED   2024-01-15 10:30:05
f1a2b3c4-d5e6-7890-abcd-444444444444    order_processing       FAILED   2024-01-15 11:15:44
```

### Step 2: Get Details for Each Failed Workflow

```bash
conductor workflow get-execution f1a2b3c4-d5e6-7890-abcd-111111111111 -c
```

**Response (order_processing #1):**
```json
{
  "workflowId": "f1a2b3c4-d5e6-7890-abcd-111111111111",
  "status": "FAILED",
  "reasonForIncompletion": "Task timed out",
  "tasks": [
    {"taskReferenceName": "validate_order", "status": "COMPLETED"},
    {"taskReferenceName": "call_inventory_api", "status": "TIMED_OUT", "retryCount": 3}
  ]
}
```

```bash
conductor workflow get-execution f1a2b3c4-d5e6-7890-abcd-222222222222 -c
```

**Response (data_pipeline):**
```json
{
  "workflowId": "f1a2b3c4-d5e6-7890-abcd-222222222222",
  "status": "FAILED",
  "reasonForIncompletion": "Task timed out",
  "tasks": [
    {"taskReferenceName": "extract_data", "status": "COMPLETED"},
    {"taskReferenceName": "transform_data", "status": "TIMED_OUT", "retryCount": 2}
  ]
}
```

```bash
conductor workflow get-execution f1a2b3c4-d5e6-7890-abcd-333333333333 -c
```

**Response (email_campaign):**
```json
{
  "workflowId": "f1a2b3c4-d5e6-7890-abcd-333333333333",
  "status": "FAILED",
  "reasonForIncompletion": "Invalid email template",
  "tasks": [
    {"taskReferenceName": "render_template", "status": "FAILED_WITH_TERMINAL_ERROR"}
  ]
}
```

```bash
conductor workflow get-execution f1a2b3c4-d5e6-7890-abcd-444444444444 -c
```

**Response (order_processing #2):**
```json
{
  "workflowId": "f1a2b3c4-d5e6-7890-abcd-444444444444",
  "status": "FAILED",
  "reasonForIncompletion": "Task timed out",
  "tasks": [
    {"taskReferenceName": "call_inventory_api", "status": "TIMED_OUT", "retryCount": 3}
  ]
}
```

### Step 3: Present Findings

```
Found 4 failed workflows from today:

WORKFLOW ID       NAME              FAILED TASK          REASON              RETRIES
...111111111111   order_processing  call_inventory_api   Task timed out      3
...222222222222   data_pipeline     transform_data       Task timed out      2
...333333333333   email_campaign    render_template      Invalid template    0 (terminal)
...444444444444   order_processing  call_inventory_api   Task timed out      3

Timeout failures (retryable): 3 workflows
Terminal failures (not retryable): 1 workflow (email_campaign — needs template fix)
```

### Step 4: Retry Timeout Failures

```bash
conductor workflow retry f1a2b3c4-d5e6-7890-abcd-111111111111
conductor workflow retry f1a2b3c4-d5e6-7890-abcd-222222222222
conductor workflow retry f1a2b3c4-d5e6-7890-abcd-444444444444
```

### Step 5: Verify Retries

```bash
conductor workflow status f1a2b3c4-d5e6-7890-abcd-111111111111
# RUNNING
conductor workflow status f1a2b3c4-d5e6-7890-abcd-222222222222
# RUNNING
conductor workflow status f1a2b3c4-d5e6-7890-abcd-444444444444
# RUNNING
```

## Summary Provided to User

```
Failed workflow analysis and retry complete.

Found: 4 failed workflows from today

Retried (timeout failures): 3
  - order_processing (...111) → now RUNNING
  - data_pipeline (...222) → now RUNNING
  - order_processing (...444) → now RUNNING

Skipped (terminal failures): 1
  - email_campaign (...333) — "Invalid email template"
    This failed with FAILED_WITH_TERMINAL_ERROR on render_template.
    The template needs to be fixed before this workflow can succeed.

Recommendation: If the inventory API timeouts persist, consider
increasing the task timeout in the order_processing workflow definition.
```

## Key Features Demonstrated

- Search with status and time filters to narrow results
- Detailed execution inspection to diagnose root causes
- Distinguishing retryable failures (timeouts) from terminal failures (bad data)
- Batch retry of selected workflows
- Post-retry verification
- Actionable recommendations based on failure patterns
