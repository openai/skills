# Prompt Engineering

## Basics

Higgsfield models reward concrete, sensory prompts.

- Subject + setting + style: "a red fox curled in a snowy pine forest, golden hour, cinematic"
- Camera: lens, angle, framing, camera motion.
- Lighting: rim light, neon glow, moody backlight.
- Style/medium: photograph, anime, 3D render, watercolor.

Keep prompts concise. Very long prompts can reduce adherence.

## Image References

When passing a reference image in `params.medias`, describe the transformation, not every visible detail.

Bad: "a man with brown hair in a leather jacket holding coffee, made into anime"
Good: "transform into anime style, vibrant colors, soft cel shading"

## Image-To-Video

Use `role: "start_image"` when the image should anchor the first frame. Prompt the motion:

- Camera motion: zooms in, dollies left, sweeping pan.
- Subject motion: the dancer spins, smoke rises slowly.
- Mood: handheld UGC, cinematic, polished commercial.

Do not redescribe the static frame; the model already has it.

## Positive Phrasing

Most models do not need negative prompts. Phrase positively:

- Instead of "no blur" → "tack sharp".
- Instead of "no people" → "uninhabited landscape".

## Aspect Ratio Guidance

- `16:9` — landscape, cinematic.
- `9:16` — vertical social.
- `1:1` — square, profile/icon.
- `4:3`, `3:4`, `21:9` — model dependent; inspect with `models_explore`.

## Safety

Avoid real public figures, sexual content, and trademarked characters unless the user clearly has rights and the request is allowed.
