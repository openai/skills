---
title: Sanity Schema Best Practices
description: Rules for defining Sanity Content Models (Schemas), including field definitions, strict typing, and validation patterns.
---

# Sanity Schema Best Practices

## 1. Core Philosophy: Data > Presentation
Model **what things are**, not **what they look like**.
- ❌ **Bad:** `bigHeroText`, `redButton`, `threeColumnRow`, `color`, `fontSize`
- ✅ **Good:** `heroStatement`, `callToAction`, `featuresSection`, `status`, `role`

**The test:** "If we redesigned the site, would this field name still make sense?"
- `threeColumnLayout` → ❌ Fails (what if we go to 2 columns?)
- `features` → ✅ Passes (features are features regardless of layout)

## 2. Strict Definition Syntax
Always use the helper functions from `sanity` for type safety and autocompletion.

- **ALWAYS** use `defineType` for the root export.
- **ALWAYS** use `defineField` for fields.
- **ALWAYS** use `defineArrayMember` for items inside arrays.

```typescript
import { defineType, defineField, defineArrayMember } from 'sanity'
import { TagIcon } from '@sanity/icons'

export const article = defineType({
  name: 'article',
  title: 'Article',
  type: 'document',
  icon: TagIcon,
  fields: [
    defineField({
      name: 'title',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'tags',
      type: 'array',
      of: [
        // ALWAYS use defineArrayMember for array items
        defineArrayMember({ type: 'reference', to: [{ type: 'tag' }] })
      ]
    })
  ]
})
```

## 3. Shared Fields Pattern
Export arrays of fields to reuse common patterns (e.g., SEO, standard page headers).

```typescript
// src/schemaTypes/shared/seoFields.ts
export const seoFields = [
  defineField({ name: 'seoTitle', type: 'string', title: 'SEO Title' }),
  defineField({ name: 'seoDesc', type: 'text', title: 'SEO Description' })
]

// Usage
defineType({
  name: 'page',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    ...seoFields // Spread shared fields
  ]
})
```

## 4. Field Patterns

### A. Array Keys (`_key`)
Every item in a Sanity array automatically gets a `_key` property. This is **critical** for:
- React reconciliation (use as `key` prop)
- Visual Editing overlays (click-to-edit)
- Portable Text rendering

**Schema:** Sanity auto-generates `_key` for array items. You don't define it.

**Frontend:** Always use `_key` as React's `key`:
```typescript
// ✅ Correct
{items.map((item) => <Component key={item._key} {...item} />)}

// ❌ Wrong - index keys break Visual Editing
{items.map((item, i) => <Component key={i} {...item} />)}
```

**Querying:** Always include `_key` in array projections:
```groq
*[_type == "page"][0]{
  pageBuilder[]{
    _key,  // Always include _key in queries
    _type,
    ...
  }
}
```

