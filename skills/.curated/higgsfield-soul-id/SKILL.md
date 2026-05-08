---
name: higgsfield-soul-id
description: >-
  Train a Higgsfield Soul Character through the Higgsfield MCP server for
  identity-faithful generation from face photos. Use for reusable face
  references, digital twins, avatars, or identity setup for generated images
  and videos. Not for one-shot face swaps or non-photo character prompts.
---

# Higgsfield Soul Character

Train a face-faithful identity model through the Higgsfield MCP server. Reuse the resulting Soul Character in Higgsfield generation.

## MCP Tools

- `show_characters` — list, train, and check Soul Characters with widget support.
- `media_upload`, `media_confirm` — prepare local face photos before training.
- `generate_image` — use a ready Soul Character with `model: "soul_2"` or `model: "soul_cinematic"`.

If MCP tools are unavailable, tell the user that the Higgsfield MCP dependency is missing or not connected. Do not silently switch to shell commands unless the user explicitly asks for them.

## MCP setup

If the Higgsfield MCP server is not connected, ask the user whether to add it:

```bash
codex mcp add higgsfield --url https://mcp.higgsfield.ai/mcp
codex mcp login higgsfield
```

After successful login, the user may need to restart Codex before retrying the task.

## UX Rules

1. Be concise. Say when training has started and when the Soul Character is ready.
2. Detect language and respond in it. MCP parameter names stay English.
3. Ask for the smallest missing set: name + 5–20 face photos.
4. Training takes minutes. Use status/list polling instead of repeated chat narration.

## Training Workflow

1. Get a short name for the character.
2. Get 5–20 clear face photos with varied angles and lighting.
3. For local files, call `media_upload`, upload bytes to the returned URL(s), then call `media_confirm` with `type: "image"`.
4. Call `show_characters`:

```json
{
  "action": "train",
  "name": "Alex",
  "images": ["<media_id_1>", "<media_id_2>", "<media_id_3>", "<media_id_4>", "<media_id_5>"]
}
```

5. Use `show_characters` with `action: "status"` or `action: "list"` until the character is ready.
6. Deliver the Soul Character name and id.

## Use The Soul

For personalized image generation, call `generate_image`:

```json
{
  "params": {
    "model": "soul_2",
    "prompt": "editorial portrait in soft window light",
    "soul_id": "<soul_id>",
    "quality": "2k"
  }
}
```

Use `soul_cinematic` instead when the user wants cinematic stills.

## Listing Existing Souls

Call `show_characters`:

```json
{ "action": "list", "status": "ready", "size": 20 }
```

## Errors

- Not authenticated → ask the user to connect/authenticate the Higgsfield MCP server.
- Plan/upgrade error → tell the user Soul training requires a paid plan.
- Too few/many photos → ask for 5–20 face photos.
- Training failed → ask for sharper, better-lit, more varied face photos.

## Reference Docs

- `references/photo-guide.md` — what photos work best.
- `references/troubleshooting.md` — common training failures.
