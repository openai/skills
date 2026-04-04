---
title: "Sanity Image Rules"
description: "Best practices for handling images in Sanity: Schema, URL generation, and Next.js Image integration."
---

# Sanity Image Rules

## 1. Schema Definition
**Always** enable `hotspot: true`. This allows editors to control cropping and the focal point.

```typescript
defineField({
  name: 'mainImage',
  title: 'Main Image',
  type: 'image',
  options: {
    hotspot: true // CRITICAL
  },
  fields: [
    defineField({
      name: 'alt',
      type: 'string',
      title: 'Alternative Text',
      validation: rule => rule.required().warning('Alt text is important for SEO')
    })
  ]
})
```

## 2. URL Builder (`urlFor`)
Use the Sanity Image URL Builder to generate optimized URLs (resize, crop, format).

**Setup (`sanity/lib/image.ts`):**
```typescript
import createImageUrlBuilder from '@sanity/image-url'
import { dataset, projectId } from '../env'

const builder = createImageUrlBuilder({ projectId, dataset })

export const urlFor = (source: any) => {
  return builder.image(source)
}
```

**Usage:** The URL builder automatically uses hotspot/crop data when available:
```typescript
const imageUrl = urlFor(mainImage)
  .width(800)
  .height(600)
  .fit('crop')  // Respects hotspot when cropping
  .url()
```

## 3. Next.js Image Component Pattern
Create a reusable `SanityImage` component that handles the `urlFor` logic and `next/image` props.

```typescript
import Image from 'next/image'
import { urlFor } from '@/sanity/lib/image'

interface SanityImageProps {
  value: any // SanityImageSource
  width?: number
  height?: number
  className?: string
  priority?: boolean
}

export function SanityImage({ value, width = 800, height, className, priority }: SanityImageProps) {
  if (!value?.asset) return null

  return (
    <Image
      className={className}
      src={urlFor(value)
        .width(width)
        .height(height || Math.round(width / 1.5)) // Default aspect ratio if no height
        .url()}
      alt={value.alt || ''}
      width={width}
      height={height || Math.round(width / 1.5)}
      priority={priority}
      // Optional: Use LQIP (Low Quality Image Placeholder)
      placeholder={value.asset.metadata?.lqip ? 'blur' : 'empty'}
      blurDataURL={value.asset.metadata?.lqip}
    />
  )
}
```

## 4. Querying Images

**Critical:** LQIP (Low Quality Image Placeholder) is **not automatic**. You must explicitly query it via `asset->{ metadata { lqip } }`.

### Minimal Query (No LQIP)
```groq
mainImage {
  asset->{ _id, url },
  alt
}
```

### Full Query (With LQIP & Dimensions)
```groq
mainImage {
  asset->{
    _id,
    url,
    metadata {
      lqip,                          // Base64 blur placeholder
      dimensions { width, height }   // For aspect ratio
    }
  },
  alt,
  hotspot,  // Include if using hotspot cropping
  crop      // Include if using cropping
}
```

**Why this matters:** Without querying `metadata.lqip`, the `blurDataURL` in your component will be `undefined` and the blur effect won't work.

## 5. Performance Tips
- **Auto Format:** Sanity CDN automatically serves WebP/AVIF if the browser supports it (no need to specify `.format('webp')` manually in most cases, but `next/image` handles this too).
- **Sizing:** Always request the exact size you need using `.width()` and `.height()` in `urlFor`. Don't download a 4000px image for a thumbnail.
