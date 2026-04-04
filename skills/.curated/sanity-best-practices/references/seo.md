---
title: Sanity SEO Best Practices
description: SEO best practices for Sanity with Next.js, including metadata, Open Graph, sitemaps, redirects, and JSON-LD structured data.
---

# Sanity SEO Best Practices

## 1. Core Philosophy

SEO doesn't require complex configurations. A few core principles, applied consistently:

- **Smart defaults with optional overrides** — Don't require SEO fields; use existing content as fallback
- **Use GROQ for fallback logic** — Move conditional logic into queries, not components
- **Leverage Next.js APIs** — Use `generateMetadata`, `sitemap.ts`, not manual `<meta>` tags
- **Structured content = structured data** — Your content model is already SEO-ready

## 2. SEO Schema Type (Reusable)

Create a reusable SEO object type for consistent metadata across document types.

```typescript
// schemaTypes/seoType.ts
import { defineField, defineType } from "sanity";

export const seoType = defineType({
  name: "seo",
  title: "SEO",
  type: "object",
  fields: [
    defineField({
      name: "title",
      description: "Overrides the page title if provided",
      type: "string",
    }),
    defineField({
      name: "description",
      type: "text",
      rows: 3,
    }),
    defineField({
      name: "image",
      description: "Image for social sharing (1200x630 recommended)",
      type: "image",
      options: { hotspot: true },
    }),
    defineField({
      name: "noIndex",
      description: "Hide this page from search engines",
      type: "boolean",
      initialValue: false,
    }),
  ],
});
```

**Usage in document types:**
```typescript
defineField({
  name: "seo",
  type: "seo",
})
```

## 3. GROQ Queries with Fallbacks

Use `coalesce()` to provide fallback values. This keeps frontend logic clean.

```groq
*[_type == "page" && slug.current == $slug][0]{
  ...,
  "seo": {
    // Use SEO field if provided, otherwise fall back to main title
    "title": coalesce(seo.title, title, ""),
    "description": coalesce(seo.description, ""),
    "image": seo.image,
    "noIndex": seo.noIndex == true
  }
}
```

**Key principle:** `seo.title` will never be `null` — it contains either the SEO override, the page title, or empty string.

## 4. Next.js Metadata (The Right Way)

Use `generateMetadata` — never render `<title>` or `<meta>` tags directly in components.

```typescript
// app/(frontend)/[slug]/page.tsx
import type { Metadata } from "next";
import { urlFor } from "@/sanity/lib/image";

type RouteProps = {
  params: Promise<{ slug: string }>;
};

// Extract fetch to reuse in both functions
const getPage = async (params: RouteProps["params"]) =>
  sanityFetch({
    query: PAGE_QUERY,
    params: await params,
    stega: false, // Critical for SEO!
  });

export async function generateMetadata({ params }: RouteProps): Promise<Metadata> {
  const { data: page } = await getPage(params);

  if (!page) return {};

  const metadata: Metadata = {
    title: page.seo.title,
    description: page.seo.description,
  };

  // Open Graph image
  if (page.seo.image) {
    metadata.openGraph = {
      images: {
        url: urlFor(page.seo.image).width(1200).height(630).url(),
        width: 1200,
        height: 630,
      },
    };
  }

  // noIndex robots directive
  if (page.seo.noIndex) {
    metadata.robots = "noindex";
  }

  return metadata;
}

export default async function Page({ params }: RouteProps) {
  const { data: page } = await getPage(params);
  // ... render page
}
```

**Critical:** Always set `stega: false` when fetching for metadata. Stega characters in `<title>` destroy SEO.

## 5. Dynamic Sitemap

Use Next.js `sitemap.ts` convention to auto-generate from Sanity content.

### GROQ Query
```groq
*[_type in ["page", "post"] && defined(slug.current) && seo.noIndex != true] {
  "href": select(
    _type == "page" => "/" + slug.current,
    _type == "post" => "/posts/" + slug.current,
    slug.current
  ),
  _updatedAt
}
```

