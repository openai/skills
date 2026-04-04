# Content Reuse Patterns

Effective content models maximize reuse while minimizing duplication. Here are patterns for achieving both.

## The Content Reuse Spectrum

```
Full Duplication ←————————————————→ Full Reference
(Copy everything)                    (Link to one source)
```

Most real-world content sits somewhere in between.

## Pattern 1: Shared Components

Create reusable content blocks that can be embedded anywhere.

**Use case:** Testimonials, FAQs, CTAs that appear on multiple pages.

```typescript
// Standalone testimonial documents
defineType({
  name: 'testimonial',
  type: 'document',
  fields: [
    defineField({ name: 'quote', type: 'text' }),
    defineField({ name: 'author', type: 'string' }),
    defineField({ name: 'company', type: 'string' }),
  ]
})

// Reference in page builders
defineField({
  name: 'pageBuilder',
  type: 'array',
  of: [
    { type: 'reference', to: [{ type: 'testimonial' }] }
  ]
})
```

## Pattern 2: Shared Field Sets

Extract common fields into reusable definitions.

**Use case:** SEO fields, social metadata, common dates.

```typescript
// Shared field definition
export const seoFields = [
  defineField({ name: 'seoTitle', type: 'string' }),
  defineField({ name: 'seoDescription', type: 'text' }),
  defineField({ name: 'ogImage', type: 'image' }),
]

// Spread into multiple types
defineType({
  name: 'page',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    ...seoFields
  ]
})

defineType({
  name: 'post',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    ...seoFields
  ]
})
```

## Pattern 3: Taxonomy References

Centralize classification for consistent tagging.

**Use case:** Categories, tags, topics that span content types.

```typescript
// Central taxonomy
defineType({
  name: 'category',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'slug', type: 'slug' }),
  ]
})

// Used across content types
defineField({
  name: 'categories',
  type: 'array',
  of: [{ type: 'reference', to: [{ type: 'category' }] }]
})
```

## Pattern 4: Content Fragments

Small, reusable pieces that combine into larger content.

**Use case:** Bios, addresses, contact info.

```typescript
// Fragment type
defineType({
  name: 'contactInfo',
  type: 'object',
  fields: [
    defineField({ name: 'email', type: 'email' }),
    defineField({ name: 'phone', type: 'string' }),
    defineField({ name: 'address', type: 'text' }),
  ]
})

// Reused across types
defineType({
  name: 'office',
  fields: [
    defineField({ name: 'name', type: 'string' }),
    defineField({ name: 'contact', type: 'contactInfo' }),
  ]
})
```

## Anti-Pattern: Over-Abstraction

Not everything needs to be reusable. If content is only used in one place, embedding is simpler.

**Signs of over-abstraction:**
- References that are only used once
- Editors navigating multiple documents for one page
- Complex queries joining rarely-shared content
