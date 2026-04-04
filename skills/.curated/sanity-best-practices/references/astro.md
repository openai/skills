---
title: Astro & Sanity Integration Rules
description: Integration guide for Astro, including @sanity/astro, visual editing, and data fetching.
---

# Astro & Sanity Integration Rules

## 1. Setup & Configuration

### Configuration (`astro.config.mjs`)
Use the official `@sanity/astro` integration.

```javascript
import { defineConfig } from "astro/config";
import sanity from "@sanity/astro";

export default defineConfig({
  integrations: [
    sanity({
      projectId: "YOUR_PROJECT_ID",
      dataset: "production",
      useCdn: false, // False for static builds
      studioBasePath: "/admin", // If embedding Studio
    }),
  ],
});
```

### Client Type Safety
Enable types in `tsconfig.json`.

```json
{
  "compilerOptions": {
    "types": ["@sanity/astro/module"]
  }
}
```

## 2. Data Fetching

### Basic Fetching
Use `sanityClient` from `sanity:client` in the frontmatter of your `.astro` files.

```astro
---
import { sanityClient } from "sanity:client";
import { defineQuery } from "groq";

const POSTS_QUERY = defineQuery(`*[_type == "post"]{title, slug}`);
const posts = await sanityClient.fetch(POSTS_QUERY);
---
<ul>
  {posts.map(post => <li>{post.title}</li>)}
</ul>
```

### Helper Functions
It's best practice to abstract queries into a utility file (e.g., `src/utils/sanity.ts`).

```typescript
import { sanityClient } from "sanity:client";
import { defineQuery } from "groq";

const POSTS_QUERY = defineQuery(`*[_type == "post" && defined(slug.current)]`);

export async function getPosts() {
  return await sanityClient.fetch(POSTS_QUERY);
}
```

## 3. Portable Text
Use `astro-portabletext` for rendering rich text.

```astro
---
import { PortableText } from "astro-portabletext";
const { body } = Astro.props;
---
<div class="prose">
  <PortableText value={body} />
</div>
```

## 4. Image Handling
Use `@sanity/image-url` to generate optimized image URLs.

```typescript
import imageUrlBuilder from "@sanity/image-url";
import { sanityClient } from "sanity:client";

const builder = imageUrlBuilder(sanityClient);

export function urlFor(source) {
  return builder.image(source);
}
```

## 5. Visual Editing (Live Preview)
Astro handles visual editing slightly differently depending on if you are using Hybrid or Static mode.

### Setup
Ensure `stega` is enabled in your client configuration if you want clickable overlays.

For real-time updates in the presentation tool, you typically need a React component wrapper (since Astro components don't re-render on the client) or use the View Transitions API with a loader.

*Note: The `@sanity/astro` integration is evolving. Check the latest docs for "Visual Editing" support.*
