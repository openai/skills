---
title: "Sanity Page Builder Patterns"
description: Patterns for Sanity Page Builder arrays, block components, and live editing.
---

# Sanity Page Builder Patterns

This guide covers **Page Builder** patterns—arrays of block objects that allow content teams to compose flexible page layouts. For Portable Text (rich text within documents), see `portable-text.md`.

## 1. What is a Page Builder?

A page builder is an **array of objects** (`pageBuilder[]`) that allows content teams to compose pages from reusable blocks without developer intervention.

**When to use:**
- Flexible layouts needed (marketing pages, landing pages)
- Content can be reordered
- Different components on different pages

**When NOT to use:**
- Rigid, formulaic content (blog posts, product pages)
- Highly structured data that doesn't change layout
- Rich text within a document body—use Portable Text instead

## 2. Schema Organization

### Directory Structure
```
schemaTypes/
├── blocks/           # Page builder blocks (objects)
│   ├── heroType.ts
│   ├── featuresType.ts
│   └── faqsType.ts
├── pageBuilderType.ts  # The array definition
└── pageType.ts         # Document using the page builder
```

### Objects vs References

| Use **Objects** | Use **References** |
|-----------------|-------------------|
| Content is unique to this page | Content reused across many pages |
| Simpler queries | Needs central management |
| Default choice | FAQs, CTAs, testimonials |

**Rule:** Use references sparingly. Most blocks should be objects.

### Page Builder Array
```typescript
// pageBuilderType.ts
import { defineType, defineArrayMember } from "sanity";

export const pageBuilderType = defineType({
  name: "pageBuilder",
  type: "array",
  of: [
    defineArrayMember({ type: "hero" }),
    defineArrayMember({ type: "splitImage" }),
    defineArrayMember({ type: "features" }),
    defineArrayMember({ type: "faqs" }),
  ],
  options: {
    insertMenu: {
      views: [
        // Optional: Show visual thumbnails in the insert menu grid
        { name: "grid", previewImageUrl: (type) => `/block-previews/${type}.png` },
      ],
    },
  },
});
```

### Block Preview Pattern
Every block should have consistent previews:

```typescript
import { defineType } from "sanity";
import { BlockContentIcon } from "@sanity/icons";

export const splitImageType = defineType({
  name: "splitImage",
  type: "object",
  icon: BlockContentIcon,
  fields: [/* ... */],
  preview: {
    select: { title: "title", media: "image" },
    prepare({ title, media }) {
      return {
        title: title || "Untitled",
        subtitle: "Split Image", // Block type name
        media: media ?? BlockContentIcon, // Fallback to icon
      };
    },
  },
});
```

## 3. Querying Page Builders

Expand references only for blocks that need them:

```groq
*[_type == "page" && slug.current == $slug][0]{
  ...,
  content[]{
    ...,
    _type == "faqs" => {
      ...,
      faqs[]->  // Expand only FAQ references
    }
  }
}
```

## 4. Rendering Page Builders

### TypeScript Typing
Use `Extract` to type individual blocks from the query result:

```typescript
import { PAGE_QUERYResult } from "@/sanity/types";

type HeroProps = Extract<
  NonNullable<NonNullable<PAGE_QUERYResult>["content"]>[number],
  { _type: "hero" }
>;

export function Hero({ title, image }: HeroProps) {
  // Fully typed!
}
```

### Switch-Based Rendering
```typescript
export function PageBuilder({ content }: { content: Block[] }) {
  if (!Array.isArray(content)) return null;

  return (
    <main>
      {content.map((block) => {
        switch (block._type) {
          case "hero":
            return <Hero key={block._key} {...block} />;
          case "features":
            return <Features key={block._key} {...block} />;
          case "splitImage":
            return <SplitImage key={block._key} {...block} />;
          default:
            return <div key={block._key}>Unknown: {block._type}</div>;
        }
      })}
    </main>
  );
}
```

