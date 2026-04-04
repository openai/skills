---
title: Sanity Getting Started Guide
description: Use these rules when users ask to 'Get started with Sanity' or need help setting up a new Sanity project.
---

# Sanity Getting Started Guide

## Overview

Getting started with Sanity follows three phases:
1. **Studio & Schema** — Set up Sanity Studio and define your content model
2. **Content** — Import existing content or generate placeholder content via MCP
3. **Frontend** — Integrate with your application (framework-specific)

## Communication Style

**Keep responses succinct:**

- Tell the user what you did: "Created post schema with title, body, and slug"
- Ask direct questions: "What kind of content are you building?"
- Avoid verbose explanations of what you're about to do
- Don't explain every step unless the user asks

**Examples:**

- **Good**: "Schema deployed. Ready to add some content?"
- **Bad**: "I'm going to deploy your schema to the Content Lake so that the MCP server can recognize your new document types. This will allow..."

---

## Get Started with Sanity (Interactive Guide)

**TRIGGER PHRASE:** When the user says "Get started with Sanity" or similar, follow these steps.

**Before starting:** Let the user know they can pause and resume anytime by saying "Continue Sanity setup".

**RESUME TRIGGER:** If the user says "Continue Sanity setup", check what's already configured:
- Does `sanity.config.ts` exist? → Studio is set up
- Are there files in `schemaTypes/`? → Schema exists
- Is there a frontend framework in `package.json`? → May need integration

Resume from where they left off.

---

## Phase 1: Studio & Schema

### Step 1: Check for Existing Studio

**Look for `sanity.config.ts` or `sanity.cli.ts`:**

**If NO Studio found:**
- Ask: "Want to create a new Sanity Studio?"
- If yes, run:
  ```bash
  npm create sanity@latest -- --template clean --typescript
  ```

**If Studio exists:**
- Read the config to get `projectId` and `dataset`
- Proceed to Step 2

### Step 2: Check for Existing Schema

**Look in `schemaTypes/`, `schemas/`, or `src/sanity/schemaTypes/`:**

**If NO schema found:**
- Ask: "What kind of content are you building? (e.g., Blog, E-commerce, Portfolio)"
- Create appropriate schema types based on their answer
- See `schema.md` for patterns

**If schema exists:**
- Show them what you found
- Ask: "Want to add more content types or modify existing ones?"

**If they want a quick example:**
Create a basic blog schema:
```typescript
// schemaTypes/post.ts
import { defineType, defineField } from 'sanity'

export const post = defineType({
  name: 'post',
  title: 'Post',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'slug', type: 'slug', options: { source: 'title' } }),
    defineField({ name: 'body', type: 'array', of: [{ type: 'block' }] }),
  ],
})
```

### Step 3: Deploy Schema

**Required before Phase 2:**

```bash
npx sanity schema deploy
```

This uploads your schema to the Content Lake so MCP tools can work with it.

---

## Phase 2: Content

### Step 1: Check for Existing Content

**Use MCP `query_documents` to check:**
```
*[_type == "post"][0...5]
```

**If content exists:**
- Show them a summary
- Ask: "Want to add more content or move to frontend integration?"

**If NO content:**
- Ask: "Do you want to:
  1. Import existing content (from another CMS, markdown, etc.)
  2. Generate sample content with AI
  3. Skip this and add content manually in the Studio"

### Step 2a: Import Existing Content

If migrating from another CMS or files:
- See `migration.md`
- Use MCP `migrate_content` tool for guidance

### Step 2b: Generate Sample Content (MCP)

Use the Sanity MCP Server:
```
Tool: create_document
Type: post
Content: Create a sample blog post about getting started with Sanity
```

**If MCP fails:** Remind them to run `npx sanity schema deploy` first.

### MCP Setup (If Not Configured)

**Quick start via Sanity CLI:**
```bash
npx sanity@latest mcp configure
```

