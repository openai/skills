# AI/AEO Considerations

Answer Engine Optimization (AEO) prepares content to be selected as authoritative answers by AI systems like ChatGPT, Perplexity, Google AI Overviews, and Bing Copilot.

## How AI Selects Answers

AI systems evaluate content based on:

1. **Clarity:** Is the answer direct and easy to extract?
2. **Authority:** Is the source trustworthy?
3. **Comprehensiveness:** Does it fully address the question?
4. **Recency:** Is the information up to date?
5. **Structure:** Can the AI parse and understand it?

## Content Structure for AI

### Direct Answers First
Lead with the answer, then explain.

**Bad:**
> The history of JavaScript dates back to 1995 when Brendan Eich... [500 words later] ...JavaScript runs in the browser.

**Good:**
> JavaScript is a programming language that runs in web browsers. It was created in 1995 by Brendan Eich...

### Clear Headings
Use descriptive H2/H3 headings that match user questions.

**Bad:** "Overview" → "Details" → "More Information"
**Good:** "What is X?" → "How does X work?" → "When should you use X?"

### Lists and Tables
AI extracts structured information more easily than prose.

```markdown
## Benefits of Structured Content

- **Reusability:** Use content across channels
- **Flexibility:** Change presentation without changing content
- **Scalability:** Manage large content volumes
```

### FAQ Format
Question-answer pairs are ideal for AI extraction.

```typescript
// Schema for AI-friendly FAQs
defineType({
  name: 'faq',
  type: 'document',
  fields: [
    defineField({ name: 'question', type: 'string' }),
    defineField({ name: 'answer', type: 'text' }),
    defineField({ name: 'category', type: 'reference', to: [{ type: 'faqCategory' }] }),
  ]
})
```

## Technical Implementation

### Structured Data (Critical)
JSON-LD helps AI understand content type and relationships.

```typescript
// FAQ structured data
const faqSchema = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqs.map(faq => ({
    "@type": "Question",
    name: faq.question,
    acceptedAnswer: {
      "@type": "Answer",
      text: faq.answer
    }
  }))
}
```

### Canonical Content
Ensure AI finds your authoritative version, not copies.

- Set canonical URLs
- Avoid duplicate content across pages
- Use `rel="canonical"` for syndicated content

### Freshness Signals
AI systems prefer current information.

- Display publish and update dates prominently
- Update content regularly with substantive changes (superficial updates like changing dates without meaningful edits can be counterproductive)
- Use `dateModified` in structured data

## Content Quality Signals

### Author Credentials
AI systems increasingly check author authority.

- Display author name and credentials
- Link to author profiles
- Include author structured data

### Citations and Sources
Linking to authoritative sources increases trust.

- Cite primary sources
- Link to studies, documentation, official sources
- Avoid circular citations (sites citing each other)

### Comprehensive Coverage
AI prefers content that fully answers questions.

- Cover related questions users might have
- Include definitions for technical terms
- Address common misconceptions

## Google AI Overviews

Google's AI Overviews (formerly SGE) now appear in many search results. To optimize:

- **Be the cited source:** AI Overviews cite specific pages. Concise, authoritative answers increase citation likelihood.
- **Structure for extraction:** Use clear headings, direct answers, and lists that AI can easily parse.
- **Cover follow-up questions:** AI Overviews often address related queries. Anticipate and answer them on the same page or link to dedicated pages.
- **Monitor in Search Console:** Google Search Console provides data on AI Overview impressions and clicks.

## AI Crawler Management

Make conscious decisions about which AI systems can crawl your content:

- **robots.txt directives:** Use `User-agent: GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended` to control access.
- **Allowing crawlers** increases chances of being cited as a source in AI responses.
- **Blocking crawlers** prevents content from being used in AI training (but may reduce AI citations).
- Review your policy regularly — this is one of the most actively evolving areas of SEO.

## Measuring AEO Success

### Monitor AI Mentions
Track when AI assistants cite your content:
- Use Google Search Console's AI Overview data for impression and click tracking
- Monitor referral traffic from AI platforms (Perplexity, ChatGPT, Bing Copilot)
- Search for your brand + "according to" in AI assistants
- Consider third-party AEO tracking tools for comprehensive monitoring

### Track Zero-Click Queries
If AI answers questions directly, traditional rankings matter less.

### Featured Snippet Capture
Featured snippets often become AI answers. Track which you own.

## AEO vs SEO Balance

AEO and SEO largely align—quality content serves both. Key differences:

| Aspect | SEO Focus | AEO Focus |
|--------|-----------|-----------|
| Goal | Rank on page 1 | Be THE answer |
| Format | Varies | Direct, structured |
| Length | Often longer | Concise + comprehensive |
| Links | Link building | Source citations |
