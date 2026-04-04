---
title: Sanity TypeGen Rules
description: Workflow for generating TypeScript types from Sanity Schema and GROQ queries.
---

# Sanity TypeGen Rules

## 1. The Workflow
Sanity TypeGen generates TypeScript types from your schema and GROQ queries. Types can be generated automatically or manually.

### Automatic (Recommended)
Enable in `sanity.cli.ts` — types regenerate during `sanity dev` and `sanity build`:

```typescript
// sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true,
  },
})
```

### Manual
Run the extract + generate cycle whenever schema or queries change:

1.  **Extract:** Converts your Schema (TS/JS) into a static JSON representation.
2.  **Generate:** Scans your codebase for GROQ queries and generates TypeScript types.

```bash
npx sanity schema extract && npx sanity typegen generate
```

### Watch Mode (for separate frontends)
If your frontend is in a separate repo from the Studio, use watch mode:

```bash
npx sanity typegen generate --watch
```

## 2. The "Update Types" Pattern
For manual workflows, implement a single script:

**package.json:**
```json
"scripts": {
  "typegen": "sanity schema extract && sanity typegen generate"
}
```

### Git Strategy for Generated Files

**Option A: Commit generated types (Recommended for most teams)**
- Types available immediately after `git pull`
- CI/CD doesn't need to run typegen
- Can cause merge conflicts

**Option B: Generate in CI (Recommended for larger teams)**
Add to `.gitignore`:
```gitignore
# Sanity TypeGen (generated)
sanity.types.ts
schema.json
```

Then ensure CI runs typegen before build:
```yaml
# Example GitHub Actions
- run: npm run typegen
- run: npm run build
```

## 3. Configuration (`sanity.cli.ts`)

> **Note:** `sanity-typegen.json` is deprecated. Move your configuration to `sanity.cli.ts`.

```typescript
// sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true, // Auto-generate during sanity dev/build
    path: "./src/**/*.{ts,tsx,js,jsx,astro,svelte,vue}", // Glob to find queries
    schema: "schema.json", // Schema file from extract
    generates: "./sanity.types.ts", // Output file
    overloadClientMethods: true, // Auto-type client.fetch() calls
  },
})
```

### Project Structure Examples

**Single Repo / Embedded Studio (most common):**
Use defaults — no extra config needed.

**Monorepo** (Studio in `apps/studio`, Frontend in `apps/web`):
```typescript
export default defineCliConfig({
  typegen: {
    path: "../web/src/**/*.{ts,tsx,js,jsx}",
    schema: "schema.json",
    generates: "../web/sanity.types.ts",
  },
})
```

**Separate Repos:**
Use `--watch` mode in your frontend: `sanity typegen generate --watch`

## 4. Usage in Code

### Automatic Type Inference (Recommended)
With `overloadClientMethods: true` (default), `client.fetch()` automatically returns typed results when you use `defineQuery`:

```typescript
import { defineQuery } from "groq";
import { createClient } from "@sanity/client";

const client = createClient({...});

const POSTS_QUERY = defineQuery(`*[_type == "post"]{ title, slug }`);

// Return type is automatically inferred — no manual type import needed!
const posts = await client.fetch(POSTS_QUERY);
```

### Manual Type Import (Alternative)
You can also import generated types directly:

```typescript
import { defineQuery } from "groq";
// Next.js re-exports defineQuery for convenience:
// import { defineQuery } from "next-sanity";

const AUTHOR_QUERY = defineQuery(`*[_type == "author" && slug.current == $slug][0]{ name, bio }`);

import type { AUTHOR_QUERYResult } from "@/sanity.types";

export default function Author({ data }: { data: AUTHOR_QUERYResult }) {
  return <h1>{data.name}</h1>
}
```

### Required Fields
Use `--enforce-required-fields` during extraction to translate `validation: rule => rule.required()` into non-optional types:

```bash
npx sanity schema extract --enforce-required-fields
npx sanity typegen generate
```

> **Warning:** If you use draft previews, fields may still be `undefined` even with required validation, since drafts can be in an invalid state.

### Type Utilities
TypeGen provides utilities for working with complex types:

```typescript
import type { Get, FilterByType } from 'sanity'
import type { Page, PageBuilder } from './sanity.types'

// Extract deeply nested type (up to 20 levels)
type HeroSection = Get<Page, 'sections', number, 'hero'>

// Filter specific types from unions using _type discriminator
type HeroBlock = FilterByType<PageBuilder, 'hero'>
```

### Unique Query Names
All queries must have unique variable names. Duplicate names across files will cause TypeGen to silently overwrite types. Use descriptive, scoped names:

```typescript
// Unique names
const POSTS_INDEX_QUERY = defineQuery(`*[_type == "post"]{ title }`)
const POST_DETAIL_QUERY = defineQuery(`*[_type == "post" && slug.current == $slug][0]`)

// Duplicate names will conflict
const QUERY = defineQuery(`*[_type == "post"]`)  // file-a.ts
const QUERY = defineQuery(`*[_type == "author"]`) // file-b.ts — overwrites!
```

### Supported Query Formats
Queries must be assigned to a variable using `groq` or `defineQuery`:

```typescript
// Works — groq template tag
const query = groq`*[_type == "post"]`

// Works — defineQuery
const query = defineQuery(`*[_type == "post"]`)

// Won't work — inline query
await client.fetch(groq`*[_type == "post"]`)
```

### Supported File Types
TypeGen parses queries from: `.ts`, `.tsx`, `.js`, `.jsx`, `.astro`, `.svelte`, `.vue`

### tsconfig Requirements
Ensure `sanity.types.ts` is included in your `tsconfig.json`'s `include` array. If your config restricts includes (e.g., `["src/**/*"]`) and the types file is at the project root, TypeScript won't pick up the generated types:

```json
{
  "include": ["src/**/*", "sanity.types.ts"]
}
```

### Skipping Individual Queries
Add `@sanity-typegen-ignore` in a comment before a query to skip type generation:

```typescript
// @sanity-typegen-ignore
const debugQuery = groq`*[_type == "debug"]`
```
