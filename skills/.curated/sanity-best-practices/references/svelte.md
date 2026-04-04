---
title: "SvelteKit & Sanity Integration Rules"
description: Integration guide for SvelteKit with Sanity, including @sanity/svelte-loader, Visual Editing, and Preview Mode.
---

# SvelteKit & Sanity Integration Rules

## 1. Setup & Configuration

### Installation
```bash
npm install @sanity/svelte-loader @sanity/client @sanity/visual-editing
```

### Client Configuration (`src/lib/sanity.ts`)
Define the client with `stega` enabled for the studio URL.

```typescript
import { createClient } from '@sanity/client'
import { PUBLIC_SANITY_PROJECT_ID, PUBLIC_SANITY_DATASET, PUBLIC_SANITY_API_VERSION, PUBLIC_SANITY_STUDIO_URL } from '$env/static/public'

export const client = createClient({
  projectId: PUBLIC_SANITY_PROJECT_ID,
  dataset: PUBLIC_SANITY_DATASET,
  apiVersion: PUBLIC_SANITY_API_VERSION,
  useCdn: true,
  stega: {
    studioUrl: PUBLIC_SANITY_STUDIO_URL,
  },
})
```

### Server Client (`src/lib/server/sanity.ts`)
Use the read token for fetching preview content.

```typescript
import { SANITY_API_READ_TOKEN } from '$env/static/private'
import { client } from '$lib/sanity'

export const serverClient = client.withConfig({
  token: SANITY_API_READ_TOKEN,
  stega: true, // Optional: enable stega on server too if needed
})
```

## 2. Hooks & Request Handler (Critical)

You **must** configure `createRequestHandler` in `src/hooks.server.ts` to handle preview sessions and inject `loadQuery` into locals.

```typescript
// src/hooks.server.ts
import { createRequestHandler, setServerClient } from '@sanity/svelte-loader'
import { serverClient } from '$lib/server/sanity'

setServerClient(serverClient)

export const handle = createRequestHandler()
```

**Update `app.d.ts` types:**
```typescript
import type { LoaderLocals } from '@sanity/svelte-loader'

declare global {
  namespace App {
    interface Locals extends LoaderLocals {}
  }
}
```

## 3. Preview State Propagation

Pass the preview state from the server to the client via the root layout.

**Server Layout (`src/routes/+layout.server.ts`):**
```typescript
import type { LayoutServerLoad } from './$types'

export const load: LayoutServerLoad = ({ locals: { preview } }) => {
  return { preview }
}
```

**Client Layout (`src/routes/+layout.ts`):**
```typescript
import { setPreviewing } from '@sanity/svelte-loader'
import type { LayoutLoad } from './$types'

export const load: LayoutLoad = ({ data: { preview } }) => {
  setPreviewing(preview)
}
```

## 4. Data Fetching (Loaders)

Use `locals.loadQuery` in your page server loaders.

```typescript
// src/routes/[slug]/+page.server.ts
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ locals: { loadQuery }, params }) => {
  const initial = await loadQuery(QUERY, params)
  return { initial }
}
```

## 5. Real-time Preview & Visual Editing

### Component Usage (`useQuery`)
Use `useQuery` in your Svelte component to handle real-time updates.

```svelte
<!-- src/routes/[slug]/+page.svelte -->
<script lang="ts">
  import { useQuery } from '@sanity/svelte-loader'
  import type { PageData } from './$types'

  export let data: PageData
  const { initial } = data

  // Hydrate with initial data
  const query = useQuery(initial)

  // Reactive data access
  $: ({ data: post, loading, encodeDataAttribute } = $query)
</script>

{#if !loading && post}
  <!-- Use encodeDataAttribute for overlays -->
  <h1 data-sanity={encodeDataAttribute('title')}>
    {post.title}
  </h1>
{/if}
```

### Enable Visual Editing (`+layout.svelte`)
Enable Visual Editing and Live Mode in your root layout.

```svelte
<script lang="ts">
  import { useLiveMode } from '@sanity/svelte-loader'
  import { enableVisualEditing } from '@sanity/visual-editing'
  import { PUBLIC_SANITY_STUDIO_URL } from '$env/static/public'
  import { onMount } from 'svelte'

  onMount(() => enableVisualEditing())

  onMount(() => useLiveMode({
    studioUrl: PUBLIC_SANITY_STUDIO_URL
  }))
</script>

<slot />
```
