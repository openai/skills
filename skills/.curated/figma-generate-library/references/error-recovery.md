> Part of the [figma-generate-library skill](../SKILL.md).

# Error Recovery Reference

Protocol for handling failures, partial state, and incomplete runs across a 20–100+ call design system build.

---

## 1. Core Protocol: STOP → Inspect → Identify → Clean → Fix → Retry

**Never retry a failed script without cleanup first.** A failed script may have created partial state — frames, components, or variables that are half-built. Retrying on top of partial state compounds the problem and can make recovery impossible.

The mandatory recovery sequence:

```
1. STOP   — Do not run any more use_figma writes.
2. INSPECT — Call get_metadata on the current page. Optionally call get_screenshot.
3. IDENTIFY — Find artifacts from the failed attempt using dsb_run_id pluginData tags.
4. CLEAN   — Run a targeted cleanup script to remove orphaned nodes (pluginData-based, never name-based).
5. VERIFY  — Run get_metadata again to confirm cleanup was complete.
6. FIX     — Correct the script that failed.
7. RETRY   — Re-run the corrected script from the last clean checkpoint.
8. PERSIST — Update the state ledger with the outcome.
```

Do not skip step 4 even if the failure seems minor. Partial frames and components accumulate and cause confusing results in later steps.

---

## 2. `pluginData`-Based Cleanup: Why Name Matching is Dangerous

### Why name-prefix matching fails

A cleanup script that deletes "all nodes whose name starts with `Button`" will also delete nodes the user may have created manually with that name, or nodes from a previous approved phase. Name-based cleanup has no way to distinguish "orphan from a failed attempt" from "intentional user node."

Furthermore, variant names (`Size=Medium, Style=Primary, State=Default`) do not have consistent prefixes that are safe to target without also hitting legitimate nodes.

### How `setPluginData` / `getPluginData` works

`pluginData` is a key-value store attached to individual nodes. It persists across sessions and is invisible to the user in the Figma UI. Only plugins with the same `pluginId` can read/write data scoped to that plugin. Use three keys:

```javascript
node.setPluginData('dsb_run_id', 'ds-build-2024-001'); // identifies the build run
node.setPluginData('dsb_phase',  'phase3');             // which phase created this node
node.setPluginData('dsb_key',    'componentset/button');// unique logical key

// Reading:
const runId = node.getPluginData('dsb_run_id'); // returns '' if never set
const key   = node.getPluginData('dsb_key');
```

`getPluginData` returns `''` (empty string, not null) for unset keys. Always check for `!== ''`.

**Tag every created node immediately after creation** — before any further operations that might fail. If a failure happens between `createComponent()` and the tagging line, the node will be an untagged orphan. To minimize this window, tag in the same statement sequence as creation:

```javascript
const comp = figma.createComponent();
comp.setPluginData('dsb_run_id', RUN_ID);  // tag immediately
comp.setPluginData('dsb_key', key);         // tag immediately
// ... then do the rest of the setup
```

### Complete `cleanupOrphans` script using `dsb_run_id`

This script finds all nodes tagged with a given `dsb_run_id` and optionally a `dsb_phase` filter, then removes them. Run it on the specific page where the failure occurred.

```javascript
(async () => {
  try {
    const TARGET_RUN_ID = 'ds-build-2024-001'; // run ID to clean
    const TARGET_PHASE  = 'phase3';            // optionally filter by phase ('' = all phases)
    const PAGE_NAME     = 'Button';            // page to clean (or null for all pages)

    const pagesToSearch = PAGE_NAME
      ? [figma.root.children.find(p => p.name === PAGE_NAME)].filter(Boolean)
      : figma.root.children;

    const removed = [];
    const skipped = [];

    for (const page of pagesToSearch) {
      await figma.setCurrentPageAsync(page);

      const orphans = page.findAll(node => {
        const runId = node.getPluginData('dsb_run_id');
        if (runId !== TARGET_RUN_ID) return false;
        if (TARGET_PHASE && node.getPluginData('dsb_phase') !== TARGET_PHASE) return false;
        return true;
      });

      // Remove leaf-first to avoid removing parents before children
      // Sort by depth (deepest first) to avoid double-remove errors
      const sorted = orphans.slice().sort((a, b) => {
        let depthA = 0, depthB = 0;
        let n = a; while (n.parent) { depthA++; n = n.parent; }
        n = b; while (n.parent) { depthB++; n = n.parent; }
        return depthB - depthA;
      });

      for (const node of sorted) {
        try {
          if (node.removed) continue; // already removed (was a child of removed parent)
          node.remove();
          removed.push({ id: node.id, name: node.name, key: node.getPluginData('dsb_key') });
        } catch (e) {
          skipped.push({ id: node.id, name: node.name, error: e.message });
        }
      }
    }

    figma.closePlugin(JSON.stringify({ removed: removed.length, skipped: skipped.length, details: removed }));
  } catch (e) { figma.closePluginWithFailure(e.toString()); }
})();
```

