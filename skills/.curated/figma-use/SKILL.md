---
name: figma-use
description: "**MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context — e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically."
metadata:
  mcp-server: figma, figma-staging
---

# use_figma — Figma Plugin API Skill

Use `use_figma` MCP to execute JavaScript in Figma files via the Plugin API. All detailed reference docs live in `references/`.

**Always pass `skillNames: "figma-use"` when calling `use_figma`.** This is a logging parameter used to track skill usage — it does not affect execution.

**If the task involves building or updating a full page, screen, or multi-section layout in Figma from code**, also load [figma-generate-design](../figma-generate-design/SKILL.md). It provides the workflow for discovering design system components via `search_design_system`, importing them, and assembling screens incrementally. Both skills work together: this one for the API rules, that one for the screen-building workflow.

Before anything, load [plugin-api-standalone.index.md](references/plugin-api-standalone.index.md) to understand what is possible. When you are asked to write plugin API code, use this context to grep [plugin-api-standalone.d.ts](references/plugin-api-standalone.d.ts) for relevant types, methods, and properties. This is the definitive source of truth for the API surface. It is a large typings file, so do not load it all at once, grep for relevant sections as needed.

IMPORTANT: Whenever you work with design systems, start with [working-with-design-systems/wwds.md](references/working-with-design-systems/wwds.md) to understand the key concepts, processes, and guidelines for working with design systems in Figma. Then load the more specific references for components, variables, text styles, and effect styles as needed.

## 1. Critical Rules