### B. Icons
Always assign an icon from `@sanity/icons` to documents and objects. This improves the Studio UX significantly. Browse all icons at [icons.sanity.build](https://icons.sanity.build/all).

| Content Type | Icon |
|--------------|------|
| Article, Post | `DocumentTextIcon` |
| Author, Person | `UserIcon` |
| Category, Tag | `TagIcon` |
| Settings | `CogIcon` |
| Page | `DocumentIcon` |
| Image block | `ImageIcon` |
| Video block | `PlayIcon` |
| FAQ | `HelpCircleIcon` |
| Link | `LinkIcon` |

### C. Boolean vs. List
Avoid boolean fields for binary states that might expand later.
- **Prefer:** `options.list` with "radio" layout.

```typescript
defineField({
  name: 'status',
  type: 'string',
  options: {
    list: [
      { title: 'Draft', value: 'draft' },
      { title: 'Published', value: 'published' }
    ],
    layout: 'radio'
  }
})
```

### D. The "Toggle" Pattern (Conditional Fields)
Use a radio/boolean field to toggle visibility of other fields (often grouped in fieldsets).

```typescript
defineField({
  name: 'linkType',
  type: 'string',
  options: { list: ['internal', 'external'], layout: 'radio' }
}),
defineField({
  name: 'internalLink',
  type: 'reference',
  hidden: ({ parent }) => parent?.linkType !== 'internal'
}),
defineField({
  name: 'externalUrl',
  type: 'url',
  hidden: ({ parent }) => parent?.linkType !== 'external'
})
```

## 5. References vs Nested Objects

A **critical modeling decision**: when to use `reference` vs embedding an `object`.

### Use References When:
- Content is **reusable** across documents (authors, categories, products)
- Content needs its **own editing interface** in Studio
- You need to query/filter by the related content independently
- Multiple documents should share the **same instance** (update once, reflect everywhere)

```typescript
// ✅ Author is reusable and independently editable
defineField({
  name: 'author',
  type: 'reference',
  to: [{ type: 'author' }]
})
```

### Use Nested Objects When:
- Content is **specific to this document** (not shared)
- Content doesn't make sense on its own (address, SEO metadata)
- You want **simpler editing** (all fields in one place)
- You need the data to be **copied** not linked

```typescript
// ✅ SEO is document-specific, not shared
defineField({
  name: 'seo',
  type: 'object',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'description', type: 'text' })
  ]
})
```

### Quick Decision Matrix

| Scenario | Use |
|----------|-----|
| Blog post author | `reference` (reusable) |
| Product category | `reference` (shared taxonomy) |
| Page SEO fields | `object` (page-specific) |
| Hero section content | `object` (page-specific) |
| Team member on About page | `reference` (might be used elsewhere) |
| Call-to-action button | `object` (usually page-specific) |

### Querying Differences
```groq
// Reference requires expansion
*[_type == "post"]{ author->{ name, bio } }

// Object is already inline
*[_type == "post"]{ seo { title, description } }
```

## 6. Safe Schema Updates (The Deprecation Pattern)

**NEVER** delete a field that contains production data. It will cause data loss or Studio crashes. Instead, follow the **ReadOnly -> Hidden -> Deprecated** lifecycle.

### The Pattern
1.  **`deprecated`**: Adds a visual warning and reason.
2.  **`readOnly: true`**: Prevents new edits but keeps data visible.
3.  **`hidden`**: Hides it from *new* documents (where value is undefined).
4.  **`initialValue: undefined`**: Ensures new documents don't get this field.

```typescript
defineField({
  name: 'oldTitle', // The field you want to remove
  title: 'Article Title (Deprecated)',
  type: 'string',
  deprecated: {
    reason: 'Use the new "seoTitle" field instead. This will be removed in v2.'
  },
  readOnly: true,
  hidden: ({ value }) => value === undefined,
  initialValue: undefined
})
```

### Migration Workflow

**Phase 1: Deprecate** — Apply the deprecation pattern above. Deploy.

**Phase 2: Migrate** — Update frontend to use new fields (with `coalesce()` fallbacks). Create a migration:

```typescript
// migrations/rename-oldTitle-to-newTitle/index.ts
import {defineMigration, at, setIfMissing, unset} from 'sanity/migrate'

export default defineMigration({
  title: 'Rename oldTitle to newTitle',
  documentTypes: ['article'],
  filter: 'defined(oldTitle) && !defined(newTitle)',
  migrate: {
    document(doc) {
      if (!doc.oldTitle || doc.newTitle) return
      return [
        at('newTitle', setIfMissing(doc.oldTitle)),
        at('oldTitle', unset())
      ]
    }
  }
})
```

```bash
# Dry run first (default)
sanity migration run rename-oldTitle-to-newTitle

# Execute when ready
sanity migration run rename-oldTitle-to-newTitle --no-dry-run
```

**Phase 3: Remove** — Once `oldTitle` is undefined for all documents, delete the field definition.

## 7. Validation Patterns

Beyond `rule.required()`, Sanity offers powerful validation options.

### Common Patterns

```typescript
// Email validation
defineField({
  name: 'email',
  type: 'string',
  validation: (rule) => rule.email().required()
})

// URL validation (with custom message)
defineField({
  name: 'website',
  type: 'url',
  validation: (rule) => rule.uri({
    scheme: ['http', 'https']
  }).error('Must be a valid URL starting with http:// or https://')
})

// Length constraints
defineField({
  name: 'excerpt',
  type: 'text',
  validation: (rule) => rule.max(200).warning('Keep it under 200 characters for best SEO')
})

// Regex pattern
defineField({
  name: 'slug',
  type: 'slug',
  validation: (rule) => rule.required().custom((slug) => {
    if (!slug?.current) return 'Required'
    if (!/^[a-z0-9-]+$/.test(slug.current)) {
      return 'Slug must be lowercase with hyphens only'
    }
    return true
  })
})
```

### Cross-Field Validation

```typescript
defineField({
  name: 'endDate',
  type: 'datetime',
  validation: (rule) => rule.custom((endDate, context) => {
    const startDate = context.document?.startDate
    if (startDate && endDate && new Date(endDate) < new Date(startDate)) {
      return 'End date must be after start date'
    }
    return true
  })
})
```

### Array Validation

```typescript
defineField({
  name: 'tags',
  type: 'array',
  of: [{ type: 'string' }],
  validation: (rule) => rule
    .min(1).error('Add at least one tag')
    .max(10).warning('Too many tags may hurt SEO')
    .unique()
})
```

### Async Validation (Uniqueness Check)

```typescript
defineField({
  name: 'slug',
  type: 'slug',
  validation: (rule) => rule.required().custom(async (slug, context) => {
    if (!slug?.current) return true

    const client = context.getClient({ apiVersion: '2026-02-01' })
    const id = context.document?._id?.replace(/^drafts\./, '')

    const existing = await client.fetch(
      `count(*[_type == "post" && slug.current == $slug && _id != $id])`,
      { slug: slug.current, id }
    )

    return existing === 0 || 'Slug already exists'
  })
})
```