After running cleanup, call `get_metadata` on the target page to confirm the orphaned nodes are gone before retrying.

---

## 3. Idempotency Patterns: Check-Before-Create

Run an idempotency check at the start of every create operation. If the entity already exists (tagged with the expected `dsb_key`), skip creation and return the existing ID.

### Check-before-create for a variable collection

```javascript
(async () => {
  try {
    const KEY = 'collection/color';
    const RUN_ID = 'ds-build-2024-001';
    const COLLECTION_NAME = 'Color';

    // Check: does a collection tagged with this key already exist?
    const allCollections = await figma.variables.getLocalVariableCollectionsAsync();
    // Variables/collections support pluginData too — check by name as fallback
    // Note: VariableCollection pluginData is set via collection.setPluginData(...)
    const existing = allCollections.find(c =>
      c.getPluginData('dsb_key') === KEY
    );

    if (existing) {
      figma.closePlugin(JSON.stringify({
        collectionId: existing.id,
        modeIds: existing.modes.map(m => ({ name: m.name, id: m.modeId })),
        alreadyExisted: true,
      }));
      return;
    }

    // Create fresh
    const collection = figma.variables.createVariableCollection(COLLECTION_NAME);
    collection.setPluginData('dsb_run_id', RUN_ID);
    collection.setPluginData('dsb_key', KEY);

    // Rename default mode, add second mode
    collection.renameMode(collection.modes[0].modeId, 'Light');
    const darkModeId = collection.addMode('Dark');

    figma.closePlugin(JSON.stringify({
      collectionId: collection.id,
      modeIds: [
        { name: 'Light', id: collection.modes[0].modeId },
        { name: 'Dark',  id: darkModeId },
      ],
    }));
  } catch (e) { figma.closePluginWithFailure(e.toString()); }
})();
```

### Check-before-create for a page

```javascript
(async () => {
  try {
    const KEY = 'page/button';
    const PAGE_NAME = 'Button';
    const RUN_ID = 'ds-build-2024-001';

    // Check by pluginData key first, then by name as fallback
    let page = figma.root.children.find(p => p.getPluginData('dsb_key') === KEY);
    if (!page) {
      page = figma.root.children.find(p => p.name === PAGE_NAME);
    }

    if (page) {
      // Ensure it's tagged if it was found by name only
      if (!page.getPluginData('dsb_key')) {
        page.setPluginData('dsb_run_id', RUN_ID);
        page.setPluginData('dsb_key', KEY);
      }
      figma.closePlugin(JSON.stringify({ pageId: page.id, alreadyExisted: true }));
      return;
    }

    page = figma.createPage();
    page.name = PAGE_NAME;
    page.setPluginData('dsb_run_id', RUN_ID);
    page.setPluginData('dsb_key', KEY);

    figma.closePlugin(JSON.stringify({ pageId: page.id, alreadyExisted: false }));
  } catch (e) { figma.closePluginWithFailure(e.toString()); }
})();
```

### Check-before-create for a component set

```javascript
(async () => {
  try {
    const KEY = 'componentset/button';
    const PAGE_ID = 'PAGE_ID_FROM_STATE';
    const RUN_ID = 'ds-build-2024-001';

    const page = await figma.getNodeByIdAsync(PAGE_ID);
    await figma.setCurrentPageAsync(page);

    const existing = page.findAll(n =>
      n.type === 'COMPONENT_SET' && n.getPluginData('dsb_key') === KEY
    );

    if (existing.length > 0) {
      figma.closePlugin(JSON.stringify({
        componentSetId: existing[0].id,
        alreadyExisted: true,
      }));
      return;
    }

    // ... proceed with creation
    figma.closePlugin(JSON.stringify({ componentSetId: null, alreadyExisted: false }));
  } catch (e) { figma.closePluginWithFailure(e.toString()); }
})();
```

---

## 4. State Ledger