**Cursor:** [One-click install →](cursor://anysphere.cursor-deeplink/mcp/install?name=Sanity&config=eyJ1cmwiOiJodHRwczovL21jcC5zYW5pdHkuaW8iLCJ0eXBlIjoiaHR0cCJ9Cg==)

Or add to `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "Sanity": {
      "type": "http",
      "url": "https://mcp.sanity.io"
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add Sanity -t http https://mcp.sanity.io --scope user
```

**VS Code:** Command Palette → `MCP: Open User Configuration` → add:
```json
{
  "servers": {
    "Sanity": {
      "type": "http",
      "url": "https://mcp.sanity.io"
    }
  }
}
```

---

## Phase 3: Frontend Integration

### Step 1: Detect Framework

**Check `package.json` dependencies:**

| Dependency | Framework | Rule File |
|------------|-----------|-----------|
| `next` | Next.js | `nextjs.md` |
| `@remix-run/react` or `react-router` | React Router / Remix | `remix.md` |
| `svelte` or `@sveltejs/kit` | SvelteKit | `svelte.md` |
| `nuxt` | Nuxt | `nuxt.md` |
| `astro` | Astro | `astro.md` |

**If NO framework found:**
- Ask: "Which framework are you using, or would you like to create a new app?"
- Guide them to create one or specify their choice

### Step 2: Next.js Integration (Inline)

If Next.js is detected, follow these essential steps:

**Install dependencies:**
```bash
npm install @sanity/client @sanity/image-url @portabletext/react
```

**Create the client (`src/sanity/client.ts`):**
```typescript
import { createClient } from "@sanity/client";

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  apiVersion: "2026-02-01", // Use current date for new projects
  useCdn: false, // Use API directly for server-side rendering; set true for client-side reads
});
```

**Fetch content in a Server Component:**
```typescript
// app/posts/page.tsx
import { client } from "@/sanity/client";

import { defineQuery } from "groq";

const POSTS_QUERY = defineQuery(`*[_type == "post"]{ _id, title, slug }`);

export default async function PostsPage() {
  const posts = await client.fetch(POSTS_QUERY);

  return (
    <ul>
      {posts.map((post) => (
        <li key={post._id}>
          <a href={`/posts/${post.slug.current}`}>{post.title}</a>
        </li>
      ))}
    </ul>
  );
}
```

**Add environment variables (`.env.local`):**
```
NEXT_PUBLIC_SANITY_PROJECT_ID=your-project-id
NEXT_PUBLIC_SANITY_DATASET=production
```

For advanced patterns (TypeGen, Visual Editing, `defineLive`), see `nextjs.md`.

### Step 3: Other Frameworks

For non-Next.js frameworks, read the corresponding rule file and follow its integration guide:

- **React Router / Remix:** `remix.md`
- **SvelteKit:** `svelte.md`
- **Nuxt:** `nuxt.md`
- **Astro:** `astro.md`

Each rule file contains framework-specific patterns for data fetching, Portable Text rendering, and Visual Editing.

---

## What's Next

Once setup is complete, let the user know:

"You're all set! Here are some things I can help with:

- **Visual Editing** — Click-to-edit in the Presentation tool (`visual-editing.md`)
- **TypeGen** — Type-safe queries with generated types (`typegen.md`)
- **Studio Structure** — Customize the Studio sidebar (`studio-structure.md`)
- **SEO** — Metadata, sitemaps, and Open Graph (`seo.md`)
- **i18n** — Multi-language content (`localization.md`)

Just ask about any of these!"

---

## Environment Variables

### Framework-Specific Prefixes

| Framework | Client-Side Prefix | Example |
|-----------|-------------------|---------|
| Next.js | `NEXT_PUBLIC_` | `NEXT_PUBLIC_SANITY_PROJECT_ID` |
| React Router / Remix | None (use loader) | `SANITY_PROJECT_ID` |
| SvelteKit | `PUBLIC_` | `PUBLIC_SANITY_PROJECT_ID` |
| Nuxt | `NUXT_PUBLIC_` | `NUXT_PUBLIC_SANITY_PROJECT_ID` |
| Astro | `PUBLIC_` | `PUBLIC_SANITY_PROJECT_ID` |

---

## Common Commands

```bash
npx sanity@latest mcp configure  # Configure MCP for your editor
npx sanity dev                   # Start Studio locally
npx sanity schema deploy         # Deploy schema (required for MCP!)
npx sanity deploy                # Deploy Studio to Sanity hosting
npx sanity manage                # Open project settings
npm run typegen                  # Generate TypeScript types
```

---

## Important Notes

- **Be succinct** — Guide step-by-step without over-explaining
- **Check context first** — Read existing files before suggesting changes
- **Don't give up** — If something fails, give the user a way to complete manually
- **Deploy schema early** — MCP tools won't work without it
- **One phase at a time** — Complete each phase before moving to the next
