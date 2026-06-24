# Packing and Slicing

Use this file before extracting frames from approved strips and before building the final spritesheet.

## The Main Rule

Do not assume a generated strip is safely sliceable into 8 equal columns.

Many good-looking row strips still fail at packing because:

- spacing between poses is uneven
- limbs or props cross the visual midpoint between frames
- the background is still opaque white when the packer expects alpha

## Preferred Extraction Order

1. Best: export individual frames directly
2. Good: slice a strip using known uniform geometry
3. Acceptable: gap-aware slicing using real empty space between poses
4. Avoid: blind equal-width slicing of a strip with uneven spacing

## Before Slicing

- remove the background so alpha is real
- confirm that empty space between characters is actually empty
- inspect the strip for legs, hands, cables, hair, or props near likely cut lines

If the source background is white:

- remove only border-connected white background
- do not key out interior whites that belong to the design

## Gap-Aware Slicing

When a strip is not uniform:

- inspect the alpha or occupancy per x-column
- look for local valleys near expected frame boundaries
- cut on real gaps, not on equal fractions alone

This is especially important for:

- directional rows with stretched limbs
- rows with long cables or tools
- flop or jump rows with large pose width changes

## Transparent Pixel Cleanup

After background removal:

- zero RGB in fully transparent pixels if preview garbage remains

This does not change the visible sprite, but it prevents ugly viewer artifacts in some previews.

## Packing Rules

When building the final `1536x1872` sheet:

- keep frames in fixed `192x208` cells
- use one scale per row, not per frame
- use one baseline per row
- keep `8-12px` of padding from the cell edge

Do not “solve” bad anatomy or bad slicing by shrinking everything until it fits.

## Validator Interpretation

Run the validator after packing.

Hard blockers (errors):

- wrong sheet dimensions
- empty frame
- spritesheet has no transparent pixels (background was not removed)
- malformed `pet.json` — missing required fields, wrong types, absolute or traversing `spritesheetPath`

Warnings that still need visual review:

- a single frame is fully opaque
- edge contact
- high row width drift
- high row height drift
- `spritesheetPath` in `pet.json` does not match the sheet under validation
- `id` in `pet.json` differs from the parent directory name

Interpretation:

- edge contact usually means crop risk
- width/height drift can be acceptable if the action truly changes shape, but still needs visual confirmation
- a fully-opaque frame is almost always a missing alpha-cleanup step, not a creative choice

## Install Discipline

Only install:

- approved rows
- correctly sliced frames
- validated final sheet

If the installed pet looks broken, suspect slicing before suspecting Codex.
