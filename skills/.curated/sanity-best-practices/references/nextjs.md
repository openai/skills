---
title: Next.js & Sanity Integration Rules
description: Integration guide for Next.js App Router, Live Content API, and Sanity Studio (Embedded or Standalone).
---

# Next.js & Sanity Integration Rules

## 1. Architecture Patterns

### Option A: Embedded Studio (Recommended)
**Best for:** Most Next.js projects. Unified deployment, simpler setup.

The Studio lives inside your Next.js app at `/app/studio/[[...tool]]/page.tsx`.
- **Config:** `sanity.config.ts` lives in the project root.
- See `project-structure.md` rule for detailed structure.

### Option B: Monorepo (Alternative)
**Best for:** Separation of concerns, multiple frontends, or strict dependency isolation.

The Studio and Next.js app live in separate folders:
```
apps/
├── studio/     # Sanity Studio (standalone)
└── web/        # Next.js frontend
```

- **Config:** Add your Next.js app URL to **CORS Origins** in Sanity project settings.
- See `project-structure.md` rule for detailed structure.

## 2. Data Fetching (Live Content API)

We use `defineLive` (next-sanity v11+) to enable real-time content updates and Visual Editing automatically.

### Setup (`src/sanity/lib/live.ts`)

```typescript
import { defineLive } from 'next-sanity'
import { client } from './client'

export const { sanityFetch, SanityLive } = defineLive({
  client: client.withConfig({
    apiVersion: '2026-02-01'
  }),
  serverToken: process.env.SANITY_API_READ_TOKEN,
  browserToken: process.env.SANITY_API_READ_TOKEN,
})
```

### Rendering (`src/app/layout.tsx`)

You **must** render `<SanityLive />` in the root layout to enable real-time updates.

```typescript
import { SanityLive } from '@/sanity/lib/live'
import { VisualEditing } from 'next-sanity/visual-editing'
import { draftMode } from 'next/headers'

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <SanityLive />
        {(await draftMode()).isEnabled && <VisualEditing />}
      </body>
    </html>
  )
}
```

## 3. Caching & Revalidation

### Prefer Live Content API (Default)

**Use `defineLive` by default.** It handles fetching, caching, and invalidation automatically. Only implement manual caching when you need fine-grained control.

### When to Use Manual Caching

| Scenario | Approach |
|----------|----------|
| Real-time updates, Visual Editing | `defineLive` (default) |
| Static marketing pages, rarely updated | Time-based revalidation |
| Blog posts, products with frequent edits | Tag-based revalidation |
| Critical accuracy (stock levels, prices) | Path-based + short revalidation |

### Debugging: Enable Fetch Logging

See every fetch with cache HIT/MISS status:

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
};
```

Console output shows cache status:
```text
GET /posts 200 in 39ms
 │ GET https://...apicdn.sanity.io/... 200 in 5ms (cache hit)
```

### Sanity CDN vs API

| Setting | Speed | Freshness | Use When |
|---------|-------|-----------|----------|
| `useCdn: true` | Fast | May have brief delay | Default for all runtime fetches |
| `useCdn: false` | Slower | Guaranteed fresh | `generateStaticParams`, webhooks |

Override per-request:
```typescript
// For static generation, use API directly
export async function generateStaticParams() {
  const slugs = await client
    .withConfig({ useCdn: false })
    .fetch(SLUGS_QUERY);
  return slugs;
}
```

### Manual `sanityFetch` Helper (Advanced)

For manual caching control, create a wrapper:

```typescript
// src/sanity/lib/client.ts
export async function sanityFetch<const QueryString extends string>({
  query,
  params = {},
  revalidate = 60,
  tags = [],
}: {
  query: QueryString;
  params?: QueryParams;
  revalidate?: number | false;
  tags?: string[];
}) {
  return client.fetch(query, params, {
    next: {
      revalidate: tags.length ? false : revalidate,
      tags,
    },
  });
}
```

### Time-Based Revalidation

Simple and predictable. Good for content that changes infrequently.

```typescript
const posts = await sanityFetch({
  query: POSTS_QUERY,
  revalidate: 3600, // Revalidate every hour
});
```

**The "Typo Problem":** With time-based only, content authors may wait up to an hour to see changes. Use webhooks for instant updates.

### Path-Based Revalidation

Surgically revalidate specific routes when documents change.

**1. Create API Route:**
```typescript
// src/app/api/revalidate/path/route.ts
import { revalidatePath } from 'next/cache';
import { type NextRequest, NextResponse } from 'next/server';
import { parseBody } from 'next-sanity/webhook';

type WebhookPayload = { path?: string };

