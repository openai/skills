---
title: Sanity App SDK
description: Rules for building custom applications with the Sanity App SDK, including React hooks, document handles, real-time patterns, and Suspense best practices.
---

# Sanity App SDK

Build custom React applications that interact with Sanity content in real-time.

## Tech Stack

- **Framework:** React 19+, TypeScript
- **Packages:** `@sanity/sdk`, `@sanity/sdk-react`
- **Optional UI:** `@sanity/ui`, `styled-components`
- **Runtime:** Node.js 20+

## Commands

```bash
# Basic quickstart
npx sanity@latest init --template app-quickstart --organization <your-org-id> --output-path . --typescript --skip-mcp

# With Sanity UI components
npx sanity@latest init --template app-sanity-ui --organization <your-org-id> --output-path . --typescript --skip-mcp

# Start development server
npm run dev

# Deploy to Sanity
npx sanity@latest deploy

# Install Sanity UI
npm install @sanity/ui styled-components
```

## Project Structure

```
my-app/
├── sanity.cli.ts        # CLI config (org ID, entry point)
├── src/
│   ├── App.tsx          # Root component with SanityApp provider
│   ├── App.css          # Global styles
│   └── components/      # Your components
├── package.json
└── tsconfig.json
```

## Boundaries

- **Always:** Wrap data-fetching components in `<Suspense>`, use `documentId` as React `key`, read/write directly to Content Lake (not local state)
- **Always:** Use `useDocuments` for lists, `useDocumentProjection` for display, `useDocument` + `useEditDocument` for editing
- **Ask first:** Before using `useQuery` with raw GROQ (prefer `useDocuments` + `useDocumentProjection`)
- **Ask first:** Before adding multiple data-fetching hooks in a single component
- **Never:** Use `useState` for form values that should sync with Content Lake
- **Never:** Use array index as React `key` for document lists (breaks real-time updates)
- **Never:** Forget the `fallback` prop on `<SanityApp>` and `<Suspense>` boundaries

---

## Configuration

### CLI Config (`sanity.cli.ts`)

```typescript
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  app: {
    organizationId: 'your-org-id',
    entry: './src/App.tsx',
  },
})
```

### App Root (`src/App.tsx`)

```typescript
import { SanityApp, type SanityConfig } from '@sanity/sdk-react'

export default function App() {
  const config: SanityConfig[] = [
    {
      projectId: 'your-project-id',
      dataset: 'production',
    },
  ]

  return (
    <SanityApp config={config} fallback={<div>Loading...</div>}>
      <YourComponents />
    </SanityApp>
  )
}
```

### With Sanity UI

```typescript
import { SanityApp, type SanityConfig } from '@sanity/sdk-react'
import { ThemeProvider } from '@sanity/ui'
import { buildTheme } from '@sanity/ui/theme'

const theme = buildTheme()

export default function App() {
  const config: SanityConfig[] = [
    { projectId: 'your-project-id', dataset: 'production' },
  ]

  return (
    <ThemeProvider theme={theme}>
      <SanityApp config={config} fallback={<div>Loading...</div>}>
        <YourComponents />
      </SanityApp>
    </ThemeProvider>
  )
}
```

### Environment Variables

Prefix with `SANITY_APP_` for automatic bundling:

```bash
SANITY_APP_PROJECT_ID=abc123
SANITY_APP_DATASET=production
```

Access: `process.env.SANITY_APP_PROJECT_ID`

---

## Document Handles

Lightweight references to documents. Fetch handles first, then load content as needed.

```typescript
interface DocumentHandle {
  documentId: string
  documentType: string
  projectId?: string
  dataset?: string
}
```

### Creating Handles

```typescript
// Best: From useDocuments hook
const { data: handles } = useDocuments({ documentType: 'article' })

// Good: With helper (preserves literal types for TypeGen)
import { createDocumentHandle } from '@sanity/sdk'
const handle = createDocumentHandle({
  documentId: 'my-doc-id',
  documentType: 'article',
})

// Good: With as const (preserves literal types)
const handle = {
  documentId: 'my-doc-id',
  documentType: 'article',
} as const
```

---

## Hook Selection

| Hook | Use Case | Returns |
|------|----------|---------|
| `useDocuments` | List of documents (infinite scroll) | Document handles |
| `usePaginatedDocuments` | Paginated lists with page controls | Document handles |
| `useDocument` | Single document, real-time editing | Full document or field |
| `useDocumentProjection` | Specific fields, display only | Projected data |
| `useQuery` | Complex GROQ queries (use sparingly) | Raw query results |

---

## Code Patterns

### Fetching a Document List

```typescript
// Good: Fetch handles, render items with Suspense
import { Suspense } from 'react'
import { useDocuments } from '@sanity/sdk-react'

function ArticleList() {
  const { data, hasMore, loadMore, isPending } = useDocuments({
    documentType: 'article',
    batchSize: 10,
    orderings: [{ field: '_updatedAt', direction: 'desc' }],
  })

  return (
    <>
      <ul>
        {data.map((handle) => (
          <Suspense key={handle.documentId} fallback={<li>Loading...</li>}>
            <ArticleItem {...handle} />
          </Suspense>
        ))}
      </ul>
      {hasMore && (
        <button onClick={loadMore} disabled={isPending}>
          Load More
        </button>
      )}
    </>
  )
}
```

