# Avatars

Marketing Studio avatars are presenters for ads and UGC-style videos.

## Preset Vs Custom

| | Preset | Custom |
|---|---|---|
| Source | Curated by Higgsfield | User uploaded |
| Best for | Fast generic ads | Founder, employee, creator, brand-specific face |
| Creation | Already available | Requires media upload and create step |

## Listing

Call `show_marketing_studio`:

```json
{ "action": "list", "type": "avatar", "size": 20 }
```

Use `search` to narrow large libraries.

## Creating A Custom Avatar

1. Upload/confirm one image with `media_upload` and `media_confirm`.
2. Call `show_marketing_studio`:

```json
{
  "action": "create",
  "type": "avatar",
  "avatars": [
    {
      "name": "Founder",
      "medias": [
        { "value": "<media_id>", "role": "image", "url": "<cdn_url_if_available>", "type": "media_input" }
      ]
    }
  ]
}
```

Avatar media should be an image. If the MCP response says a URL is required for a media input, include the CDN URL returned by the upload flow.

## Passing To Generation

For `generate_video` with `model: "marketing_studio_video"`, pass:

```json
{
  "params": {
    "model": "marketing_studio_video",
    "prompt": "organic UGC product review",
    "avatars": [{ "id": "<avatar_id>", "type": "preset" }]
  }
}
```

Use `type: "custom"` for user-created avatars. For UGC modes, an avatar can be omitted when a generic presenter is acceptable.