export async function POST(req: NextRequest) {
  try {
    const { isValidSignature, body } = await parseBody<WebhookPayload>(
      req,
      process.env.SANITY_REVALIDATE_SECRET,
      true // Add delay to allow CDN to update
    );

    if (!isValidSignature) {
      return new Response('Invalid signature', { status: 401 });
    }
    if (!body?.path) {
      return new Response('Missing path', { status: 400 });
    }

    revalidatePath(body.path);
    return NextResponse.json({ revalidated: body.path });
  } catch (err) {
    return new Response((err as Error).message, { status: 500 });
  }
}
```

**2. Create GROQ-Powered Webhook:**
- URL: `https://yoursite.com/api/revalidate/path`
- Filter: `_type in ["post"]`
- Projection: `{ "path": "/posts/" + slug.current }`
- Add `SANITY_REVALIDATE_SECRET` to webhook and `.env.local`

### Tag-Based Revalidation

"Update once, revalidate everywhere" — best for referenced content.

**1. Tag Your Queries:**
```typescript
// Posts index - revalidate when ANY post, author, or category changes
const posts = await sanityFetch({
  query: POSTS_QUERY,
  tags: ['post', 'author', 'category'],
});

// Individual post - more granular, includes slug-specific tag
const post = await sanityFetch({
  query: POST_QUERY,
  params,
  tags: [`post:${params.slug}`, 'author', 'category'],
});
```

**2. Create API Route:**
```typescript
// src/app/api/revalidate/tag/route.ts
import { revalidateTag } from 'next/cache';
import { type NextRequest, NextResponse } from 'next/server';
import { parseBody } from 'next-sanity/webhook';

type WebhookPayload = { tags: string[] };

export async function POST(req: NextRequest) {
  try {
    const { isValidSignature, body } = await parseBody<WebhookPayload>(
      req,
      process.env.SANITY_REVALIDATE_SECRET,
      true
    );

    if (!isValidSignature) {
      return new Response('Invalid signature', { status: 401 });
    }
    if (!Array.isArray(body?.tags) || !body.tags.length) {
      return new Response('Missing tags', { status: 400 });
    }

    body.tags.forEach((tag) => revalidateTag(tag));
    return NextResponse.json({ revalidated: body.tags });
  } catch (err) {
    return new Response((err as Error).message, { status: 500 });
  }
}
```

**3. Create GROQ-Powered Webhook:**
- URL: `https://yoursite.com/api/revalidate/tag`
- Filter: `_type in ["post", "author", "category"]`
- Projection: `{ "tags": [_type, _type + ":" + slug.current] }`

### Stale Data After Webhook?

Webhooks fire *before* Sanity CDN updates. If you see stale data:

1. **Add delay** — Pass `true` as third arg to `parseBody`
2. **Or bypass CDN** — Set `useCdn: false` in client config (use sparingly)

## 4. Visual Editing (Stega) & Clean Data

Visual Editing injects invisible characters into strings to enable click-to-edit.

### A. The Golden Rule of Stega

If a string field controls logic (alignment, colors, IDs), you **must** clean it before comparing.

```typescript
import { stegaClean } from "@sanity/client/stega";

export function Layout({ align }: { align: string }) {
  // ❌ Bad: Will fail in Edit Mode due to invisible chars
  // if (align === 'center') ...

  // ✅ Good: Clean the value first
  const cleanAlign = stegaClean(align);
  return <div className={cleanAlign === 'center' ? 'mx-auto' : ''} />
}
```

### B. Metadata & SEO (Critical)

**Never** let Stega characters leak into `<head>` tags. Always set `stega: false` for metadata fetching.

```typescript
export async function generateMetadata({ params }) {
  const { data } = await sanityFetch({
    query: SEO_QUERY,
    params: await params,
    stega: false // 👈 Critical for SEO
  })
  return { title: data?.title }
}
```

### C. Static Params

When generating static params, fetch only published content and disable stega.

```typescript
export async function generateStaticParams() {
  const { data } = await sanityFetch({
    query: SLUGS_QUERY,
    perspective: 'published', // 👈 No drafts
    stega: false
  })
  return data
}
```

## 5. Setup: Embedded Studio

Mount the Studio on a Next.js route.

**`src/app/studio/[[...tool]]/page.tsx`:**

```typescript
import { NextStudio } from 'next-sanity/studio'
import config from '../../../../sanity.config'

export const dynamic = 'force-static'
export { metadata, viewport } from 'next-sanity/studio'

export default function StudioPage() {
  return <NextStudio config={config} />
}
```

## 6. Setup: Draft Mode

Enable Presentation Tool and Visual Editing by setting up a draft mode route.

**`src/app/api/draft-mode/enable/route.ts`:**

