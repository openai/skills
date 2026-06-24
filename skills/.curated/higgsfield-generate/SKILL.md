---
name: higgsfield-generate
description: >-
  Generate images and videos with Higgsfield AI through the Higgsfield MCP
  server, including general generation, visual edits, image-to-video, media
  references, Soul-aware generation, Marketing Studio ads, products, avatars,
  hooks/settings, and ad references. Use for images, videos, animations,
  UGC/product-demo/brand clips, or avatar/product-based ads. Not for Soul
  training, product photoshoots, marketplace cards, chat, or TTS.
---

# Higgsfield Generate

Use the Higgsfield MCP server as the primary interface for image/video generation and Marketing Studio workflows.

## MCP Tools

- `models_explore` — list, search, recommend, or inspect model schemas.
- `generate_image` — submit image jobs.
- `generate_video` — submit video jobs.
- `show_marketing_studio` — browse/create/fetch avatars, products, webproducts, presets, hooks, settings, and ad references.
- `show_generations`, `job_status`, `job_display` — browse, poll, and display generation results.
- `media_upload`, `media_confirm` — prepare local image, video, or audio files for MCP generation.

If MCP tools are unavailable, tell the user that the Higgsfield MCP dependency is missing or not connected. Do not silently switch to shell commands unless the user explicitly asks for them.

## MCP setup

If the Higgsfield MCP server is not connected, ask the user whether to add it:

```bash
codex mcp add higgsfield --url https://mcp.higgsfield.ai/mcp
codex mcp login higgsfield
```

After successful login, the user may need to restart Codex before retrying the task.

## UX Rules

1. Be concise. Return ready result URLs or a short status summary.
2. Do not expose raw JSON unless the user asks.
3. Detect the user's language and respond in it. MCP model IDs and parameter names stay English.
4. Ask one missing-input question at a time; otherwise pick a strong default model.
5. Do not pre-estimate cost or optimize for cheaper models unless the user asks.
6. For non-terminal jobs, use `job_status` with the returned job id and respect `poll_after_seconds` if present.

## Generic Generation

1. Pick a model. Use `models_explore` with `action: "recommend"` when uncertain, then `action: "get"` for constraints.

   Image defaults:
   - Product photoshoot / Pinterest / hero banner / ad pack / virtual try-on → use `higgsfield-product-photoshoot`, not this skill.
   - Product concept, package, label text, graphic design, UI, banners, typography → `gpt_image_2`.
   - Character, cartoon, stylized, or reference-driven image → `nano_banana_2`.
   - Soul Character id from `higgsfield-soul-id` → `soul_2` for stills, `soul_cinematic` for cinematic stills.
   - Branded ad image with avatar/product context → `marketing_studio_image`.
   - Default general image → `gpt_image_2`.

   Video defaults:
   - Ads, UGC, product demos, unboxing, TV spots, branded product clips → `marketing_studio_video`.
   - Serious general video, image-to-video, motion-heavy, multi-shot, 4–15s → `seedance_2_0`.
   - Simpler single-plane video when cost matters → `kling3_0`.
   - Highest cinema-grade video → `cinematic_studio_3_0`.
   - Fast batch / volume → `veo3_1_lite`.

2. Prepare media.
   - For HTTPS URLs, previous job IDs, or existing media IDs, pass them in `params.medias`.
   - For local files, call `media_upload`, upload bytes to the returned presigned URL(s), then call `media_confirm`. Use confirmed media IDs in `params.medias`.
   - Use the model's declared roles from `models_explore`: `image`, `start_image`, `end_image`, `video`, or `audio`.

3. Submit with `generate_image` or `generate_video`.

```json
{
  "params": {
    "model": "gpt_image_2",
    "prompt": "neon city at dusk, cinematic reflections",
    "aspect_ratio": "16:9"
  }
}
```

```json
{
  "params": {
    "model": "seedance_2_0",
    "prompt": "camera slowly dollies in, soft morning light",
    "duration": 12,
    "aspect_ratio": "16:9",
    "medias": [{ "value": "<media_or_job_id>", "role": "start_image" }]
  }
}
```

4. Deliver the result URL when completed. If the response is pending, poll with `job_status`.

## Marketing Studio

Use Marketing Studio for branded ads, avatar/product campaigns, UGC clips, product demos, and Click-to-Ad flows.

### Product Or Webproduct

- Existing library: `show_marketing_studio` with `action: "list"`, `type: "product"` or `type: "webproduct"`.
- Product URL: `show_marketing_studio` with `action: "fetch"` and `url`.
- Uploaded product images: upload/confirm local media first, then `show_marketing_studio` with `action: "create"`, `type: "product"`, `title`, and `medias`.
- App Store / Play Store / SaaS pages: use `type: "webproduct"` when the ad promotes the app/site instead of one physical item.

For URL-driven Click-to-Ad, call `show_marketing_studio(action: "fetch")`, then immediately follow the returned `next_step` and call `generate_video` with those exact params.

### Avatars

- Presets/custom avatars: `show_marketing_studio` with `action: "list"`, `type: "avatar"`.
- Custom avatar from local media: upload/confirm the image, then `show_marketing_studio` with `action: "create"`, `type: "avatar"`, and `avatars`.
- For UGC modes, an avatar is optional if the brief only needs a generic person; pass one when the user wants a specific presenter.

### Hooks, Settings, And Modes

- Presets: `show_marketing_studio` with `action: "presets"`.
- Hooks: `show_marketing_studio` with `action: "list"`, `type: "hook"`.
- Settings: `show_marketing_studio` with `action: "list"`, `type: "setting"`.
- Pass selected IDs to `generate_video` as `hook_id` and/or `setting_id`.
- Hooks/settings are valid only for Marketing Studio modes listed in `marketing-modes.md`.
- Do not combine `hook_id`/`setting_id` with `ad_reference_id`.

### Ad References

Use ad references when the user says "make a video like this", "copy this ad style", "use this clip as reference", or similar.

1. For a local reference video, use `media_upload` and `media_confirm` with type `video`.
2. Call `show_marketing_studio` with `action: "create"`, `type: "ad_reference"`, and `video_input_id`; optionally bind one avatar and/or one product.
3. Follow the returned `next_step` when present. It includes `ad_reference_id` for `generate_video`.
4. If the user wants to refine the extracted concept, use `show_marketing_studio` with `action: "update"`, `type: "ad_reference"`, and edited concept fields.

## Errors

- Missing prompt → ask for the prompt.
- Invalid enum or unknown param → call `models_explore(action: "get", model_id: ...)` and retry with supported params.
- Auth failure → tell the user to connect/authenticate the Higgsfield MCP server.
- Failed generation / safety status → briefly explain and ask for a safer revision.
- Upload issue → retry `media_upload`/`media_confirm`; local paths cannot be passed directly to generation tools.

## Reference Docs

Load on demand:

- `references/model-catalog.md` — picking models and checking schemas.
- `references/media-inputs.md` — MCP media upload and role handling.
- `references/prompt-engineering.md` — prompt patterns.
- `references/troubleshooting.md` — MCP errors and retry handling.
- `references/marketing-avatars.md` — avatar workflows.
- `references/marketing-products.md` — product and webproduct workflows.
- `references/marketing-setup-items.md` — hooks/settings.
- `references/marketing-ad-references.md` — ad reference videos.
- `references/marketing-modes.md` — Marketing Studio modes.
