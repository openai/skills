# Marketing Studio Ad References

Ad references are reusable inspiration videos for "make a video like this" workflows. They extract a reference clip's scenario, pacing, hook, narration style, and composition so `marketing_studio_video` can follow it.

## When To Use

Use an ad reference when the user says:

- "Make a video like this."
- "Recreate this ad."
- "Use this clip as a reference."
- "Copy the structure/style of this product video."

Do not combine ad references with hooks/settings. Pick either:

- Reference-driven: `ad_reference_id`.
- Composed setup: `hook_id` and/or `setting_id`.

## Create From Local Video

1. Call `media_upload` for the local video.
2. Upload bytes to the returned URL.
3. Call `media_confirm` with `type: "video"`.
4. Call `show_marketing_studio`:

```json
{
  "action": "create",
  "type": "ad_reference",
  "video_input_id": "<video_media_id>"
}
```

Optionally bind one avatar and/or one product:

```json
{
  "action": "create",
  "type": "ad_reference",
  "video_input_id": "<video_media_id>",
  "avatars": [{ "id": "<avatar_id>", "type": "preset" }],
  "product_ids": ["<product_id>"]
}
```

The response may include `next_step`; follow it to call `generate_video` with `ad_reference_id`.

## List Or Inspect

Use `show_marketing_studio`:

```json
{ "action": "list", "type": "ad_reference", "size": 20 }
```

The response includes status and processed reference metadata. A reference is usable when status is completed.

## Edit Extracted Concept

After analysis, the user can refine the extracted concept:

```json
{
  "action": "update",
  "type": "ad_reference",
  "ad_reference_id": "<ad_reference_id>",
  "edited_concept_text": "Keep the same pacing, but make the hook focus on battery life."
}
```

Then call `generate_video` with the same `ad_reference_id`.
