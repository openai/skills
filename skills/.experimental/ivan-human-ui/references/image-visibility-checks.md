# Image Visibility Checks

Run this checklist whenever logos, testimonials, or generated images are part of the page.

## Required Visual Tracks

When testimonial/background variants are requested, ensure all three tracks exist and render:

1. animal
2. abstract
3. business

## Verification Steps

1. Confirm each file exists in the expected folder (`public/...` or equivalent).
2. Confirm extension and case match the actual file (`.jpg` vs `.jpeg`, letter case).
3. Confirm image path in code is correct and not stale after rename.
4. Confirm no CSS makes assets invisible (`opacity: 0`, zero height, covered layers).
5. Confirm layout does not clip image to zero visible area.
6. Confirm all three tracks render in browser at runtime.

## Fix Protocol For "Two Not Showing"

If two assets fail to display:

1. Recheck filename and path casing first.
2. Re-export missing files to consistent dimensions and format.
3. Replace temporary remote URLs with local stable files.
4. Rebuild/reload and verify again in page.
5. Keep fallback placeholders only until local files render successfully.

Do not hand off until the three-track visibility check passes.
