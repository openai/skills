---
title: "Sanity Visual Editing Rules"
description: Comprehensive guide for Sanity Visual Editing, including Presentation Tool, Stega (Content Source Maps), and Overlays.
---

# Sanity Visual Editing Rules

## 1. Concepts

### Presentation Tool
The Studio plugin (`sanity/presentation`) that renders your front-end application inside an iframe in the Studio. It enables the "Edit" overlay and bidirectional navigation.

### Content Source Maps (Stega)
Invisible characters embedded in strings that tell the Presentation Tool which field in which document the content comes from.
- **Mechanism:** Sanity encodes document ID, field path, and dataset info into string values.
- **Result:** Click-to-edit functionality in the preview.

### Loaders
Framework-agnostic or specific libraries that handle:
1.  Fetching data (production vs. preview).
2.  Subscribing to real-time updates (Live Content API).
3.  Encoding Stega strings (if not handled by the Content Lake automatically).

## 2. The Golden Rule of Stega (Clean Data)

When Visual Editing is enabled, string fields will contain invisible characters. You **MUST** clean them before using the value for logic.

| Scenario | Clean? | Why |
|----------|--------|-----|
| Comparing strings (`if (x === 'y')`) | ✅ Yes | Stega breaks equality |
| Using as object keys | ✅ Yes | Keys won't match |
| Using as HTML IDs | ✅ Yes | Invalid characters |
| Passing to third-party libraries | ✅ Yes | May validate input |
| Rendering text (`<h1>{title}</h1>`) | ❌ No | Breaks click-to-edit |
| Passing to `<PortableText />` | ❌ No | Handles internally |
| Passing to image helpers | ❌ No | Handles internally |

```typescript
import { stegaClean } from "@sanity/client/stega";

export function Layout({ align }: { align: string }) {
  // Good: Clean before comparison
  const cleanAlign = stegaClean(align);
  return <div className={cleanAlign === 'center' ? 'mx-auto' : ''} />
}
```

## 3. Token Handling (Security)

Store your read token in a dedicated file that throws if missing:

```typescript
// src/sanity/lib/token.ts
export const token = process.env.SANITY_API_READ_TOKEN

if (!token) {
  throw new Error('Missing SANITY_API_READ_TOKEN')
}
```

**Never** expose tokens in client bundles. Pass to `defineLive` for server/browser use only when Draft Mode is enabled.

## 4. Setup: Presentation Tool

**File:** `sanity.config.ts`

```typescript
import { defineConfig } from 'sanity'
import { presentationTool } from 'sanity/presentation'
import { resolve } from '@/sanity/presentation/resolve'

export default defineConfig({
  // ...
  plugins: [
    presentationTool({
      resolve, // Document locations (see below)
      previewUrl: {
        previewMode: {
          enable: '/api/draft-mode/enable',
        },
      },
    }),
  ],
})
```

### Document Locations

Show where documents appear in the front-end — enables quick navigation between Structure and Presentation tools.

```typescript
// src/sanity/presentation/resolve.ts
import { defineLocations, PresentationPluginOptions } from 'sanity/presentation'

export const resolve: PresentationPluginOptions['resolve'] = {
  locations: {
    post: defineLocations({
      select: { title: 'title', slug: 'slug.current' },
      resolve: (doc) => ({
        locations: [
          { title: doc?.title || 'Untitled', href: `/posts/${doc?.slug}` },
          { title: 'Posts index', href: `/posts` },
        ],
      }),
    }),
    // Add more document types as needed
  },
}
```

## 5. Visual Editing Overlays

Render `<VisualEditing />` in Draft Mode for click-to-edit overlays.

**Next.js (App Router):**
```typescript
// layout.tsx
import { VisualEditing } from 'next-sanity/visual-editing'
import { draftMode } from 'next/headers'
import { DisableDraftMode } from '@/components/disable-draft-mode'

export default async function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        {(await draftMode()).isEnabled && (
          <>
            <DisableDraftMode />
            <VisualEditing />
          </>
        )}
      </body>
    </html>
  )
}
```

### Disable Draft Mode Button

Useful for content authors to exit preview and see published content:

