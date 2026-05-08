---
name: hatch-pet
description: Create, repair, validate, preview, and package Codex-compatible animated pets and pet spritesheets from character art, screenshots, generated images, or visual references. Use when a user wants to hatch a Codex pet, create a custom animated pet, or build a built-in pet asset with an 8x9 atlas, transparent unused cells, row-by-row animation prompts, QA contact sheets, preview videos, and pet.json packaging. This skill composes the installed $imagegen system skill for visual generation and uses bundled scripts for deterministic spritesheet assembly.
---

# Hatch Pet

## Overview

Create a Codex-compatible animated pet from a concept, one or more reference images, or both. This skill owns pet-specific prompt planning, animation rows, frame extraction, atlas geometry, QA, previews, and packaging. It delegates visual generation to `$imagegen`.

User-facing inputs are optional. If the user omits a pet name, infer one from the concept or reference filenames; if that is not possible, choose a short appropriate name. If the user omits a description, infer one from the concept or references. If the user omits reference images, generate the base pet from text first, then use that base as the canonical reference for every animation row.

## Generation Delegation

Use `$imagegen` for all normal visual generation.

Before generating base art, row strips, or repair rows, load and follow the installed image generation skill:

```text
${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/SKILL.md
```

Do not call the Image API directly for the normal path. Let `$imagegen` choose its own built-in-first path and its own CLI fallback rules. If `$imagegen` says a fallback requires confirmation, ask the user before continuing.

When invoking `$imagegen` from this skill, pass the generated pet prompt as the authoritative visual spec. Do not wrap it in the generic `$imagegen` shared prompt schema and do not add extra polish, hero-art, photo, product, or illustration-style augmentation. Pet prompts should stay terse, sprite-specific, and digital-pet oriented; only add role labels for input images and any essential user constraint.

Use this skill's scripts for deterministic work only: preparing prompts and manifests, ingesting selected `$imagegen` outputs, extracting frames, validating rows, composing the final atlas, creating QA media, and packaging.

Hard boundary: do not create, draw, tile, warp, mirror, or synthesize pet visuals with local Python/Pillow scripts, SVG, canvas, HTML/CSS, or other code-native art as a substitute for `$imagegen`. For a normal pet run, expect up to 10 visual generation jobs: 1 base pet plus 9 row-strip jobs. The only exception is `running-left`, which may be derived by mirroring `running-right` only after `running-right` has been generated, visually inspected, and explicitly approved as safe to mirror. If mirroring is not appropriate, generate `running-left` as a normal grounded `$imagegen` row. If those calls are too expensive, blocked, or unavailable, stop and explain the blocker instead of fabricating row strips locally.

Do not mark visual jobs complete by editing `imagegen-jobs.json`, copying files into `decoded/`, or writing helper scripts that populate row outputs. Use `record_imagegen_result.py` for selected built-in `$imagegen` outputs, or `generate_pet_images.py` only for the documented secondary fallback. The deterministic scripts may only process already-generated visual outputs.

Only the base job may be prompt-only. Every row-strip job generated through `$imagegen` must use the input images listed in `imagegen-jobs.json`, including the canonical base reference created after the base job is recorded. Treat any row generation without attached grounding images as invalid.

## Codex Digital Pet Style

Default pet art should match the Codex app's built-in digital pets: small pixel-art-adjacent mascots with compact chibi proportions, chunky readable silhouettes, thick dark 1-2 px outlines, visible stepped/pixel edges, limited palettes, flat cel shading, simple expressive faces, and tiny limbs. Even if the reference art is more detailed, complex or realistic, the generated pet should be simplified into this style.

Do NOT generate polished illustration, painterly rendering, anime key art, 3D rendering, glossy app-icon treatment, realistic fur or material texture, soft gradients, high-detail antialiasing, and complex tiny accessories. References that are more detailed than this should be simplified into the house style before row generation.

## Transparency And Effects

Pet rows are processed into transparent 192x208 cells, so every generated pixel must either belong to the pet sprite or be cleanly removable chroma-key background. Prefer pose, expression, and silhouette changes over decorative effects.

Allowed effects must satisfy all of these conditions:

