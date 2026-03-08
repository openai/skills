# Example: Create and Run a Workflow

## User Request

> "Create a workflow that calls a weather API and then sends a notification, then run it"

## Workflow Execution

### Step 1: Check Prerequisites

```bash
conductor --version
# conductor-cli v1.2.0
```

CLI available. Check server:

```bash
echo $CONDUCTOR_SERVER_URL
# http://localhost:8080/api
```

### Step 2: Consult Workflow Schema

Load `references/workflow-definition.md` for task types and JSON structure.

### Step 3: Create Workflow Definition

```json
{
  "name": "weather_notification",
  "description": "Fetch weather data and send a notification",
  "version": 1,
  "schemaVersion": 2,
  "inputParameters": ["city", "notifyEmail"],
  "tasks": [
    {
      "name": "fetch_weather",
      "taskReferenceName": "fetch_weather",
      "type": "HTTP",
      "inputParameters": {
        "http_request": {
          "uri": "https://api.weather.example.com/current?city=${workflow.input.city}",
          "method": "GET",
          "headers": {
            "Accept": "application/json"
          }
        }
      }
    },
    {
      "name": "send_notification",
      "taskReferenceName": "send_notification",
      "type": "HTTP",
      "inputParameters": {
        "http_request": {
          "uri": "https://api.notify.example.com/send",
          "method": "POST",
          "headers": {
            "Content-Type": "application/json"
          },
          "body": {
            "to": "${workflow.input.notifyEmail}",
            "subject": "Weather Update",
            "message": "Current weather in ${workflow.input.city}: ${fetch_weather.output.response.body.temperature}°F, ${fetch_weather.output.response.body.condition}"
          }
        }
      }
    }
  ],
  "outputParameters": {
    "weather": "${fetch_weather.output.response.body}",
    "notificationStatus": "${send_notification.output.response.statusCode}"
  }
}
```

### Step 4: Register Workflow

```bash
conductor workflow create weather_notification.json
# Workflow weather_notification created successfully
```

### Step 5: Start Workflow

```bash
conductor workflow start -w weather_notification -i '{"city": "San Francisco", "notifyEmail": "user@example.com"}'
# a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### Step 6: Check Execution Status

```bash
conductor workflow get-execution a1b2c3d4-e5f6-7890-abcd-ef1234567890 -c
```

**Response:**
```json
{
  "workflowId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "workflowName": "weather_notification",
  "status": "COMPLETED",
  "startTime": "2024-01-15T10:30:00Z",
  "endTime": "2024-01-15T10:30:02Z",
  "tasks": [
    {
      "taskReferenceName": "fetch_weather",
      "status": "COMPLETED",
      "outputData": {"response": {"body": {"temperature": 62, "condition": "Partly Cloudy"}}}
    },
    {
      "taskReferenceName": "send_notification",
      "status": "COMPLETED",
      "outputData": {"response": {"statusCode": 200}}
    }
  ]
}
```

## Summary Provided to User

```
Workflow created and executed successfully.

- Workflow: weather_notification (v1)
- Execution ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
- Status: COMPLETED
- Duration: 2 seconds

Tasks:
  1. fetch_weather — COMPLETED (62°F, Partly Cloudy)
  2. send_notification — COMPLETED (HTTP 200)

Output: Weather notification sent to user@example.com
```

## Key Features Demonstrated

- HTTP task type for external API calls
- Input expressions (`${workflow.input.city}`) for parameterization
- Task-to-task data passing (`${fetch_weather.output.response.body.temperature}`)
- Workflow output parameters for aggregated results
- CLI commands: create → start → get-execution