```typescript
// src/components/disable-draft-mode.tsx
'use client'
import { useDraftModeEnvironment } from 'next-sanity/hooks'

export function DisableDraftMode() {
  const environment = useDraftModeEnvironment()
  // Only show outside of Presentation Tool
  if (environment !== 'live' && environment !== 'unknown') return null

  return (
    <a href="/api/draft-mode/disable" className="fixed bottom-4 right-4 bg-gray-50 px-4 py-2">
      Disable Draft Mode
    </a>
  )
}
```

**Remix/Svelte:** See framework-specific rules for `useLiveMode` and `enableVisualEditing` patterns.

## 6. SEO & Metadata (Critical)

**NEVER** allow Stega strings in `<head>` tags (Title, Description, Canonical URLs). It destroys SEO rankings and looks broken in search results.

-   **Next.js:** Set `stega: false` in `generateMetadata`.
-   **General:** Explicitly clean fields used in `<title>` or `<meta>`.

```typescript
// Next.js Example — disable stega at fetch level
export async function generateMetadata({ params }) {
  const { data } = await sanityFetch({
    query: SEO_QUERY,
    stega: false // Critical
  })
  return { title: data.title }
}
```

**Alternative:** If you can't disable stega at the fetch level, clean explicitly:

```typescript
import { stegaClean } from "@sanity/client/stega";

export async function generateMetadata({ params }) {
  const { data } = await sanityFetch({ query: PAGE_QUERY })
  return { 
    title: stegaClean(data.title),
    description: stegaClean(data.description),
    openGraph: { url: stegaClean(data.canonicalUrl) }
  }
}
```

## 7. Drag-and-Drop Reordering (Advanced)

For arrays (e.g., "Related Posts"), enable drag-and-drop in the preview using `data-sanity` attributes and `useOptimistic`:

```typescript
import { createDataAttribute } from 'next-sanity'
import { useOptimistic } from 'next-sanity/hooks'

// Add data-sanity to array container
<ul data-sanity={createDataAttribute({ id: documentId, type: 'post', path: 'relatedPosts' }).toString()}>
  {items.map((item) => (
    <li key={item._key} data-sanity={createDataAttribute({
      id: documentId, type: 'post', path: `relatedPosts[_key=="${item._key}"]`
    }).toString()}>
      {item.title}
    </li>
  ))}
</ul>
```

**Key requirements:**
- Query must include `_key` for array items
- Use `useOptimistic` hook for instant UI updates during mutations

## 8. Optimistic Updates for Faster Editing

By default, editing a field in the Presentation Tool triggers a full page re-render. For pages with many components, this can feel sluggish. **Presentation queries** solve this by fetching only the specific block being edited.

### The Concept

Instead of:
1. User edits a field -> Full page query re-runs -> All components re-render

You get:
1. User edits a field -> Block-specific query runs -> Only that component re-renders

### How It Works

1. **Create a targeted query** that fetches just the block data using `_key`:

```groq
*[_id == $documentId][0]{
  "heroBlock": pageBuilder[_key == $blockKey && _type == "hero"][0]{
    title, subtitle, image
  }
}
```

2. **Use a presentation query hook** in your component (e.g., `usePresentationQuery` in Next.js)

3. **Fall back to initial props** when not in presentation mode

This pattern works for both Page Builder blocks (`pageBuilder[]`) and Portable Text blocks (`body[]`).

**See framework-specific rules for implementation:**
- Next.js: `nextjs.md` (Section 9)
- Page Builder: `page-builder.md` (Section 5)
- Portable Text: `portable-text.md` (Section 7)

## 9. Framework Specifics

| Framework | Loader Package | Key Components |
| :--- | :--- | :--- |
| **Next.js** | `next-sanity` | `<VisualEditing />`, `defineLive`, `usePresentationQuery` |
| **Remix** | `@sanity/react-loader` | `createQueryStore`, `useLiveMode`, `enableVisualEditing` |
| **Svelte** | `@sanity/svelte-loader` | `createRequestHandler`, `useLiveMode`, `enableVisualEditing` |
| **Nuxt** | `@nuxtjs/sanity` | Automatic via module config (`visualEditing: {}`) |
| **Astro** | `@sanity/astro` | `sanity({ useCdn: false, stega: true })` |