- The effect is state-relevant and helps explain the animation.
- The effect is physically attached to, touching, or overlapping the pet silhouette, not floating nearby.
- The effect is inside the same frame slot as the pet and does not create a separate sprite component.
- The effect is opaque, hard-edged, pixel-style, and uses non-chroma-key colors.
- The effect is small enough to remain readable at 192x208 without clutter.

Examples of allowed effects: a tear touching the face, a small smoke puff touching the box or head, or tiny stars overlapping the pet during a failed/dizzy reaction.

Avoid these by default because they usually break transparent-background cleanup or component extraction:

- wave marks, motion arcs, speed lines, action streaks, afterimages, blur, or smears
- detached stars, loose sparkles, floating punctuation, floating icons, falling tear drops, separated smoke clouds, or loose dust
- cast shadows, contact shadows, drop shadows, oval floor shadows, floor patches, landing marks, impact bursts, glow, halo, aura, or soft transparent effects
- text, labels, frame numbers, visible grids, guide marks, speech bubbles, thought bubbles, UI panels, code snippets, checkerboard transparency, white backgrounds, black backgrounds, or scenery
- chroma-key-adjacent colors in the pet, prop, effects, highlights, or shadows
- stray pixels, disconnected outline bits, speckle/noise, cropped body parts, overlapping poses, or any pose that crosses into a neighboring frame slot

### Frame Extraction And Playback Stability

Generated row strips may intentionally keep the pet at a constant apparent scale while a pose moves within the slot. Do not accept a final atlas that re-crops each frame to make the character fill the 192x208 cell when the row strip already has stable scale and baseline. This causes visible size popping in preview videos, especially for sitting, crying, crouching, jumping, split poses, or any action that intentionally shifts lower in the slot.

Prefer normal component extraction when it preserves scale and separates frames cleanly. If the contact sheet or preview videos show per-frame size changes caused by cropping, re-finalize with `--extract-method fixed-slots --allow-slot-extraction` so each frame uses shared row-level slot geometry. Fixed-slot extraction must still use mask/component cleanup and shared placement; reject crude slot crops that clip wide limbs, include neighboring-slot fragments, or leave colored residue in transparent areas.

Wide poses must be QAed against the contact sheet at native cell size. If a split jump, raised arm, prop, or long accessory touches a cell edge or is cut off, repair the row or enlarge the row-level safe padding before accepting it. Hidden RGB in fully transparent pixels must be cleared by the deterministic atlas composer; reject WebP/PNG outputs that show colored blocks, stripes, or remnants in external viewers.

State-specific guidance:

- `idle`: keep this calm and low-distraction. Use only subtle breathing, a tiny blink, a slight head/body bob, a very small material sway, or another quiet persona-preserving motion. Idle frames may be subtle, but they must not be near-identical copies; plan visible micro-variation across the loop, such as open eyes, blink, softer smile, tiny head tilt, breathing up/down, and return-to-neutral. Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- `waving`: show the wave through paw pose only. Do not draw wave marks, motion arcs, lines, sparkles, or symbols around the paw.
- `jumping`: show vertical motion through body position only. Do not draw shadows, dust, landing marks, impact bursts, bounce pads, or floor cues.
- `failed`: tears, attached smoke puffs, or attached stars are allowed if they obey the allowed-effects rules; do not use red X marks, floating symbols, detached smoke, detached stars, or separate tear droplets.
- `review`: show focus through lean, blink, eyes, head tilt, or paw position. Do not add magnifying glasses, papers, code, UI, punctuation, or symbols unless that prop already exists in the base pet identity.
- `running-right` and `running-left`: show directional locomotion through body, limb, and prop movement only. `running-right` must face and travel right; `running-left` must face and travel left. The leg cycle must alternate clearly across frames, not repeat one static stride with small offsets. When deriving a mirrored row, mirror each frame in place and preserve temporal frame order. Do not draw speed lines, dust clouds, floor shadows, or motion trails.
- `running`: show an active working/in-progress loop, as if the pet is busy running a task. Do not show literal foot-running, jogging, sprinting, treadmill motion, raised knees, long steps, pumping arms, or directional travel.

## Pet Naming

