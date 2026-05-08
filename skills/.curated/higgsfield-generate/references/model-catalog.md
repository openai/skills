# Model Catalog

Use `models_explore` as the source of truth for current model IDs, accepted parameters, media roles, aspect ratios, and durations.

Recommended quick defaults:

- Images/design/text: `gpt_image_2`.
- Video: `seedance_2_0`.
- Character/stylized/reference image work: `nano_banana_2`.
- Soul-aware image work: `soul_2` or `soul_cinematic`.
- Ads/UGC/product demos: `marketing_studio_video` or `marketing_studio_image`.

## Image Models

| Model | Provider | What it's for |
|---|---|---|
| `gpt_image_2` | OpenAI | Default high-fidelity image generation, graphic design, UI, banners, typography, and on-image text. |
| `nano_banana_2` | Google | Character, cartoon, stylized, and reference-driven image work. |
| `soul_2` | Higgsfield | Aesthetic UGC, fashion editorial, lifestyle character generation; accepts Soul Character IDs. |
| `soul_cinematic` | Higgsfield | Cinematic stills with Soul identity support. |
| `soul_cast` | Higgsfield | Distinctive text-only personas. |
| `soul_location` | Higgsfield | Environments and no-person locations. |
| `seedream_v4_5` | Bytedance | Vector illustrations and complex instruction-based edits. |
| `z_image` | Tongyi-MAI | Fast drafts and iteration. |
| `flux_2` / `flux_kontext` | Black Forest Labs | Prompt adherence, style transfer, typography remix. |
| `marketing_studio_image` | Higgsfield | Branded image ads with avatar/product context. |

## Video Models

| Model | Provider | What it's for |
|---|---|---|
| `seedance_2_0` | Bytedance | Default serious video, image-to-video, multi-shot, strong identity consistency. |
| `kling3_0` | Kling | Simpler single-plane scenes, lower-cost motion work. |
| `cinematic_studio_3_0` | Higgsfield | Highest-fidelity cinema-grade video. |
| `marketing_studio_video` | Higgsfield | Ads, UGC, unboxing, product demos, TV spots, Click-to-Ad. |
| `veo3_1_lite` | Google | Fast batch and volume. |
| `veo3_1` / `veo3` | Google | Cinematic video with stricter format constraints. |
| `minimax_hailuo` | Hailuo | Budget physics-heavy clips. |
| `wan2_7` / `wan2_6` | Wan | Stylized or experimental creative. |

## Picking Flow

Image:

1. Product photoshoot / Pinterest / hero banner / ad pack / virtual try-on / restyle → use `higgsfield-product-photoshoot`.
2. Product concept, package, label text, graphic design, UI, banner → `gpt_image_2`.
3. Branded ad image with avatar/product context → `marketing_studio_image`.
4. Soul Character ID available → `soul_2` or `soul_cinematic`.
5. Character/cartoon/reference-driven image → `nano_banana_2`.
6. Environments/no-person scenes → `soul_location`.
7. Fast draft → `z_image`.
8. Default general image → `gpt_image_2`.

Video:

1. Ads, UGC, unboxing, product demos, branded commercial → `marketing_studio_video`.
2. Serious general video / image-to-video / multi-shot → `seedance_2_0`.
3. Simpler cheaper video → `kling3_0`.
4. Highest cinema-grade video → `cinematic_studio_3_0`.
5. Fast batch → `veo3_1_lite`.

## Schema Checks

Call `models_explore` with `action: "get"` before passing uncommon params. Use the returned schema for:

- Aspect ratios.
- Duration bounds.
- Model-specific params.
- Accepted media roles.

Do not invent model IDs or params.
