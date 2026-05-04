---
name: working-backwards
description: Amazon's PR-FAQ method, the five customer questions, and how it forces customer-first scope at Gate 1.
type: reference
---

# Working Backwards

## Origin

"Working Backwards" is the Amazon product development practice articulated publicly by Colin Bryar and Bill Carr (former Amazon executives) in their 2021 book _Working Backwards: Insights, Stories, and Secrets from Inside Amazon_ (St. Martin's Press). The technique was institutionalised at Amazon in the early 2000s by Jeff Bezos and S Team. The thesis is the inverse of capability-led product development: instead of starting from "what can we build with the technology we have?", start from "what would the customer-facing announcement read like the day this ships?".

The artefact is the **PR-FAQ**: a press release plus a frequently-asked-questions document. The team writes the PR-FAQ before any code, design, or roadmap commitment. The PR-FAQ becomes the gate; if you cannot write a credible one-page PR, the product is not yet ready to be built.

## The PR-FAQ format

A canonical Amazon PR-FAQ is structured in seven sections:

1. **Heading.** Product name + tagline. Twelve words or fewer.
2. **Sub-heading.** The customer for the product and the problem solved, in one sentence.
3. **Summary paragraph.** What it does, who it is for, and why it matters. Four sentences.
4. **Problem paragraph.** The customer's pain in their own words.
5. **Solution paragraph.** How this product solves the pain.
6. **Quotes.** One quote from a leader at the company; one quote from a hypothetical customer. The customer quote is the load-bearing one.
7. **Call to action.** How to get started, where to learn more.

The FAQ portion supplements the PR with the hard questions: "Why now?", "How is this different from competitor X?", "What does it cost?", "What is the riskiest assumption?", "What is the v1 scope and what is explicitly not in v1?".

## The five customer questions

Bryar and Carr distil the PR-FAQ ritual into five customer-anchored questions every team must answer before building:

1. **Who is the customer?** Specific, named, segmentable. Not "developers" but "solo technical founders building a B2B SaaS MVP in 2026 who have not yet incorporated".
2. **What is the customer problem or opportunity?** Stated in the customer's words, with the cost of the problem quantified where possible.
3. **What is the most important customer benefit?** One benefit. Force-ranked. The PR-FAQ headline tests whether you can pick.
4. **How do you know what the customer needs or wants?** Evidence: interviews, sign-ups, paid pilots, retention data, support tickets. "We just know" is not an answer.
5. **What does the customer experience look like?** The first session, the first success, the first re-visit, the first share with a colleague. Concrete, narrative.

The five questions overlap with the 14 mandatory discovery questions in this skill. Q1 (Golden Path), Q2 (persona + pain), Q4 (10-min success signal), Q5 (outcome metric), and Q12 (numeric competitive benchmark) all trace back to the Amazon PR-FAQ.

## Why Working Backwards prevents capability-bloat

The capability-led failure mode goes: "We have a vector database. We have an LLM. We have a deploy pipeline. Let us combine them and announce the result." The PR-FAQ forces the inverse: write the announcement first. If the announcement reads "We combined three commodity components and produced an output the customer did not ask for", the team sees the failure on day one instead of month four.

The AI-product-builder example from this skill's origin story is exactly this trap. A capability-led PR-FAQ would have read: "Today we are launching the Multi-Agent Orchestrator that can plan, generate, test, and deploy code with five backends and a queue." A customer-first PR-FAQ would have read: "Today, a solo technical founder went from idea to deployed SaaS at solofounder.example in twelve minutes, paid $50, and is in production." The first sentence sells the team. The second sentence sells the customer. Working Backwards forces the second.

## How the skill operationalises Working Backwards

`templates/pr-faq.md` (already shipped under `templates/`) is the PR-FAQ skeleton the team fills before code starts. Gate 1's `audit_constitution.py` requires:

- A one-sentence Golden Path -- the equivalent of the PR sub-heading.
- A persona+pain -- the equivalent of the customer + problem section.
- A 10-minute success signal (Q4) -- the equivalent of the PR-FAQ headline benefit.
- A numeric competitive benchmark (Q12) -- the equivalent of the FAQ "How is this different from X?" answer.

The audit cannot judge prose quality, but it catches "the team has not written this" vs. "the team has written this". The Gate 1 review meeting reads the PR-FAQ aloud and asks: "If TechCrunch picked this up tomorrow, would the customer recognise themselves in it?". If not, back to the PR-FAQ.

## The "no-PowerPoint" rule

Bezos famously banned PowerPoint in S Team meetings in 2004, replacing it with six-page narrative memos. The reason: bullet points let writers hide. A PR-FAQ written as bullets reads "we will support X, Y, Z capabilities". A PR-FAQ written as prose forces the writer to make causal claims ("because X, Y, Z, the customer feels..."), which are falsifiable. Falsifiable claims are the prerequisite for kill criteria.

This skill applies the same rule: PRODUCT.md and PLAN.md are markdown narratives, not slide decks. The audits look for headings and prose, not for bullet-density.

## Common anti-patterns

**The aspirational PR.** "Today we changed the way humanity builds software." The CEO loves this; the customer skips it. Replace with a specific outcome: "Today, Sarah, a B2B SaaS founder, deployed her CRM idea to production in 12 minutes."

**The capability PR.** "Multi-agent orchestrator with five model backends, queue, and observability." Capability-led, customer-empty. Replace with a benefit-led outcome.

**The roadmap-FAQ.** A PR-FAQ that reads "v1 will support... v2 will add... v3 will introduce...". A PR-FAQ should describe a single moment: launch day. Roadmap belongs in PLAN.md, not in the PR-FAQ.

**The vague quote.** "I love it!" -- John Doe, customer. Replace with a quote that names a specific outcome at a specific time: "I went from idea to a paying customer in 48 hours. The previous quarter I had spent six weekends on a half-built version with [competitor]."

## Reading list

- Bryar and Carr, _Working Backwards_, St. Martin's, 2021.
- Bezos, "2004 Shareholder Letter" (origin of the narrative-memo rule), aboutamazon.com.
- The "Day 1 vs Day 2" framing -- Bezos 2017 letter.
- Templates collection: https://www.workingbackwards.com.