Ask the user for a pet name when they have not provided one and only if the conversation naturally allows it. If asking would slow down a direct execution request, choose a short appropriate name from the pet concept, reference image, or personality, then use that name consistently as the display name and as the source for the package folder slug.

Good built-in style examples:

- Codex - The original Codex companion.
- Dewey - A tidy duck for calm workspace days.
- Fireball - Hot path energy for fast iteration.
- Rocky - A steady rock when the diff gets large.
- Seedy - Small green shoots for new ideas.
- Stacky - A balanced stack for deep work.
- BSOD - A tiny blue-screen gremlin.
- Null Signal - Quiet signal from the void.

## Visible Progress Plan

For every pet run, keep a visible checklist so the user can see where the work is up to. Create the checklist before starting, keep one step active at a time, and update it as each step finishes.

Before creating the checklist, establish the pet name when possible. Use the user-provided name when available; otherwise infer a short appropriate name from the concept or references. If the name is too long, not settled, or not appropriate for a friendly checklist, use `your pet` instead.

Use this checklist for a normal pet run, replacing `<Pet>` with the pet's name or `your pet`:

1. Getting `<Pet>` ready.
2. Imagining `<Pet>`'s main look.
3. Picturing `<Pet>`'s poses.
4. Hatching `<Pet>`.

What each step means:

- `Getting <Pet> ready.` Choose or confirm the pet name, description, source images, and working folder.
- `Imagining <Pet>'s main look.` Generate the pet's main reference image. This is required for new pets, even when the user does not provide an image, because it becomes the visual source of truth.
- `Picturing <Pet>'s poses.` Create the pose rows, starting with `idle` and `running-right` to confirm the pet still looks consistent. Confirm idle frames have visible micro-variation, and confirm the directional running row faces right with clear alternating legs. Only mirror `running-left` if `running-right` clearly works when flipped.
- `Hatching <Pet>.` Turn the approved poses into the final pet files, review the contact sheet, previews, and validation results, fix any broken parts, save `pet.json` and `spritesheet.webp` into the pet folder, then tell the user where the pet and QA files were saved.

Only mark a step complete when the real file, image, or decision exists. If this is just a repair run, start from the first relevant step instead of restarting the whole checklist.

## Default Workflow

1. Prepare a pet run folder and imagegen job manifest:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/hatch-pet"
python "$SKILL_DIR/scripts/prepare_pet_run.py" \
  --pet-name "<Name>" \
  --description "<one sentence>" \
  --reference /absolute/path/to/reference.png \
  --output-dir /absolute/path/to/run \
  --pet-notes "<stable pet description>" \
  --style-notes "<style notes>" \
  --force
```

All arguments above are optional except any flags needed to express user constraints. For text-only requests, pass the concept through `--pet-notes` and omit `--reference`; `prepare_pet_run.py` will infer a name, description, chroma key, and output directory as needed.

2. Inspect the next ready `$imagegen` jobs:

```bash
python "$SKILL_DIR/scripts/pet_job_status.py" --run-dir /absolute/path/to/run
```

3. For each ready job, invoke `$imagegen` with:

- the prompt file listed in `imagegen-jobs.json`
- every input image listed for the job, with its role label
- the default built-in `image_gen` path unless `$imagegen` itself routes otherwise

The base job must complete first. If user references exist, the base job uses them. If no references exist, the base job may be prompt-only. After recording the base, `record_imagegen_result.py` writes `decoded/base.png` and `references/canonical-base.png`; all row jobs use the original references if present plus those canonical base images.

`prepare_pet_run.py` also creates 9 row-specific layout guide images under `references/layout-guides/`, one per animation state. Row jobs attach the matching guide as a layout-only input so the model can follow the correct frame count, spacing, centering, and safe padding. Treat these guides as invisible construction references: the generated row strip must not include visible boxes, borders, center marks, labels, guide colors, or the guide background.

When generating row strips, keep the identity lock in the row prompt authoritative: do not redesign the pet, and preserve the same head shape, face, markings, palette, prop, outline weight, body proportions, and silhouette. A row that looks like a related but different pet is failed even if the deterministic geometry QA passes.

Generate and record `running-right` before deciding how to complete `running-left`. Inspect `running-right` against the base and references. The row must actually face right and show a readable alternating gait; a row that faces left or repeats one static stride is a failed `running-right` even if geometry validation passes. If the pet is visually symmetric enough that a horizontal mirror preserves identity, prop placement, handedness, markings, lighting, text-free details, and direction semantics, derive `running-left` with:

```bash
python "$SKILL_DIR/scripts/derive_running_left_from_running_right.py" \
  --run-dir /absolute/path/to/run \
  --confirm-appropriate-mirror \
  --decision-note "<why mirroring preserves this pet's identity>"
