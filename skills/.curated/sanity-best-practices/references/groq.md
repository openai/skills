---
title: GROQ Query Maintenance & Best Practices
description: Guidelines for GROQ queries, type safety, performance optimization, and syntax highlighting.
---

# GROQ Query Maintenance & Best Practices

## 1. Query Definition & Imports

### The `defineQuery` Function
**ALWAYS** wrap GROQ queries in `defineQuery` for TypeGen support. The import location depends on your framework:

```typescript
// Framework-agnostic (Remix, SvelteKit, Astro, vanilla)
import { defineQuery } from "groq";

// Next.js (re-exported for convenience)
import { defineQuery } from "next-sanity";
```

### Syntax Highlighting
For VS Code syntax highlighting, either:
1. Use the `groq` tagged template (recommended): `groq\`...\``
2. Or prefix with `/* groq */` comment when using `defineQuery`

```typescript
import { defineQuery } from "groq";

// ✅ Option A: groq tag (provides highlighting automatically)
import groq from "groq";
const QUERY = defineQuery(groq`*[_type == "post"]`);

// ✅ Option B: Comment prefix (for plain template literals)
const QUERY = defineQuery(/* groq */ `*[_type == "post"]`);

// ✅ Also valid: Just defineQuery (TypeGen works, but no editor highlighting)
const QUERY = defineQuery(`*[_type == "post"]`);
```

## 2. Query Fragments
Use string interpolation to reuse query logic and keep queries maintainable.

```typescript
// src/sanity/fragments/image.ts
export const imageFragment = /* groq */ `
  asset->{
    _id,
    url,
    metadata { lqip, dimensions }
  },
  alt
`;

// src/sanity/queries/post.ts
import { defineQuery } from "groq";
import { imageFragment } from "../fragments/image";

export const POST_QUERY = defineQuery(/* groq */ `
  *[_type == "post"][0] {
    title,
    mainImage {
      ${imageFragment}
    }
  }
`);
```

## 3. Expansion Patterns (Page Builder)
When building a Page Builder query, expand all potential component types.

**Best Practice:** Use a `pageFields` fragment or similar strategy to keep the main query clean.

```typescript
const pageBuilderExpansion = /* groq */ `
  pageBuilder[] {
    ...,
    _type == "hero" => {
      ...,
      cta[] { link, label }
    },
    _type == "gallery" => {
      images[] { ${imageFragment} }
    }
  }
`;
```

## 4. Maintenance Workflow
When you add a new field or component to the Schema:
1.  **Update the Query:** Add the new field/expansion to the relevant GROQ query immediately.
2.  **Run TypeGen:** If you have `typegen.enabled: true` in `sanity.cli.ts`, types regenerate automatically during `sanity dev`/`sanity build`. Otherwise, run `npm run typegen` manually.
3.  **Verify:** Ensure the new field is available in the generated types.

## 5. Common Patterns

### Ordering
```groq
// Single field
*[_type == "post"] | order(publishedAt desc)

// Multiple fields (tiebreaker)
*[_type == "post"] | order(featured desc, publishedAt desc)

// ⚠️ Order BEFORE slice, not after!
*[_type == "post"] | order(publishedAt desc)[0...10]  // ✅ Correct
*[_type == "post"][0...10] | order(publishedAt desc)  // ❌ Wrong order
```

### Slice Notation
```groq
*[_type == "post"][0]       // Single document (object, not array)
*[_type == "post"][0...5]   // First 5 (exclusive) ← Most common
*[_type == "post"][$start...$end]  // Pagination with params
```

### Default Values with `coalesce()`
```groq
*[_type == "page"]{
  "title": coalesce(seoTitle, title, "Untitled"),
  "image": coalesce(ogImage, mainImage, defaultImage)
}
```

### Conditionals with `select()`
```groq
*[_type == "product"]{
  title,
  "badge": select(
    stock == 0 => "Out of Stock",
    stock < 5 => "Low Stock",
    "In Stock"
  )
}
```

### Aggregation with `count()`
```groq
// Total count
count(*[_type == "post" && defined(slug.current)])

// Count per document
*[_type == "category"]{
  title,
  "postCount": count(*[_type == "post" && references(^._id)])
}
```

### Reverse References
```groq
*[_type == "author"]{
  name,
  "posts": *[_type == "post" && references(^._id)]{ title, slug }
}
```

### Array Filtering
```groq
*[_type == "movie"]{
  title,
  "mainCast": castMembers[role == "lead"]->{name}
}

// Check if value exists in array
*[_type == "post" && "tech" in categories[]->slug.current]
```

### Special Variables
```groq
// ^ = parent document (in nested queries)
*[_type == "author"]{
  name,
  "posts": *[_type == "post" && author._ref == ^._id]
}

// @ = current item (in array operations)
*[_type == "post"]{
  "tagCount": count(tags[@ != null])
}
```