### JSON Schema

Maintain a state ledger in your context (not in the Figma file) across calls. This is your source of truth for node IDs, completed steps, and pending validations.

```json
{
  "runId": "ds-build-2024-001",
  "phase": "phase3",
  "step": "component-button/combine-variants",
  "completedSteps": [
    "phase0",
    "phase1/collections",
    "phase1/primitives",
    "phase1/semantics",
    "phase2/pages",
    "phase2/foundations-docs",
    "phase3/component-avatar",
    "phase3/component-icon"
  ],
  "entities": {
    "collections": {
      "primitives": "VariableCollectionId:1234:5678",
      "color":      "VariableCollectionId:1234:5679",
      "spacing":    "VariableCollectionId:1234:5680"
    },
    "variables": {
      "color/bg/primary":         "VariableId:2345:1",
      "color/bg/secondary":       "VariableId:2345:2",
      "color/bg/disabled":        "VariableId:2345:3",
      "color/text/on-primary":    "VariableId:2345:4",
      "color/text/on-secondary":  "VariableId:2345:5",
      "color/text/disabled":      "VariableId:2345:6",
      "spacing/sm":               "VariableId:2345:7",
      "spacing/md":               "VariableId:2345:8",
      "spacing/lg":               "VariableId:2345:9",
      "radius/md":                "VariableId:2345:10"
    },
    "modes": {
      "color/light": "2345:1",
      "color/dark":  "2345:2"
    },
    "pages": {
      "Cover":       "0:1",
      "Foundations": "0:2",
      "Button":      "0:3"
    },
    "components": {
      "Icon":        "3456:1",
      "Avatar":      "3456:2",
      "Button":      "3456:3"
    },
    "componentSets": {
      "Button": "4567:1"
    }
  },
  "pendingValidations": [
    "Button:metadata",
    "Button:screenshot"
  ],
  "userCheckpoints": {
    "phase0": "approved-2024-01-15",
    "phase1": "approved-2024-01-15",
    "phase2": "approved-2024-01-15",
    "component-avatar": "approved-2024-01-15"
  }
}
```

### Persisting between calls

After every successful `use_figma` call:
1. Extract all IDs from the `closePlugin` return value
2. Add them to the appropriate `entities` section of the ledger
3. Add the completed step to `completedSteps`
4. Remove from `pendingValidations` if this call validated something
5. Update `phase` and `step` to the current position

### Rehydrating at session start

If a conversation is interrupted and resumed, read the state ledger and verify key entities still exist:

```javascript
(async () => {
  try {
    // Verify that critical nodes from the ledger still exist
    const toVerify = {
      'color-collection':  'VariableCollectionId:1234:5679',
      'button-page':       '0:3',
      'button-componentset': '4567:1',
    };

    const results = {};
    for (const [label, id] of Object.entries(toVerify)) {
      const node = await figma.getNodeByIdAsync(id)
        .catch(() => null);
      results[label] = node ? { found: true, name: node.name } : { found: false };
    }

    figma.closePlugin(JSON.stringify(results));
  } catch (e) { figma.closePluginWithFailure(e.toString()); }
})();
```

If any entity is missing, treat the phase that created it as incomplete and re-run from that checkpoint.

---

## 5. Resume Protocol

### Step 1: Inspect the file for `dsb_run_id` tags

```javascript
(async () => {
  try {
    const TARGET_RUN_ID = 'ds-build-2024-001';
    const inventory = { pages: [], variables: [], componentSets: [], frames: [] };

    // Scan pages
    for (const page of figma.root.children) {
      if (page.getPluginData('dsb_run_id') === TARGET_RUN_ID) {
        inventory.pages.push({ id: page.id, name: page.name, key: page.getPluginData('dsb_key') });
      }
    }

    // Scan variables
    const allVars = await figma.variables.getLocalVariablesAsync();
    for (const v of allVars) {
      if (v.getPluginData('dsb_run_id') === TARGET_RUN_ID) {
        inventory.variables.push({ id: v.id, name: v.name, key: v.getPluginData('dsb_key') });
      }
    }

    // Scan all component sets and frames on each page
    for (const page of figma.root.children) {
      await figma.setCurrentPageAsync(page);
      const nodes = page.findAll(n => n.getPluginData('dsb_run_id') === TARGET_RUN_ID);
      for (const n of nodes) {
        if (n.type === 'COMPONENT_SET') {
          inventory.componentSets.push({ id: n.id, name: n.name, key: n.getPluginData('dsb_key') });
        } else if (n.type === 'FRAME') {
          inventory.frames.push({ id: n.id, name: n.name, key: n.getPluginData('dsb_key') });
        }
      }
    }

    figma.closePlugin(JSON.stringify(inventory));
  } catch (e) { figma.closePluginWithFailure(e.toString()); }
})();
```

