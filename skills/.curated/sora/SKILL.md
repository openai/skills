---
name: "sora"
description: "Use when the user asks to generate, edit, extend, poll, list, download, or delete Sora videos, create reusable non-human Sora character references, or run local multi-video queues via the bundled CLI (`scripts/sora.py`); includes requests like: (i) generate AI video, (ii) edit this Sora clip, (iii) extend this video, (iv) create a character reference, (v) download video/thumbnail/spritesheet, and (vi) Sora batch planning; requires `OPENAI_API_KEY` and Sora API access."
---


# Sora Video Generation Skill

Creates or manages Sora video jobs for the current project (product demos, marketing spots, cinematic shots, social clips, UI mocks). Defaults to `sora-2` with structured prompt augmentation and prefers the bundled CLI for deterministic runs. Note: `$sora` is a skill tag in prompts, not a shell command.

## When to use
- Generate a new video clip from a prompt
- Create a reusable character reference from a short non-human source clip
- Edit an existing generated video with a targeted prompt change
- Extend a completed video with a continuation prompt
- Poll status, list jobs, or download assets (video/thumbnail/spritesheet)
- Run a local multi-job queue now, or plan a true Batch API submission for offline rendering

## Decision tree
- If the user has a short non-human reference clip they want to reuse across shots → `create-character`
- If the user has a completed video and wants the next beat/continuation → `extend`
- If the user has a completed video and wants a targeted change while preserving the shot → `edit`
- If the user has a video id and wants status or assets → `status`, `poll`, or `download`
- If the user needs many renders immediately inside Codex → `create-batch` (local fan-out, not the Batch API)
- If the user needs many renders for offline processing or a studio pipeline → use the official Batch API flow described in `references/video-api.md`
- Otherwise → `create` (or `create-and-poll` if they need a ready asset in one step)

## Workflow
1. Decide intent: create vs create-character vs edit vs extend vs status/download vs local queue vs official Batch API.
2. Collect inputs: prompt, model, size, seconds, any image reference, and any character IDs.
3. Prefer CLI augmentation flags (`--use-case`, `--scene`, `--camera`, etc.) instead of hand-writing a long structured prompt. If you already have a structured prompt file, pass `--no-augment`.
4. Run the bundled CLI (`scripts/sora.py`) with sensible defaults. For long prompts, prefer `--prompt-file` to avoid shell-escaping issues.
5. For async jobs, poll until terminal status (or use `create-and-poll`).
6. Download assets (video/thumbnail/spritesheet) and save them locally before URLs expire.
7. If the user wants continuity across many shots, create character assets first, then reference them in later `create` calls.
8. If the user wants to iterate on a completed shot, prefer `edit`; if they want the shot to continue in time, prefer `extend`.
9. Use one targeted change per iteration.

## Authentication
- `OPENAI_API_KEY` must be set for live API calls.

If the key is missing, give the user these steps:
1. Create an API key in the OpenAI platform UI: https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` as an environment variable in their system.
3. Offer to guide them through setting the environment variable for their OS/shell if needed.
- Never ask the user to paste the full key in chat. Ask them to set it locally and confirm when ready.

## Defaults & rules
- Default model: `sora-2` (use `sora-2-pro` for higher fidelity).
- Default size: `1280x720`.
- Default seconds: `4` (allowed: `"4"`, `"8"`, `"12"`, `"16"`, `"20"`).
- Always set size and seconds via API params; prose will not change them.
- `sora-2-pro` is required for `1920x1080` and `1080x1920`.
- Use up to two characters per generation.
- Use the OpenAI Python SDK (`openai` package). If high-level SDK helpers lag the latest Sora guide, use low-level `client.post/get/delete` inside the official SDK rather than standalone HTTP code.
- Require `OPENAI_API_KEY` before any live API call.
- If uv cache permissions fail, set `UV_CACHE_DIR=/tmp/uv-cache`.
- Input reference images must be jpg/png/webp and should match target size.
- JSON `input_reference` objects use either `file_id` or `image_url`; uploaded file paths use multipart.
- Download URLs expire after about 1 hour; copy assets to your own storage.
- Batch-generated videos remain downloadable for up to 24 hours after the batch completes.
- `create-batch` in `scripts/sora.py` is a local concurrent queue, not the official Batch API.
- Prefer the bundled CLI and **never modify** `scripts/sora.py` unless the user asks.
- Sora can generate audio; if a user requests voiceover/audio, specify it explicitly in the `Audio:` and `Dialogue:` lines and keep it short.

## API limitations
- Models are limited to `sora-2` and `sora-2-pro`.
- API access to Sora models requires an organization-verified account.
- Duration must be set via the `seconds` parameter and currently supports `4`, `8`, `12`, `16`, and `20`.
- Character uploads currently work best with short `2`-`4` second non-human MP4s in `16:9` or `9:16`, at `720p`-`1080p`.
- Extensions can add up to `20` seconds each, up to six times per source video, for a maximum total length of `120` seconds.
- Extensions currently do not support characters or image references.
- This skill supports editing existing generated videos by ID.
- The official Batch API currently supports `POST /v1/videos` only, with JSON bodies rather than multipart uploads.
- Output sizes are limited by model (see `references/video-api.md` for the supported sizes).
- Video creation is async; you must poll for completion before downloading.
- Rate limits apply by usage tier (do not list specific limits).
- Content restrictions are enforced by the API (see Guardrails below).

## Guardrails (must enforce)
- Only content suitable for audiences under 18.
- No copyrighted characters or copyrighted music.
- No real people (including public figures).
- Input images with human faces are rejected.
- Character uploads in this skill are for non-human subjects only.

## Prompt augmentation
Reformat prompts into a structured, production-oriented spec. Only make implicit details explicit; do not invent new creative requirements.

Template (include only relevant lines):
```
Use case: <where the clip will be used>
Primary request: <user's main prompt>
Scene/background: <location, time of day, atmosphere>
Subject: <main subject>
Action: <single clear action>
Camera: <shot type, angle, motion>
Lighting/mood: <lighting + mood>
Color palette: <3-5 color anchors>
Style/format: <film/animation/format cues>
Timing/beats: <counts or beats>
Audio: <ambient cue / music / voiceover if requested>
Text (verbatim): "<exact text>"
Dialogue:
<dialogue>
- Speaker: "Short line."
</dialogue>
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

