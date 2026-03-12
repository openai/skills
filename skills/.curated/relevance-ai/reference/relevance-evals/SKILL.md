---
name: relevance-evals
description: Manages agent evaluations in Relevance AI - creating test cases, running evaluations, and analyzing results. Use when testing agent behavior, setting up automated testing, or reviewing evaluation results.
---

# Agent Evals Skill

Skill for managing and running agent evaluations in Relevance AI.

> **Full API Documentation:** `https://api-{region}.stack.tryrelevance.com/latest/documentation` (replace `{region}` with your project's region)

## Overview

Agent Evals provide a systematic way to evaluate AI agent performance against defined criteria:

- **Test Cases (Scenarios)**: Simulated user interactions with expected outcomes
- **Test Sets**: Collections of test cases organized for specific testing purposes
- **Rules**: Natural language evaluation criteria that an LLM judge evaluates
- **Eval Runs**: Individual evaluation executions
- **Eval Batches**: Groups of eval runs triggered together

### Two Evaluation Modes

| Mode                 | Description                                                          | Use Case                                      |
| -------------------- | -------------------------------------------------------------------- | --------------------------------------------- |
| `generate_and_score` | Generates new conversations from test case scenarios, then evaluates | Automated testing with predefined scenarios   |
| `score_only`         | Evaluates existing conversations against agent-level rules           | Testing against real production conversations |

**Key Difference:**

- `score_only` uses **agent-level rules** (created via `POST /evals/rules`)
- `generate_and_score` uses **test case rules** (expectedOutcomes defined in test cases)

---

## Eval Workflow (Step-by-Step)

**IMPORTANT:** Follow this workflow in order. Each step depends on the previous one.

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Create a NEW Test Set                                  │
│  └─► ALWAYS create a dedicated test set (don't use default)     │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Create Test Cases (Scenarios)                          │
│  └─► Add test cases to the NEW test set with prompts + rules    │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Run Evaluation                                         │
│  └─► Trigger generate_and_score with test case IDs              │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Poll & Read Results                                    │
│  └─► Check batch status, get detailed run results               │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Create a NEW Test Set

> **IMPORTANT:** Always create a new, dedicated test set for your evaluations. Do NOT use the default test set.

**Why create a new test set?**

- **Organization:** Keep test cases grouped by purpose (e.g., "Smoke Tests", "Regression Suite", "Edge Cases")
- **Isolation:** Avoid mixing test cases from different evaluation runs
- **Clarity:** Named test sets make it clear what's being tested
- **Cleanup:** Easier to delete/manage test sets independently

```typescript
// First, check existing test sets (optional - for reference)
const testSets = await relevance_api_request({
  endpoint: `/evals/test-sets/agent/${agentId}`,
  method: 'GET',
});
// Returns: { test_sets: [{ display_id, name, test_case_count, is_default }, ...] }

// ALWAYS create a NEW test set - don't use the default
const newTestSet = await relevance_api_request({
  endpoint: `/evals/test-sets/agent/${agentId}`,
  method: 'POST',
  body: {
    name: 'My Agent Test Suite', // Use a descriptive name
    test_case_ids: [], // Start empty, add test cases in Step 2
  },
});
// Returns: { display_id: "..." }
const testSetId = newTestSet.display_id; // Save this for Step 2
```

### Step 2: Create Test Cases

Create test cases with scenarios and expected outcomes. **Always attach them to your new test set** using the `test_set_id` query parameter.

```typescript
// Create test case attached to your NEW test set (from Step 1)
// IMPORTANT: Always use ?test_set_id= to attach to your test set
const testCase = await relevance_api_request({
  endpoint: `/evals/agent/${agentId}/test-cases?test_set_id=${testSetId}`,
  method: 'POST',
  body: {
    name: 'Basic Greeting',
    scenario: {
      prompt: 'Hello, I need help',
      max_turns: 5,
    },
    expectedOutcomes: [
      { name: 'Greets user', rule: 'The agent greets the user warmly' },
      { name: 'Offers help', rule: 'The agent asks how it can help' },
    ],
  },
});
// Returns: { display_id: "test-case-id-here" }

// Create additional test cases - all attached to the SAME test set
const testCase2 = await relevance_api_request({
  endpoint: `/evals/agent/${agentId}/test-cases?test_set_id=${testSetId}`,
  method: 'POST',
  body: {
    name: 'Error Handling',
    scenario: {
      prompt: "I need help with something you can't do",
      max_turns: 3,
    },
    expectedOutcomes: [
      {
        name: 'Acknowledges limitation',
        rule: 'The agent clearly states it cannot help with this request',
      },
      {
        name: 'Offers alternative',
        rule: 'The agent suggests an alternative or escalation path',
      },
    ],
  },
});
```

> **Note:** If you omit `?test_set_id=`, the test case goes to the default test set. Always specify your test set ID.

### Step 3: Run Evaluation

Trigger the evaluation with the test case IDs you want to run.

```typescript
// First, list test cases to get their IDs
const { test_cases } = await relevance_api_request({
  endpoint: `/evals/agent/${agentId}/test-cases`,
  method: 'GET',
});

// Run evaluation with selected test cases
const evalResult = await relevance_api_request({
  endpoint: `/evals/agents/${agentId}/conversations`,
  method: 'POST',
  body: {
    conversation_ids: [], // Empty for generate_and_score
    evaluation_run_name: 'My Eval Run - ' + new Date().toISOString(),
    type: 'generate_and_score',
    scenario_ids: test_cases.map((tc) => tc.display_id),
  },
});
// Returns: { eval_batch_id: "...", eval_run_ids: ["...", "..."] }
```

### Step 4: Poll & Read Results

Use two endpoints: `/runs` for per-run details, `/summary` for the overall score.

> **NOTE:** `GET /evals/runs/{eval_run_id}` does NOT exist. Always use the batch endpoint to get run details.

1. **Get all runs:** Call `relevance_api_request` with `GET /evals/batches/{evalBatchId}/runs`. Returns `{ runs: EvalRunDetail[], total_count: number }`.

2. **Poll until complete:** Keep calling the runs endpoint until no runs have status `running` or `queued`.

3. **Read results:** Each completed run has `result.rule_results` inline with `rule_name`, `passed`, and `reason` for each rule.

4. **Get summary (optional):** Call `GET /evals/batches/{evalBatchId}/summary` for the overall score. Returns `{ tasks_evaluated, total_runs, summary_score, name, rules }`.

---

## Eval Design Philosophy

### The Purpose of Evals

The core idea behind evals is to **test actual user use-cases and situations**. When an eval runs:

1. The system triggers the agent with the test scenario prompt
2. The agent generates a real conversation response
3. An LLM judge evaluates the conversation against the defined rules
4. Results show whether the agent met the expected criteria

### Designing a Good Test Suite

A well-designed eval suite follows these principles:

| Principle              | Description                                                                       |
| ---------------------- | --------------------------------------------------------------------------------- |
| **Full Coverage**      | Cover all major use-cases and functionalities the agent should handle             |
| **Minimal Test Cases** | Keep the number of test cases small - each eval is expensive and time-consuming   |
| **Targeted Scenarios** | Each test case should focus on testing specific behaviors, not everything at once |
| **Realistic Prompts**  | Use prompts that mirror how real users would interact with the agent              |
| **Specific Rules**     | Each test case has its own rules tailored to what that scenario should achieve    |

### Test Case Design Guidelines

**DO:**

- Test one primary capability per test case
- Use realistic user language and requests
- Include edge cases (budget constraints, special requirements, errors)
- Write rules that are specific and measurable
- Cover the "happy path" and common variations

**DON'T:**

- Create dozens of overlapping test cases
- Use artificial or overly formal prompts
- Write vague rules like "agent is helpful"
- Test everything in a single test case
- Ignore error handling scenarios

### Example: Flight Search Agent Test Suite (5 tests)

| Test Case                | Use Case Covered                   | Key Rules                                            |
| ------------------------ | ---------------------------------- | ---------------------------------------------------- |
| Basic One-Way Flight     | Core search functionality          | Uses tool correctly, presents options, shows details |
| Round-Trip International | Return dates, international routes | Handles both legs, correct airports                  |
| Business Class Request   | Travel class preferences           | Sets correct class, premium options                  |
| Family Travel            | Multi-passenger handling           | Correct passenger count, total pricing               |
| Budget-Conscious Search  | Price optimization                 | Prioritizes price, acknowledges flexibility          |

This suite covers 5 distinct use cases with 15 targeted rules, providing comprehensive coverage without redundancy.

### Cost-Benefit Tradeoff

Each eval run:

- Triggers the agent (costs credits)
- Generates a full conversation (takes time)
- Runs LLM judge evaluation (costs credits)

**Optimize by:**

- Combining related behaviors into single test cases where natural
- Using lower `max_turns` when full conversations aren't needed
- Running full suites only on significant changes
- Using smaller "smoke test" subsets for quick validation

---

## Test Set Best Practices

### Always Create a New Test Set

| DO                                                       | DON'T                                      |
| -------------------------------------------------------- | ------------------------------------------ |
| Create a dedicated test set for each evaluation purpose  | Use the default test set                   |
| Use descriptive names like "Sales Agent - Core Features" | Use generic names like "Test Set 1"        |
| Delete old/unused test sets to keep things clean         | Let test sets accumulate indefinitely      |
| Group related test cases in the same test set            | Scatter related tests across multiple sets |

### Recommended Test Set Naming Conventions

```
{Agent Name} - {Purpose} [{Date if versioned}]
```

Examples:

- `Flight Search - Core Functionality`
- `Customer Support - Edge Cases`
- `Sales Agent - Regression Suite 2026-02`
- `Onboarding Bot - Smoke Tests`

### Managing Test Sets

```typescript
// List all test sets for an agent
const { test_sets } = await relevance_api_request({
  endpoint: `/evals/test-sets/agent/${agentId}`,
  method: 'GET',
});

// Delete an old test set (also deletes its test cases)
await relevance_api_request({
  endpoint: `/evals/test-sets/${testSetId}`,
  method: 'DELETE',
});

// Update test set name
await relevance_api_request({
  endpoint: `/evals/test-sets/${testSetId}`,
  method: 'PUT',
  body: { name: 'New Test Set Name' },
});
```

### Clean Start Workflow

When re-running evals, start clean:

1. List existing test cases with `GET /evals/agent/{agentId}/test-cases`
2. Delete each test case by calling `DELETE /evals/test-cases/{display_id}` for each one
3. Create a fresh test set with `POST /evals/test-sets/agent/{agentId}`
4. Add new test cases to the fresh test set (continue with Step 2 of the workflow)

---

## No Dedicated MCP Tools

Evals use `relevance_api_request` since there are no dedicated MCP tools. The workflow above shows all the API calls needed.

## API Reference

### Test Case Endpoints

| Method   | Endpoint                             | Description      |
| -------- | ------------------------------------ | ---------------- |
| `POST`   | `/evals/agent/{agent_id}/test-cases` | Create test case |
| `GET`    | `/evals/agent/{agent_id}/test-cases` | List test cases  |
| `GET`    | `/evals/test-cases/{test_case_id}`   | Get test case    |
| `PUT`    | `/evals/test-cases/{test_case_id}`   | Update test case |
| `DELETE` | `/evals/test-cases/{test_case_id}`   | Delete test case |

### Test Set Endpoints

| Method   | Endpoint                            | Description     |
| -------- | ----------------------------------- | --------------- |
| `POST`   | `/evals/test-sets/agent/{agent_id}` | Create test set |
| `GET`    | `/evals/test-sets/agent/{agent_id}` | List test sets  |
| `PUT`    | `/evals/test-sets/{test_set_id}`    | Update test set |
| `DELETE` | `/evals/test-sets/{test_set_id}`    | Delete test set |

### Evaluation Endpoints

| Method   | Endpoint                                                 | Description                        |
| -------- | -------------------------------------------------------- | ---------------------------------- |
| `POST`   | `/evals/agents/{agent_id}/conversations`                 | Trigger evaluation                 |
| `GET`    | `/evals/batches/{eval_batch_id}/runs`                    | Get all runs with full details     |
| `GET`    | `/evals/batches/{eval_batch_id}/summary`                 | Get batch summary score            |
| `POST`   | `/evals/agents/{agent_id}/runs`                          | List runs for agent (with filters) |
| `POST`   | `/evals/runs/{eval_run_id}/cancel`                       | Cancel a specific run              |
| `POST`   | `/evals/batches/{eval_batch_id}/cancel`                  | Cancel all runs in a batch         |
| `GET`    | `/evals/resources/{resource_type}/{resource_id}/batches` | List batches for a resource        |
| `DELETE` | `/evals/batches/{eval_batch_id}`                         | Delete batch                       |

### Agent-Level Rule Endpoints (for score_only mode)

| Method   | Endpoint                      | Description |
| -------- | ----------------------------- | ----------- |
| `POST`   | `/evals/rules`                | Create rule |
| `GET`    | `/evals/rules/{agent_id}`     | List rules  |
| `PATCH`  | `/evals/rules/{eval_rule_id}` | Update rule |
| `DELETE` | `/evals/rules/{eval_rule_id}` | Delete rule |

## Writing Effective Rules

Rules are evaluated by an LLM judge. Write rules that are:

**Good Rules (Specific & Observable):**

```typescript
{ name: "Greeting", rule: "The agent greets the user within the first message" }
{ name: "No hallucination", rule: "The agent does not make up information not present in the provided context" }
{ name: "Escalation path", rule: "When unable to help, the agent offers to transfer to a human agent" }
{ name: "Mentions pricing", rule: "The agent mentions at least one specific price or pricing tier" }
```

**Bad Rules (Vague):**

```typescript
{ name: "Helpful", rule: "The agent is helpful" }  // Too vague - what makes it helpful?
{ name: "Understands", rule: "The agent understands the user" }  // Not observable
{ name: "Good response", rule: "The response is good" }  // No criteria
```

## Common Issues

### "No active rules found for this agent"

This happens when using `score_only` mode without agent-level rules.

- **Solution:** Either create agent-level rules first with `POST /evals/rules`, or use `generate_and_score` with test cases.

### "scenario_ids are required when type is 'generate_and_score'"

You need to specify which test cases to run.

- **Solution:** List test cases first with `GET /evals/agent/{id}/test-cases`, then provide their display_ids.

### Evaluation takes too long

Complex scenarios with many turns take time to generate and evaluate.

- **Solution:** Reduce `max_turns`, simplify prompts, or run fewer test cases at once.

### Rules are too vague - inconsistent results

The LLM judge can't determine pass/fail clearly.

- **Solution:** Rewrite rules to be specific and observable. Include concrete criteria like "at least two", "within the first message", "mentions by name".

## Request/Response Schemas

### Create Test Case Request

```typescript
{
  name: string;           // Human-readable name
  scenario: {
    prompt: string;       // The user message to simulate
    max_turns?: number;   // 1-50, default: 10
  };
  expectedOutcomes: Array<{
    name: string;         // Rule name
    rule: string;         // Natural language criterion
  }>;  // 1-5 rules required
}
```

### EvalRunDetail (returned inline in batch runs)

```typescript
{
  eval_run_id: string;
  status: "queued" | "running" | "completed" | "failed";
  task_name: string;                    // Test case name
  conversation_display_id: string;      // Generated conversation ID
  agent_version_display_id?: string;    // Agent version used
  test_case_display_id?: string;        // Test case ID (generate_and_score only)
  error_message?: string;               // Present when status is "failed"
  debug_info?: object;
  result?: {                            // Present when status is "completed"
    rule_results: Array<{
      rule_id: string;
      rule_name: string;
      reason: string;      // LLM explanation
      passed: boolean;
    }>;
    credits_cost: number;
  };
}
```

### GET /evals/batches/:id/runs Response

```typescript
{
  runs: EvalRunDetail[];        // Full details for each run
  total_count: number;
}
```

### GET /evals/batches/:id/summary Response

```typescript
{
  rules: Array<{
    rule_id: string;
    name: string;
    rule: string;
  }>;
  tasks_evaluated: number; // Completed evaluations
  total_runs: number;
  summary_score: number | null; // Percentage passed (0-100)
  name: string; // Batch name
```
