---
title: "Sanity + Shopify + Hydrogen Rules"
description: Integration guide for Sanity with Shopify using the Hydrogen framework (React Router 7).
---

# Sanity + Shopify + Hydrogen Rules

**Package:** [`hydrogen-sanity`](https://github.com/sanity-io/hydrogen-sanity) — requires `@shopify/hydrogen >= 2025.5.0`

## 1. Architecture Overview

| Component | Purpose |
|-----------|---------|
| **Shopify** | Product catalog, inventory, checkout (source of truth for commerce) |
| **Sanity Connect** | Syncs Shopify data to Sanity in real-time |
| **Sanity Studio** | Editorial content, rich descriptions, media (enhances Shopify data) |
| **Hydrogen** | React Router 7 front-end optimized for Shopify |

**Project Structure:**
```
./
├── /studio    # Sanity Studio
└── /web       # Hydrogen front-end
```

## 2. Environment Variables

```bash
# web/.env
PUBLIC_STOREFRONT_API_TOKEN="your-public-storefront-token"
PRIVATE_STOREFRONT_API_TOKEN="your-private-storefront-token"
PUBLIC_STORE_DOMAIN="your-store.myshopify.com"
SESSION_SECRET="your-random-session-secret"

# Sanity
SANITY_PROJECT_ID="your-project-id"
SANITY_DATASET="production"
SANITY_API_VERSION="2026-02-01"
SANITY_PREVIEW_TOKEN="your-sanity-viewer-token"  # Viewer token for previews
```

## 3. Sanity Client Setup

### Vite Config
```typescript
// web/vite.config.ts
import {hydrogen} from '@shopify/hydrogen/vite'
import {sanity} from 'hydrogen-sanity/vite'

export default defineConfig({
  plugins: [hydrogen(), sanity()],
})
```

### Context Setup
```typescript
// web/app/lib/context.ts
import {createSanityContext, type SanityContext} from 'hydrogen-sanity'
import {PreviewSession} from 'hydrogen-sanity/preview/session'
import {isPreviewEnabled} from 'hydrogen-sanity/preview'

const sanity = await createSanityContext({
  request,
  cache,
  waitUntil,
  client: {
    projectId: env.SANITY_PROJECT_ID,
    dataset: env.SANITY_DATASET,
    apiVersion: env.SANITY_API_VERSION || '2026-02-01',
    useCdn: true,
    stega: {
      enabled: isPreviewEnabled(env.SANITY_PROJECT_ID, previewSession),
      studioUrl: 'http://localhost:3333',
    }
  },
  preview: {
    token: env.SANITY_PREVIEW_TOKEN,
    session: previewSession,
  }
})
```

### Provider Setup (entry.server.tsx)
```typescript
const {SanityProvider} = context.sanity

const body = await renderToReadableStream(
  <NonceProvider>
    <SanityProvider>
      <ServerRouter context={reactRouterContext} url={request.url} nonce={nonce} />
    </SanityProvider>
  </NonceProvider>,
)
```

### Root Layout (root.tsx)
```typescript
import {Sanity} from 'hydrogen-sanity'

export function Layout({children}) {
  const nonce = useNonce()
  return (
    <html>
      <body>
        {children}
        <Sanity nonce={nonce} />  {/* Required for client-side */}
        <Scripts nonce={nonce} />
      </body>
    </html>
  )
}
```

## 4. Data Fetching

Fetch from **both** Shopify (GraphQL) and Sanity (GROQ). Use `defineQuery` for TypeGen support.

### Recommended: `query` + `Query` component
```typescript
import {defineQuery} from 'groq'
import {Query} from 'hydrogen-sanity'

const PRODUCT_QUERY = defineQuery(`*[_type == "product" && store.slug.current == $handle][0]{ body }`)

// Loader
export async function loader({params, context: {sanity}}: LoaderFunctionArgs) {
  const initial = await context.sanity.query(PRODUCT_QUERY, params)
  return {initial}
}

// Component - auto-enables live preview when active
export default function ProductPage({loaderData}) {
  return (
    <Query query={PRODUCT_QUERY} options={{initial: loaderData.initial}}>
      {(data) => <div>{data?.body}</div>}
    </Query>
  )
}
```

### Alternative methods
| Method | Use Case |
|--------|----------|
| `sanity.query()` + `Query` | Recommended - auto preview mode |
| `sanity.loadQuery()` | Manual loader integration |
| `sanity.fetch()` | No preview needed, lightweight |
| `sanity.client` | Mutations in actions |

### Images
```typescript
import {useImageUrl} from 'hydrogen-sanity'

function Hero({image}) {
  const imageUrl = useImageUrl(image)
  return <img src={imageUrl.width(1200).height(600).url()} />
}
```

**Key Insight:** Shopify fields synced via Sanity Connect are `readOnly`. Use Sanity for editorial enhancements only.

## 5. Visual Editing Setup

### Root Layout
```typescript
// web/app/root.tsx
import {usePreviewMode} from 'hydrogen-sanity/preview'
import {VisualEditing} from 'hydrogen-sanity/visual-editing'

export function Layout({children}: {children?: React.ReactNode}) {
  const previewMode = usePreviewMode()

  return (
    <html>
      <body>
        {children}
        {previewMode ? <VisualEditing action="/api/preview" /> : null}
      </body>
    </html>
  )
}
```

### Preview Route
```typescript
// web/app/routes/api.preview.ts
export {action, loader} from 'hydrogen-sanity/preview/route'
```

### Content Security Policy
```typescript
// web/entry.server.tsx
const {nonce, header, NonceProvider} = createContentSecurityPolicy({
  frameAncestors: isPreviewEnabled ? [studioHostname] : [],
  connectSrc: [
    `https://${projectId}.api.sanity.io`,
    `wss://${projectId}.api.sanity.io`,
  ],
})
```

## 6. Studio: Presentation Tool

```typescript
// studio/sanity.config.ts
import {presentationTool} from 'sanity/presentation'

export default defineConfig({
  plugins: [
    presentationTool({
      resolve: {
        locations: {
          product: defineLocations({
            select: { title: 'store.title', slug: 'store.slug.current' },
            resolve: (doc) => ({
              locations: [
                { title: doc?.title || 'Untitled', href: `/products/${doc?.slug}` },
                { title: 'Products', href: `/collections/all` },
              ],
            }),
          }),
        },
      },
      previewUrl: {
        origin: 'http://localhost:3000',
        previewMode: { enable: '/api/preview' },
      },
    }),
  ],
})
```

## 7. Commands

```bash
# Install dependencies
pnpm add hydrogen-sanity @sanity/client @portabletext/react

# Development (run in separate terminals)
cd studio && pnpm dev    # Studio at localhost:3333
cd web && pnpm dev       # Hydrogen at localhost:3000

# Sanity Manage (CORS, tokens)
pnpm dlx sanity manage
```

## 8. Boundaries

- Always:
  - Query Shopify for commerce data (price, inventory, variants)
  - Query Sanity for editorial content (rich text, custom fields)
  - Use `hydrogen-sanity` package for Visual Editing
  - Add Hydrogen URL to CORS origins in Sanity Manage

- Ask First:
  - Before modifying Sanity Connect sync settings
  - Before changing CSP configuration

- Never:
  - Edit Shopify-synced fields in Sanity (they're `readOnly`)
  - Expose `SANITY_API_TOKEN` to client-side code
  - Query Sanity for commerce data that should come from Shopify
