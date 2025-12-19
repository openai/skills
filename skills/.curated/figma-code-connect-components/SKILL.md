---
name: figma-code-connect-components
description: Connects Figma design components to code components using Code Connect. Use when user says "code connect", "connect this component to code", "connect Figma to code", "map this component", "link component to code", "create code connect mapping", "add code connect", "connect design to code", or wants to establish mappings between Figma designs and code implementations. Requires Figma MCP server connection.
---

# Code Connect Components

## Overview

This skill helps you connect Figma design components to their corresponding code implementations using Figma's Code Connect feature. It analyzes the Figma design structure, searches your codebase for matching components, and establishes mappings that maintain design-code consistency.

## Prerequisites

- Figma MCP server must be connected and accessible
- User must provide a Figma URL with node ID: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
  - **IMPORTANT:** The Figma URL must include the `node-id` parameter. Code Connect mapping will fail without it.
- **OR** when using `figma-desktop` MCP: User can select a node directly in the Figma desktop app (no URL required)
- **IMPORTANT:** The Figma component must be published to a team library. Code Connect only works with published components or component sets.
- Access to the project codebase for component scanning

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 1: Get Node ID and Extract Metadata

#### Option A: Parse from Figma URL

When the user provides a Figma URL with file key and node ID, first run `get_metadata` to fetch the node structure and identify all Figma components.

**IMPORTANT:** When extracting the node ID from a Figma URL, convert the format:

- URL format uses hyphens: `node-id=1-2`
- Tool expects colons: `nodeId=1:2`

**Parse the Figma URL:**

- URL format: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
- Extract file key: `:fileKey` (segment after `/design/`)
- Extract node ID: `1-2` from URL, then convert to `1:2` for the tool

**Note:** When using the local desktop MCP (`figma-desktop`), `fileKey` is not passed as a parameter to tool calls. The server automatically uses the currently open file, so only `nodeId` is needed.

**Example:**

```
get_metadata(fileKey=":fileKey", nodeId="1:2")
```

#### Option B: Use Current Selection from Figma Desktop App (figma-desktop MCP only)

When using the `figma-desktop` MCP and the user has NOT provided a URL, the tools automatically use the currently selected node from the open Figma file in the desktop app.

**Note:** Selection-based prompting only works with the `figma-desktop` MCP server. The remote server requires a link to a frame or layer to extract context. The user must have the Figma desktop app open with a node selected.

This returns:

- Node structure and hierarchy in XML format
- Node types (identify `<symbol>` nodes as Figma components)
- Node IDs, layer names, positions, and sizes
- Child nodes that may also be components

**Identify components:** For each node or child node returned, if the type is `<symbol>`, that indicates it's a Figma component that can be code connected.

### Step 2: Check Existing Code Connect Mappings

For each Figma component identified (nodes with type `<symbol>`), check if it's already code connected using `get_code_connect_map`.

**Example:**

```
get_code_connect_map(fileKey=":fileKey", nodeId="1:2")
```

**If the component is already connected:**

- Skip to the next component
- Inform the user that this component is already mapped

**If not connected:**

- Proceed to Step 3 to analyze the component and create a mapping

### Step 3: Get Design Context for Un-Connected Components

For components that are not yet code connected, run `get_design_context` to fetch detailed component structure.

**Example:**

```
get_design_context(fileKey=":fileKey", nodeId="1:2")
```

This returns:

- Component structure and hierarchy
- Layout properties and styling
- Text content and variants
- Design properties that map to code props

### Step 4: Scan Codebase for Matching Component

Using the output from `get_design_context`, scan the codebase to find a component with similar structure.

**What to look for:**

- Component names that match or are similar to the Figma component name
- Component structure that aligns with the Figma hierarchy
- Props that correspond to Figma properties (variants, text, styles)
- Files in typical component directories (`src/components/`, `components/`, `ui/`, etc.)

**Search strategy:**

1. Search for component files with matching names
2. Read candidate files to check structure and props
3. Compare the code component's props with Figma design properties
4. Detect the programming language (TypeScript, JavaScript) and framework (React, Vue, etc.)
5. Identify the best match based on structural similarity, weighing:
   - Prop names and their correspondence to Figma properties
   - Default values that match Figma defaults
   - CSS classes or style objects
   - Descriptive comments that clarify intent
6. If multiple candidates are equally good, pick the one with the closest prop-interface match and document your reasoning in a 1–2 sentence comment before your tool call

**Example search patterns:**

- If Figma component is "PrimaryButton", search for `Button.tsx`, `PrimaryButton.tsx`, `Button.jsx`
- Check common component paths: `src/components/`, `app/components/`, `lib/ui/`
- Look for variant props like `variant`, `size`, `color` that match Figma variants

### Step 5: Offer Code Connect Mapping

Present your findings to the user and offer to create the Code Connect mapping.

**What to communicate:**

- Which code component you found that matches the Figma component
- File path of the component
- Component name
- Language and framework detected

