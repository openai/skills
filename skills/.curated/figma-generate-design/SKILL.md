---
name: figma-generate-design
description: "Use this skill alongside figma-use when the task involves translating an application page, view, or multi-section layout into Figma. Triggers: 'write to Figma', 'create in Figma from code', 'push page to Figma', 'take this app/page and build it in Figma', 'create a screen', 'build a landing page in Figma', 'update the Figma screen to match code'. This is the preferred workflow skill whenever the user wants to build or update a full page, screen, or view in Figma from code or a description. Discovers design system components via search_design_system, imports them with importComponentByKeyAsync/importComponentSetByKeyAsync, and assembles screens incrementally section-by-section."
---

# Build / Update Screens from Design System Components

Use this skill to create or update full-page screens in Figma by **reusing published design system components** rather than drawing primitives. The key insight: the Figma file likely has a published design system with components that correspond 1:1 to the UI components in the codebase (buttons, inputs, navigation elements, cards, accordions, etc.). Find and use those instead of drawing boxes.

**MANDATORY**: You MUST also load [figma-use](../figma-use/SKILL.md) before any `use_figma` call. That skill contains critical rules (closePlugin, try/catch wrapper, color ranges, font loading, etc.) that apply to every script you write.

**Always pass `skillNames: "figma-generate-design"` when calling `use_figma` as part of this skill.** This is a logging parameter — it does not affect execution.

## Skill Boundaries

- Use this skill when the deliverable is a **Figma screen** (new or updated) composed of design system component instances.
- If the user wants to generate **code from a Figma design**, switch to [implement-design](../implement-design/SKILL.md).
- If the user wants to create **new reusable components or variants**, use [figma-use](../figma-use/SKILL.md) directly.
- If the user wants to write **Code Connect mappings**, switch to [code-connect-components](../code-connect-components/SKILL.md).

## Prerequisites

- Figma MCP server (`figma` or `figma-staging`) must be connected
- The target Figma file must have a published design system with components (or access to a team library)
- User should provide either:
  - A Figma file URL / file key to work in
  - Or context about which file to target (the agent can discover pages)
- Source code or description of the screen to build/update

## Parallel Workflow with generate_figma_design (Web Apps Only)

When building a screen from a **web app** that can be rendered in a browser, the best results come from running both approaches in parallel:

1. **In parallel:**
   - Start building the screen using this skill's workflow (use_figma + design system components)
   - Run `generate_figma_design` to capture a pixel-perfect screenshot of the running web app
2. **Once both complete:** Update the use_figma output to match the pixel-perfect layout from the `generate_figma_design` capture. The capture provides the exact spacing, sizing, and visual treatment to aim for, while your use_figma output has proper component instances linked to the design system.
3. **Once confirmed looking good:** Delete the `generate_figma_design` output — it was only used as a visual reference.

This combines the best of both: `generate_figma_design` gives pixel-perfect layout accuracy, while use_figma gives proper design system component instances that stay linked and updatable.

**This workflow only applies to web apps** where `generate_figma_design` can capture the running page. For non-web apps (iOS, Android, etc.) or when updating existing screens, use the standard workflow below.

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 1: Understand the Screen

Before touching Figma, understand what you're building:

1. If building from code, read the relevant source files to understand the page structure, sections, and which components are used.
2. Identify the major sections of the screen (e.g., Header, Hero, Content Panels, Pricing Grid, FAQ Accordion, Footer).
3. For each section, list the UI components involved (buttons, inputs, cards, navigation pills, accordions, etc.).

### Step 2: Discover Design System Components

**Preferred: inspect existing screens first.** If the target file already contains screens using the same design system, skip `search_design_system` and inspect existing instances directly. `search_design_system` returns results from many unrelated libraries and is slow to filter. A single `use_figma` call that walks an existing frame's instances gives you an exact, authoritative component map in seconds:

```js
(async () => {
  try {
    const frame = figma.currentPage.findOne(n => n.name === "Existing Screen");
    const uniqueSets = new Map();
    frame.findAll(n => n.type === "INSTANCE").forEach(inst => {
      const mc = inst.mainComponent;
      const cs = mc?.parent?.type === "COMPONENT_SET" ? mc.parent : null;
      const key = cs ? cs.key : mc?.key;
      const name = cs ? cs.name : mc?.name;
      if (key && !uniqueSets.has(key)) {
        uniqueSets.set(key, { name, key, isSet: !!cs, sampleVariant: mc.name });
      }
    });
    figma.closePlugin(JSON.stringify([...uniqueSets.values()]));
  } catch(e) { figma.closePluginWithFailure(e.toString()); }
})()
```

Only fall back to `search_design_system` when the file has no existing screens to reference. When using it, **search broadly** — try multiple terms and synonyms to maximize coverage (e.g., "button", "input", "nav", "card", "accordion", "header", "footer", "tag", "avatar", "toggle", "icon", etc.).

