# Conductor Workflow Definition Reference

## Workflow definition schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Workflow name (unique identifier) |
| `description` | string | no | Human-readable description |
| `version` | integer | no | Version number (default: 1) |
| `tasks` | array | yes | Ordered list of task definitions |
| `inputParameters` | array | no | Expected input parameter names |
| `outputParameters` | object | no | Mapping of output keys to expressions |
| `schemaVersion` | integer | no | Schema version (use 2) |
| `restartable` | boolean | no | Whether workflow can be restarted (default: true) |
| `ownerEmail` | string | no | Owner email for notifications |
| `timeoutPolicy` | string | no | `ALERT_ONLY` or `TIME_OUT_WF` |
| `timeoutSeconds` | long | no | Workflow timeout (0 = no timeout) |
| `failureWorkflow` | string | no | Workflow to run on failure |
| `variables` | object | no | Workflow-level variables |

## Task definition in workflow

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Task name (must match task definition for SIMPLE tasks) |
| `taskReferenceName` | string | yes | **Must be unique** across the entire workflow definition |
| `type` | string | yes | Task type (see below) |
| `inputParameters` | object | no | Input mapping using `${...}` expressions |
| `optional` | boolean | no | If true, failure won't fail the workflow |
| `startDelay` | integer | no | Delay in seconds before starting |
| `asyncComplete` | boolean | no | If true, task completes via external signal |

## Input expressions

Reference workflow input, task output, or variables:

- `${workflow.input.paramName}` — workflow input
- `${taskRefName.output.fieldName}` — output from a prior task
- `${workflow.variables.varName}` — workflow variable

---

## System task types

### SIMPLE
Worker task polled and executed by external workers.
```json
{"name": "my_task", "taskReferenceName": "my_task_ref", "type": "SIMPLE", "inputParameters": {"param1": "${workflow.input.data}"}}
```

