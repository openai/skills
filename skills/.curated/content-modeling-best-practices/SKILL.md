---
name: content-modeling-best-practices
description: General principles for structured content modeling that apply across CMSs, with Sanity-specific guidance. Use when designing content schemas, planning content architecture, or evaluating content reuse strategies.
metadata:
  short-description: Structured content modeling principles
---

# Content Modeling Best Practices

Principles for designing structured content that's flexible, reusable, and maintainable. These concepts apply to any headless CMS but include Sanity-specific implementation notes.

## When to Apply

Reference these guidelines when:
- Starting a new project and designing the content model
- Evaluating whether content should be structured or free-form
- Deciding between references and embedded content
- Planning for multi-channel content delivery
- Refactoring existing content structures

## Core Principles

1. **Content is data, not pages** — Structure content for meaning, not presentation
2. **Single source of truth** — Avoid content duplication
3. **Future-proof** — Design for channels that don't exist yet
4. **Editor-centric** — Optimize for the people creating content

## References

See `references/` for detailed guidance on specific topics:
- `references/separation-of-concerns.md` — Separating content from presentation
- `references/reference-vs-embedding.md` — When to use references vs embedded objects
- `references/content-reuse.md` — Content reuse patterns and the reuse spectrum
- `references/taxonomy-classification.md` — Flat, hierarchical, and faceted classification
