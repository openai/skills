# Agent Evals API Reference

Complete API reference for all evaluation endpoints.

## Evaluation Execution

### POST /evals/agents/:agent_id/conversations

Trigger an evaluation run for an agent.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | The agent display ID |

**Request Body:**

```typescript
{
  conversation_ids: string[];           // Required - array of conversation IDs (empty for generate_and_score)
  evaluation_run_name: string;          // Required - name for this evaluation batch
  type?: 'score_only' | 'generate_and_score';  // Default: 'score_only'
  scenario_ids?: string[];              // Required when type is 'generate_and_score'
  active_version_id?: string;           // Optional - specific agent version to evaluate
  agent_override?: object;              // Optional - override agent config (max 10KB)
}
```

**Response:**

```typescript
{
  eval_batch_id: string;    // Display ID of the created batch
  eval_run_ids: string[];   // Display IDs of individual eval runs
}
```

**Error Codes:**

- `400` - Missing agent_id, invalid type, or missing scenario_ids for generate_and_score
- `400` - No active rules found for agent (score_only mode)
- `400` - More than 50 conversations (score_only limit)
- `404` - Agent or project not found
- `422` - Agent override configuration too large

---

## Test Case Management

### POST /evals/:resource_type/:resource_id/test-cases

Create a new test case.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resource_type` | 'agent' \| 'workforce' | Yes | Resource type |
| `resource_id` | string | Yes | Resource display ID |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `test_set_id` | string | No | Test set display ID to attach this test case to |

**Request Body:**

```typescript
{
  name: string;           // Human-readable name for the test case
  scenario: {
    prompt: string;       // The initial user message to simulate
    max_turns?: number;   // Maximum conversation turns (1-50, default: 10)
  };
  expectedOutcomes: Array<{
    name: string;         // Rule name
    rule: string;         // Natural language evaluation criterion
    display_id?: string;  // Optional - for updating existing rules
  }>;  // 1-5 rules required
}
```

**Response:**

```typescript
{
  display_id: string;
}
```

---

### GET /evals/:resource_type/:resource_id/test-cases

List all test cases for a resource.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page_size` | string | No | Number of results per page |
| `offset` | string | No | Pagination offset |
| `test_set_id` | string | No | Filter by test set |

**Response:**

```typescript
{
  test_cases: Array<{
    display_id: string;
    name: string;
    prompt: string;
    max_turns: number;
    project_id: string;
    created_at?: string;
    updated_at?: string;
    rules: Array<{
      name: string;
      rule: string;
      display_id?: string;
    }>;
  }>;
}
```

---

### GET /evals/test-cases/:test_case_id

Get a specific test case by ID.

**Response:** Same structure as items in list response.

---

### PUT /evals/test-cases/:test_case_id

Update an existing test case.

**Request Body:** Same as create, all fields required.

**Response:** Empty object `{}`

---

### DELETE /evals/test-cases/:test_case_id

Delete a test case.

**Response:** Empty object `{}`

---

## Test Set Management

### POST /evals/test-sets/:resource_type/:resource_id

Create a new test set.

**Request Body:**

```typescript
{
  name: string;              // Human-readable name
  test_case_ids?: string[];  // Optional - test case display IDs to include
}
```

**Response:**

```typescript
{
  display_id: string;
}
```

---

### GET /evals/test-sets/:resource_type/:resource_id

List all test sets for a resource.

**Response:**

```typescript
{
  test_sets: Array<{
    display_id: string;
    name: string;
    test_case_count: number;
    project_id: string;
    created_at?: string;
    updated_at?: string;
    is_default: boolean; // True for the auto-created default test set
  }>;
}
```

---

### PUT /evals/test-sets/:test_set_id

Update a test set name.

**Request Body:**

```typescript
{
  name: string;
}
```

---

### DELETE /evals/test-sets/:test_set_id

Delete a test set.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `delete_test_cases` | 'true' \| 'false' | No | If 'true', also deletes all test cases in the set |

---

## Agent-Level Rule Management

Used for `score_only` evaluations against existing conversations.

### POST /evals/rules

Create a rule for an agent.

**Request Body:**

```typescript
{
  agent_id: string;         // Agent display ID
  user_definition: {
    name: string;           // Rule name
    rule: string;           // Natural language evaluation criterion
    display_id?: string;    // Optional custom display ID
  };
}
```

