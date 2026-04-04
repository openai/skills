---
title: "Sanity Portable Text Rules"
description: Portable Text (Rich Text) rendering and custom component creation for React/Next.js.
---

# Sanity Portable Text Rules

Portable Text is Sanity's rich text format, used for content like article bodies (`body[]`). This guide covers rendering and creating custom PTE components.

**Note:** For page-level layout blocks (`pageBuilder[]`), see `page-builder.md`.

## 1. The Component
Use the `PortableText` component from `next-sanity` (or `@portabletext/react`).

```typescript
import { PortableText } from "next-sanity";
// or import { PortableText } from "@portabletext/react";

export function Content({ value }: { value: any }) {
  return <PortableText value={value} components={components} />;
}
```

## 2. Custom Components (`components` prop)
**Always** define a typed components object to handle custom blocks, marks, and list styles.

```typescript
import { PortableTextComponents } from "next-sanity";

const components: PortableTextComponents = {
  // 1. Block styles (paragraphs, headings)
  block: {
    h1: ({ children }) => <h1 className="text-4xl font-bold">{children}</h1>,
    h2: ({ children }) => <h2 className="text-3xl font-bold">{children}</h2>,
    blockquote: ({ children }) => <blockquote className="border-l-4 pl-4">{children}</blockquote>,
  },

  // 2. Custom types (non-text blocks like images, videos)
  types: {
    image: ({ value }) => <SanityImage value={value} />,
    callToAction: ({ value }) => <Button href={value.url}>{value.text}</Button>,
  },

  // 3. Marks (inline decorators and annotations)
  marks: {
    strong: ({ children }) => <strong className="font-bold">{children}</strong>,
    em: ({ children }) => <em className="italic">{children}</em>,
    link: ({ children, value }) => {
      const rel = !value.href.startsWith("/") ? "noreferrer noopener" : undefined;
      return <a href={value.href} rel={rel} className="underline text-blue-600">{children}</a>;
    },
  },

  // 4. Lists
  list: {
    bullet: ({ children }) => <ul className="list-disc ml-4">{children}</ul>,
    number: ({ children }) => <ol className="list-decimal ml-4">{children}</ol>,
  },
};
```

## 3. Component Categories

Portable Text has three types of custom components, each with different patterns:

| Type | Examples | Pattern |
|------|----------|---------|
| **Block styles** | h1, h2, blockquote, normal | Text blocks with `children` prop |
| **Custom types** | image, video, callToAction | Non-text blocks with `value` prop |
| **Marks** | link, strong, productRef | Inline annotations wrapping text |

## 4. Creating Block Style Components

Block styles are text blocks like headings and paragraphs. For simple styling, inline components work fine:

```typescript
block: {
  h2: ({ children }) => <h2 className="mt-8 mb-4 text-3xl font-bold">{children}</h2>,
  normal: ({ children }) => <p className="mb-4 leading-relaxed">{children}</p>,
}
```

### With Visual Editing Support

For live editing in the Presentation Tool, block style components may need **both** a client and server version:

```typescript
// Heading2.tsx (Server - simple SSR for production)
export function Heading2({ children }: { children: React.ReactNode }) {
  return <h2 className="mt-8 mb-4 text-3xl font-bold">{children}</h2>;
}

// Heading2Client.tsx (Client - for visual editing context)
'use client'
export function Heading2Client({ children, value }: { children: React.ReactNode; value: any }) {
  // Can access block data via `value` for advanced patterns
  return <h2 className="mt-8 mb-4 text-3xl font-bold">{children}</h2>;
}
```

Use `useIsPresentationTool` to conditionally render the client version:

```typescript
import { useIsPresentationTool } from 'next-sanity/hooks'

function Heading2Wrapper(props) {
  const isPresentationTool = useIsPresentationTool()

  if (isPresentationTool) {
    return <Heading2Client {...props} />
  }
  return <Heading2 {...props} />
}
```

## 5. Creating Custom Type Components

Custom types are non-text blocks like images, videos, or CTAs embedded in rich text.

### Schema Definition

```typescript
// schemaTypes/blocks/pteImageBlock.ts
import { defineType, defineField } from 'sanity'

export const pteImageBlock = defineType({
  name: 'pteImage',
  title: 'Image',
  type: 'object',
  fields: [
    defineField({ name: 'image', type: 'image', options: { hotspot: true } }),
    defineField({ name: 'caption', type: 'string' }),
    defineField({ name: 'alt', type: 'string', validation: (r) => r.required() }),
  ],
  preview: {
    select: { title: 'caption', media: 'image' },
  },
})
```

### Register in Body Schema

```typescript
defineField({
  name: 'body',
  type: 'array',
  of: [
    { type: 'block' },      // Standard text
    { type: 'pteImage' },   // Custom image block
    { type: 'pteVideo' },   // Custom video block
  ],
})
```

### Frontend Component

