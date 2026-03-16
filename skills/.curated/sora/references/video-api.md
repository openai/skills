# Sora Video API quick reference

Keep this file short; the full source of truth is the latest OpenAI Sora guide plus the API changelog.

## Source-of-truth note
- The March 2026 changelog and Sora guide added characters, 16s/20s clips, `1920x1080` / `1080x1920` on `sora-2-pro`, extensions, and edits.
- Some typed SDK and API-reference pages may still show the older `4`/`8`/`12` and pre-1080p enums.
- If they disagree, follow the latest guide/changelog and use the bundled CLI, which bridges the SDK lag with low-level official-client calls.

## Models
- `sora-2`: faster, flexible iteration
- `sora-2-pro`: higher fidelity, slower, more expensive

## Sizes (by model)
- `sora-2`: `1280x720`, `720x1280`
- `sora-2-pro`: `1280x720`, `720x1280`, `1024x1792`, `1792x1024`, `1920x1080`, `1080x1920`
- Use `sora-2-pro` for 1080p exports.

## Duration
- `seconds`: `"4"`, `"8"`, `"12"`, `"16"`, `"20"`
- Use shorter clips first when iterating on motion, timing, or composition.

## Input references
- `input_reference` guides the first frame of a generation.
- Multipart requests use an uploaded image file.
- JSON requests use an object with exactly one of `file_id` or `image_url`.
- Supported image formats: jpg/jpeg, png, webp.
- Input references should match the target `size`.

## Characters
- Create reusable non-human characters via `POST /v1/videos/characters`.
- Character source clips work best as short MP4s (`2`-`4`s) in `16:9` or `9:16`, at `720p`-`1080p`.
- Reference up to two characters per generation with `characters: [{"id": "..."}]`.
- Mention the character name verbatim in the prompt; the ID alone is not enough.
- Characters can be combined with `input_reference`.
- In this skill, character workflows are limited to non-human subjects.

## Edits vs remix
- Preferred: `POST /v1/videos/edits`
- Legacy/deprecated: `POST /v1/videos/{video_id}/remix`
- Use edits for new integrations.
- In this skill, use edits for existing generated video IDs only.

## Extensions
- Use `POST /v1/videos/extensions` to continue a completed video.
- Each extension can add up to `20` seconds.
- A single video can be extended up to six times, for a maximum total length of `120` seconds.
- Extensions do not support characters or image references.

## Jobs and status
- Creation, edit, and extension jobs are async.
- Common statuses: `queued`, `in_progress`, `completed`, `failed`
- Poll every `10`-`20`s or use webhooks.
- Webhook events: `video.completed`, `video.failed`

## Core endpoints
- `POST /videos`: create
- `POST /videos/characters`: create a reusable character
- `POST /videos/edits`: edit an existing generated video by ID
- `POST /videos/extensions`: extend a completed video
- `GET /videos/{id}`: retrieve status/details
- `GET /videos/{id}/content`: download content
- `GET /videos`: list
- `DELETE /videos/{id}`: delete
- `POST /videos/{id}/remix`: legacy/deprecated

## Download variants
- `video` -> mp4
- `thumbnail` -> webp
- `spritesheet` -> jpg

Download URLs expire after about 1 hour; save assets to your own storage promptly.

## Batch API
- The official Batch API supports `POST /v1/videos` only.
- Batch requests must use JSON, not multipart.
- Upload assets ahead of time and reference them in the JSON body.
- For image-guided Batch jobs, use JSON `input_reference` with `file_id` or `image_url`.
- Batch-generated videos remain downloadable for up to 24 hours after the batch completes.
- The bundled `scripts/sora.py create-batch` command is a local fan-out helper, not the official Batch API.

## Guardrails
- Only content suitable for audiences under 18
- No copyrighted characters or copyrighted music
- No real people (including public figures)
- Input images with human faces are currently rejected
