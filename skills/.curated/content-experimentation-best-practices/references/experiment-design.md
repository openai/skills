# Experiment Design Principles

Well-designed experiments produce actionable insights. Poorly designed ones waste time and can mislead.

## The Experiment Framework

### 1. Hypothesis
State what you believe and why.

**Bad:** "Let's test a new headline"
**Good:** "We believe a benefit-focused headline will increase signup rate by 10% because users are currently confused about our value proposition"

Structure: "We believe [change] will [impact metric] because [reasoning]"

### 2. Success Metric
Define primary and guardrail metrics.

**Primary metric:** The main thing you're trying to improve (conversion rate, engagement time)
**Guardrail metrics:** Things that shouldn't get worse (bounce rate, page load time)

### 3. Sample Size
Calculate required sample size before starting.

Factors:
- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical significance level (usually 95%)
- Statistical power (usually 80%)

Use calculators like [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html).

### 4. Duration
Run tests for full business cycles.

- Minimum: 1-2 weeks (capture weekly patterns)
- Include weekends
- Avoid holidays and major events
- Don't stop early when you see "winning" results

## What to Test

### High-Impact Areas
- Headlines and value propositions
- Call-to-action text and placement
- Form length and fields
- Pricing presentation
- Social proof placement

### Lower-Impact (Usually)
- Button colors
- Minor copy tweaks
- Image variations (unless hero)
- Footer changes

### Test Priority Matrix

| Impact | Effort | Priority |
|--------|--------|----------|
| High | Low | Do first |
| High | High | Plan carefully |
| Low | Low | Quick wins |
| Low | High | Avoid |

## Sanity Integration Pattern

```typescript
// Experiment variant schema
defineType({
  name: 'experimentVariant',
  type: 'object',
  fields: [
    defineField({ name: 'name', type: 'string' }),
    defineField({ name: 'weight', type: 'number', description: 'Traffic allocation (0-100)' }),
    defineField({ name: 'content', type: 'reference', to: [{ type: 'page' }] }),
  ]
})

// Experiment document
defineType({
  name: 'experiment',
  type: 'document',
  fields: [
    defineField({ name: 'name', type: 'string' }),
    defineField({ name: 'hypothesis', type: 'text' }),
    defineField({ name: 'status', type: 'string', options: { 
      list: ['draft', 'running', 'concluded'] 
    }}),
    defineField({ name: 'variants', type: 'array', of: [{ type: 'experimentVariant' }] }),
    defineField({ name: 'startDate', type: 'datetime' }),
    defineField({ name: 'endDate', type: 'datetime' }),
    defineField({ name: 'winner', type: 'string' }),
    defineField({ name: 'learnings', type: 'text' }),
  ]
})
```

## Avoiding Common Mistakes

### Don't peek and stop early
Statistical significance can fluctuate. Commit to your sample size.

### Don't test too many things at once
Each variable multiplies required sample size.

### Don't ignore segmentation
Winners may differ by device, traffic source, or user type.

### Document everything
Future you (and your team) will thank you.