```

If there is any asymmetric side-specific marking, readable text, non-mirrored logo, handed prop, one-sided accessory, lighting cue, or direction-specific pose that would become wrong when flipped, do not mirror. Generate `running-left` with `$imagegen` using its row prompt and all listed grounding images, including `decoded/running-right.png` as a gait reference.

Mirroring must preserve animation timing. Use `derive_running_left_from_running_right.py`, which mirrors each frame slot in place; do not mirror the whole strip in a way that reverses frame order.

For the built-in path, record the selected source image from `$CODEX_HOME/generated_images/.../ig_*.png`. Do not record files from the run directory, `tmp/`, hand-made fixtures, deterministic row folders, or post-processed copies as visual job sources.

4. After selecting a generated output for a job, ingest it:

```bash
python "$SKILL_DIR/scripts/record_imagegen_result.py" \
  --run-dir /absolute/path/to/run \
  --job-id <job-id> \
  --source /absolute/path/to/generated-output.png
```

This copies the image to the exact decoded path expected by the deterministic pipeline and records source metadata in `imagegen-jobs.json`.

5. When all jobs are complete, finalize:

```bash
python "$SKILL_DIR/scripts/finalize_pet_run.py" \
  --run-dir /absolute/path/to/run
```

Use the default extraction first for a normal clean row strip. If the generated row strip has stable character scale but the final atlas or preview videos show size popping because each frame was individually fit to the cell, re-finalize with fixed-slot extraction:

```bash
python "$SKILL_DIR/scripts/finalize_pet_run.py" \
  --run-dir /absolute/path/to/run \
  --extract-method fixed-slots \
  --allow-slot-extraction
