# Tools (TypeScript ADK)

## Built-in tools
Use built-in tools from `@google/adk` and pass them in `tools`.

```ts
import {LlmAgent, GOOGLE_SEARCH} from '@google/adk';

const agent = new LlmAgent({
  name: 'search_assistant',
  model: 'gemini-3-flash-preview',
  instruction: 'Answer questions using Google Search when needed.',
  tools: [GOOGLE_SEARCH],
});
```

Some tools cannot be combined in a single agent. If you hit a tool limit, check:
- https://google.github.io/adk-docs/tools/limitations/
If a tool is marked one-tool-per-agent, split it into a dedicated sub-agent and call it via `AgentTool`.

## FunctionTool pattern
Define parameters with Zod and return an object.

```ts
import {FunctionTool} from '@google/adk';
import {z} from 'zod';

async function getStockPrice({ticker}: {ticker: string}) {
  return {status: 'success', price: '$123.45'};
}

const getStockPriceTool = new FunctionTool({
  name: 'get_stock_price',
  description: 'Gets the current price of a stock.',
  parameters: z.object({
    ticker: z.string().describe('Stock ticker symbol.'),
  }),
  execute: getStockPrice,
});
```

### Tool schema compatibility
- Pin `zod` to v3 when targeting Vertex tool calls. Zod v4 can emit schema fields that Vertex rejects (e.g. `~standard`, `def`).
- Avoid passing tools via `generateContentConfig.tools`; always use `LlmAgent.tools`.

## Agent-as-a-Tool
Wrap another agent with `AgentTool`.

```ts
import {AgentTool, LlmAgent} from '@google/adk';

const summarizer = new LlmAgent({
  name: 'summary_agent',
  model: 'gemini-3-flash-preview',
  instruction: 'Summarize the given text.',
});

const mainAgent = new LlmAgent({
  name: 'main_agent',
  model: 'gemini-3-flash-preview',
  instruction: 'Use the summary_agent for long texts.',
  tools: [new AgentTool({agent: summarizer, skipSummarization: true})],
});
```

## Source
- https://google.github.io/adk-docs/tools/
- https://google.github.io/adk-docs/tools-custom/function-tools/