For each result, note:
- **Component key** — needed for `importComponentByKeyAsync` or `importComponentSetByKeyAsync`
- **Variant properties** — what variants exist (e.g., `variant=primary`, `size=medium`, `state=default`)
- **Whether it's a component or component set** — determines which import function to use

Build a **component map** before writing any scripts. **Include component properties** — you need to know which TEXT properties each component exposes so you can use `setProperties()` for text overrides later. Create a temporary instance, read its `componentProperties` (and those of nested instances), then remove the temp instance:

```js
(async () => {
  try {
    const compSet = await figma.importComponentSetByKeyAsync("COMPONENT_SET_KEY");
    const tempInstance = compSet.defaultVariant.createInstance();

    // Read top-level properties
    const props = tempInstance.componentProperties;

    // Read nested instance properties
    const nested = tempInstance.findAll(n => n.type === "INSTANCE").map(ni => ({
      name: ni.name,
      properties: ni.componentProperties
    }));

    tempInstance.remove(); // clean up

    figma.closePlugin(JSON.stringify({ props, nested }));
  } catch(e) { figma.closePluginWithFailure(e.toString()); }
})()
```

Example component map with property info:

```
Component Map:
- Button → key: "abc123", type: COMPONENT_SET
  Properties: { "Label#2:0": TEXT, "Has Icon#4:64": BOOLEAN }
- PricingCard → key: "ghi789", type: COMPONENT_SET
  Properties: { "Device": VARIANT, "Variant": VARIANT }
  Nested "Text Heading" has: { "Text#2104:5": TEXT }
  Nested "Button" has: { "Label#2:0": TEXT }
```

### Step 3: Create the Page Wrapper Frame First

**Do NOT build sections as top-level page children and reparent them later** — moving nodes across `use_figma` calls with `appendChild()` silently fails and produces orphaned frames. Instead, create the wrapper first, then build each section directly inside it.

Create the page wrapper in its own `use_figma` call. Position it away from existing content and return its ID:

```js
(async () => {
  try {
    // Find clear space
    let maxX = 0;
    for (const child of figma.currentPage.children) {
      maxX = Math.max(maxX, child.x + child.width);
    }

    const wrapper = figma.createFrame();
    wrapper.name = "Homepage";
    wrapper.layoutMode = "VERTICAL";
    wrapper.primaryAxisAlignItems = "CENTER";
    wrapper.counterAxisAlignItems = "CENTER";
    wrapper.resize(1440, 100);
    wrapper.layoutSizingHorizontal = "FIXED";
    wrapper.layoutSizingVertical = "HUG";
    wrapper.x = maxX + 200;
    wrapper.y = 0;

    figma.closePlugin(JSON.stringify({
      success: true,
      wrapperId: wrapper.id
    }));
  } catch(e) { figma.closePluginWithFailure(e.toString()); }
})()
```

### Step 4: Build Each Section Inside the Wrapper

**This is the most important step.** Build one section at a time, each in its own `use_figma` call. At the start of each script, fetch the wrapper by ID and append new content directly to it.

```js
(async () => {
  try {
    const createdNodeIds = [];
    const wrapper = await figma.getNodeByIdAsync("WRAPPER_ID_FROM_STEP_3");

    // Import design system components by key
    const buttonSet = await figma.importComponentSetByKeyAsync("BUTTON_SET_KEY");
    const primaryButton = buttonSet.children.find(c =>
      c.type === "COMPONENT" && c.name.includes("variant=primary")
    ) || buttonSet.defaultVariant;

    // Build section frame
    const section = figma.createFrame();
    section.name = "Header";
    section.layoutMode = "HORIZONTAL";
    // ... configure layout ...

    // Create instances inside the section
    const btnInstance = primaryButton.createInstance();
    section.appendChild(btnInstance);
    createdNodeIds.push(btnInstance.id);

    // Append section to wrapper
    wrapper.appendChild(section);
    section.layoutSizingHorizontal = "FILL"; // AFTER appending

    createdNodeIds.push(section.id);
    figma.closePlugin(JSON.stringify({ success: true, createdNodeIds }));
  } catch(e) {
    figma.closePluginWithFailure(e.toString());
  }
})()
```

After each section, validate with `get_screenshot` before moving on. Look closely for cropped/clipped text (line heights cutting off content) and overlapping elements — these are the most common issues and easy to miss at a glance.

#### Override instance text with setProperties()

