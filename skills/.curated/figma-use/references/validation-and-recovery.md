# Validation Workflow & Error Recovery

> Part of the [use_figma skill](../SKILL.md). How to debug, validate, and recover from errors.

## Contents

- `get_metadata` vs `get_screenshot`
- Error Recovery After Failed `use_figma`
- Cleanup Pattern
- Recommended Workflow


## `get_metadata` vs `get_screenshot`

After each `use_figma` call, validate results using the right tool for the job. Do NOT reach for `get_screenshot` every time — it is expensive and should be reserved for visual checks.

### `get_metadata` — Use for intermediate validation (preferred)

`get_metadata` returns an XML tree of node IDs, types, names, positions, and sizes. Use it to confirm:

- **Structure & hierarchy**: correct parent-child relationships, component nesting, section contents
- **Node counts**: expected number of variants created, children present
- **Naming**: variant property names follow the `property=value` convention
- **Positioning & alignment**: x/y coordinates, width/height values match expectations
- **Layout properties**: auto-layout direction, sizing mode, padding, spacing
- **Component set membership**: all expected variants are inside the ComponentSet

```
Example: After creating a ComponentSet with 120 variants, call get_metadata on the
ComponentSet node to verify all 120 children exist with correct names, sizes, and positions
— without waiting for a full render.
```

**When to use `get_metadata`:**
- After creating/modifying nodes — to verify structure, counts, and names
- After layout operations — to verify positions and dimensions
- After combining variants — to confirm all components are in the ComponentSet
- After binding variables — to verify node properties (use use_figma to read bound variables if needed)
- Between multi-step workflows — to confirm step N succeeded before starting step N+1

### `get_screenshot` — Use after each major creation milestone

`get_screenshot` renders a pixel-accurate image. It is the only way to verify visual correctness (colors, typography rendering, effects, variable mode resolution). It is slower and produces large responses, so don't call it after every single `use_figma` — but do call it after each major milestone to catch visual problems early.

**When to use `get_screenshot`:**
- **After creating a component set** — verify variants look correct, grid is readable, nothing is collapsed or overlapping
- **After composing a layout** — verify overall structure and spacing
- **After binding variables/modes** — verify colors and tokens resolved correctly
- **After any fix or recovery** — verify the fix didn't introduce new visual issues
- **Before reporting results to the user** — final visual proof

**What to look for in screenshots** — these are the most commonly missed issues:
- **Cropped/clipped text** — line heights or frame sizing cutting off descenders, ascenders, or entire lines
- **Overlapping content** — elements stacking on top of each other due to incorrect sizing or missing auto-layout
- **Placeholder text** still showing ("Title", "Heading", "Button") instead of actual content

## CRITICAL: Error Recovery After Failed `use_figma`

> **THIS IS NOT OPTIONAL.** Every `use_figma` error MUST trigger the recovery steps below. Skipping these steps leaves orphaned nodes in the file that will cause duplicates and inconsistencies on retry.

**Scripts can partially execute before hitting an error.** A failed `use_figma` does NOT roll back — nodes created before the error line persist in the file. This leaves the file in an **inconsistent, partially-modified state**.

**Mandatory recovery steps when `use_figma` returns an error (DO NOT SKIP):**
1. **STOP — do NOT immediately fix the code and retry.** The file has partial state that must be inspected first.
2. **Immediately call `get_metadata`** on the parent node (section, page, or ComponentSet) to see what was partially created.
3. **If `get_metadata` doesn't make the damage clear** (e.g. positions look fine but visual state is uncertain), call `get_screenshot` to assess visual damage.
4. **Write a cleanup script** to remove orphaned/incomplete nodes before retrying. Use `page.findChildren()` to locate stray nodes.
5. **Only after cleanup is confirmed**, fix the original script and retry.
6. **Never retry the failed script blindly** — the partial state means a retry will create duplicates or hit new errors.

```
Example: A script creating 8 components fails on component #5.
Components 1-4 exist on the page. A naive retry creates components 1-8 again,
leaving 12 components total (4 orphaned duplicates). Always clean up first.
```

### Cleanup Pattern

```js
// Cleanup pattern: find and remove orphaned nodes from a failed run
(async () => {
  try {
    const page = figma.currentPage;
    // Find orphaned components that weren't combined into a ComponentSet
    const orphans = page.findChildren(n =>
      n.type === 'COMPONENT' && n.name.includes('variant=')
    );
    for (const orphan of orphans) orphan.remove();
    figma.closePlugin('Cleaned up ' + orphans.length + ' orphaned nodes');
  } catch(e) { figma.closePluginWithFailure(e.toString()); }
})()
```

## Recommended Workflow

```
1. use_figma  →  Create/modify nodes
2. get_metadata     →  Verify structure, counts, names, positions (fast, cheap)
3. use_figma  →  Fix any structural issues found
4. get_metadata     →  Re-verify fixes
5. ... repeat as needed ...
6. get_screenshot   →  Visual check after each major milestone

⚠️ ON ERROR at any step:
   a. get_metadata    →  Inspect partial state (always do this first)
   b. get_screenshot  →  Only if metadata doesn't make the damage clear
   c. use_figma →  Clean up orphaned/incomplete nodes
   d. THEN retry the failed operation
```