### Route Implementation
```typescript
// app/sitemap.ts
import { MetadataRoute } from "next";
import { client } from "@/sanity/lib/client";
import { SITEMAP_QUERY } from "@/sanity/lib/queries";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : "http://localhost:3000";

  try {
    const paths = await client.fetch(SITEMAP_QUERY);
    if (!paths) return [];

    return paths.map((path) => ({
      url: new URL(path.href!, baseUrl).toString(),
      lastModified: new Date(path._updatedAt),
      changeFrequency: "weekly",
      priority: 1,
    }));
  } catch (error) {
    console.error("Sitemap generation failed:", error);
    return [];
  }
}
```

**Note:** Sitemap limit is 50,000 URLs per file. For larger sites, use sitemap index.

## 6. Redirects (Managed in Sanity)

Create a redirect document type for content team management.

### Schema
```typescript
// schemaTypes/redirectType.ts
import { defineField, defineType, SanityDocumentLike } from "sanity";
import { LinkIcon } from "@sanity/icons";

function isValidPath(value: string | undefined) {
  if (!value) return "Required";
  if (!value.startsWith("/")) return "Must start with /";
  if (/[^a-zA-Z0-9\-_/:]/.test(value)) return "Invalid characters";
  return true;
}

export const redirectType = defineType({
  name: "redirect",
  title: "Redirect",
  type: "document",
  icon: LinkIcon,
  validation: (Rule) =>
    Rule.custom((doc: SanityDocumentLike | undefined) => {
      if (doc?.source === doc?.destination) {
        return "Source and destination cannot be the same";
      }
      return true;
    }),
  fields: [
    defineField({
      name: "source",
      type: "string",
      validation: (Rule) => Rule.required().custom(isValidPath),
    }),
    defineField({
      name: "destination",
      type: "string",
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: "permanent",
      description: "301 (permanent) or 302 (temporary)",
      type: "boolean",
      initialValue: true,
    }),
    defineField({
      name: "isEnabled",
      type: "boolean",
      initialValue: true,
    }),
  ],
});
```

### Next.js Config
```typescript
// next.config.ts
import { fetchRedirects } from "@/sanity/lib/fetchRedirects";

const nextConfig: NextConfig = {
  async redirects() {
    return await fetchRedirects();
  },
};
```

**Limits:** Vercel allows max 1,024 redirects in `next.config`. For more, use middleware.

## 7. Dynamic Open Graph Images

Generate OG images on-the-fly using Next.js Edge Runtime at `/api/og`.

```typescript
// app/api/og/route.tsx
import { ImageResponse } from "next/og";
export const runtime = "edge";

export async function GET(request: Request) {
  const id = new URL(request.url).searchParams.get("id");
  if (!id) return new Response("Missing id", { status: 400 });

  const data = await client.fetch(`*[_id == $id][0]{ title }`, { id });

  return new ImageResponse(
    <div tw="flex w-full h-full bg-blue-500 text-white p-10">
      <h1 tw="text-6xl font-bold">{data?.title || "Untitled"}</h1>
    </div>,
    { width: 1200, height: 630 }
  );
}
```

Use as fallback in metadata: `url: page.seo.image ? urlFor(page.seo.image).url() : \`/api/og?id=\${page._id}\``

## 8. JSON-LD Structured Data

Use `schema-dts` for type-safe structured data.

```bash
npm install schema-dts
```

### FAQ Example
```typescript
import { FAQPage, WithContext } from "schema-dts";

const generateFaqData = (faqs: FAQ[]): WithContext<FAQPage> => ({
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqs.map((faq) => ({
    "@type": "Question",
    name: faq.title,
    acceptedAnswer: {
      "@type": "Answer",
      text: faq.text, // Use pt::text() in GROQ to get plain text
    },
  })),
});

// In component
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(generateFaqData(faqs)) }}
/>
```

### GROQ for Plain Text
```groq
faqs[]->{
  _id,
  title,
  body,
  "text": pt::text(body)  // Convert Portable Text to plain string
}
```

## 9. Testing Tools

- **Open Graph:** [opengraph.ing](https://opengraph.ing/)
- **Facebook:** [Sharing Debugger](https://developers.facebook.com/tools/debug/)
- **Twitter:** [Card Validator](https://cards-dev.twitter.com/validator)
- **LinkedIn:** [Post Inspector](https://www.linkedin.com/post-inspector/)
- **Sitemap:** [XML Sitemaps Validator](https://www.xml-sitemaps.com/validate-xml-sitemap.html)