**Example message:**

```
I found a matching component in your codebase:
- File: src/components/Button.tsx
- Component: Button
- Language: TypeScript/JavaScript
- Framework: React

Would you like me to create a Code Connect mapping for this component?
```

**If no exact match is found:**

- Show the 2 closest candidates
- Explain the differences
- Ask the user to confirm which component to use or provide the correct path

### Step 6: Create the Code Connect Mapping

If the user accepts, run `add_code_connect_map` to establish the connection.

**Tool parameters:**

```
add_code_connect_map(
  nodeId="1:2",
  source="src/components/Button.tsx",
  componentName="Button",
  clientLanguages="typescript,javascript",
  clientFrameworks="react"
)
```

**Key parameters:**

- `nodeId`: The Figma node ID (with colon format: `1:2`)
- `source`: Path to the code component file (relative to project root)
- `componentName`: Name of the component to connect (e.g., "Button", "Card")
- `clientLanguages`: Comma-separated list of languages (e.g., "typescript,javascript", "javascript")
- `clientFrameworks`: Framework being used (e.g., "react", "vue", "svelte", "angular")
- `label`: The framework or language label for this Code Connect mapping. Valid values include:
  - Web: 'React', 'Web Components', 'Vue', 'Svelte', 'Storybook', 'Javascript'
  - iOS: 'Swift UIKit', 'Objective-C UIKit', 'SwiftUI'
  - Android: 'Compose', 'Java', 'Kotlin', 'Android XML Layout'
  - Cross-platform: 'Flutter'

### Step 7: Repeat for All Un-Connected Components

After successfully connecting one component, return to Step 2 and repeat the process for all other un-connected Figma components identified in the node tree from Step 1.

**Workflow for multiple components:**

1. From the metadata obtained in Step 1, identify all nodes with type `<symbol>`
2. For each component node:
   - Check if already code connected (Step 2)
   - If not connected, proceed with Steps 3-6
   - Track which components have been processed
3. After processing all components, provide a summary:
   - Total components found
   - Components successfully connected
   - Components skipped (already connected)
   - Components that could not be connected (with reasons)

**Example summary:**

```
Code Connect Summary:
- Total components found: 5
- Successfully connected: 3
  - Button (1:2) → src/components/Button.tsx
  - Card (1:5) → src/components/Card.tsx
  - Input (1:8) → src/components/Input.tsx
- Already connected: 1
  - Icon (1:3) → src/icons/Icon.tsx
- Could not connect: 1
  - CustomWidget (1:10) - No matching component found in codebase
```

## Examples

### Example 1: Connecting a Button Component

User says: "Connect this Figma button to my code: https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15"

**Actions:**

1. Parse URL: fileKey=`kL9xQn2VwM8pYrTb4ZcHjF`, nodeId=`42-15` (from URL)
2. Convert node ID: `42-15` → `42:15`
3. Run `get_metadata(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42:15")` to get node structure
4. Metadata shows: Node type is `<symbol>` (Figma component), name is "Button"
5. Run `get_code_connect_map(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42:15")` to check existing mappings
6. Result: No existing mapping found
7. Run `get_design_context(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42:15")` to get detailed structure
8. Design context shows: Button component with `variant` (primary/secondary) and `size` (sm/md/lg) properties
9. Search codebase for Button components: Find `src/components/Button.tsx`
10. Read `Button.tsx` and confirm it has `variant` and `size` props
11. Offer mapping: "I found Button.tsx with matching variant and size props. Connect?"
12. User confirms: "Yes"
13. Detect that it's a TypeScript React component
14. Run `add_code_connect_map(nodeId="42:15", source="src/components/Button.tsx", componentName="Button", clientLanguages="typescript,javascript", clientFrameworks="react")`

**Result:** Figma button component is now connected to the code Button component.

### Example 2: Multiple Candidates Scenario

User says: "Connect this card: https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Components?node-id=10-50"

**Actions:**

1. Parse URL: fileKey=`pR8mNv5KqXzGwY2JtCfL4D`, nodeId=`10-50` → convert to `10:50`
2. Run `get_metadata(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10:50")` to get node structure
3. Metadata shows: Node type is `<symbol>` (Figma component), name is "ProductCard"
4. Run `get_code_connect_map(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10:50")` to check existing mappings
5. Result: No existing mapping found
6. Run `get_design_context(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10:50")`
7. Design context shows: Card with title, description, image, and action button
8. Search codebase: Find two candidates:
   - `src/components/Card.tsx` (basic card)
   - `src/components/ProductCard.tsx` (card with image and CTA)
9. Read both files and compare structure
10. Present to user: "Found two card components:

- Card.tsx: Basic card with title and description
- ProductCard.tsx: Card with image, title, description, and action button (closer match)

Which should I connect?"

11. User: "ProductCard.tsx"
12. Detect that it's a TypeScript React component
13. Run `add_code_connect_map(nodeId="10:50", source="src/components/ProductCard.tsx", componentName="ProductCard", clientLanguages="typescript,javascript", clientFrameworks="react")`

