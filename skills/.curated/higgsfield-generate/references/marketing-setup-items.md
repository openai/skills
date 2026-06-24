# Marketing Studio Hooks And Settings

Hooks and settings are optional building blocks for `marketing_studio_video`.

- Hook (`hook_id`) controls the opening angle or ad mechanic.
- Setting (`setting_id`) controls environment or scene context.
- They are supported by `marketing_studio_video`, not `marketing_studio_image`.
- They are mutually exclusive with `ad_reference_id`.

## Discover Items

Hooks:

```json
{ "action": "list", "type": "hook", "size": 20 }
```

Settings:

```json
{ "action": "list", "type": "setting", "size": 20 }
```

Use `search` when the list is large. Responses include `items`, pagination cursor fields, and each setup item's `id`, `name`, `prompt`, `source`, and metadata.

## Generate With Setup Items

Pass one or both IDs to `generate_video`:

```json
{
  "params": {
    "model": "marketing_studio_video",
    "prompt": "casual UGC ad for the product",
    "mode": "ugc",
    "product_ids": ["<product_id>"],
    "hook_id": "<hook_id>",
    "setting_id": "<setting_id>",
    "duration": 15,
    "aspect_ratio": "9:16"
  }
}
```

When using a hook, include product context whenever possible; hooks are designed to pivot into a product pitch.

Setup items are valid only for: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, and `ugc_virtual_try_on`. See `marketing-modes.md`.