**Response:**

```typescript
{
  rule_id: string;
}
```

---

### GET /evals/rules/:agent_id

List all rules for an agent.

**Response:**

```typescript
{
  rules: Array<{
    name: string;
    rule: string;
    display_id: string;
    created_at: string;
  }>;
}
```

---

### PATCH /evals/rules/:eval_rule_id

Update a rule.

**Request Body:**

```typescript
{
  user_definition: {
    name: string;
    rule: string;
    display_id?: string;
  };
}
```

---

### DELETE /evals/rules/:eval_rule_id

Delete a rule (soft delete).

---

## Batch Management

### GET /evals/resources/:resource_type/:resource_id/batches

List all evaluation batches for a resource.

**Response:**

```typescript
{
  batches: Array<{
    batch_id: string;
    name: string;
    created_at: string;
  }>;
}
```

---

### GET /evals/batches/:eval_batch_id/runs

Get all runs with full details for a batch. This is the primary endpoint for reading eval results.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | string | No | Page number |
| `page_size` | string | No | Results per page |

**Response:**

```typescript
{
  runs: Array<{
    eval_run_id: string;
    status: 'queued' | 'running' | 'completed' | 'failed';
    task_name: string;
    conversation_display_id: string;
    agent_version_display_id?: string;
    test_case_display_id?: string;
    error_message?: string;
    debug_info?: object;
    result?: {
      // Present when status is 'completed'
      rule_results: Array<{
        rule_id: string;
        rule_name: string;
        reason: string;
        passed: boolean;
      }>;
      credits_cost: number;
    };
  }>;
  total_count: number;
}
```

---

### GET /evals/batches/:eval_batch_id/summary

Get summary info for a batch (overall score, rule definitions).

**Response:**

```typescript
{
  rules: Array<{
    rule_id: string;
    name: string;
    rule: string;
  }>;
  tasks_evaluated: number; // Number of completed evaluations
  total_runs: number;
  summary_score: number | null; // Percentage of rules passed (0-100)
  name: string; // Batch name
}
```

---

### POST /evals/runs/:eval_run_id/cancel

Cancel a specific eval run.

**Response:**

```typescript
{
  status: string;
  message: string;
}
```

---

### POST /evals/batches/:eval_batch_id/cancel

Cancel all pending and running eval runs in a batch.

**Response:**

```typescript
{
  status: string;
  message: string;
  cancelled_count: number;
}
```

---

### POST /evals/agents/:agent_id/runs

List eval runs for an agent with filtering and pagination.

**Request Body:**

```typescript
{
  page?: number;                // Page number (1-based)
  page_size?: number;           // 1-100
  filters?: Array<EvalRunFilter>;  // Combined with AND logic
  date_range: {                 // Required, max 31 days
    start_date: string;         // ISO 8601
    end_date: string;           // ISO 8601
  };
  sort?: {
    direction?: 'asc' | 'desc'; // Default: 'desc'
  };
}
```

**Response:**

```typescript
{
  runs: EvalRunDetail[];
  total_count: number;
}
```

---

### DELETE /evals/batches/:eval_batch_id

Delete a batch and all its runs.

---

## TypeScript Types

```typescript
// Enums
type EvalRunStatus = 'queued' | 'running' | 'completed' | 'failed';
type EvalRunType = 'score_only' | 'generate_and_score';
type EvalResourceType = 'agent' | 'workforce';

// Rule definition
interface UserRuleDefinition {
  name: string;
  rule: string;
  display_id?: string;
}

// Eval rule (persisted)
interface EvalRule {
  name: string;
  rule: string;
  display_id: string;
  created_at: string;
}

// Evaluation result
interface EvalResponse {
  rule_results: Array<{
    reason: string;
    passed: boolean;
    rule_id: string;
    rule_name: string;
  }>;
  credits_cost: number;
}

// Test case
interface TestCase {
  display_id: string;
  name: string;
  prompt: string;
  max_turns: number;
  project_id: string;
  created_at?: string;
  updated_at?: string;
  rules: UserRuleDefinition[];
}

// Test set summary
interface TestSetSummary {
  display_id: string;
  name: string;
  test_case_count: number;
  project_id: string;
  created_at?: string;
  updated_at?: string;
  is_default: boolean;
}
```
