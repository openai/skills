# Models and Authentication (TypeScript ADK)

## Model selection
Pass a model string directly to `LlmAgent` for Gemini models.

```ts
import {LlmAgent} from '@google/adk';

const agent = new LlmAgent({
  name: 'example_agent',
  model: 'gemini-3-flash-preview',
  instruction: 'You are helpful.',
});
```
If preview access is not enabled in your Vertex project, use `gemini-2.5-flash`.

## Google AI Studio (API key)
Set environment variables for local dev:
```bash
export GOOGLE_GENAI_API_KEY="YOUR_GOOGLE_API_KEY"
# or export GEMINI_API_KEY="YOUR_GOOGLE_API_KEY"
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
```
API keys do not work with Vertex; use ADC or a service account when `GOOGLE_GENAI_USE_VERTEXAI=true`.

## Vertex AI (Google Cloud)
Use ADC or service account and set:
```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="YOUR_VERTEX_AI_LOCATION" # e.g., us-central1
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

If using a service account key outside GCP:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

## Gemini 3 preview on Vertex
- Set `GOOGLE_CLOUD_LOCATION=global` for Gemini 3 preview models.
- Ensure your project/region has access to the preview model.
- If you see "Publisher Model ... was not found", verify the model string and region (global).

## Model overrides
Set a custom model string:
```bash
export ADK_MODEL="gemini-3-flash-preview"
```

## Source
- https://google.github.io/adk-docs/agents/models/
