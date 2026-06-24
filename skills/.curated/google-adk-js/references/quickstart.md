# TypeScript Quickstart (ADK)

## Summary
- Use Node.js 20.12.7+ and npm 9.2.0+.
- Create a minimal project with `agent.ts`, `package.json`, and `.env` (generate `tsconfig.json` later).
- Install `@google/adk` and `@google/adk-devtools`.

## Project structure
```
my-agent/
  agent.ts
  package.json
  .env
```

## Minimal agent example
```ts
import {FunctionTool, LlmAgent} from '@google/adk';
import {z} from 'zod';

const getCurrentTime = new FunctionTool({
  name: 'get_current_time',
  description: 'Returns the current time in a specified city.',
  parameters: z.object({
    city: z.string().describe('The city name to retrieve the time for.'),
  }),
  execute: ({city}) => {
    return {status: 'success', report: `The current time in ${city} is 10:30 AM`};
  },
});

export const rootAgent = new LlmAgent({
  name: 'hello_time_agent',
  model: 'gemini-3-flash-preview',
  description: 'Tells the current time in a specified city.',
  instruction: 'Use the get_current_time tool to answer time questions.',
  tools: [getCurrentTime],
});
```
Note: Docs show `gemini-2.5-flash`. If your project does not have access to Gemini 3 preview, use `gemini-2.5-flash`.

## Install and configure
```bash
npm init --yes
npm install -D typescript
npx tsc --init
npm install @google/adk @google/adk-devtools zod@^3
```

Update `tsconfig.json`:
```json
{
  "compilerOptions": {
    "verbatimModuleSyntax": false
  }
}
```

Optional: set `main` in `package.json` to `agent.ts`.

## Compile
```bash
npx tsc
```

## API key
Create `.env`:
```bash
echo 'GEMINI_API_KEY="YOUR_API_KEY"' > .env
```
ADK reads `GEMINI_API_KEY` or `GOOGLE_GENAI_API_KEY` for Gemini API mode.

## Vertex AI
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="us-central1"
```
For Gemini 3 preview models on Vertex, use `GOOGLE_CLOUD_LOCATION=global`.

## Run
```bash
npx @google/adk-devtools run agent.ts
```

Web dev UI:
```bash
npx @google/adk-devtools web
```

Note: ADK Web UI is for development only.

## Source
- https://google.github.io/adk-docs/get-started/typescript/