### Step 2: Reconstruct state from inventory

Map the inventory keys back to the state ledger schema. For each entity found with a `dsb_key`, add its ID to the appropriate section. Mark the corresponding step as `completedSteps`.

Example mapping:
```
key: 'collection/color'        → entities.collections.color
key: 'variable/color/bg/primary' → entities.variables['color/bg/primary']
key: 'page/button'             → entities.pages.Button
key: 'componentset/button'     → entities.componentSets.Button
```

### Step 3: Identify the resume point

The resume point is the first step in the workflow that is NOT in `completedSteps`. If the inventory shows the Button component set exists but the pending validations list shows `'Button:screenshot'`, the resume point is the screenshot validation call, not re-creation.

Use the checkpoint table from the workflow to determine which phase to continue from:

```
Phase 0 complete: all planned pages listed in entities.pages
Phase 1 complete: all planned variables listed in entities.variables with correct scopes
Phase 2 complete: all structural pages + foundations doc frames present
Phase 3 complete (per component): componentSet exists + no pending validations + user checkpoint recorded
```

---

## 6. Failure Taxonomy

### Recoverable Errors

These can be fixed and retried without affecting already-created entities:

| Category | Examples | Recovery |
|---|---|---|
| Layout errors | Variants stacked at (0,0), wrong padding values | Re-run the positioning step only |
| Naming issues | Typo in variant name, wrong casing | Find nodes by `dsb_key`, update `name` property |
| Missing property wiring | `componentPropertyReferences` not set | Find component set by ID, re-run the property wiring step |
| Variable binding omission | A fill was hardcoded instead of bound | Find nodes by `dsb_key`, re-bind the fill |
| Wrong variable bound | Bound to wrong variable ID | Re-bind with correct variable ID |
| Text not visible | Font not loaded before text write | Re-run text creation with `loadFontAsync` first |
| Partial variant creation | Only 12 of 18 variants created before timeout | Run cleanup for the partial set, re-run full variant creation |

### Structural Corruption (Requires Rollback or Restart)

These errors leave the file in a state where continuing forward is unreliable:

| Category | Examples | Recovery |
|---|---|---|
| Component cycle | A component instance was accidentally nested inside itself | Full cleanup of the affected component, restart that component from Call 1 |
| combineAsVariants with non-components | Mixed node types passed to combineAsVariants, causing unexpected merges | Remove the malformed component set, re-run from variant creation |
| Variable collection ID drift | Collection was deleted and re-created, old IDs in state ledger are stale | Re-run Phase 1 completely; update all IDs in state ledger |
| Page deletion | A page was deleted after component sets were created on it | Treat as Phase 2 incomplete; re-create the page + re-run affected component creations |
| Mode limit exceeded | `addMode` threw because the plan is Starter or Professional | Redesign variable collection architecture to fit mode limits, restart Phase 1 |

**Recovery from structural corruption**: run `cleanupOrphans` for the entire run ID, then restart from the affected phase. Do NOT attempt to patch corrupted structure in-place.

---

## 7. Common Error Table