Component instances ship with placeholder text ("Title", "Heading", "Button"). Use the component property keys you discovered in Step 2 to override them with `setProperties()` — this is more reliable than direct `node.characters` manipulation. See [component-patterns.md](../figma-use/references/component-patterns.md#overriding-text-in-a-component-instance) for the full pattern.

For nested instances that expose their own TEXT properties, call `setProperties()` on the nested instance:

```js
const nestedHeading = cardInstance.findOne(n => n.type === "INSTANCE" && n.name === "Text Heading");
if (nestedHeading) {
  nestedHeading.setProperties({ "Text#2104:5": "Actual heading from source code" });
}
```

Only fall back to direct `node.characters` for text that is NOT managed by any component property.

#### Read source code defaults carefully

When translating code components to Figma instances, check the component's default prop values in the source code, not just what's explicitly passed. For example, `<Button size="small">Register</Button>` with no variant prop — check the component definition to find `variant = "primary"` as the default. Selecting the wrong variant (e.g., Neutral instead of Primary) produces a visually incorrect result that's easy to miss.

#### What to build manually vs. import

| Build manually (frames, text, rectangles) | Import from design system |
|-------------------------------------------|--------------------------|
| Page wrapper frame | Any component found via `search_design_system` |
| Section container frames | (buttons, cards, inputs, nav elements, etc.) |
| Layout grids (rows, columns) | |
| Spacing / divider frames | |
| Section background fills | |
| One-off text (headings, body copy) | |

### Step 5: Validate the Full Screen

After composing all sections, call `get_screenshot` on the full page frame and compare against the source. Fix any issues with targeted `use_figma` calls — don't rebuild the entire screen.

**Screenshot individual sections, not just the full page.** A full-page screenshot at reduced resolution hides text truncation, wrong colors, and placeholder text that hasn't been overridden. Take a screenshot of each section by node ID to catch:
- **Cropped/clipped text** — line heights or frame sizing cutting off descenders, ascenders, or entire lines
- **Overlapping content** — elements stacking on top of each other due to incorrect sizing or missing auto-layout
- Placeholder text still showing ("Title", "Heading", "Button")
- Truncated content from layout sizing bugs
- Wrong component variants (e.g., Neutral vs Primary button)

### Step 6: Updating an Existing Screen

When updating rather than creating from scratch:

1. Use `get_metadata` to inspect the existing screen structure.
2. Identify which sections need updating and which can stay.
3. For each section that needs changes:
   - Locate the existing nodes by ID or name
   - Swap component instances if the design system component changed
   - Update text content, variant properties, or layout as needed
   - Remove deprecated sections
   - Add new sections
4. Validate with `get_screenshot` after each modification.

```js
// Example: Swap a button variant in an existing screen
(async () => {
  try {
    const existingButton = await figma.getNodeByIdAsync("EXISTING_BUTTON_INSTANCE_ID");
    if (existingButton && existingButton.type === "INSTANCE") {
      // Import the updated component
      const buttonSet = await figma.importComponentSetByKeyAsync("BUTTON_SET_KEY");
      const newVariant = buttonSet.children.find(c =>
        c.name.includes("variant=primary") && c.name.includes("size=lg")
      ) || buttonSet.defaultVariant;
      existingButton.swapComponent(newVariant);
    }
    figma.closePlugin(JSON.stringify({ success: true, mutatedNodeIds: [existingButton.id] }));
  } catch(e) {
    figma.closePluginWithFailure(e.toString());
  }
})()
```

## Reference Docs

For detailed API patterns and gotchas, load these from the [figma-use](../figma-use/SKILL.md) references as needed:

- [component-patterns.md](../figma-use/references/component-patterns.md) — importing by key, finding variants, setProperties, text overrides, working with instances
- [gotchas.md](../figma-use/references/gotchas.md) — layout pitfalls (HUG/FILL interactions, counterAxisAlignItems, sizing order), paint/color issues, page context resets

## Error Recovery

Follow the error recovery process from [figma-use](../figma-use/SKILL.md#6-error-recovery--self-correction):

1. **STOP** on error — do not retry immediately.
2. Call `get_metadata` to inspect partial state.
3. Clean up orphaned nodes before retrying.
4. Fix the script based on inspection results.
5. Retry only after cleanup.

Because this skill works incrementally (one section per call), errors are naturally scoped to a single section. If a section fails, only that section needs cleanup — previous sections remain intact.

## Best Practices

- **Always search before building.** The design system likely has what you need. Manual construction should be the exception, not the rule.
- **Search broadly.** Try synonyms and partial terms. A "NavigationPill" might be found under "pill", "nav", "tab", or "chip".
- **Prefer component instances over manual builds.** Instances stay linked to the source component and update automatically when the design system evolves.
- **Work section by section.** Never build more than one major section per `use_figma` call.
- **Return node IDs from every call.** You'll need them to compose sections and for error recovery.
- **Validate visually after each section.** Use `get_screenshot` to catch issues early.
- **Match existing conventions.** If the file already has screens, match their naming, sizing, and layout patterns.