Augmentation rules:
- Keep it short; add only details the user already implied or provided elsewhere.
- For edits, explicitly list invariants ("same shot, change only X").
- For character-based shots, mention the character name verbatim in the prompt.
- If any critical detail is missing and blocks success, ask a question; otherwise proceed.
- If you pass a structured prompt file to the CLI, add `--no-augment` to avoid the tool re-wrapping it.

## Examples

### Generation example (single shot)
```
Use case: product teaser
Primary request: a close-up of a matte black camera on a pedestal
Action: slow 30-degree orbit over 4 seconds
Camera: 85mm, shallow depth of field, gentle handheld drift
Lighting/mood: soft key light, subtle rim, premium studio feel
Constraints: no logos, no text
```

### Edit example (invariants)
```
Primary request: same shot and framing, switch palette to teal/sand/rust with warmer backlight
Constraints: keep the subject and camera move unchanged
```

### Character consistency example
```
Primary request: Mossy, a moss-covered teapot mascot, hurries through a lantern-lit market at dusk
Camera: cinematic tracking shot, 35mm, shoulder height
Lighting/mood: warm dusk practicals, soft haze
Constraints: keep Mossy’s silhouette and moss texture consistent across the shot
```

## Prompting best practices (short list)
- One main action + one camera move per shot.
- Use counts or beats for timing ("two steps, pause, turn").
- Keep text short and the camera locked-off for UI or on-screen text.
- Add a brief avoid line when artifacts appear (flicker, jitter, fast motion).
- Shorter prompts are more creative; longer prompts are more controlled.
- Put dialogue in a dedicated block; keep lines short for 4-8s clips.
- Mention character names verbatim when using uploaded character IDs.
- State invariants explicitly for edits (same shot, same camera move).
- Prefer `edit` for targeted changes and `extend` for timeline continuation.
- Iterate with single-change follow-ups to preserve continuity.

## Guidance by asset type
Use these modules when the request is for a specific artifact. They provide targeted templates and defaults.
- Cinematic shots: `references/cinematic-shots.md`
- Social ads: `references/social-ads.md`

## CLI + environment notes
- CLI commands + examples: `references/cli.md`
- API parameter quick reference: `references/video-api.md`
- Prompting guidance: `references/prompting.md`
- Sample prompts: `references/sample-prompts.md`
- Troubleshooting: `references/troubleshooting.md`
- Network/sandbox tips: `references/codex-network.md`

## Reference map
- **`references/cli.md`**: how to run create/edit/extend/create-character/poll/download/local-queue flows via `scripts/sora.py`.
- **`references/video-api.md`**: API-level knobs (models, sizes, duration, characters, edits, extensions, official Batch API).
- **`references/prompting.md`**: prompt structure, character continuity, editing, and extension guidance.
- **`references/sample-prompts.md`**: copy/paste prompt recipes (examples only; no extra theory).
- **`references/cinematic-shots.md`**: templates for filmic shots.
- **`references/social-ads.md`**: templates for short social ad beats.
- **`references/troubleshooting.md`**: common errors and fixes.
- **`references/codex-network.md`**: network/approval troubleshooting.