**Always use `_key` for React keys:**
```typescript
// Breaks Visual Editing and causes hydration issues
{items.map((item, i) => <Component key={i} {...item} />)}

// Always use Sanity's _key
{items.map((item) => <Component key={item._key} {...item} />)}
```

### Cleaning Values for Logic
Use `stegaClean` when block fields control rendering logic:

```typescript
import { stegaClean } from "next-sanity";

function SplitImage({ orientation, title, image }) {
  return (
    <section data-orientation={stegaClean(orientation) || "imageLeft"}>
      {/* ... */}
    </section>
  );
}
```

## 5. Presentation Queries for Live Editing (Next.js)

For faster live updates in the Presentation Tool, use **presentation queries** that fetch only the specific block being edited, rather than re-fetching the entire page.

> **Note:** This pattern uses `usePresentationQuery` from `next-sanity/hooks`. For other frameworks, check your loader package for equivalent functionality.

### The Pattern

1. **Create a block-specific presentation query:**

```typescript
// queries.ts
export const HERO_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    _id,
    _type,
    "heroBlock": pageBuilder[_key == $blockKey && _type == "hero"][0]{
      title,
      subtitle,
      image,
      // ... all fields the component needs
    }
  }
`)
```

2. **Use `usePresentationQuery` in your component:**

```typescript
'use client'
import { usePresentationQuery } from 'next-sanity/hooks'
import { HERO_PRESENTATION_QUERY } from '@/sanity/lib/queries'

type HeroProps = {
  _key: string
  documentId: string
  // ... initial props from page query
}

export function Hero({ _key, documentId, ...initialProps }: HeroProps) {
  // Fetch block-specific data for faster updates
  const { data } = usePresentationQuery({
    query: HERO_PRESENTATION_QUERY,
    params: { documentId, blockKey: _key },
  })

  // Use presentation data if available, fallback to initial props
  const blockData = data?.heroBlock || initialProps

  return (
    <section>
      <h1>{blockData.title}</h1>
      {/* ... */}
    </section>
  )
}
```

### Why This Is Faster

- **Without:** Editing a field triggers a full page re-render with all blocks
- **With:** Only the specific block re-renders with its targeted query

This pattern is especially valuable for pages with many blocks or complex nested data.

**Note:** See `nextjs.md` for more details on `usePresentationQuery` and `visual-editing.md` for the conceptual overview.

## 6. Page Builder Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too many block variations | Split into separate blocks if >2 variants |
| Paradox of choice | Limit blocks per document type |
| Overusing references | Default to objects; references only for truly shared content |
| Unused blocks accumulate | Prune regularly; see deprecation patterns |
| Inconsistent previews | Always set title, subtitle (block name), and media/icon |

## 7. Component Alignment Pattern
Map Sanity "alignment" fields (usually string/select) to CSS classes using utility functions.

**Schema:**
```typescript
defineField({
  name: 'align',
  type: 'string',
  options: { list: ['left', 'center', 'right'], layout: 'radio' }
})
```

**Implementation (Utility):**
```typescript
import { stegaClean } from "@sanity/client/stega";

export function getTextAlign(align?: string) {
  // CLEAN the value before switching!
  switch (stegaClean(align)) {
    case 'left': return 'text-left';
    case 'right': return 'text-right';
    default: return 'text-center';
  }
}
```

## 8. Semantic Heading Levels
**Rule:** Do NOT store heading levels (h1, h2) in Sanity schema options. Determine them dynamically in the frontend to ensure accessibility.

**Bad Schema:**
```typescript
// Don't do this
{ name: 'level', type: 'string', options: { list: ['h1', 'h2'] } }
```

**Good Component:**
Pass a `semanticLevel` prop based on the component's context/nesting.

```typescript
type Props = {
  block: HeroBlock;
  level?: 'h1' | 'h2' | 'h3'; // Default to h2 if undefined
}

export default function Section({ block, level = 'h2' }: Props) {
  const Tag = level;
  return <Tag>{block.title}</Tag>;
}
```

*Note: For Image patterns, see `image.md`. For Portable Text patterns, see `portable-text.md`.*
