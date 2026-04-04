# Taxonomy and Classification

Organizing content with taxonomies enables filtering, navigation, and content relationships. Well-designed taxonomies scale; poorly designed ones become maintenance nightmares.

## Types of Classification

### Flat Taxonomy
Simple list of terms with no hierarchy.

**Use for:** Tags, simple categories
**Example:** Blog tags: "javascript", "react", "tutorial"

```typescript
defineType({
  name: 'tag',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'slug', type: 'slug' }),
  ]
})
```

### Hierarchical Taxonomy
Terms with parent-child relationships.

**Use for:** Product categories, content sections
**Example:** Electronics > Phones > Smartphones

```typescript
defineType({
  name: 'category',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'slug', type: 'slug' }),
    defineField({ 
      name: 'parent', 
      type: 'reference', 
      to: [{ type: 'category' }],
      description: 'Parent category (leave empty for top-level)'
    }),
  ]
})
```

### Faceted Classification
Multiple independent dimensions.

**Use for:** Complex filtering (e-commerce)
**Example:** Filter by color AND size AND price range

```typescript
// Multiple taxonomy types
defineField({ name: 'color', type: 'reference', to: [{ type: 'color' }] })
defineField({ name: 'size', type: 'reference', to: [{ type: 'size' }] })
defineField({ name: 'material', type: 'reference', to: [{ type: 'material' }] })
```

## Design Principles

### 1. Mutual Exclusivity (When Appropriate)
Categories should be distinct. If items frequently belong to multiple categories, consider tags instead.

**Categories:** One primary classification
**Tags:** Many optional classifications

### 2. User-Centric Naming
Use terms your audience uses, not internal jargon.

**Bad:** "Content Assets" (internal term)
**Good:** "Resources" or "Downloads" (user term)

### 3. Balanced Depth
Too shallow: Everything lumped together
Too deep: Users can't find anything

**Rule of thumb:** 3-4 levels max for hierarchies

### 4. Scalable Structure
Design for 10x growth. Will your structure work with 10,000 items?

## Querying Taxonomies

### Get all items in a category

```groq
*[_type == "product" && category._ref == $categoryId]
```

### Get items in category OR children

```groq
// First get all descendant category IDs
*[_type == "product" && category._ref in 
  *[_type == "category" && (
    _id == $categoryId || 
    parent._ref == $categoryId ||
    parent->parent._ref == $categoryId
  )]._id
]
```

### Get category tree

```groq
*[_type == "category" && !defined(parent)]{
  title,
  slug,
  "children": *[_type == "category" && parent._ref == ^._id]{
    title,
    slug,
    "children": *[_type == "category" && parent._ref == ^._id]{
      title,
      slug
    }
  }
}
```

## Common Mistakes

### Over-categorization
Creating a category for everything results in mostly-empty categories.

**Fix:** Start minimal, add categories as content grows.

### Inconsistent Granularity
Some categories broad ("Technology"), others narrow ("React 18 Server Components").

**Fix:** Define clear criteria for category creation.

### No Governance
Anyone can create taxonomy terms, leading to duplicates and inconsistency.

**Fix:** Limit who can create/edit taxonomy documents. Use validation.