```typescript
import { client } from '@/sanity/lib/client'
import { defineEnableDraftMode } from 'next-sanity/draft-mode'
import { token } from '@/sanity/lib/token' // Helper to get token

export const { GET } = defineEnableDraftMode({
  client: client.withConfig({ token }),
})
```

## 7. Error Handling

Use `notFound()` for missing documents. Common errors:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/missing token | Check `SANITY_API_READ_TOKEN` |
| 403 Forbidden | CORS not configured | Add URL to CORS origins |
| Query syntax error | Invalid GROQ | Test in Vision plugin first |
| Empty result | Wrong filter/params | Log params, check `_type` spelling |

```typescript
import { notFound } from 'next/navigation'

export default async function PostPage({ params }: Props) {
  const { data } = await sanityFetch({ query: POST_QUERY, params: await params })
  if (!data) notFound()
  return <Post data={data} />
}
```

## 8. Presentation Queries (`usePresentationQuery`)

For faster live editing in the Presentation Tool, use `usePresentationQuery` to fetch only the specific block being edited, rather than re-rendering the entire page.

### Why Use This

- **Without:** Editing a hero title re-fetches the whole page, re-renders all blocks
- **With:** Only the hero block re-fetches and re-renders

This is especially valuable for pages with many Page Builder blocks or complex Portable Text.

### Basic Pattern

```typescript
'use client'
import { usePresentationQuery } from 'next-sanity/hooks'
import { HERO_PRESENTATION_QUERY } from '@/sanity/lib/queries'

type HeroProps = {
  _key: string
  documentId: string
  title: string
  subtitle?: string
  // ... other initial props from page query
}

export function Hero({ _key, documentId, title, subtitle, ...rest }: HeroProps) {
  // Fetch block-specific data for faster updates in Presentation Tool
  const { data } = usePresentationQuery({
    query: HERO_PRESENTATION_QUERY,
    params: { documentId, blockKey: _key },
  })

  // Use presentation data if available, fallback to initial server props
  const blockData = data?.heroBlock || { title, subtitle, ...rest }

  return (
    <section>
      <h1>{blockData.title}</h1>
      {blockData.subtitle && <p>{blockData.subtitle}</p>}
    </section>
  )
}
```

### The Presentation Query

Create a query that targets the specific block by `_key`:

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
      theme,
      // Include all fields the component needs
    }
  }
`)
```

### Passing Document Context

Your PageBuilder component needs to pass `documentId` to each block:

```typescript
export function PageBuilder({ content, documentId }: { content: Block[]; documentId: string }) {
  return (
    <main>
      {content.map((block) => {
        switch (block._type) {
          case "hero":
            return <Hero key={block._key} documentId={documentId} {...block} />
          // ... other blocks
        }
      })}
    </main>
  )
}
```

### For Portable Text Blocks

The same pattern works for custom blocks inside Portable Text:

```typescript
export const PTE_IMAGE_PRESENTATION_QUERY = defineQuery(`
  *[_id == $documentId][0]{
    "pteImageBlock": body[_key == $blockKey && _type == "pteImage"][0]{
      image,
      caption,
      alt
    }
  }
`)
```

**See also:** `visual-editing.md` for the conceptual overview and `page-builder.md` for full Page Builder patterns.

## 9. Pagination Pattern

For listing pages with many entries, use offset-based pagination with a count query.

### Queries
```typescript
// Paginated listing
export const ARTICLES_QUERY = defineQuery(`
  *[_type == "article" && defined(slug.current)]
  | order(date desc) [$start...$end] {
    _id, title, "slug": slug.current, date
  }
`);

// Total count for pagination UI
export const ARTICLES_COUNT_QUERY = defineQuery(`
  count(*[_type == "article" && defined(slug.current)])
`);
```

### Listing Page
```typescript
const ENTRIES_PER_PAGE = 10;

export default async function BlogPage({
  searchParams
}: {
  searchParams: Promise<{ page?: string }>
}) {
  const { page: pageParam } = await searchParams;
  const page = parseInt(pageParam || "1");
  const start = (page - 1) * ENTRIES_PER_PAGE;
  const end = start + ENTRIES_PER_PAGE;

  const [{ data: articles }, { data: total }] = await Promise.all([
    sanityFetch({ query: ARTICLES_QUERY, params: { start, end } }),
    sanityFetch({ query: ARTICLES_COUNT_QUERY })
  ]);

  const totalPages = Math.ceil(total / ENTRIES_PER_PAGE);

  return (
    <main>
      {articles.map(article => (
        <ArticleCard key={article._id} article={article} />
      ))}
      <Pagination current={page} total={totalPages} />
    </main>
  );
}
```
