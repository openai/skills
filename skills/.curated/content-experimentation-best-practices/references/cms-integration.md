# CMS Integration Patterns

Integrating experimentation with your CMS enables content teams to run tests without developer intervention.

## Architecture Options

### 1. CMS-Managed Variants
Store experiment variants as content in the CMS.

**Pros:** Content team autonomy, version controlled
**Cons:** More complex queries, potential publish coordination

```typescript
// Experiment document
defineType({
  name: 'experiment',
  type: 'document',
  fields: [
    defineField({ name: 'name', type: 'string' }),
    defineField({ name: 'status', type: 'string', options: { 
      list: ['draft', 'running', 'paused', 'concluded'] 
    }}),
    defineField({ 
      name: 'variants', 
      type: 'array',
      of: [{
        type: 'object',
        fields: [
          defineField({ name: 'name', type: 'string' }),
          defineField({ name: 'weight', type: 'number' }),
          defineField({ name: 'content', type: 'reference', to: [{ type: 'page' }] }),
        ]
      }]
    }),
    defineField({ name: 'startDate', type: 'datetime' }),
    defineField({ name: 'endDate', type: 'datetime' }),
  ]
})
```

### 2. Field-Level Variants
Store variants as fields on the content document.

**Pros:** Simpler queries, content stays together
**Cons:** Less flexible, schema complexity

```typescript
defineType({
  name: 'landingPage',
  fields: [
    defineField({ name: 'headline', type: 'string' }),
    defineField({ 
      name: 'headlineVariantB', 
      type: 'string',
      description: 'A/B test variant (leave empty if not testing)'
    }),
    defineField({ name: 'activeExperiment', type: 'string' }),
  ]
})
```

### 3. External Experimentation Platform
Use dedicated tools (Optimizely, LaunchDarkly, VWO) with CMS content.

**Pros:** Robust analytics, proven platforms
**Cons:** Additional cost, integration complexity

```typescript
// CMS stores experiment IDs, platform handles assignment
defineField({
  name: 'experimentId',
  type: 'string',
  description: 'Optimizely experiment ID'
})
```

## Implementation Pattern (CMS-Managed)

### 1. Experiment Schema

```typescript
defineType({
  name: 'experiment',
  type: 'document',
  fields: [
    defineField({ name: 'name', type: 'string', validation: r => r.required() }),
    defineField({ name: 'hypothesis', type: 'text' }),
    defineField({ 
      name: 'status', 
      type: 'string', 
      options: { list: ['draft', 'running', 'concluded'] },
      initialValue: 'draft'
    }),
    defineField({
      name: 'variants',
      type: 'array',
      of: [{
        type: 'object',
        name: 'variant',
        fields: [
          defineField({ name: 'id', type: 'string' }),
          defineField({ name: 'name', type: 'string' }),
          defineField({ name: 'weight', type: 'number', initialValue: 50 }),
        ]
      }],
      validation: r => r.min(2).error('Need at least 2 variants')
    }),
    defineField({ name: 'targetPage', type: 'reference', to: [{ type: 'page' }] }),
    defineField({ name: 'targetField', type: 'string' }),
  ]
})
```

### 2. Variant Content

```typescript
// On the page being tested
defineField({
  name: 'experimentVariants',
  type: 'array',
  of: [{
    type: 'object',
    fields: [
      defineField({ name: 'experimentId', type: 'reference', to: [{ type: 'experiment' }] }),
      defineField({ name: 'variantId', type: 'string' }),
      defineField({ name: 'headline', type: 'string' }),
      // Other variant-specific fields
    ]
  }]
})
```

### 3. Frontend Assignment

```typescript
// Middleware or server-side
function assignVariant(experimentId: string, variants: Variant[]): string {
  // Check for existing assignment in cookie
  const cookieKey = `exp_${experimentId}`
  const existing = getCookie(cookieKey)
  if (existing) return existing
  
  // Random assignment based on weights
  const rand = Math.random() * 100
  let cumulative = 0
  for (const variant of variants) {
    cumulative += variant.weight
    if (rand <= cumulative) {
      setCookie(cookieKey, variant.id, { maxAge: 30 * 24 * 60 * 60 })
      return variant.id
    }
  }
  return variants[0].id
}
```

### 4. Query with Variant

```groq
*[_type == "page" && slug.current == $slug][0]{
  ...,
  "experiment": experimentVariants[experimentId->status == "running"][0]{
    experimentId->{name, _id},
    variantId,
    headline
  }
}
```

## Analytics Integration

### Event Tracking

```typescript
// Track experiment exposure
function trackExposure(experimentId: string, variantId: string) {
  analytics.track('Experiment Viewed', {
    experimentId,
    variantId,
    timestamp: new Date().toISOString()
  })
}

// Track conversion
function trackConversion(experimentId: string, variantId: string, metric: string) {
  analytics.track('Experiment Conversion', {
    experimentId,
    variantId,
    metric,
    timestamp: new Date().toISOString()
  })
}
```

### Data Layer

```typescript
// Push to data layer for analytics tools
window.dataLayer.push({
  event: 'experiment_assignment',
  experiment_id: experimentId,
  variant_id: variantId
})
```

## Best Practices

### Content Team Workflow
1. Create experiment document with hypothesis
2. Create variant content
3. Set status to "running"
4. Monitor results
5. Set status to "concluded" and record winner

### Avoid Flicker
- Assign variants server-side when possible
- Use CSS to hide content until variant determined
- Pre-render both variants, show based on assignment

### Clean Up
- Archive concluded experiments
- Remove losing variant content
- Implement winner as default
