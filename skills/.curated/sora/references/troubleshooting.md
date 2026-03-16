# Troubleshooting

## Job fails with size or seconds errors
- Cause: size is not supported by the chosen model, or seconds is outside `4`, `8`, `12`, `16`, `20`.
- Fix: match size to model; use `sora-2-pro` for `1920x1080` or `1080x1920`.

## Docs and SDK disagree on the latest limits or helpers
- Cause: the March 2026 Sora guide/changelog is ahead of some typed SDK/API-reference surfaces.
- Fix: follow the latest guide/changelog and use the bundled CLI, which bridges new flows through the official client’s low-level methods.

## `edit`, `extend`, or `create-character` isn't available in your installed Python SDK
- Cause: the published SDK may not expose new Sora helpers yet.
- Fix: use `scripts/sora.py`; it uses the official OpenAI client directly for those endpoints.

## openai SDK not installed
- Cause: running `python "$SORA_CLI" ...` without the OpenAI SDK available.
- Fix: run with `uv run --with openai python "$SORA_CLI" ...`.

## uv cache permission error
- Cause: uv cache directory is not writable in CI or sandboxed environments.
- Fix: set `UV_CACHE_DIR=/tmp/uv-cache` (or another writable path) before running `uv`.

## Prompt shell escaping issues
- Cause: multi-line prompts or quotes break the shell.
- Fix: use `--prompt-file prompt.txt`.

## Prompt looks double-wrapped ("Primary request: Use case: ...")
- Cause: you structured the prompt manually but left CLI augmentation on.
- Fix: add `--no-augment`, or use the CLI fields (`--use-case`, `--scene`, etc.) instead of pre-formatting.

## Input reference rejected
- Cause: the file is not jpg/png/webp, includes a human face, or does not match the target size.
- Fix: convert to jpg/png/webp, remove faces, and resize to match `--size`.

## Character continuity is weak
- Cause: the character clip is too long, mismatched in aspect ratio, outside the skill's non-human character workflow, or the prompt never names the character.
- Fix: use a short non-human MP4, match aspect ratio to the target shot, and mention the character name verbatim in the prompt.

## Extension looks jumpy or drifts
- Cause: the continuation prompt changes too many things at once, or asks for a hard scene break.
- Fix: describe the next beat only, preserve motion direction, and avoid introducing unrelated subjects or abrupt camera changes.

## Remix drifts from the original
- Cause: remix is a legacy endpoint and too many changes were requested at once.
- Fix: prefer `edit`, state invariants explicitly, and change one element at a time.

## Download fails or returns expired URL
- Cause: normal download URLs expire after about 1 hour.
- Fix: re-download while the link is fresh and copy the asset to your own storage promptly.

## Video completes but looks unstable or flickers
- Cause: multiple actions, aggressive camera motion, or overly long prompt timing for the clip length.
- Fix: reduce to one main action and one camera move; keep beats simple; add constraints like `avoid flicker` or `stable motion`.

## Text is unreadable
- Cause: text is too long, too small, or moving.
- Fix: shorten text, keep the camera locked-off, and avoid fast motion.

## Job stuck in `queued` or `in_progress`
- Cause: temporary queue delays or slower higher-resolution renders.
- Fix: increase timeout, poll less aggressively, and expect longer waits for `16`/`20` second or 1080p jobs.

## `create-batch` is not behaving like the Batch API
- Cause: `create-batch` is a local concurrent helper, not the official Batch API.
- Fix: use the Files + Batches APIs for true offline batching; use `create-batch` only for immediate local fan-out.

## Cleanup blocked by sandbox policy
- Cause: some environments block `rm`.
- Fix: skip cleanup, or truncate temporary files instead of deleting them.
