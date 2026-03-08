# Writing Conductor Workers

Workers execute SIMPLE tasks in a workflow. They poll the Conductor server for tasks, execute business logic, and report results back. Workers are stateless and idempotent.

## How workers work

1. Workflow reaches a SIMPLE task
2. Task is placed in a queue
3. Worker polls the queue, picks up the task
4. Worker executes logic using task's `inputData`
5. Worker returns result (COMPLETED or FAILED) with `outputData`
6. Workflow continues to the next task

## SDKs

| Language | Package | Install |
|----------|---------|---------|
| Python | `conductor-python` | `pip install conductor-python` |
| JavaScript/TypeScript | `@io-orkes/conductor-javascript` | `npm install @io-orkes/conductor-javascript` |
| Java | `org.conductoross:conductor-client` | Maven/Gradle (see below) |
| Go | `github.com/conductor-sdk/conductor-go` | `go get github.com/conductor-sdk/conductor-go` |
| C# | [conductor-oss/csharp-sdk](https://github.com/conductor-oss/csharp-sdk) | NuGet |
| Ruby | [conductor-oss/ruby-sdk](https://github.com/conductor-oss/ruby-sdk) | Gem |
| Rust | [conductor-oss/rust-sdk](https://github.com/conductor-oss/rust-sdk) | Cargo |

All SDKs connect via the same env vars: `CONDUCTOR_SERVER_URL`, `CONDUCTOR_AUTH_KEY`, `CONDUCTOR_AUTH_SECRET`.

---

## Python

```bash
pip install conductor-python
```

### Define a worker

```python
from conductor.client.worker.worker_task import worker_task

@worker_task(task_definition_name='process_order')
def process_order(order_id: str, amount: float) -> dict:
    # Your business logic here
    return {'status': 'processed', 'order_id': order_id, 'total': amount * 1.1}
```

Function parameters are automatically mapped from the task's `inputParameters`. The return value becomes the task's `outputData`.

### Start workers

```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration

config = Configuration()  # reads CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET
with TaskHandler(configuration=config, scan_for_annotated_workers=True) as handler:
    handler.start_processes()
    # Workers poll until stopped
```

---

## JavaScript / TypeScript

```bash
npm install @io-orkes/conductor-javascript
```

### Define and run a worker

```typescript
import {
  orkesConductorClient,
  TaskManager,
} from "@io-orkes/conductor-javascript";

const client = await orkesConductorClient({
  serverUrl: "http://localhost:8080/api",
});

const taskManager = new TaskManager(client, [
  {
    taskType: "process_order",
    execute: async ({ inputData }) => {
      return {
        status: "COMPLETED",
        outputData: {
          status: "processed",
          order_id: inputData.order_id,
        },
      };
    },
  },
]);

taskManager.startPolling();
```

---

## Java

**Gradle:**
```gradle
implementation 'org.conductoross:conductor-client:5.0.0'
```

**Maven:**
```xml
<dependency>
    <groupId>org.conductoross</groupId>
    <artifactId>conductor-client</artifactId>
    <version>5.0.0</version>
</dependency>
```

### Option A: Implement Worker interface

```java
public class ProcessOrderWorker implements Worker {
    @Override
    public String getTaskDefName() {
        return "process_order";
    }

    @Override
    public TaskResult execute(Task task) {
        String orderId = (String) task.getInputData().get("order_id");
        TaskResult result = new TaskResult(task);
        result.setStatus(TaskResult.Status.COMPLETED);
        result.addOutputData("status", "processed");
        result.addOutputData("order_id", orderId);
        return result;
    }
}
```

### Option B: @WorkerTask annotation

```java
public class Workers {
    @WorkerTask("process_order")
    public Map<String, Object> processOrder(@InputParam("order_id") String orderId) {
        return Map.of("status", "processed", "order_id", orderId);
    }
}
```

### Start workers

```java
ConductorClient client = ConductorClient.builder()
    .basePath("http://localhost:8080/api")
    .build();

TaskClient taskClient = new TaskClient(client);
new TaskRunnerConfigurer.Builder(taskClient, List.of(new ProcessOrderWorker()))
    .withThreadCount(10)
    .build()
    .init();
```

---

## Go

```bash
go get github.com/conductor-sdk/conductor-go
```

### Define and run a worker

```go
package main

import (
    "fmt"
    "time"
    "github.com/conductor-sdk/conductor-go/sdk/client"
    "github.com/conductor-sdk/conductor-go/sdk/model"
    "github.com/conductor-sdk/conductor-go/sdk/worker"
)

func ProcessOrder(task *model.Task) (interface{}, error) {
    orderId := fmt.Sprintf("%v", task.InputData["order_id"])
    return map[string]interface{}{
        "status":   "processed",
        "order_id": orderId,
    }, nil
}

func main() {
    apiClient := client.NewAPIClientFromEnv()
    taskRunner := worker.NewTaskRunnerWithApiClient(apiClient)
    taskRunner.StartWorker("process_order", ProcessOrder, 1, time.Millisecond*100)
    // Blocks and polls until stopped
    select {}
}
```

---

## Linking workers to workflows

In your workflow definition, use `"type": "SIMPLE"` and set `"name"` to the task type your worker polls for:

```json
{
  "name": "process_order",
  "taskReferenceName": "process_order_ref",
  "type": "SIMPLE",
  "inputParameters": {
    "order_id": "${workflow.input.order_id}",
    "amount": "${workflow.input.amount}"
  }
}
```

The worker registered for task type `process_order` will automatically pick up this task when the workflow reaches it.

## Best practices

- **Idempotent**: Workers may receive the same task on retry. Design for safe re-execution.
- **Timeouts**: Set `responseTimeoutSeconds` on task definitions so stuck tasks get rescheduled.
- **Error handling**: Return `FAILED` status with a `reasonForIncompletion` message for graceful failures. Return `FAILED_WITH_TERMINAL_ERROR` to fail the task without retrying.
- **Scaling**: Run multiple worker instances for throughput. Each polls independently.
- **Domain isolation**: Use task domains to route tasks to specific worker groups (e.g. region-specific workers).
