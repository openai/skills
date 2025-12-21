# Multi-Agent Architecture (ADK JS)

Use a root LLM agent as an orchestrator. Let it decide whether to ask clarifying questions or delegate to deterministic workflows. Avoid hardcoded intent routing.

## Orchestrator + pipeline blueprint
```ts
import {LlmAgent, ParallelAgent, SequentialAgent} from '@google/adk';

const inventoryParallel = new ParallelAgent({
  name: 'inventory_parallel',
  description: 'Runs independent inventory fetchers in parallel.',
  subAgents: [flightAgent, hotelAgent],
});

const tripPipeline = new SequentialAgent({
  name: 'trip_pipeline',
  description: 'Compiles inventory and itinerary.',
  subAgents: [inventoryParallel, itineraryAgent],
});

export const rootAgent = new LlmAgent({
  name: 'trip_planner_root',
  model: process.env.ADK_MODEL ?? 'gemini-3-flash-preview',
  description: 'Orchestrates trip planning and clarifying questions.',
  instruction: [
    'Act as the orchestration layer.',
    'If required trip details are missing, ask one concise question.',
    'If user is greeting/small talk, reply briefly and ask for trip details.',
    'When details are sufficient, transfer to trip_pipeline.',
  ].join('\n'),
  subAgents: [tripPipeline],
});
```

## Execution semantics to remember
- **SequentialAgent:** shares the same invocation context; state is read/write across steps.
- **ParallelAgent:** runs on branch contexts but shares the same session state (use unique keys).
- **LoopAgent:** repeats until `maxIterations` or a sub-agent escalates with `EventActions.escalate=true`.

## LLM-driven delegation
- LLM agents can call `transfer_to_agent(agent_name="...")` when subAgents are present.
- Keep sub-agent `description` fields specific so the orchestrator routes correctly.

## Loop + isolation pattern
- Use `LoopAgent` for repeatable tasks.
- Wrap complex sub-flows as `AgentTool` to isolate state per iteration.
- Persist outputs in `toolContext.state` for downstream agents to summarize.

## Prompt hygiene
- Add a `beforeModelCallback` to ensure `request.contents` always includes at least one `parts` entry.
- Prefer `includeContents: "default"` for consistent context delivery.
