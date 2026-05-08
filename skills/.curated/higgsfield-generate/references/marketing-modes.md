# Marketing Studio Modes

Use `mode` in `generate_video` params for `marketing_studio_video`.

| Mode slug | Human-readable label | Hook/setting | Best for |
|---|---|---|---|
| `ugc` | UGC | Yes | Default casual, organic presenter content. |
| `ugc_how_to` | Tutorial | Yes | Explainer or "how to use this" ad. |
| `ugc_unboxing` | Unboxing | Yes | Package opening and reveal. |
| `product_showcase` | Product Showcase | No | Polished product-first highlight. |
| `product_review` | Product Review | Yes | Presenter opinion/review. |
| `tv_spot` | TV Spot | No | Broadcast-style commercial. |
| `wild_card` | Wild Card | No | Experimental creative direction. |
| `ugc_virtual_try_on` | UGC Virtual Try On | Yes | Organic clothing/accessory try-on. |
| `virtual_try_on` | Pro Virtual Try On | No | Polished try-on. |

Default when unspecified: `ugc`.

## Picking Flow

- Real-person phone-shot feel → `ugc`, `ugc_how_to`, `ugc_unboxing`, or `ugc_virtual_try_on`.
- Polished broadcast commercial → `tv_spot`.
- Product-first, less presenter → `product_showcase`.
- Opinion / testimonial → `product_review`.
- Clothing/accessory try-on → `ugc_virtual_try_on` or `virtual_try_on`.
- Surprise / experimental → `wild_card`.

## Common Params

- `aspect_ratio`: `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`.
- `duration`: integer seconds; inspect current bounds with `models_explore(action: "get", model_id: "marketing_studio_video")`.
- `resolution`: `480p` or `720p`.
- `generate_audio`: boolean.
- `avatars`: array of `{ "id": "...", "type": "preset" | "custom" }`.
- `product_ids`: array of product UUIDs.
- `hook_id`, `setting_id`: optional setup item UUIDs.
- `ad_reference_id`: optional ad-reference UUID; do not combine with hooks/settings.
- `medias`: optional references with role `image`, `start_image`, or `end_image`.
- `url`: Click-to-Ad product/webproduct URL.

## URL-Driven Click-To-Ad

1. Call `show_marketing_studio` with `action: "fetch"` and `url`.
2. Follow `next_step` exactly when present; it calls `generate_video` with the right URL/type params.
3. If no `next_step` is returned, call `generate_video` with `model: "marketing_studio_video"` and the same `url`.