## 6. Performance Rules

### Optimizable vs Non-Optimizable Filters
GROQ uses indexes for **optimizable** filters. Non-optimizable filters scan ALL documents.

| Pattern | Optimizable | Example |
|---------|-------------|---------|
| `_type == "x"` | ✅ Yes | `*[_type == "post"]` |
| `_id == "x"` | ✅ Yes | `*[_id == "abc123"]` |
| `slug.current == $slug` | ✅ Yes | `*[slug.current == "hello"]` |
| `defined(field)` | ✅ Yes | `*[defined(publishedAt)]` |
| `references($id)` | ✅ Yes | `*[references("author-123")]` |
| `field->attr == x` | ❌ No | Resolves reference for every doc |
| `fieldA < fieldB` | ❌ No | Compares two attributes |

**Fix non-optimizable filters by stacking:**
```groq
// Stack optimizable filters FIRST to reduce search space
*[_type == "product" && defined(salePrice) && salePrice < displayPrice]
```

### Avoid Joins in Filters
Reference resolution (`->`) in filters is expensive. Use `_ref` instead:

```groq
// ❌ Slow: Resolves reference for every document
*[_type == "post" && author->name == "Bob Woodward"]

// ✅ Fast: Direct _ref comparison
*[_type == "post" && author._ref == "author-bob-woodward-id"]
```

**When you need dynamic lookups** (don't know the ID upfront):

```groq
// Two-step approach:
// 1. Get the reference ID first
*[_type == "author" && name == "Bob Woodward"][0]._id

// 2. Use that ID in your main query
*[_type == "post" && author._ref == $authorId]

// Or use a subquery (still better than -> in filter):
*[_type == "post" && author._ref in *[_type == "author" && name == "Bob Woodward"]._id]
```

### Merge Repeated Reference Resolutions
Each `->` is a subquery. Don't repeat it:

```groq
// ❌ Slow: Two separate subqueries
*[_type == "category"]{
  "parentTitle": parent->title,
  "parentSlug": parent->slug.current
}

// ✅ Fast: Single subquery, merged
*[_type == "category"]{
  ...(parent->{ "parentTitle": title, "parentSlug": slug.current })
}
```

### Cursor-Based Pagination (Not Deep Slicing)
Deep slices are slow because all skipped docs must be sorted first.

```groq
// ❌ Slow: Must sort and skip 10,000 docs
*[_type == "article"] | order(_id)[10000...10020]

// ✅ Fast: Cursor-based, only fetches 20
*[_type == "article" && _id > $lastId] | order(_id)[0...20]
```

**For custom sort orders**, include the sort field in the cursor:

```groq
// Compound cursor: publishedAt + _id for deterministic pagination
*[_type == "article" && (
  publishedAt < $lastDate || 
  (publishedAt == $lastDate && _id > $lastId)
)] | order(publishedAt desc, _id)[0...20]
```

### Always Project Fields
Always use projections to return only the fields your application needs. Fetching entire documents wastes bandwidth and processing time.

```groq
// ❌ Returns ALL fields including unused ones, metadata, revisions
*[_type == "post"]

// ✅ Only fetch what the component needs
*[_type == "post"]{
  _id,
  title,
  "slug": slug.current,
  publishedAt,
  excerpt
}
```

Apply projections at every level, including nested references:

```groq
*[_type == "post"]{
  title,
  author->{ name, "avatar": image.asset->url },
  categories[]->{ title, "slug": slug.current }
}
```

Use conditional projections for different contexts:

```groq
*[_type == "post"]{
  title,
  slug,
  // Only include body for single post view
  $includeBody == true => { body }
}
```

### Don't Filter/Sort on Projected Values
Computed attributes can't use indexes:

```groq
// ❌ Not optimizable (computed attribute)
*[_type == "person"]{
  "fullName": firstName + " " + lastName
} | order(fullName)

// ✅ Optimizable (original attribute)
*[_type == "person"] | order(firstName, lastName)
```

### Quick Checklist
| Rule | Why |
|------|-----|
| Always project `{ fields }` | Reduces data returned |
| Use `defined()` checks | Filters use indexes |
| Use `$params` not interpolation | Prevents query manipulation + enables caching |
| Order BEFORE slice | `order()[0...N]` not `[0...N] order()` |
| Use `_ref` not `->field` in filters | Avoids expensive joins |
| Merge repeated `->` calls | Single subquery vs many |
| Cursor pagination for deep pages | Avoids sorting entire dataset |

## 7. API Version Best Practices

Always use dated versions (`YYYY-MM-DD`) for consistent behavior:

```typescript
const client = createClient({
  apiVersion: '2026-02-01', // Use current date for new projects
})
```

- **New projects:** Use current date (e.g., `2026-02-01`)
- **Existing projects:** Keep current version unless you need new features
- Dated versions lock behavior; `v1` or `vX` may change unexpectedly