```

After using fixed-slot extraction, inspect for the opposite failure mode: wide poses, raised arms, props, hoops, ribbons, or split jumps clipped by the fixed frame. If that happens, repair only the affected row or regenerate it with more safe padding; do not accept a clipped atlas just because playback scale is stable.

Expected output:

```text
run/
  pet_request.json
  imagegen-jobs.json
  prompts/
  decoded/
  frames/frames-manifest.json
  final/spritesheet.png
  final/spritesheet.webp
  final/validation.json
  qa/contact-sheet.png
  qa/review.json
  qa/run-summary.json
  qa/videos/*.mp4
```

Package output is written outside the run directory by default. If `CODEX_HOME` is set, use it; otherwise use `$HOME/.codex`.

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/
  pet.json
  spritesheet.webp
```

Review `qa/contact-sheet.png`, `qa/review.json`, `final/validation.json`, and `qa/videos/` before accepting the pet.

Deterministic validation is necessary but not sufficient. Before calling the pet done, visually inspect the contact sheet for identity consistency. Block acceptance if any row changes species/body type, face, markings, palette, prop design, prop side unexpectedly, or overall silhouette.

Preview videos are required for playback-specific QA. Block acceptance if videos show unintended character size popping, sudden vertical jumps caused by cropping, wrong facing direction, reversed or non-alternating gait, idle frames that are effectively identical, or transparent-color blocks that were hidden in the contact sheet.

## Subagent Row Generation

After the base job has been recorded and `references/canonical-base.png` exists, row-strip visual generation must use subagents unless the user explicitly says not to use subagents for this session. Before row generation, state that subagents are being used and which row jobs are being delegated. If subagents cannot be spawned because the current environment or tool policy blocks them, stop before row-strip generation, explain the blocker, and ask for explicit user direction before continuing sequentially.

The parent agent must own the manifest and package writes.

Default flow:

1. Parent runs `prepare_pet_run.py`.
2. Parent generates and records `base`.
3. Parent runs `pet_job_status.py`.
4. Parent spawns subagents for `idle` and `running-right` first as identity and gait checks.
5. Parent records the selected `idle` and `running-right` results returned by subagents.
6. Parent decides whether `running-left` is safe to derive by mirror; if not, parent treats it as a normal grounded row job delegated to a subagent.
7. Parent spawns subagents for every remaining non-derived row image-generation job.
8. Each subagent receives the row prompt and every listed input image path, invokes `$imagegen`, and returns only the selected `$CODEX_HOME/generated_images/.../ig_*.png` source path.
9. Parent alone runs `record_imagegen_result.py`, `derive_running_left_from_running_right.py`, repair queueing, finalization, QA, and packaging.

Subagent write boundary: do not let subagents edit `imagegen-jobs.json`, copy files into `decoded/`, run `record_imagegen_result.py`, run `derive_running_left_from_running_right.py`, run `finalize_pet_run.py`, or package the pet. This avoids manifest races and keeps provenance checks centralized.

Subagent handoff contract:

- Give each subagent exactly one row job unless you are intentionally batching adjacent simple rows.
- Include the row id, the absolute prompt file path, the full prompt text or an instruction to read that exact prompt file, and every input image path with its role label from `imagegen-jobs.json`.
- Explicitly remind the subagent that the prompt's transparency and effects rules are mandatory: no detached effects, no wave marks for `waving`, no speed lines or dust for directional running rows, no literal foot-running for the non-directional `running` row, and only attached opaque sprite-like tears/smoke/stars when allowed by the state prompt.
- Tell the subagent to inspect the generated candidate for frame count, identity consistency, clean flat chroma-key background, safe spacing, and forbidden detached effects before returning it.
- Tell the subagent to return only the selected original `$CODEX_HOME/generated_images/.../ig_*.png` source path plus a one-sentence QA note. The parent decides whether to record or repair it.

Use this template for each subagent:

```text
Generate the `<row-id>` row for this hatch-pet run.

Run dir: <absolute run dir>
Prompt file: <absolute prompt file>
Input images:
- <absolute path> — <role>
- <absolute path> — <role>

Read and follow the row prompt exactly, including the Transparency and artifact rules. Use `$imagegen` only; do not use local scripts to draw, tile, edit, or synthesize sprites.

Before returning, visually check:
- exact requested frame count
- same pet identity as the canonical base
- clean flat chroma-key background
- complete, separated, unclipped poses
- no forbidden detached effects or slot-crossing artifacts
- for `idle`, visible subtle expression or posture variation across the loop
- for `running-right` and `running-left`, correct facing direction and clear alternating legs

Do not edit manifests, copy into decoded, record results, mirror rows, finalize, repair, or package. Return only:
selected_source=/absolute/path/to/$CODEX_HOME/generated_images/.../ig_*.png
qa_note=<one sentence>
```

No silent sequential fallback: if subagents cannot be used for row-strip visual generation, stop and ask for explicit user direction before continuing without them. Only an explicit user instruction such as "do not use subagents" or "run this sequentially" authorizes a normal sequential row-generation path. The final answer must report which row jobs were delegated to subagents and which, if any, were mirrored or repaired by the parent.

## Repair Workflow

If finalization stops because row QA failed, queue targeted repair jobs:

```bash
python "$SKILL_DIR/scripts/queue_pet_repairs.py" \
  --run-dir /absolute/path/to/run
```

Then repeat the `$imagegen` generation and `record_imagegen_result.py` ingest loop for each reopened row job. Regenerate the smallest failing scope: the failed row, not the whole sheet.

For identity repairs, use the canonical base image, original references, contact sheet, and exact row failure note as grounding context. Repair only the failed row while preserving the canonical pet identity.

For playback-size popping where the generated horizontal strip itself has correct relative scale, do not regenerate images first. Re-run finalization with `--extract-method fixed-slots --allow-slot-extraction`, then re-check `qa/contact-sheet.png` and `qa/videos/`. If fixed slots clip a wide pose, repair only that row with more safe padding or a clearer row prompt.

For directional running repairs, regenerate `running-right` if it faces the wrong way or lacks alternating legs. If the repaired `running-right` is safe to mirror, derive `running-left` from it with `derive_running_left_from_running_right.py` so the left row is a per-frame mirror with the same timing order.

## Secondary Image Generation Fallback

`scripts/generate_pet_images.py` is a secondary fallback for this skill.

Use it only when the installed `$imagegen` system skill is unavailable or cannot be invoked in the current environment. Normal pet creation should delegate visual generation to `$imagegen`, because `$imagegen` owns the built-in-first image generation policy and its own CLI fallback behavior.

Run the secondary fallback only after explaining why `$imagegen` cannot be used:

```bash
python "$SKILL_DIR/scripts/generate_pet_images.py" \
  --run-dir /absolute/path/to/run \
  --model gpt-image-2 \
  --states all
```

The secondary fallback requires `OPENAI_API_KEY`.

## Rules

- Keep `$imagegen` as the primary generation layer.
- Keep reference images attached/visible for `$imagegen` whenever the chosen path supports references.
- Attach the row's `references/layout-guides/<state>.png` image to every row-strip job as a layout-only guide, and do not accept outputs that copy guide pixels.
- Use subagents for row-strip visual generation after the parent records the base image. The parent may generate the base, but row-strip jobs belong to subagents unless the user explicitly says not to use subagents for this session.
- Generate every normal visual job with `$imagegen`: base plus all row strips that are not explicitly approved `running-left` mirror derivations.
- Treat only the base job as eligible for prompt-only generation; every row job must attach its listed grounding images.
- Delegate `running-right` first, then mirror `running-left` only when visual inspection confirms a mirror preserves identity and semantics; otherwise delegate `running-left` as a normal grounded `$imagegen` row.
- Treat a `running-right` row that faces left as failed. Treat a `running-left` row that faces right as failed.
- Treat directional walking/running rows as failed if the legs do not visibly alternate across the cycle.
- When mirroring `running-left`, mirror each frame in place and preserve frame order; never reverse the temporal sequence by mirroring the whole strip incorrectly.
- Never substitute locally drawn, tiled, transformed, or code-generated row strips for missing `$imagegen` outputs.
- Never manually mutate `imagegen-jobs.json` to claim a visual job completed.
- Do not rely on generated images for exact atlas geometry; use this skill's deterministic scripts.
- Do not accept per-frame fit-to-cell extraction when it creates playback size popping. Use fixed-slot extraction for rows whose generated strips already preserve stable scale and placement.
- Use the chroma key stored in `pet_request.json`; do not force a fixed green screen.
- Keep the pet's silhouette, face, materials, palette, and props consistent across all rows.
- Enforce the transparency and effects rules above in every base, row, and repair prompt.
- Treat visual identity drift as a blocker even when `qa/review.json` and `final/validation.json` have no errors.
- Treat idle rows with near-identical frames as failed; the loop must have visible but calm micro-variation.
- Treat a contact sheet that shows cropped references, repeated tiles, white cell backgrounds, or non-sprite fragments as failed.
- Treat clipped wide poses, raised limbs, long accessories, or prop/extremity cutoffs as failed, even if fixed-slot extraction solved scale stability.
- Treat hidden transparent-pixel color residue that appears as colored blocks, stripes, or smears in preview/export as failed.
- Treat forbidden detached effects, chroma-key-adjacent artifacts, shadows, glows, smears, dust, landing marks, wave marks, speed lines, or motion trails as failed rows.
- Treat `qa/review.json` errors as blockers. Warnings require visual review.

## Acceptance Criteria

- Final atlas is PNG or WebP, `1536x1872`, transparent-capable, and based on `192x208` cells.
- Used cells are non-empty and unused cells are fully transparent.
- Atlas follows the row/frame counts in `references/animation-rows.md`.
- Contact sheet and preview videos have been produced unless explicitly skipped.
- `qa/review.json` has no errors.
- Row-by-row review confirms the animation cycles are complete enough for the Codex app.
- Preview videos show stable intended character scale and placement, with no unintended size popping from per-frame cropping.
- Directional rows face the correct way and use readable alternating gait frames.
- Idle has visible calm expression or posture variation rather than repeated copies.
- Wide poses and props are not clipped, and transparent areas render cleanly without hidden color blocks.
- `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/pet.json` and `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/spritesheet.webp` are staged together for custom pets.
