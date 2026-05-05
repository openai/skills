---
name: "codex-pet-generator"
description: "Create Codex desktop pets from character references by defining row semantics, generating tiny-UI-readable loops, approving or rejecting rows, following slicing guidance, packing a 1536x1872 spritesheet with the bundled packer, validating it, and installing under ~/.codex/pets."
license: "MIT"
---

# Codex Pet Generator

Use this skill when the user wants to create, revise, validate, package, or install a custom Codex desktop pet.

## Core Principles

- Animation direction first, image generation second, deterministic packing third.
- Optimize for tiny UI readability, not for how pretty a large strip looks in isolation.
- Treat each row as one loopable state machine, not eight poster poses.
- Keep canon anchors: one approved scale reference, one seated-body reference, one standing-body reference, and one prop-language reference.
- Every generated row must be marked `approved` or `unapproved` before it can advance.

## Codex Format

Custom pets live at:

```text
~/.codex/pets/<pet-id>/
  pet.json
  spritesheet.png|webp
```

Required spritesheet:

- `1536x1872`
- `8x9` grid
- `192x208` per frame
- transparent final background
- PNG or WebP

Required `pet.json`:

```json
{
  "id": "<pet-id>",
  "displayName": "<Display Name>",
  "description": "<one-line description>",
  "spritesheetPath": "spritesheet.webp"
}
```

`spritesheetPath` is resolved relative to the `pet.json` file. Use the same `<pet-id>` as the parent directory name.

Row order is fixed:

1. `idle`
2. `running-right`
3. `running-left`
4. `waving`
5. `jumping`
6. `failed`
7. `waiting`
8. `running`
9. `review`

For row-by-row semantics, common failure modes, and tiny-UI design guidance, read [references/row-semantics.md](references/row-semantics.md) before prompting.

## Workflow

1. Gather references and write a character bible in plain language.
2. Define all 9 row semantics before generating anything.
3. Pick canon anchors:
   - one approved overall scale reference
   - one approved seated reference
   - one approved standing reference
   - one approved prop-language reference
4. Generate one row strip at a time, or individual frames. Do not generate a full 72-frame sheet as the final asset.
5. Review each row with the acceptance ladder in [references/acceptance-checklist.md](references/acceptance-checklist.md).
6. Mark every candidate `approved` or `unapproved`. Only approved rows advance.
7. Extract individual frames into per-row directories. The skill provides written slicing guidance in [references/packing-and-slicing.md](references/packing-and-slicing.md), but the actual extraction is manual — either export frames directly from the generator, or cut strips with your image tool of choice. The bundled packer assumes per-frame inputs and does not slice strips for you.
8. Pack with `scripts/pack_codex_pet.py`.
9. Validate with `scripts/validate_codex_pet.py`.
10. Install into `~/.codex/pets/<pet-id>`.
11. When iterating in the Codex UI, use a new pet id such as `<pet-id>-v2` to avoid cached spritesheets.

## Prompting Rules

Prompts should explicitly state:

- one row equals one loopable action
- frame `8` must hand off cleanly to frame `1`
- frames are sequential animation states, not unrelated poster poses
- same character, same camera, same scale across the row
- exactly two arms and exactly two legs
- no cropped body parts
- no props outside the row-specific action
- final target is a tiny desktop pet sprite, so readability beats nuance

If a row is hard to read:

- do not merely “polish” it
- redesign the motion around bolder state changes
- prefer binary readable mechanics such as `open/closed`, `upright/flat`, `connect/fail`, `tension/release`, or `in/out`

High-risk guidance:

- Standing rows are high-risk for vertical stretch. Always anchor them to an approved compact standing canon.
- Directional rows often collapse into generic running. Reject them if the intended action semantics vanish.
- Gestures often fail when they rely on finger nuance alone. If needed, redesign them into chunkier hand states.
- Failure rows often become generic sadness. Prefer unmistakable failure silhouettes or prop logic.
- Jump rows often become athletic. Heavy toy-like characters usually need compression, shock, or flop logic instead.

## Background and Alpha Rules

- Prefer generating with a removable flat background when possible.
- If you need chroma key, use flat `#00ff00`, no shadows, no gradients, and no green on the character.
- Remove the background locally before packing.
- Zero the RGB channels of fully transparent pixels before final install artifacts if your cleanup leaves preview garbage.

## Approval Gate

Do not carry ambiguous rows forward.

- `approved`: chosen final candidate for that row
- `unapproved`: rejected, superseded, or still exploratory

Only approved rows should be sliced, packed, validated, and installed.

The acceptance ladder and rejection patterns live in [references/acceptance-checklist.md](references/acceptance-checklist.md).

## Slicing and Packing Rules

Slicing is **manual** — the skill provides guidance, not an automated slicer. The packer takes per-frame inputs and assembles them into the final sheet using one uniform scale per row.

- Do not assume a generated row strip is cut into 8 equal visual columns.
- Do not slice approved strips into equal widths unless the spacing is known to be uniform.
- Prefer per-frame export or gap-aware manual slicing based on real empty space between poses.
- The packer uses one scale per row, not one scale per frame.
- Keep at least `8-12px` of padding from cell edges (packer default is `10`, hard cap is half-cell-minus-one).
- Keep exactly one directory per row index inside the rows root. Multiple matching directories (`01-idle-explore`, `01-idle-final`) cause the packer to abort instead of silently picking one — this protects the approval gate.

See [references/packing-and-slicing.md](references/packing-and-slicing.md) for manual slicing workflow guidance.

## Bundled Scripts

Pack approved rows into a final sheet:

```bash
python scripts/pack_codex_pet.py <rows-root> <output.webp>
```

Validate the final sheet:

```bash
python scripts/validate_codex_pet.py <spritesheet.webp>
```

If `pet.json` sits next to the spritesheet, the validator picks it up automatically and checks the install contract (`id`, `displayName`, `description`, `spritesheetPath`). To validate against a `pet.json` in a different location use `--pet-json <path>`. To skip pet.json entirely use `--no-pet-json`.

Both scripts require `Pillow`. Install with `pip install -r requirements.txt`. Run from the bundle root, or use absolute paths.

Interpretation rule:

- validator `errors` are hard blockers — wrong dimensions, empty frames, missing alpha, fully-opaque sheet, malformed `pet.json`
- validator `warnings` still require visual review — fully-opaque single frame, edge contact, width/height drift, `spritesheetPath` mismatch
- width or height drift warnings may reflect real performance changes, but edge-contact warnings usually mean crop risk

## Install Notes

- Install final assets under `~/.codex/pets/<pet-id>/`
- Keep `pet.json` and the spritesheet in the same folder
- Prefer a new id when testing revisions in the UI

If the UI looks broken, first suspect:

- bad row semantics
- bad slicing
- bad alpha cleanup
- bad packing

Do not assume the generator is the only failure point.
