# Reference vs Embedding Content

When should content be linked (referenced) vs copied (embedded)? This decision affects reusability, query complexity, and editing workflows.

## The Trade-offs

| Aspect | Reference | Embedded Object |
|--------|-----------|-----------------|
| Reusability | ✅ Shared across documents | ❌ Copied per document |
| Single source | ✅ Update once, reflects everywhere | ❌ Must update each copy |
| Query complexity | Requires joins/expansion | Inline, simpler queries |
| Editing UX | Separate editing interface | All fields in one place |
| Independence | Can exist on its own | Only exists within parent |

## When to Reference

Use references when content:
- **Is reusable** — Same author across many articles
- **Needs central management** — Update product info once
- **Has its own lifecycle** — Published/draft independent of parent
- **Should stay in sync** — Price changes reflect everywhere

**Examples:**
- Author profiles
- Product catalog items
- Shared testimonials
- Category taxonomy
- Reusable CTAs

## When to Embed

Use embedded objects when content:
- **Is unique to this document** — Page-specific hero
- **Doesn't make sense alone** — SEO metadata
- **Should be copied, not linked** — Historical snapshot
- **Simplifies editing** — All fields in one form

**Examples:**
- SEO metadata
- Page-specific sections
- Address information
- Social links
- Configuration options

## Sanity Implementation

```typescript
// Reference: Author is reusable
defineField({
  name: 'author',
  type: 'reference',
  to: [{ type: 'author' }]
})

// Embedded: SEO is page-specific
defineField({
  name: 'seo',
  type: 'object',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'description', type: 'text' })
  ]
})
```

## The Hybrid Approach

Sometimes you want both: a reference for the canonical data, plus embedded overrides.

```typescript
defineField({
  name: 'featuredProduct',
  type: 'object',
  fields: [
    defineField({ 
      name: 'product', 
      type: 'reference', 
      to: [{ type: 'product' }] 
    }),
    defineField({ 
      name: 'overrideTitle', 
      type: 'string',
      description: 'Optional: Override the product title for this context'
    }),
  ]
})
```

Query uses `coalesce(overrideTitle, product->title)`.