### HTTP
Make HTTP requests. Supports GET, POST, PUT, DELETE, OPTIONS, HEAD with headers, body, and timeouts.
```json
{
  "name": "http_call", "taskReferenceName": "call_api", "type": "HTTP",
  "inputParameters": {
    "http_request": {
      "uri": "https://api.example.com/data",
      "method": "POST",
      "headers": {"Authorization": "Bearer ${workflow.input.token}"},
      "body": {"key": "${workflow.input.value}"},
      "accept": "application/json",
      "contentType": "application/json",
      "connectionTimeOut": 3000,
      "readTimeOut": 3000
    }
  }
}
```
**Input schema** (inside `http_request`):

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `uri` | string | yes | — | Full URL to call |
| `method` | string | yes | — | HTTP method: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`, `HEAD` |
| `headers` | map\<string, object\> | no | `{}` | Request headers as key-value pairs |
| `body` | object/string | no | — | Request body (auto-serialized to JSON) |
| `accept` | string | no | `"application/json"` | Accept header MIME type |
| `contentType` | string | no | `"application/json"` | Content-Type header MIME type |
| `connectionTimeOut` | integer | no | `3000` | Connection timeout in milliseconds |
| `readTimeOut` | integer | no | `3000` | Read timeout in milliseconds |
| `vipAddress` | string | no | — | Discovery-based address (Eureka) |
| `appName` | string | no | — | Application name for discovery |

**Output schema** — the task outputs a `response` object:
```json
{
  "response": {
    "statusCode": 200,
    "reasonPhrase": "OK",
    "headers": {"Content-Type": ["application/json"]},
    "body": { }
  }
}
```
- `response.statusCode` (int) — HTTP status code
- `response.reasonPhrase` (string) — HTTP reason phrase (e.g. `"OK"`, `"Not Found"`)
- `response.headers` (map) — response headers (each value is an array of strings)
- `response.body` (object/array/string/number) — parsed response body (auto-parsed as JSON if possible, otherwise raw string)

To reference in subsequent tasks: `${call_api.output.response.body.fieldName}`, `${call_api.output.response.statusCode}`.

### JSON_JQ_TRANSFORM
Transform data using jq expressions. Powerful for reshaping, filtering, and aggregating JSON.
```json
{
  "name": "transform", "taskReferenceName": "jq_ref", "type": "JSON_JQ_TRANSFORM",
  "inputParameters": {
    "data": "${workflow.input.items}",
    "queryExpression": "[.[] | {name: .name, id: .id}]"
  }
}
```
Common jq patterns:
- Filter: `[.[] | select(.status == "active")]`
- Map: `[.[] | {id: .id, label: .name}]`
- Aggregate: `{total: ([.[].amount] | add), count: length}`
- Flatten: `[.[][] | .field]`

> **Rule for all JavaScript-evaluated tasks (INLINE, DO_WHILE, SWITCH with `javascript` evaluator):**
> Every variable referenced as `$.varName` inside a script or condition **must** be declared as an `inputParameters` key on that task. The `$` object in the script is the task's resolved `inputParameters` map.

### INLINE
Execute lightweight scripts (JavaScript via GraalVM).
```json
{
  "name": "inline_task", "taskReferenceName": "compute", "type": "INLINE",
  "inputParameters": {
    "evaluatorType": "graaljs",
    "expression": "function e() { return $.value * 2; } e();",
    "value": "${workflow.input.number}"
  }
}
```
**Important**: Every variable referenced as `$.varName` inside the script **must** be declared as an `inputParameters` key. For example, if the script uses `$.value` and `$.name`, both `value` and `name` must be present in `inputParameters`:
```json
{
  "name": "inline_task", "taskReferenceName": "compute", "type": "INLINE",
  "inputParameters": {
    "evaluatorType": "graaljs",
    "expression": "function e() { return $.name + ' is ' + $.age; } e();",
    "name": "${workflow.input.name}",
    "age": "${workflow.input.age}"
  }
}
```
The `$` object inside the script is the task's resolved `inputParameters` map (excluding `evaluatorType` and `expression`).

### SWITCH
Conditional branching based on a value or JavaScript expression.
```json
{
  "name": "switch_task", "taskReferenceName": "route", "type": "SWITCH",
  "evaluatorType": "value-param",
  "expression": "switchCaseValue",
  "inputParameters": {"switchCaseValue": "${workflow.input.type}"},
  "decisionCases": {
    "typeA": [{"...task A...": ""}],
    "typeB": [{"...task B...": ""}]
  },
  "defaultCase": [{"...default task...": ""}]
}
```
When using `evaluatorType: "javascript"`, the same `$.varName` rule applies — all variables referenced in the expression must be declared in `inputParameters`:
```json
{
  "name": "switch_task", "taskReferenceName": "js_route", "type": "SWITCH",
  "evaluatorType": "javascript",
  "expression": "$.priority > 5 ? 'high' : 'low'",
  "inputParameters": {"priority": "${workflow.input.priority}"},
  "decisionCases": {
    "high": [{"...urgent task...": ""}],
    "low": [{"...normal task...": ""}]
  },
  "defaultCase": [{"...default task...": ""}]
}
```

### FORK_JOIN / JOIN
Execute tasks in parallel. Always pair FORK_JOIN with a JOIN task.
```json
{"name": "fork", "taskReferenceName": "parallel", "type": "FORK_JOIN", "forkTasks": [[{"...task A...": ""}], [{"...task B...": ""}]]}
```
```json
{"name": "join", "taskReferenceName": "join_ref", "type": "JOIN", "joinOn": ["taskA_ref", "taskB_ref"]}
```

### DO_WHILE
Loop until a condition is met.
```json
{
  "name": "loop", "taskReferenceName": "loop_ref", "type": "DO_WHILE",
  "loopCondition": "if ($.loop_ref['iteration'] < $.value) true; else false;",
  "loopOver": [{"...task...": ""}],
  "inputParameters": {
    "value": "${workflow.input.count}",
    "loop_ref": "${loop_ref.output}"
  }
}
```
**Important**: The `loopCondition` is evaluated as JavaScript. The same `$.varName` rule applies — every variable referenced as `$.varName` must be declared in `inputParameters`. Here, `$.loop_ref['iteration']` requires `loop_ref` to be declared. The mapping `"loop_ref": "${loop_ref.output}"` wires the task's own output (which includes the `iteration` counter) back into the script's scope.

### WAIT
Pause execution until a signal, a duration elapses, or a specific date/time is reached. Use `conductor task signal` to resume a signal-based wait.

**Wait forever (signal mode)** — pauses until explicitly signaled via API or CLI:
```json
{"name": "wait_task", "taskReferenceName": "wait_for_signal", "type": "WAIT", "inputParameters": {}}
```

**Wait for a duration** — resumes automatically after the specified time:
```json
{"name": "wait_task", "taskReferenceName": "wait_10m", "type": "WAIT", "inputParameters": {"duration": "10m"}}
```
Duration format: `[Xd] [Xh] [Xm] [Xs]` — combine any units, case-insensitive, integers only (no decimals).
- Days: `days`, `day`, `d`
- Hours: `hours`, `hour`, `hrs`, `hr`, `h`
- Minutes: `minutes`, `minute`, `mins`, `min`, `m`
- Seconds: `seconds`, `second`, `secs`, `sec`, `s`
- Examples: `"5s"`, `"5m"`, `"2h"`, `"5d"`, `"5d 5h 5m 5s"`, `"30m 10s"`
- Invalid: `"5"` (no unit), `"5.0s"` (no decimals)

**Wait until a specific date/time** — resumes at the given timestamp:
```json
{"name": "wait_task", "taskReferenceName": "wait_until", "type": "WAIT", "inputParameters": {"until": "2026-01-15 17:00"}}
```
Until format (parsed in order): `yyyy-MM-dd HH:mm`, `yyyy-MM-dd HH:mm z`, or `yyyy-MM-dd`.
- With timezone: `"2026-01-15 17:00 GMT+04:00"`, `"2026-01-15 17:00 PST"`
- Without timezone: `"2026-01-15 17:00"` (uses server timezone)
- Date only: `"2026-01-15"` (midnight)
- Dynamic: `"until": "${workflow.input.scheduledTime}"`

Note: you cannot specify both `duration` and `until` — the task will fail with `FAILED_WITH_TERMINAL_ERROR`.

### HUMAN
Wait for human input (similar to WAIT but designed for human-in-the-loop).
```json
{"name": "human_task", "taskReferenceName": "approval", "type": "HUMAN"}
```

### SUB_WORKFLOW
Execute another workflow as a task. The parent workflow waits for the sub-workflow to complete.
```json
{"name": "sub", "taskReferenceName": "sub_ref", "type": "SUB_WORKFLOW", "subWorkflowParam": {"name": "child_workflow", "version": 1}, "inputParameters": {"data": "${workflow.input.payload}"}}
```

### START_WORKFLOW
Start another workflow asynchronously (fire-and-forget). Unlike SUB_WORKFLOW, the parent does NOT wait — it immediately completes and outputs the child's workflowId.
```json
{
  "name": "start_wf", "taskReferenceName": "start_ref", "type": "START_WORKFLOW",
  "inputParameters": {
    "startWorkflow": {
      "name": "child_workflow",
      "version": 1,
      "input": {"key": "${workflow.input.value}"},
      "correlationId": "${workflow.correlationId}"
    }
  }
}
```
**Outputs**: `workflowId` (the started workflow's ID).

### DYNAMIC
Dynamically resolve the task type at runtime. The `dynamicTaskNameParam` input specifies which input parameter holds the actual task name to execute.
```json
{
  "name": "dynamic_task", "taskReferenceName": "dynamic_ref", "type": "DYNAMIC",
  "dynamicTaskNameParam": "taskToExecute",
  "inputParameters": {
    "taskToExecute": "${workflow.input.taskName}",
    "param1": "${workflow.input.data}"
  }
}
```

### FORK_JOIN_DYNAMIC
Dynamically create parallel branches at runtime. A `dynamicForkTasksParam` input provides the list of tasks, and `dynamicForkTasksInputParamName` provides their inputs.
```json
{
  "name": "dynamic_fork", "taskReferenceName": "dfork_ref", "type": "FORK_JOIN_DYNAMIC",
  "dynamicForkTasksParam": "dynamicTasks",
  "dynamicForkTasksInputParamName": "dynamicTasksInput",
  "inputParameters": {
    "dynamicTasks": "${generate_tasks.output.tasks}",
    "dynamicTasksInput": "${generate_tasks.output.inputs}"
  }
}
```
Always follow with a JOIN task. The `dynamicTasks` value is an array of task definitions, and `dynamicTasksInput` is a map of taskReferenceName to input objects.

### EXCLUSIVE_JOIN
Like JOIN but completes as soon as any ONE of the specified tasks completes (instead of waiting for all). Used after FORK_JOIN for exclusive/race patterns.
```json
{
  "name": "exclusive_join", "taskReferenceName": "ejoin_ref", "type": "EXCLUSIVE_JOIN",
  "inputParameters": {},
  "joinOn": ["taskA_ref", "taskB_ref"],
  "defaultExclusiveJoinTask": ["taskA_ref"]
}
```

### EVENT
Publish an event to a sink (e.g. SQS, Conductor internal).
```json
{"name": "event", "taskReferenceName": "publish", "type": "EVENT", "sink": "conductor:event_name", "inputParameters": {"payload": "${workflow.input.data}"}}
```

### KAFKA_PUBLISH
Publish a message to a Kafka topic. Requires the Kafka module to be enabled.
```json
{
  "name": "kafka_task", "taskReferenceName": "kafka_ref", "type": "KAFKA_PUBLISH",
  "inputParameters": {
    "kafka_request": {
      "topic": "my-topic",
      "bootStrapServers": "kafka-broker:9092",
      "value": {"data": "${workflow.input.payload}"},
      "key": "${workflow.input.messageKey}",
      "headers": {"source": "conductor"}
    }
  }
}
```
**Inputs** (inside `kafka_request`): `topic` (required), `bootStrapServers` (required), `value` (required), `key`, `headers`.

### SET_VARIABLE
Set workflow-level variables accessible by subsequent tasks.
```json
{"name": "set_var", "taskReferenceName": "set_ref", "type": "SET_VARIABLE", "inputParameters": {"myVar": "${some_task.output.result}"}}
```

### TERMINATE
End the workflow immediately with a status and output.
```json
{"name": "end", "taskReferenceName": "terminate_ref", "type": "TERMINATE", "inputParameters": {"terminationStatus": "COMPLETED", "workflowOutput": {"result": "${task_ref.output.data}"}}}
```
`terminationStatus` can be `COMPLETED` or `FAILED`.

### NOOP
No-operation task. Immediately completes with no side effects. Useful as a placeholder or default branch in SWITCH.
```json
{"name": "noop", "taskReferenceName": "noop_ref", "type": "NOOP"}
```


---

## AI task types

Conductor has built-in AI tasks supporting 12 LLM providers (OpenAI, Anthropic, Google Vertex AI, Azure OpenAI, AWS Bedrock, Mistral, Cohere, Grok, Perplexity, HuggingFace, Ollama, Stability AI) and vector databases (Pinecone, Postgres pgvector, MongoDB Atlas).

### LLM_CHAT_COMPLETE
Multi-turn conversational AI with optional tool calling. Supports all LLM providers.
```json
{
  "name": "chat_task", "taskReferenceName": "chat", "type": "LLM_CHAT_COMPLETE",
  "inputParameters": {
    "llmProvider": "openai",
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "message": "You are a helpful assistant."},
      {"role": "user", "message": "${workflow.input.question}"}
    ],
    "temperature": 0.7,
    "maxTokens": 500
  }
}
```
**Inputs**: `llmProvider` (required), `model` (required), `messages` (required, array of `{role, message}`), `temperature`, `maxTokens`, `topP`, `stopSequences`, `tools` (for function calling).
**Outputs**: `result` (response text), `finishReason` (`STOP`, `TOOL_CALLS`, `LENGTH`), `tokenUsed`, `promptTokens`, `completionTokens`, `toolCalls`.

### LLM_TEXT_COMPLETE
Single prompt text completion.
```json
{
  "name": "text_task", "taskReferenceName": "complete", "type": "LLM_TEXT_COMPLETE",
  "inputParameters": {
    "llmProvider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "prompt": "Summarize: ${workflow.input.text}",
    "temperature": 0.3,
    "maxTokens": 1000
  }
}
```
**Inputs**: `llmProvider`, `model`, `prompt` (all required), `temperature`, `maxTokens`.
**Outputs**: `result`, `tokenUsed`.

### LLM_GENERATE_EMBEDDINGS
Convert text to vector embeddings.
```json
{
  "name": "embed_task", "taskReferenceName": "embed", "type": "LLM_GENERATE_EMBEDDINGS",
  "inputParameters": {
    "llmProvider": "openai",
    "model": "text-embedding-3-small",
    "text": "${workflow.input.document}"
  }
}
```
**Inputs**: `llmProvider`, `model`, `text` (all required).
**Outputs**: `result` (array of floats, e.g. 1536 dimensions for OpenAI).

### GENERATE_IMAGE
Generate images from text prompts. Supports OpenAI (DALL-E-3), Vertex AI (Imagen), Azure OpenAI, Stability AI.
```json
{
  "name": "img_task", "taskReferenceName": "img", "type": "GENERATE_IMAGE",
  "inputParameters": {
    "llmProvider": "openai",
    "model": "dall-e-3",
    "prompt": "A futuristic cityscape at sunset",
    "width": 1024,
    "height": 1024,
    "style": "vivid"
  }
}
```
**Inputs**: `llmProvider`, `model`, `prompt` (all required), `width`, `height`, `n`, `style`.
**Outputs**: `url` or `b64_json`.

### GENERATE_AUDIO
Text-to-speech synthesis. Supports OpenAI TTS.
```json
{
  "name": "audio_task", "taskReferenceName": "audio", "type": "GENERATE_AUDIO",
  "inputParameters": {
    "llmProvider": "openai",
    "model": "tts-1-hd",
    "text": "${workflow.input.narration}",
    "voice": "nova"
  }
}
```
**Inputs**: `llmProvider`, `model`, `text` (all required), `voice` (e.g. `alloy`, `echo`, `nova`).
**Outputs**: `media` (array with `location` URL and `mimeType`).

### GENERATE_VIDEO
Generate videos from text/image prompts (async). Supports OpenAI Sora and Google Vertex AI Veo.
```json
{
  "name": "video_task", "taskReferenceName": "video", "type": "GENERATE_VIDEO",
  "inputParameters": {
    "llmProvider": "openai",
    "model": "sora-2",
    "prompt": "A drone flying over a mountain landscape",
    "duration": 8,
    "size": "1280x720"
  }
}
```
**Inputs**: `llmProvider`, `model`, `prompt` (all required), `duration`, `size`, `aspectRatio`, `resolution`, `style`, `n`, `inputImage` (for image-to-video), `negativePrompt`, `generateAudio` (Veo 3+).
**Outputs**: `media` (array with video URL and optional thumbnail), `jobId`, `status`, `pollCount`.

### LLM_INDEX_TEXT
Store text with auto-generated embeddings in a vector database.
```json
{
  "name": "index_task", "taskReferenceName": "index", "type": "LLM_INDEX_TEXT",
  "inputParameters": {
    "vectorDB": "pinecone-prod",
    "namespace": "docs",
    "index": "knowledge-base",
    "embeddingModelProvider": "openai",
    "embeddingModel": "text-embedding-3-small",
    "text": "${workflow.input.document}",
    "docId": "${workflow.input.docId}",
    "metadata": {"source": "upload", "category": "${workflow.input.category}"}
  }
}
```
**Inputs**: `vectorDB`, `namespace`, `index`, `embeddingModelProvider`, `embeddingModel`, `text` (all required), `docId`, `metadata`.

### LLM_STORE_EMBEDDINGS
Store pre-computed embeddings in a vector database.
```json
{
  "name": "store_task", "taskReferenceName": "store", "type": "LLM_STORE_EMBEDDINGS",
  "inputParameters": {
    "vectorDB": "postgres-prod",
    "namespace": "docs",
    "index": "articles",
    "embeddings": "${embed.output.result}",
    "docId": "${workflow.input.docId}"
  }
}
```
**Inputs**: `vectorDB`, `namespace`, `index`, `embeddings` (all required), `docId`, `metadata`.

### LLM_SEARCH_INDEX
Semantic search using a text query (auto-generates embeddings from the query).
```json
{
  "name": "search_task", "taskReferenceName": "search", "type": "LLM_SEARCH_INDEX",
  "inputParameters": {
    "vectorDB": "postgres-prod",
    "namespace": "kb",
    "index": "articles",
    "embeddingModelProvider": "openai",
    "embeddingModel": "text-embedding-3-small",
    "query": "${workflow.input.question}",
    "llmMaxResults": 5
  }
}
```
**Inputs**: `vectorDB`, `namespace`, `index`, `embeddingModelProvider`, `embeddingModel`, `query` (all required), `llmMaxResults`.

### LLM_SEARCH_EMBEDDINGS
Search using a pre-computed embedding vector.
**Inputs**: `vectorDB`, `namespace`, `index`, `embeddings` (all required), `llmMaxResults`.

### LLM_GET_EMBEDDINGS
Retrieve stored embeddings by document ID.
**Inputs**: `vectorDB`, `namespace`, `index`, `docId` (all required).
**Outputs**: `result` (array of floats).

### LIST_MCP_TOOLS
List available tools from an MCP (Model Context Protocol) server.
```json
{
  "name": "list_tools", "taskReferenceName": "mcp_tools", "type": "LIST_MCP_TOOLS",
  "inputParameters": {
    "mcpServer": "http://localhost:3001/mcp",
    "headers": {"Authorization": "Bearer ${workflow.input.mcpToken}"}
  }
}
```
**Inputs**: `mcpServer` (required), `headers`.
**Outputs**: `tools` (array of `{name, description, inputSchema}`).

### CALL_MCP_TOOL
Call a specific tool on an MCP server. All extra inputParameters are passed as tool arguments.
```json
{
  "name": "call_tool", "taskReferenceName": "mcp_call", "type": "CALL_MCP_TOOL",
  "inputParameters": {
    "mcpServer": "http://localhost:3001/mcp",
    "method": "get_weather",
    "location": "New York",
    "units": "fahrenheit"
  }
}
```
**Inputs**: `mcpServer`, `method` (both required), `headers`, plus any tool-specific parameters.
**Outputs**: `content` (array of result items), `isError`.

---

## Complete examples

### Example 1: Data pipeline with HTTP, transform, and approval

```json
{
  "name": "data_pipeline",
  "description": "Fetch, transform, and approve data",
  "version": 1,
  "schemaVersion": 2,
  "inputParameters": ["apiUrl", "authToken"],
  "tasks": [
    {
      "name": "fetch_data",
      "taskReferenceName": "fetch",
      "type": "HTTP",
      "inputParameters": {
        "http_request": {
          "uri": "${workflow.input.apiUrl}",
          "method": "GET",
          "headers": {"Authorization": "Bearer ${workflow.input.authToken}"}
        }
      }
    },
    {
      "name": "transform_data",
      "taskReferenceName": "transform",
      "type": "JSON_JQ_TRANSFORM",
      "inputParameters": {
        "data": "${fetch.output.response.body.items}",
        "queryExpression": "[.[] | {id: .id, name: .name, status: .status}]"
      }
    },
    {
      "name": "wait_for_approval",
      "taskReferenceName": "approval",
      "type": "WAIT"
    }
  ],
  "outputParameters": {
    "transformedData": "${transform.output.result}",
    "approvalStatus": "${approval.output.approved}"
  }
}
```

### Example 2: RAG workflow (search + AI chat)

```json
{
  "name": "rag_workflow",
  "description": "Retrieval-augmented generation: search knowledge base then answer",
  "version": 1,
  "schemaVersion": 2,
  "inputParameters": ["question"],
  "tasks": [
    {
      "name": "search_knowledge_base",
      "taskReferenceName": "search",
      "type": "LLM_SEARCH_INDEX",
      "inputParameters": {
        "vectorDB": "postgres-prod",
        "namespace": "kb",
        "index": "articles",
        "embeddingModelProvider": "openai",
        "embeddingModel": "text-embedding-3-small",
        "query": "${workflow.input.question}",
        "llmMaxResults": 3
      }
    },
    {
      "name": "generate_answer",
      "taskReferenceName": "answer",
      "type": "LLM_CHAT_COMPLETE",
      "inputParameters": {
        "llmProvider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "messages": [
          {"role": "system", "message": "Answer based on the following context: ${search.output.result}"},
          {"role": "user", "message": "${workflow.input.question}"}
        ],
        "temperature": 0.3
      }
    }
  ],
  "outputParameters": {
    "answer": "${answer.output.result}",
    "sources": "${search.output.result}"
  }
}
```

### Example 3: MCP tool call

```json
{
  "name": "mcp_weather_workflow",
  "description": "Call an MCP tool to get weather data",
  "version": 1,
  "schemaVersion": 2,
  "tasks": [
    {
      "name": "get_weather",
      "taskReferenceName": "weather",
      "type": "CALL_MCP_TOOL",
      "inputParameters": {
        "mcpServer": "http://localhost:3001/mcp",
        "method": "get_weather",
        "location": "${workflow.input.city}",
        "units": "fahrenheit"
      }
    }
  ]
}
```

---

## Visualization

To generate a visual diagram of any workflow definition, see the **"9) Workflow visualization"** section in [SKILL.md](../SKILL.md#9-workflow-visualization). It maps Conductor constructs (SWITCH, FORK_JOIN, DO_WHILE, WAIT, etc.) to Mermaid flowchart syntax.