**Result:** User-selected ProductCard component is successfully connected to the Figma design.

### Example 3: Component Needs Creation

User says: "Connect this icon: https://figma.com/design/8yJDMeWDyBz71EnMOSuUiw/Icons?node-id=5-20"

**Actions:**

1. Parse URL: fileKey=`8yJDMeWDyBz71EnMOSuUiw`, nodeId=`5-20` → convert to `5:20`
2. Run `get_metadata(fileKey="8yJDMeWDyBz71EnMOSuUiw", nodeId="5:20")` to get node structure
3. Metadata shows: Node type is `<symbol>` (Figma component), name is "CheckIcon"
4. Run `get_code_connect_map(fileKey="8yJDMeWDyBz71EnMOSuUiw", nodeId="5:20")` to check existing mappings
5. Result: No existing mapping found
6. Run `get_design_context(fileKey="8yJDMeWDyBz71EnMOSuUiw", nodeId="5:20")`
7. Design context shows: CheckIcon with color and size variants
8. Search codebase for CheckIcon: No matches found
9. Search for generic Icon components: Find `src/icons/` directory with other icons
10. Report to user: "I couldn't find a CheckIcon component, but I found an icons directory at src/icons/. Would you like to:

- Create a new CheckIcon.tsx component first, then connect it
- Connect to a different existing icon
- Provide the path to the CheckIcon if it exists elsewhere"

11. User provides path: "src/icons/CheckIcon.tsx"
12. Detect language and framework from the file
13. Run `add_code_connect_map(nodeId="5:20", source="src/icons/CheckIcon.tsx", componentName="CheckIcon", clientLanguages="typescript,javascript", clientFrameworks="react")`

**Result:** CheckIcon component is successfully connected to the Figma design.

## Best Practices

### Proactive Component Discovery

Don't just ask the user for the file path — actively search their codebase to find matching components. This provides a better experience and catches potential mapping opportunities.

### Accurate Structure Matching

When comparing Figma components to code components, look beyond just names. Check that:

- Props align (variant types, size options, etc.)
- Component hierarchy matches (nested elements)
- The component serves the same purpose

### Clear Communication

When offering to create a mapping, clearly explain:

- What you found
- Why it's a good match
- What the mapping will do
- How props will be connected

### Handle Ambiguity

If multiple components could match, present options rather than guessing. Let the user make the final decision about which component to connect.

### Graceful Degradation

If you can't find an exact match, provide helpful next steps:

- Show close candidates
- Suggest component creation
- Ask for user guidance

## Common Issues and Solutions

### Issue: "Failed to map node to Code Connect. Please ensure the component or component set is published to the team library"

**Cause:** The Figma component is not published to a team library. Code Connect only works with published components.
**Solution:** The user needs to publish the component to a team library in Figma:

1. In Figma, select the component or component set
2. Right-click and choose "Publish to library" or use the Team Library publish modal
3. Publish the component
4. Once published, retry the Code Connect mapping with the same node ID

### Issue: No matching component found in codebase

**Cause:** The codebase search did not find a component with a matching name or structure.
**Solution:** Ask the user if the component exists under a different name or in a different location. They may need to create the component first, or it might be located in an unexpected directory.

### Issue: Code Connect map creation fails with "component not found"

**Cause:** The source file path is incorrect, the component doesn't exist at that location, or the componentName doesn't match the actual export.
**Solution:** Verify the source path is correct and relative to the project root. Check that the component is properly exported from the file with the exact componentName specified.

### Issue: Wrong language or framework detected

**Cause:** The clientLanguages or clientFrameworks parameters don't match the actual component implementation.
**Solution:** Inspect the component file to verify the language (TypeScript, JavaScript) and framework (React, Vue, etc.). Update the parameters accordingly. For TypeScript React components, use `clientLanguages="typescript,javascript"` and `clientFrameworks="react"`.

### Issue: Code Connect mapping fails with URL errors

**Cause:** The Figma URL format is incorrect or missing the `node-id` parameter.
**Solution:** Verify the URL follows the required format: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`. The `node-id` parameter is required. Also ensure you convert `1-2` to `1:2` when calling tools.

### Issue: Multiple similar components found

**Cause:** The codebase contains multiple components that could match the Figma component.
**Solution:** Present all candidates to the user with their file paths and let them choose which one to connect. Different components might be used in different contexts (e.g., `Button.tsx` vs `LinkButton.tsx`).

## Understanding Code Connect

Code Connect establishes a bidirectional link between design and code:

**For designers:** See which code component implements a Figma component
**For developers:** Navigate from Figma designs directly to the code that implements them
**For teams:** Maintain a single source of truth for component mappings

The mapping you create helps keep design and code in sync by making these connections explicit and discoverable.

## Additional Resources

For more information about Code Connect:

- [Code Connect Documentation](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
