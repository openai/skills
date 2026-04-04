---
title: React Router (Remix) & Sanity Integration Rules
description: Integration guide for React Router (formerly Remix) with Sanity, including Loaders and Visual Editing.
---

# React Router (Remix) & Sanity Integration Rules

## Version Note

This guide covers both:
- **Remix v2** (`@remix-run/*` packages)
- **React Router v7** (the successor to Remix, `react-router` package)

The Sanity integration pattern is the same for both. Import paths differ slightly:

| Remix v2 | React Router v7 |
|----------|-----------------|
| `@remix-run/node` | `react-router` |
| `@remix-run/react` | `react-router` |
| `remix.config.js` | `react-router.config.ts` |

The examples below use Remix v2 imports. Adjust if using React Router v7.

## 1. Setup & Client Pattern

To support both server-side fetching and client-side live previews, use the **Split Loader Pattern**.

### A. Shared Loader (`app/sanity/loader.ts`)
Defines the store config (SSR enabled, client deferred).

```typescript
import { createQueryStore } from '@sanity/react-loader'

export const {
  loadQuery,
  setServerClient,
  useQuery,
  useLiveMode,
} = createQueryStore({ client: false, ssr: true })
```

### B. Server Loader (`app/sanity/loader.server.ts`)
Initializes the server client.

```typescript
import { createClient } from '@sanity/client'
import { loadQuery, setServerClient } from './loader'

const client = createClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: process.env.SANITY_DATASET,
  useCdn: true,
  apiVersion: '2026-02-01',
  stega: {
    enabled: true,
    studioUrl: 'https://my-studio-url.com',
  },
})

setServerClient(client)

export { loadQuery }
```

## 2. Data Fetching (Loaders)

Use `loadQuery` from your **server** file in route loaders.

```typescript
import type { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { loadQuery } from "~/sanity/loader.server";
import { POSTS_QUERY } from "~/sanity/queries";

export async function loader({ params }: LoaderFunctionArgs) {
  const initial = await loadQuery(POSTS_QUERY, params);
  return { initial, query: POSTS_QUERY, params };
}

export default function Index() {
  const { initial, query, params } = useLoaderData<typeof loader>();
  // ... pass to component
}
```

## 3. Real-time Preview & Visual Editing

### A. Use `useQuery` in Components
Import `useQuery` from your **shared** loader file.

```typescript
import { useQuery } from "~/sanity/loader";

export default function Page() {
  const { initial, query, params } = useLoaderData<typeof loader>();

  const { data, encodeDataAttribute } = useQuery(query, params, {
    initial
  });

  return (
    <h1 data-sanity={encodeDataAttribute('title')}>
      {data?.title}
    </h1>
  );
}
```

### B. Enable Live Mode (`VisualEditing.tsx`)
Create a component to handle the connection.

```typescript
import { enableVisualEditing } from '@sanity/visual-editing'
import { useLiveMode } from '~/sanity/loader'
import { client } from '~/sanity/client' // Your browser-safe client
import { useEffect } from 'react'

export default function VisualEditing() {
  useEffect(() => enableVisualEditing(), [])
  useLiveMode({ client })
  return null
}
```

Render this component in `root.tsx` only when valid (e.g., check env vars or user session).

## 4. Stega Cleaning
When using data for logic (routing, classNames), use `stegaClean`.

```typescript
import { stegaClean } from "@sanity/client/stega"
// ...
if (stegaClean(slug) === 'home') { ... }
```