1.  **MUST** call `figma.closePlugin()` on success and `figma.closePluginWithFailure(e.toString())` on error — NEVER use `figma.closePlugin()` in a catch block
2.  **MUST** wrap in `(async () => { try { ... } catch(e) { figma.closePluginWithFailure(e.toString()) } })()`
3.  `figma.notify()` **throws "not implemented"** — never use it
4.  `console.log()` is NOT returned — use `closePlugin()` for success output and `closePluginWithFailure()` for errors
5.  **Work incrementally in small steps.** Break large operations into multiple `use_figma` calls. Validate after each step. This is the single most important practice for avoiding bugs.
6.  Colors are **0–1 range** (not 0–255): `{r: 1, g: 0, b: 0}` = red
7.  Fills/strokes are **read-only arrays** — clone, modify, reassign
8.  Font **MUST** be loaded before any text operation: `await figma.loadFontAsync({family, style})`
9.  **Pages load incrementally** — use `await figma.setCurrentPageAsync(page)` to switch pages and load their content (see Page Rules below)
10. `setBoundVariableForPaint` returns a **NEW** paint — must capture and reassign
11. `createVariable` accepts collection **object or ID string** (object preferred)
12. **`layoutSizingHorizontal/Vertical = 'FILL'` MUST be set AFTER `parent.appendChild(child)`** — setting before append throws. Same applies to `'HUG'` on non-auto-layout nodes.
13. **Position new top-level nodes away from (0,0).** Nodes appended directly to the page default to (0,0). Scan `figma.currentPage.children` to find a clear position (e.g., to the right of the rightmost node). This only applies to page-level nodes — nodes nested inside other frames or auto-layout containers are positioned by their parent. See [Gotchas](references/gotchas.md).
14. **On `use_figma` error, STOP. Do NOT immediately retry.** Call `get_metadata` to inspect partial state and clean up orphaned nodes BEFORE retrying — failed scripts do NOT roll back; nodes created before the error line persist and will cause duplicates on retry. See [Error Recovery](#6-error-recovery--self-correction).
15. **MUST return ALL created/mutated node IDs** in the `figma.closePlugin()` response. Whenever a script creates new nodes or mutates existing ones on the canvas, collect every affected node ID and return them in a structured JSON object (e.g. `{ createdNodeIds: [...], mutatedNodeIds: [...] }`). This is essential for subsequent calls to reference, validate, or clean up those nodes.

> For detailed WRONG/CORRECT examples of each rule, see [Gotchas & Common Mistakes](references/gotchas.md).

## 2. Page Rules (Critical)

**Page context resets between `use_figma` calls** — `figma.currentPage` starts on the first page each time.

### Switching pages

Use `await figma.setCurrentPageAsync(page)` to switch pages and load their content. The sync setter `figma.currentPage = page` **throws an error** in `use_figma` runtimes.

```js
// Switch to a specific page (loads its content)
const targetPage = figma.root.children.find((p) => p.name === "My Page");
await figma.setCurrentPageAsync(targetPage);
// targetPage.children is now populated

// Iterate over all pages
for (const page of figma.root.children) {
  await figma.setCurrentPageAsync(page);
  // page.children is now loaded — read or modify them here
}
```

### Across script runs

`figma.currentPage` resets to the **first page** at the start of each `use_figma` call. If your workflow spans multiple calls and targets a non-default page, call `await figma.setCurrentPageAsync(page)` at the start of each invocation.

You can call `use_figma` multiple times to incrementally build on the file state, or to retrieve information before writing another script. For example, write a script to get metadata about existing nodes, return that data via `figma.closePlugin()`, then use it in a subsequent script to modify those nodes.

## 3. `figma.closePlugin()` Is Your Only Output Channel

The agent sees **ONLY** the string passed to `figma.closePlugin('msg')`. Everything else is invisible.

- **Returning IDs (CRITICAL)**: Every script that creates or mutates canvas nodes **MUST** return all affected node IDs — e.g. `{ createdNodeIds: [...], mutatedNodeIds: [...] }`. This is a hard requirement, not optional.
- **Progress reporting**: `figma.closePlugin(JSON.stringify({ createdNodeIds: [...], count: 5, errors: [] }))`
- **Error info**: On failure, pass structured error data
- `console.log()` output is **never** returned to the agent
- Always return actionable data (IDs, counts, status) so subsequent calls can reference created objects

## 4. Editor Mode

`use_figma` works in **design mode** (editorType `"figma"`, the default). FigJam (`"figjam"`) has a different set of available node types — most design nodes are blocked there.

Available in design mode: Rectangle, Frame, Component, Text, Ellipse, Star, Line, Vector, Polygon, BooleanOperation, Slice, Page, Section, TextPath.

**Blocked** in design mode: Sticky, Connector, ShapeWithText, CodeBlock, Slide, SlideRow, Webpage.

## 5. Incremental Workflow (How to Avoid Bugs)

The most common cause of bugs is trying to do too much in a single `use_figma` call. **Work in small steps and validate after each one.**

### The pattern

1. **Inspect first.** Before creating anything, run a read-only `use_figma` to discover what already exists in the file — pages, components, variables, naming conventions. Match what's there.
2. **Do one thing per call.** Create variables in one call, create components in the next, compose layouts in another. Don't try to build an entire screen in one script.
3. **Return IDs from every call.** Always return created node IDs, variable IDs, collection IDs via `figma.closePlugin(JSON.stringify({...}))`. You'll need these as inputs to subsequent calls.
4. **Validate after each step.** Use `get_metadata` to verify structure (counts, names, hierarchy, positions). Use `get_screenshot` after major milestones to catch visual issues.
5. **Fix before moving on.** If validation reveals a problem, fix it before proceeding to the next step. Don't build on a broken foundation.

### Suggested step order for complex tasks

```
Step 1: Inspect file — discover existing pages, components, variables, conventions
Step 2: Create tokens/variables (if needed)
       → validate with get_metadata
Step 3: Create individual components
       → validate with get_metadata + get_screenshot
Step 4: Compose layouts from component instances
       → validate with get_screenshot
Step 5: Final verification
```

### What to validate at each step

| After... | Check with `get_metadata` | Check with `get_screenshot` |
|---|---|---|
| Creating variables | Collection count, variable count, mode names | — |
| Creating components | Child count, variant names, property definitions | Variants visible, not collapsed, grid readable |
| Binding variables | Node properties reflect bindings | Colors/tokens resolved correctly |
| Composing layouts | Instance nodes have mainComponent, hierarchy correct | No cropped/clipped text, no overlapping elements, correct spacing |

## 6. Error Recovery & Self-Correction

**`use_figma` does NOT roll back on failure.** If a script fails on line 50, everything executed on lines 1–49 persists. This means partial nodes, half-created components, and orphaned elements remain in the file.

### When `use_figma` returns an error

1. **STOP.** Do not immediately fix the code and retry.
2. **Inspect partial state.** Call `get_metadata` on the parent node (page, section, or component set) to see what was partially created.
3. **If damage is unclear**, call `get_screenshot` to see the visual state.
4. **Clean up orphaned nodes** before retrying:

```js
(async () => {
  try {
    const page = figma.currentPage;
    const orphans = page.findChildren(n =>
      n.type === 'COMPONENT' && n.name.includes('variant=')
    );
    for (const orphan of orphans) orphan.remove();
    figma.closePlugin('Cleaned up ' + orphans.length + ' orphaned nodes');
  } catch(e) { figma.closePluginWithFailure(e.toString()); }
})()
```

5. **Fix the script** based on what you learned from inspection.
6. **Retry** only after cleanup is confirmed.

### Common self-correction patterns

| Error message | Likely cause | How to fix |
|---|---|---|
| `"not implemented"` | Used `figma.notify()` | Replace with `figma.closePlugin()` |
| `"node must be an auto-layout frame..."` | Set `FILL`/`HUG` before appending to auto-layout parent | Move `appendChild` before `layoutSizingX = 'FILL'` |
| `"Setting figma.currentPage is not supported"` | Used sync page setter | Use `await figma.setCurrentPageAsync(page)` |
| Property value out of range | Color channel > 1 (used 0–255 instead of 0–1) | Divide by 255 |
| `"Cannot read properties of null"` | Node doesn't exist (wrong ID, wrong page) | Check page context, verify ID |
| Script hangs / no response | Missing `figma.closePlugin()` / `figma.closePluginWithFailure()` on some code path | Add closePlugin/closePluginWithFailure to all paths |
| Duplicate nodes after retry | Retried without cleaning up partial state | Inspect with `get_metadata`, clean up first |
| `"The node with id X does not exist"` | Parent instance was implicitly detached by a child `detachInstance()`, changing IDs | Re-discover nodes by traversal from a stable (non-instance) parent frame |

### When the script succeeds but the result looks wrong

1. Call `get_metadata` to check structural correctness (hierarchy, counts, positions).
2. Call `get_screenshot` to check visual correctness. Look closely for cropped/clipped text (line heights cutting off content) and overlapping elements — these are common and easy to miss.
3. Identify the discrepancy — is it structural (wrong hierarchy, missing nodes) or visual (wrong colors, broken layout, clipped content)?
4. Write a targeted fix script that modifies only the broken parts — don't recreate everything.

> For the full validation workflow, see [Validation & Error Recovery](references/validation-and-recovery.md).

## 7. Pre-Flight Checklist

Before submitting ANY `use_figma` call, verify:

- [ ] Script is wrapped in `(async () => { try/catch })()` pattern
- [ ] `figma.closePlugin()` called on success path, `figma.closePluginWithFailure(e.toString())` in catch block
- [ ] `figma.closePlugin()` returns structured JSON with actionable data (IDs, counts)
- [ ] NO usage of `figma.notify()` anywhere
- [ ] NO usage of `console.log()` as output (only closePlugin / closePluginWithFailure)
- [ ] All colors use 0–1 range (not 0–255)
- [ ] Fills/strokes are reassigned as new arrays (not mutated in place)
- [ ] Page switches use `await figma.setCurrentPageAsync(page)` (sync setter throws)
- [ ] `layoutSizingVertical/Horizontal = 'FILL'` is set AFTER `parent.appendChild(child)`
- [ ] `loadFontAsync()` called BEFORE any text property changes
- [ ] `lineHeight`/`letterSpacing` use `{unit, value}` format (not bare numbers)
- [ ] `resize()` is called BEFORE setting sizing modes (resize resets them to FIXED)
- [ ] For multi-step workflows: IDs from previous calls are passed as string literals (not variables)
- [ ] New top-level nodes are positioned away from (0,0) to avoid overlapping existing content
- [ ] ALL created/mutated node IDs are collected and returned in `figma.closePlugin()` response

## 8. Discover Conventions Before Creating

**Always inspect the Figma file before creating anything.** Different files use different naming conventions, variable structures, and component patterns. Your code should match what's already there, not impose new conventions.

When in doubt about any convention (naming, scoping, structure), check the Figma file first, then the user's codebase. Only fall back to common patterns when neither exists.

### Quick inspection scripts

**List all pages and top-level nodes:**
```js
const pages = figma.root.children.map(p => `${p.name} id=${p.id} children=${p.children.length}`);
figma.closePlugin(pages.join('\n'));
```

**List existing components across all pages:**
```js
const results = [];
for (const page of figma.root.children) {
  await figma.setCurrentPageAsync(page);
  page.findAll(n => {
    if (n.type === 'COMPONENT' || n.type === 'COMPONENT_SET')
      results.push(`[${page.name}] ${n.name} (${n.type}) id=${n.id}`);
    return false;
  });
}
figma.closePlugin(results.join('\n'));
```

**List existing variable collections and their conventions:**
```js
const collections = figma.variables.getLocalVariableCollections();
const results = collections.map(c => ({
  name: c.name, id: c.id,
  varCount: c.variableIds.length,
  modes: c.modes.map(m => m.name)
}));
figma.closePlugin(JSON.stringify(results));
```

## 9. Reference Docs

Load these as needed based on what your task involves:

| Doc | When to load | What it covers |
|-----|-------------|----------------|
| [gotchas.md](references/gotchas.md) | Before any `use_figma` | Every known pitfall with WRONG/CORRECT code examples |
| [common-patterns.md](references/common-patterns.md) | Need working code examples | Script scaffolds: shapes, text, auto-layout, variables, components, multi-step workflows |
| [plugin-api-patterns.md](references/plugin-api-patterns.md) | Creating/editing nodes | Fills, strokes, Auto Layout, effects, grouping, cloning, styles |
| [api-reference.md](references/api-reference.md) | Need exact API surface | Node creation, variables API, core properties, what works and what doesn't |
| [validation-and-recovery.md](references/validation-and-recovery.md) | Multi-step writes or error recovery | `get_metadata` vs `get_screenshot` workflow, mandatory error recovery steps |
| [component-patterns.md](references/component-patterns.md) | Creating components/variants | combineAsVariants, component properties, INSTANCE_SWAP, variant layout, discovering existing components, metadata traversal |
| [variable-patterns.md](references/variable-patterns.md) | Creating/binding variables | Collections, modes, scopes, aliasing, binding patterns, discovering existing variables |
| [text-style-patterns.md](references/text-style-patterns.md) | Creating/applying text styles | Type ramps, font probing, listing styles, applying styles to nodes |
| [effect-style-patterns.md](references/effect-style-patterns.md) | Creating/applying effect styles | Drop shadows, listing styles, applying styles to nodes |
| [plugin-api-standalone.index.md](references/plugin-api-standalone.index.md) | Need to understand the full API surface | Index of all types, methods, and properties in the Plugin API |
| [plugin-api-standalone.d.ts](references/plugin-api-standalone.d.ts) | Need exact type signatures | Full typings file — grep for specific symbols, don't load all at once |

## 10. Snippet examples

You will see snippets throughout documentation here. These snippets contain useful plugin API code that can be repurposed. Use them as is, or as starter code as you go. If there are key concepts that are best documented as generic snippets, call them out and write to disk so you can reuse in the future.
