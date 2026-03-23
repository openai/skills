---
name: algorithmic-art
description: Design and build seeded generative art sketches, preferably as self-contained p5.js or HTML canvas artifacts. Use when the task is to create algorithmic art, generative sketches, flow fields, particle systems, parameterized visuals, or code-based art that can be rerendered from a seed.
---

# Algorithmic Art

## Overview

Use this skill to translate a visual idea into an original generative system rather than a static illustration. The deliverable should be reproducible, parameterized where helpful, and expressive through the behavior of the code itself.

## Workflow

1. Reduce the brief to an algorithmic thesis: what kind of motion, structure, accumulation, or emergence should the system create?
2. Choose the output form:
   - self-contained HTML artifact
   - standalone JavaScript sketch
   - rendered still or animation plus source
3. Always define a seed and make the output reproducible from it.
4. Expose only the few parameters that materially change the aesthetic.
5. Render, inspect, and refine until the system feels intentional rather than noisy.

## Core Rules

- Prefer original systems over imitating a recognizable living artist.
- Seed randomness explicitly and keep the seed visible in code or output metadata.
- Make parameters meaningful; avoid giant control panels with weak knobs.
- Keep palettes intentional and limited unless maximal variation is part of the concept.
- Favor one strong generative idea over several loosely connected tricks.

## Output Guidance

- For browser-based work, prefer a single self-contained HTML file that runs immediately.
- For p5.js or canvas sketches, keep the source readable enough that another person can tune it later.
- If the user wants several variants, generate them by changing the seed first, not by rewriting the whole system.
- If the work needs a static poster or cover instead of a living sketch, use the `$canvas-design` skill when it is available.

## References

Load `references/p5js-patterns.md` when the artifact will use p5.js, HTML canvas, seeded randomness, or a small parameter panel.

## Deliverables

- The runnable source
- The seed or seed-selection method
- Any parameter guidance needed to explore the work
- Rendered previews when the task calls for them
