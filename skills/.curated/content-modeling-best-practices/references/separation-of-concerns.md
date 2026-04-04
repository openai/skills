# Separation of Content and Presentation

The most important principle in structured content: **separate what content IS from how it LOOKS**.

## The Problem

When content is tied to presentation:
- Redesigns require content migration
- Content can't be reused across channels (web, mobile, voice)
- Editors make design decisions instead of content decisions
- A/B testing requires duplicate content

## The Principle

Model content based on **meaning and purpose**, not visual appearance.

### Bad: Presentation-Focused

```
BigHeroText       → What if we want small heroes?
RedButton         → What if brand colors change?
ThreeColumnLayout → What if mobile needs one column?
LeftSidebar       → Position is a frontend concern
MobileImage       → Device-specific content is fragile
```

### Good: Meaning-Focused

```
Headline          → The main message (render however)
CallToAction      → An action we want users to take
Features          → A list of things (columns decided by frontend)
RelatedContent    → Content relationships (position by context)
Image             → One image with responsive crops
```

## Testing Your Model

Ask: "If we completely redesigned the site, would these field names still make sense?"

- `threeColumnFeatures` → ❌ Fails (what if 2 columns?)
- `features` → ✅ Works (describes the content's purpose: a list of product features)
- `blueHighlightBox` → ❌ Fails (what if we go purple?)
- `callout` → ✅ Works (describes the content's role: an attention-grabbing aside)

## Sanity Implementation

```typescript
// ❌ Avoid presentation-focused names
defineField({ name: 'bigHeroText', type: 'string' })
defineField({ name: 'fontSize', type: 'number' })
defineField({ name: 'backgroundColor', type: 'color' })

// ✅ Use meaning-focused names
defineField({ name: 'headline', type: 'string' })
defineField({ name: 'emphasis', type: 'string', options: { list: ['standard', 'prominent'] } })
defineField({ name: 'tone', type: 'string', options: { list: ['neutral', 'warning', 'success'] } })
```

The frontend translates `tone: 'warning'` to visual styles. Content stays semantic.
