---
name: slack-gif-creator
description: Create and optimize animated GIFs for Slack using bundled Pillow-based helpers and validators. Use when tasks involve making a Slack emoji GIF, a short looping reaction GIF, or a compact animation from scratch or from user-provided images.
---

# Slack GIF Creator

## When to use

- Create a new GIF for Slack emoji or inline message use.
- Turn a user-provided image into a short looping animation for Slack.
- Shrink or validate an existing GIF so it fits Slack-friendly dimensions and file-size constraints.

## Bundled resources

- `scripts/gif_builder.py`: assemble frames, quantize colors, deduplicate frames, and save optimized GIFs
- `scripts/validators.py`: validate dimensions, file size, frame count, and playback metadata
- `scripts/easing.py`: easing and motion helpers for smoother animation timing
- `scripts/frame_composer.py`: small Pillow drawing helpers for backgrounds, shapes, stars, and simple text

## Workflow

1. Choose the target format before building frames.
   - Emoji GIFs: default to `128x128`, short loops, and reduced colors.
   - Message GIFs: default to a compact square such as `480x480`.
2. Install dependencies in the task workspace if needed.

```bash
uv pip install pillow numpy
```

If `uv` is unavailable:

```bash
python3 -m pip install pillow numpy
```

3. If you want local imports, copy the `scripts/` folder into the task workspace and import from it.
4. Sketch the loop before coding: subject, background, motion path, frame count, and where the loop closes.
5. Build frames with Pillow primitives or user-supplied imagery, then assemble with `GIFBuilder`.
6. Run `validate_gif()` after export. Only optimize more aggressively if the GIF is too large or the user explicitly asks for size reduction.

## Authoring rules

- Prefer simple, readable silhouettes over dense detail at emoji scale.
- Use thick outlines and strong contrast so the GIF still reads in Slack's small previews.
- Keep loops readable without captions or sound.
- Do not rely on platform emoji fonts or machine-specific assets.
- If the user supplies an image, decide whether to animate it directly or just reuse its palette, subject, or composition.
- Start with clean motion and timing. Add secondary effects only after the main loop reads clearly.

## Example

```python
from PIL import Image, ImageDraw
from scripts.gif_builder import GIFBuilder
from scripts.validators import validate_gif

builder = GIFBuilder(width=128, height=128, fps=12)

for i in range(12):
    frame = Image.new("RGB", (128, 128), (245, 247, 250))
    draw = ImageDraw.Draw(frame)
    x = 20 + i * 7
    draw.ellipse(
        (x, 44, x + 28, 72),
        fill=(217, 119, 87),
        outline=(20, 20, 20),
        width=3,
    )
    builder.add_frame(frame)

builder.save(
    "bounce.gif",
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True,
)
validate_gif("bounce.gif", is_emoji=True, verbose=True)
```

## Motion ideas

- Use `ease_out` or `bounce_out` for landings.
- Use `back_out` for slide-ins with slight overshoot.
- Use `sin()` or `cos()` offsets for shake and pulse motion.
- Use small arc motion for tosses, pops, and sticker-like movement.

## Optimization guidance

Only push file size down when needed:

- lower FPS
- shorten loop duration
- reduce color count
- enable `remove_duplicates=True`
- use `optimize_for_emoji=True` for emoji-scale exports

## Validation

Run the validator after meaningful changes:

```bash
python3 -c "from scripts.validators import validate_gif; validate_gif('out.gif', is_emoji=True, verbose=True)"
```