```typescript
// PteImageComponent.tsx
'use client'

type PteImageProps = {
  value: {
    _key: string
    image: any
    caption?: string
    alt: string
  }
}

export function PteImageComponent({ value }: PteImageProps) {
  if (!value.image) return null

  return (
    <figure className="my-8">
      <SanityImage value={value.image} alt={value.alt} />
      {value.caption && (
        <figcaption className="text-sm text-gray-600 mt-2">{value.caption}</figcaption>
      )}
    </figure>
  )
}

// Register in components
const components: PortableTextComponents = {
  types: {
    pteImage: PteImageComponent,
  },
}
```

## 6. Creating Mark Components

Marks are inline annotations that wrap text—links, highlights, or custom references.

### Schema Definition (Annotation)

```typescript
// In your block configuration
defineField({
  name: 'body',
  type: 'array',
  of: [
    {
      type: 'block',
      marks: {
        decorators: [
          { title: 'Strong', value: 'strong' },
          { title: 'Emphasis', value: 'em' },
          { title: 'Highlight', value: 'highlight' },
        ],
        annotations: [
          {
            name: 'link',
            type: 'object',
            title: 'Link',
            fields: [
              { name: 'href', type: 'url', title: 'URL' },
              { name: 'openInNewTab', type: 'boolean', title: 'Open in new tab' },
            ],
          },
          {
            name: 'productRef',
            type: 'object',
            title: 'Product Reference',
            fields: [
              { name: 'product', type: 'reference', to: [{ type: 'product' }] },
            ],
          },
        ],
      },
    },
  ],
})
```

### Frontend Component

```typescript
// LinkMark.tsx
type LinkMarkProps = {
  children: React.ReactNode
  value: {
    href: string
    openInNewTab?: boolean
  }
}

export function LinkMark({ children, value }: LinkMarkProps) {
  const { href, openInNewTab } = value
  const target = openInNewTab ? '_blank' : undefined
  const rel = openInNewTab ? 'noopener noreferrer' : undefined

  return (
    <a href={href} target={target} rel={rel} className="text-blue-600 underline">
      {children}
    </a>
  )
}

// Register in components
const components: PortableTextComponents = {
  marks: {
    link: LinkMark,
    highlight: ({ children }) => <mark className="bg-yellow-200">{children}</mark>,
  },
}
```

## 7. Presentation Queries for PTE Blocks

For faster live editing of custom PTE blocks, use presentation queries that fetch only the specific block:

```typescript
// queries.ts
export const PTE_IMAGE_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    _id,
    _type,
    "pteImageBlock": body[_key == $blockKey && _type == "pteImage"][0]{
      _key,
      image,
      caption,
      alt
    }
  }
`)
```

Then in your component:

```typescript
'use client'
import { usePresentationQuery } from 'next-sanity/hooks'

export function PteImageComponent({ value, documentId }: { value: any; documentId?: string }) {
  const { data } = usePresentationQuery({
    query: PTE_IMAGE_PRESENTATION_QUERY,
    params: { documentId, blockKey: value._key },
  })

  const blockData = data?.pteImageBlock || value

  // ... render with blockData
}
```

**Note:** You'll need to pass `documentId` through to your PTE components. See `visual-editing.md` for context patterns.

## 8. GROQ Fragment for PTE

When querying documents with Portable Text, expand custom blocks:

```groq
*[_type == "article" && slug.current == $slug][0]{
  ...,
  body[]{
    ...,
    _type == "pteImage" => {
      ...,
      "imageUrl": image.asset->url
    },
    _type == "pteVideo" => {
      ...,
      video->{ title, url }
    }
  }
}
```

## 9. Stega and Visual Editing

When Visual Editing is enabled, text content contains invisible stega characters for click-to-edit functionality.

**For text rendering:** Let stega characters pass through—they enable overlays:
```typescript
// Good - stega preserved for click-to-edit
<h2>{children}</h2>
```

**For logic/comparisons:** Clean the values first:
```typescript
import { stegaClean } from '@sanity/client/stega'

// Clean before using in logic
const cleanedStyle = stegaClean(block.style)
if (cleanedStyle === 'h2') { ... }
```

## 10. Type Safety
When using TypeGen, the Portable Text value usually has a complex generated type. You can often use `any` or `PortableTextBlock[]` for the *prop*, but cast specific blocks if needed.

```typescript
import { PortableTextBlock } from "next-sanity";

type Props = {
  value: PortableTextBlock[];
};
```

## 11. Best Practices

- **Tailwind Typography:** For simple blogs, wrap `<PortableText />` in a `<div className="prose">` (from `@tailwindcss/typography`) instead of manually styling every block.
- **Handling Nulls:** Always check if `value` exists and is an array before rendering.
- **Keys:** The `PortableText` component handles React keys automatically using the `_key` from Sanity. Do not add keys manually.
- **Separate from Page Builder:** PTE blocks live in `body[]` (rich text fields), not `pageBuilder[]` (page layout). Keep these patterns separate.
