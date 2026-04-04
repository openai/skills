---
title: Nuxt & Sanity Integration Rules
description: Integration guide for Nuxt, including @nuxtjs/sanity, visual editing, and data fetching.
---

# Nuxt & Sanity Integration Rules

## 1. Setup & Configuration

### Configuration (`nuxt.config.ts`)
Use the official `@nuxtjs/sanity` module.

**Important:** Ensure the `minimal` client is NOT enabled if you want full features.

```typescript
export default defineNuxtConfig({
  modules: ["@nuxtjs/sanity"],
  sanity: {
    projectId: process.env.NUXT_SANITY_PROJECT_ID,
    dataset: process.env.NUXT_SANITY_DATASET,
    apiVersion: "2026-02-01",
    // Live Visual Editing Configuration
    visualEditing: {
      studioUrl: process.env.NUXT_SANITY_STUDIO_URL,
      token: process.env.NUXT_SANITY_API_READ_TOKEN, // Required for fetching drafts
      stega: true, // Enable stega for visual editing
      mode: 'live-visual-editing', // Default: enables live updates
    },
  },
});
```

## 2. Data Fetching

### `useSanityQuery`
Use the composable provided by the module for reactive fetching. It automatically handles preview state when configured.

```vue
<script setup lang="ts">
const query = groq`*[_type == "post"]{title, slug}`;
const { data: posts } = await useSanityQuery(query);
</script>

<template>
  <ul>
    <li v-for="post in posts" :key="post._id">{{ post.title }}</li>
  </ul>
</template>
```

## 3. Visual Editing (Live Preview)

### Automatic Setup
When `visualEditing` is configured in `nuxt.config.ts`, the module handles:
1.  Injecting the Visual Editing overlays.
2.  Refreshing data when content changes in the Studio.
3.  Enabling Stega encoding.

### Handling Stega in Logic
Just like Next.js, if you use stega-encoded strings in logic (e.g. `v-if="post.layout === 'full'"`), you must clean them.

```typescript
import { stegaClean } from "@sanity/client/stega";

const layout = computed(() => stegaClean(props.layout));
```

## 4. Components

### Portable Text
Use the `<PortableText>` component (if installed via `@portabletext/vue` or provided by the module).

```vue
<PortableText :value="post.body" :components="customComponents" />
```

### Images
Use `@sanity/image-url` helper or a dedicated image component.

```typescript
import imageUrlBuilder from '@sanity/image-url'
const builder = imageUrlBuilder(useSanity().client)
// ... url generation logic
```
