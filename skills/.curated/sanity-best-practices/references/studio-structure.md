---
title: "Sanity Studio Structure Rules"
description: Rules for customizing the Sanity Studio Structure (S.structure).
---

# Sanity Studio Structure Rules

## 1. Setup
Custom structure is defined in `sanity.config.ts` using the `structureTool`.

```typescript
import { structureTool } from 'sanity/structure'
import { structure } from './src/structure'

export default defineConfig({
  // ...
  plugins: [
    structureTool({ structure })
  ]
})
```

## 2. Structure Definition
**Location:** `src/structure/index.ts`

Use a function that receives `S` (StructureBuilder).

```typescript
import type { StructureResolver } from 'sanity/structure'

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Content')
    .items([
      // ... items
    ])
```

## 3. Organization Principles
1.  **Singletons First:** Place critical site-wide settings (Global Settings, Homepage) at the top.
2.  **Dividers:** Use `S.divider()` to visually separate logical groups.
3.  **Filtered Lists:** Always exclude Singleton documents from generic `documentTypeList` items to avoid duplication.

## 4. Singleton Pattern (Critical)

**Singletons are enforced via Structure, NOT schema options.** There is no `singleton: true` schema option.

### How Singletons Work
1. Use `S.document().documentId('fixed-id')` to lock the document to a specific ID.
2. Filter the type from generic lists to prevent duplicate entries.

### Singleton Helper Function
```typescript
// Helper to create singleton list items
function createSingleton(S: StructureBuilder, typeName: string, title: string, icon?: ComponentType) {
  return S.listItem()
    .title(title)
    .icon(icon)
    .child(
      S.document()
        .schemaType(typeName)
        .documentId(typeName) // Fixed ID = singleton
        .title(title)
    )
}

// Usage
createSingleton(S, 'settings', 'Site Settings', CogIcon)
```

### Querying Singletons
```groq
// By fixed ID (most efficient)
*[_id == "settings"][0]

// By type (works but slower)
*[_type == "settings"][0]
```

**For localized singletons** (e.g., homepage per language), see `localization.md` Section 6.

## 5. Implementation Pattern

```typescript
// Define singleton types to exclude from generic lists
const SINGLETONS = ['settings', 'homePage']

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Website Content')
    .items([
      // 1. Singletons
      S.listItem()
        .title('Site Settings')
        .icon(CogIcon)
        .child(S.document().schemaType('settings').documentId('settings')),

      S.divider(),

      // 2. Content Verticals
      S.listItem()
        .title('Blog')
        .child(
          S.list()
            .title('Blog Content')
            .items([
              S.documentTypeListItem('post').title('Posts'),
              S.documentTypeListItem('author').title('Authors'),
            ])
        ),

      S.divider(),

      // 3. Remaining Documents (Filtered)
      ...S.documentTypeListItems().filter(
        (listItem) => !SINGLETONS.includes(listItem.getId() as string)
      )
    ])
```

## 6. Views (Split Pane)
Add "Web Preview" or other views to documents.

```typescript
export const defaultDocumentNode: DefaultDocumentNodeResolver = (S, { schemaType }) => {
  switch (schemaType) {
    case `post`:
      return S.document().views([
        S.view.form(), // Default form
        S.view.component(PreviewComponent).title('Preview') // Custom view
      ])
    default:
      return S.document().views([S.view.form()])
  }
}
```
