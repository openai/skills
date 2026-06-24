# Media Inputs

Use MCP media inputs for reference images, videos, and audio.

## Local Files

Local file paths cannot be passed directly to `generate_image` or `generate_video`.

1. Call `media_upload` with `files` and content types.
2. Upload bytes to each returned `upload_url` using the returned instructions or an equivalent PUT request.
3. Call `media_confirm` with `type: "image"`, `"video"`, or `"audio"`.
4. Use the confirmed `media_id` as `params.medias[].value`.

## Existing References

These can be passed directly as `params.medias[].value`:

- Confirmed media IDs from `media_confirm`.
- Previous generation job IDs.
- HTTPS media URLs when the receiving MCP tool supports URL ingestion.

## Roles

Each model declares accepted media roles. Check with `models_explore` using `action: "get"`.

| Model family | Common roles | Notes |
|---|---|---|
| Most image models | `image` | One or more references. |
| `seedance_2_0` | `image`, `start_image`, `end_image`, `video`, `audio` | Audio is a media role, not a separate audio-generation flag. |
| `kling3_0` | `start_image`, `end_image` | First/last frame transitions. |
| `kling2_6` | `start_image` | Single frame anchor. |
| `veo3_1` | `start_image` | Usually max one reference. |
| `veo3` | `image` | Single image-to-video reference. |
| `marketing_studio_video` | `image`, `start_image`, `end_image` | Product/avatar/ad data is passed through dedicated params. |
| Text-only models | none | Do not pass media. |

## Example Param Shapes

Image reference:

```json
{
  "params": {
    "model": "nano_banana_2",
    "prompt": "transform into watercolor style",
    "medias": [{ "value": "<media_id_or_url_or_job_id>", "role": "image" }]
  }
}
```

Image-to-video with audio reference:

```json
{
  "params": {
    "model": "seedance_2_0",
    "prompt": "person speaking naturally to camera",
    "duration": 8,
    "medias": [
      { "value": "<image_media_id>", "role": "start_image" },
      { "value": "<audio_media_id>", "role": "audio" }
    ]
  }
}
```

## Mismatches

- If a model rejects a role, call `models_explore(action: "get")` and choose one of its declared roles.
- If a model is text-only, remove `medias`.
- If multiple references fail, retry with one reference first, then add more.
