# Example: Signal a WAIT Task to Advance a Workflow

## User Request

> "I have an order processing workflow waiting for payment confirmation. The payment for workflow order-wf-789 has been received, please approve it."

## Workflow Execution

### Step 1: Check Prerequisites

```bash
conductor --version
# conductor-cli v1.2.0
```

### Step 2: Get Workflow Execution Details

```bash
conductor workflow get-execution order-wf-789 -c
```

**Response:**
```json
{
  "workflowId": "order-wf-789",
  "workflowName": "order_processing",
  "status": "RUNNING",
  "tasks": [
    {
      "taskReferenceName": "validate_order",
      "status": "COMPLETED"
    },
    {
      "taskReferenceName": "calculate_total",
      "status": "COMPLETED",
      "outputData": {"total": 149.99}
    },
    {
      "taskReferenceName": "wait_for_payment",
      "taskType": "WAIT",
      "status": "IN_PROGRESS"
    },
    {
      "taskReferenceName": "fulfill_order",
      "status": "SCHEDULED"
    }
  ]
}
```

### Step 3: Identify the Blocking Task

The workflow is blocked at `wait_for_payment` (type: WAIT, status: IN_PROGRESS). This is the task that needs to be signaled.

### Step 4: Signal the Task

```bash
conductor task signal-sync \
  --workflow-id order-wf-789 \
  --task-ref wait_for_payment \
  --status COMPLETED \
  --output '{"paymentId": "pay-456", "amount": 149.99, "method": "credit_card", "confirmed": true}'
```

**Response (updated workflow):**
```json
{
  "workflowId": "order-wf-789",
  "status": "RUNNING",
  "tasks": [
    {"taskReferenceName": "validate_order", "status": "COMPLETED"},
    {"taskReferenceName": "calculate_total", "status": "COMPLETED"},
    {"taskReferenceName": "wait_for_payment", "status": "COMPLETED"},
    {"taskReferenceName": "fulfill_order", "status": "IN_PROGRESS"}
  ]
}
```

### Step 5: Verify Workflow Progressed

```bash
conductor workflow get-execution order-wf-789
```

The workflow has moved past the WAIT task and is now executing `fulfill_order`.

## Summary Provided to User

```
Payment confirmation signal sent successfully.

- Workflow: order_processing (order-wf-789)
- Task signaled: wait_for_payment → COMPLETED
- Payment ID: pay-456 ($149.99 via credit_card)
- Workflow status: RUNNING (now executing fulfill_order)

The order is being fulfilled. You can check final status with:
  conductor workflow get-execution order-wf-789
```

## Key Features Demonstrated

- Fetching execution details to identify the blocking task
- Using `signal-sync` to signal and get the updated workflow in one call
- Passing structured output data with the signal (payment details)
- Verifying workflow progression after signaling
- WAIT task pattern for human-in-the-loop workflows