```typescript
// Bad: Over-fetching with raw GROQ, no pagination
function BadArticleList() {
  const { data } = useQuery(`*[_type == "article"]`)
  return data?.map((doc, i) => <li key={i}>{doc.title}</li>)
}
```

### Projecting Content from a Handle

```typescript
// Good: Project only needed fields
import { useDocumentProjection, type DocumentHandle } from '@sanity/sdk-react'

function ArticleItem(handle: DocumentHandle) {
  const { data } = useDocumentProjection({
    ...handle,
    projection: `{
      title,
      "authorName": author->name,
      "imageUrl": image.asset->url
    }`,
  })

  if (!data) return null

  return (
    <li>
      <h2>{data.title}</h2>
      <p>By {data.authorName}</p>
    </li>
  )
}
```

### Real-time Editing

```typescript
// Good: Read and write directly to Content Lake
import { useDocument, useEditDocument, type DocumentHandle } from '@sanity/sdk-react'

function TitleInput(handle: DocumentHandle) {
  const { data: title } = useDocument({ ...handle, path: 'title' })
  const editTitle = useEditDocument({ ...handle, path: 'title' })

  return (
    <input
      type="text"
      value={title ?? ''}
      onChange={(e) => editTitle(e.currentTarget.value)}
    />
  )
}
```

```typescript
// Bad: Local state with submit button - causes stale data
function BadTitleForm(handle: DocumentHandle) {
  const [value, setValue] = useState('')
  const editTitle = useEditDocument({ ...handle, path: 'title' })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    editTitle(value) // Only writes on submit!
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <button type="submit">Save</button>
    </form>
  )
}
```

### Document Actions

```typescript
import {
  useApplyDocumentActions,
  publishDocument,
  unpublishDocument,
  deleteDocument,
} from '@sanity/sdk-react'

function DocumentActions({ handle }: { handle: DocumentHandle }) {
  const apply = useApplyDocumentActions()

  return (
    <div>
      <button onClick={() => apply(publishDocument(handle))}>Publish</button>
      <button onClick={() => apply(unpublishDocument(handle))}>Unpublish</button>
      <button onClick={() => apply(deleteDocument(handle))}>Delete</button>
    </div>
  )
}
```

---

## Suspense Patterns

The App SDK uses React Suspense. Every data-fetching component must be wrapped.

### One Hook Per Component

```typescript
// Good: Separate fetchers into separate components
function EventsAndVenues() {
  return (
    <>
      <Suspense fallback="Loading events...">
        <EventsList />
      </Suspense>
      <Suspense fallback="Loading venues...">
        <VenuesList />
      </Suspense>
    </>
  )
}

function EventsList() {
  const { data } = useDocuments({ documentType: 'event' })
  return <List items={data} />
}

function VenuesList() {
  const { data } = useDocuments({ documentType: 'venue' })
  return <List items={data} />
}
```

```typescript
// Bad: Multiple fetchers in one component
function BadComponent() {
  const { data: events } = useDocuments({ documentType: 'event' })
  const { data: venues } = useDocuments({ documentType: 'venue' })
  // Both trigger Suspense together, causing unnecessary re-renders
}
```

### Prevent Layout Shift

```typescript
// Good: Fallback matches final component dimensions
const BUTTON_TEXT = 'Open in Studio'

export function OpenInStudio({ handle }: { handle: DocumentHandle }) {
  return (
    <Suspense fallback={<Button text={BUTTON_TEXT} disabled />}>
      <OpenInStudioButton handle={handle} />
    </Suspense>
  )
}

function OpenInStudioButton({ handle }: { handle: DocumentHandle }) {
  const { navigateToStudioDocument } = useNavigateToStudioDocument(handle)
  return <Button onClick={navigateToStudioDocument} text={BUTTON_TEXT} />
}
```

---

## Event Handling

```typescript
import { useDocumentEvent, DocumentEvent } from '@sanity/sdk-react'

function DocumentWatcher(handle: DocumentHandle) {
  useDocumentEvent({
    ...handle,
    onEvent: (event) => {
      switch (event.type) {
        case 'edited':
          console.log('Edited:', event.documentId)
          break
        case 'published':
          console.log('Published:', event.documentId)
          break
        case 'deleted':
          console.log('Deleted:', event.documentId)
          break
      }
    },
  })

  return null
}
```

---

## Multi-Project Apps

```typescript
const config: SanityConfig[] = [
  { projectId: 'project-1', dataset: 'production' },
  { projectId: 'project-2', dataset: 'staging' },
]

// Handles include project/dataset info
const handle: DocumentHandle = {
  documentId: 'doc-123',
  documentType: 'article',
  projectId: 'project-1',
  dataset: 'production',
}
```

---

## Lazy Loading with Refs

```typescript
function LazyContent(handle: DocumentHandle) {
  const ref = useRef(null)

  const { data } = useDocumentProjection({
    ...handle,
    ref, // Only loads when element enters viewport
    projection: '{ title, body }',
  })

  return <div ref={ref}>{data?.title}</div>
}
```

---

## What's NOT Included

The App SDK provides hooks and data stores. You bring:

- UI components (use Sanity UI or your own)
- Router
- Form validation
- Schema validation

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Safari dev issues | Use Chrome or Firefox during development |
| Port 3333 in use | `npm run dev -- --port 3334` |
| Auth errors | `npx sanity@latest logout && npx sanity@latest login` |
