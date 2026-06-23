# OpenRouter Tested Models

This file is informational only.

It records provider-specific compatibility notes and benchmark snapshots collected while testing the experimental `easy-memory` memory-agent integration.

This file is not a protocol source of truth.
The canonical contract remains:
- `references/openai-compatible-api.md`
- `references/response-schema.md`
- `references/memory-agent-system-prompt.md`
- `references/script-output-schema.md`

## Snapshot Date

- Test date: `2026-03-13`
- Provider endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Test scope: experimental `easy-memory` only
- Primary test path: `scripts/read_today_log.py`
- Historical success criterion at that time: the script returned the older
  structured success block used before the lightweight plain-text filtering
  contract was introduced on `2026-03-18`

## Test Method

All primary comparisons below used the same basic harness:
- one temporary initialized `easy-memory` project
- one factual memory entry in today's log
- agent mode enabled through `./easy-memory/agent-config.json`
- OpenRouter API key authentication
- a model-specific `--task-context`
- timeout set to `70` seconds

The goal was not to measure model intelligence in general.
The goal was to measure practical suitability for the `easy-memory` preprocessing path, especially:
- agent-output stability for the then-current contract
- stable fallback behavior
- cost efficiency
- response latency

## Recommended Cost-Effective Models

The following five models were the most practical candidates in this round.

### 1. `mistralai/mistral-nemo`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.02 / 1M tokens`
  - completion: `$0.04 / 1M tokens`
- Context length: `131072`
- Structured-output support:
  - `response_format`
  - `structured_outputs`
- Test result:
  - `read_today_log.py` succeeded
  - status: `ok`
  - elapsed time: about `7.15s`
- Assessment:
  - Best overall value in this test set
  - Strong default candidate for routine memory-agent preprocessing

### 2. `meta-llama/llama-3.1-8b-instruct`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.02 / 1M tokens`
  - completion: `$0.05 / 1M tokens`
- Context length: `16384`
- Structured-output support:
  - `response_format`
  - `structured_outputs`
- Test result:
  - `read_today_log.py` succeeded
  - status: `ok`
  - elapsed time: about `4.02s`
- Assessment:
  - Fastest successful low-cost candidate in this sweep
  - Good fallback model when shorter context is acceptable

### 3. `google/gemma-3-27b-it`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.03 / 1M tokens`
  - completion: `$0.11 / 1M tokens`
- Context length: `128000`
- Structured-output support:
  - `response_format`
  - `structured_outputs`
- Test result:
  - `read_today_log.py` succeeded
  - status: `ok`
  - elapsed time: about `7.26s`
- Assessment:
  - Strong balance between quality, context, and cost
  - Good choice when more instruction stability is desired than the smallest models typically provide

### 4. `qwen/qwen3.5-9b`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.10 / 1M tokens`
  - completion: `$0.15 / 1M tokens`
- Context length: `262144`
- Structured-output support:
  - `response_format`
  - `structured_outputs`
- Test result:
  - `read_today_log.py` succeeded
  - status: `ok`
  - elapsed time: about `12.17s`
- Assessment:
  - Most context headroom among the recommended candidates
  - A practical choice when staying inside the Qwen family matters more than absolute cost

### 5. `cohere/command-r7b-12-2024`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.0375 / 1M tokens`
  - completion: `$0.15 / 1M tokens`
- Context length: `128000`
- Structured-output support:
  - `response_format`
  - `structured_outputs`
- Test result:
  - `read_today_log.py` succeeded
  - status: `ok`
  - elapsed time: about `29.70s`
- Assessment:
  - Functionally successful, but clearly slower than the other recommended models in this sweep
  - More suitable as a compatibility backup than as the first default

## Additional Tested Models

The models below were tested during the same evaluation cycle but were not included in the recommended top five.

### `qwen/qwen-turbo`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.0325 / 1M tokens`
  - completion: `$0.13 / 1M tokens`
- Context length: `131072`
- Test result:
  - `read_today_log.py` fallback
  - observed error: OpenRouter `HTTP 500`
- Note:
  - This looked like provider-side instability in this run, not a confirmed schema-compliance failure

### `google/gemma-3-12b-it`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.04 / 1M tokens`
  - completion: `$0.13 / 1M tokens`
- Context length: `131072`
- Test result:
  - `read_today_log.py` fallback
  - observed error: OpenRouter `HTTP 429`
- Note:
  - This run was blocked by upstream rate limiting rather than a confirmed protocol mismatch

### `openai/gpt-oss-20b`

- OpenRouter list price on `2026-03-13`:
  - prompt: `$0.03 / 1M tokens`
  - completion: `$0.14 / 1M tokens`
- Context length: `131072`
- Test result:
  - `read_today_log.py` fallback
  - observed error: connection reset by peer
- Note:
  - This run did not provide enough signal to recommend it for this workflow

### `qwen/qwen3.5-397b-a17b`

- This model was tested separately before the broader sweep.
- Earlier results:
  - direct OpenRouter `chat/completions` call succeeded
  - `search_memory.py` succeeded
  - `read_today_log.py` initially failed because the model omitted the required `summary` field
  - after narrowing the protocol and adding an explicit JSON skeleton, `read_today_log.py` also succeeded
- Note:
  - It is viable for this workflow, but it was not selected as a top cost-efficient option for routine use

## Operational Guidance

If you need a default OpenRouter model for the experimental `easy-memory` agent path, prefer this order:

1. `mistralai/mistral-nemo`
2. `google/gemma-3-27b-it`
3. `qwen/qwen3.5-9b`
4. `meta-llama/llama-3.1-8b-instruct`
5. `cohere/command-r7b-12-2024`

When cost matters more than context length, start with:
- `mistralai/mistral-nemo`
- `meta-llama/llama-3.1-8b-instruct`

When larger context matters more than lowest cost, start with:
- `qwen/qwen3.5-9b`
- `google/gemma-3-27b-it`

## Notes

- OpenRouter pricing and provider availability can change at any time.
- The prices above were copied from the official OpenRouter model list on `2026-03-13`.
- These results describe the experimental `easy-memory` integration path only.
- Future regressions should be checked against the shared installed-skill failure log:
  - `logs/agent-failures.jsonl`