| Error message | Likely cause | Fix |
|---|---|---|
| `"Cannot create component from node"` | Tried to call `createComponentFromNode` on a node inside a component | Create a fresh component instead: `figma.createComponent()` |
| `"in addMode: Limited to N modes only"` | Plan mode limit hit (Starter=1, Professional=4) | Redesign to use fewer modes or upgrade plan |
| `"setCurrentPageAsync: page does not exist"` | Page was deleted or wrong ID | Re-create the page using the idempotency pattern |
| `"Cannot read properties of null"` | `getNodeByIdAsync` returned null — node was deleted | Run the resume protocol to find what exists, update state ledger |
| `"Expected nodes to be component nodes"` | Passed a non-ComponentNode to `combineAsVariants` | Filter the array: `nodes.filter(n => n.type === 'COMPONENT')` |
| `"in createVariable: Cannot create variable"` | Collection was deleted or ID is wrong | Verify collection exists with `getVariableCollectionByIdAsync` |
| `"font not loaded"` | Called a text property setter without `loadFontAsync` first | Add `await figma.loadFontAsync({ family, style })` before the text operation |
| `"Cannot set properties of a read-only array"` | Tried to mutate fills/strokes in-place | Clone first: `const fills = JSON.parse(JSON.stringify(node.fills))` |
| `"Expected RGBA color"` | Color value out of 0–1 range | Divide RGB 0–255 values by 255: `{ r: 65/255, g: 85/255, b: 143/255 }` |
| `"Cannot add children to a non-parent node"` | Tried to append a child to a leaf node (text, rect) | Ensure the parent is a FrameNode, ComponentNode, or GroupNode |
| `"in combineAsVariants: nodes must be in the same parent"` | Components are on different pages | Move all components to the same page before combining |
| `"Script exceeded time limit"` | Loop creating too many nodes in one call | Split the work: create N/2 variants per call |
| Component set deletes itself | Tried to create a component set with no children | `combineAsVariants` requires at least 1 node — always pass 1+ |
| `addComponentProperty` returns unexpected name | This is normal — `BOOLEAN`/`TEXT`/`INSTANCE_SWAP` get `#id:id` suffix | Save the returned key immediately and use that, not the input name |

---

## 8. Per-Phase Recovery Guidance

### Phase 1 fails mid-execution (variable creation)

Symptoms: partial variable collections exist; some variables are missing; some have wrong values.

Recovery steps:
1. Run inspection script to find all variables tagged with your `dsb_run_id`
2. For each variable with `dsb_key` matching the plan, verify its `valuesByMode` and `scopes` are correct
3. If a variable is malformed, call `variable.remove()` and recreate it
4. If the collection itself is malformed, remove the entire collection and recreate from scratch
5. Do NOT proceed to Phase 2 until ALL planned variables exist with correct scopes and code syntax

**The most common Phase 1 failure:** running out of time in a single `use_figma` call when creating many variables. Fix: batch variable creation — create at most 20–30 variables per call.

### Phase 2 fails mid-execution (page/file structure)

Symptoms: some pages exist, others are missing; foundations doc frames are incomplete.

Recovery steps:
1. Identify which pages were successfully created (check for `dsb_key` tags)
2. Mark remaining pages as pending and create them in subsequent calls
3. If a foundations doc frame is malformed, run `cleanupOrphans` for `dsb_phase: 'phase2'` on that page, then recreate

Phase 2 failures rarely require Phase 1 rollback unless the page structure itself is corrupted (which is unusual).

### Phase 3 fails mid-execution (component creation)

This is the most common failure mode in long builds. Handle by component:

```
If failure in Call 1 (page creation):
  → Idempotency check will handle on retry. Safe to re-run.

If failure in Call 2 (doc frame):
  → cleanupOrphans for dsb_key='doc/{component}', then re-run.

If failure in Call 3 (base component):
  → Remove the partial base component node, re-run from Call 3.

If failure in Call 4 (variant creation):
  → cleanupOrphans for dsb_phase='phase3' on the component page (scoped by page).
  → Re-run from Call 3 (base) or Call 4 if base was successfully tagged.

If failure in Call 5 (combineAsVariants + layout):
  → Remove the malformed component set.
  → Remove all variant ComponentNodes for this component (by dsb_key pattern).
  → Re-run from Call 3.

If failure in Call 6 (component properties):
  → The component set already exists and is structurally sound.
  → Re-run Call 6 only — addComponentProperty is safe to retry if
    you first check componentPropertyDefinitions for existing properties.
  → Idempotency check: if 'Label' property already exists, skip addComponentProperty.
```

**Idempotency for component properties (Call 6 retry):**

```javascript
const existingDefs = cs.componentPropertyDefinitions;
const labelKey = existingDefs['Label']
  ? Object.keys(existingDefs).find(k => k.startsWith('Label'))
  : cs.addComponentProperty('Label', 'TEXT', 'Button');
```

### Phase 4 fails mid-execution (QA / Code Connect)

Phase 4 is non-destructive. Failures here do not corrupt Phase 3 work. Common failures:

- **Accessibility audit finds contrast failures:** do not attempt auto-fix. Report the specific variable IDs and token names that fail, then ask the user which value to update.
- **Naming audit finds duplicates:** list all duplicates with their `dsb_key` values, ask user which to keep, then remove the duplicates.
- **Code Connect mapping fails:** treat as incomplete, not broken. Continue and leave as pending.
