---
name: jtbd
description: Christensen Jobs-to-be-Done framework, the milkshake study, and how it shapes Question 2's persona+pain answer.
type: reference
---

# Jobs to be Done (JTBD)

## Origin

The Jobs-to-be-Done framework was articulated by Clayton Christensen in his 2003 book _The Innovator's Solution_ (with Michael Raynor) and the 2005 _Harvard Business Review_ article "Marketing Malpractice: The Cause and the Cure" (https://hbr.org/2005/12/marketing-malpractice-the-cause-and-the-cure). The central reframe is that customers do not "buy products"; they "hire products to do a job". The unit of analysis is the job, not the demographic.

## The milkshake study

Christensen's most cited example is the McDonald's milkshake. McDonald's had spent years optimising the milkshake based on demographic feedback (sweeter, thicker, chunkier) with no measurable impact on sales. A JTBD-led re-analysis revealed two distinct jobs being hired:

- **Morning commute job (40% of milkshake sales).** Adults driving to work needed something to occupy a long, boring drive that would last them most of the commute, was easy to consume one-handed, would not stain a suit, and would suppress hunger until lunch. They were hiring the milkshake against bagels (too dry, crumbly), donuts (sticky), and fruit (gone in two minutes). The thicker the milkshake, the better -- it lasted longer through the straw.
- **Afternoon parent-treat job (separate market).** Parents bringing kids in for a treat needed something fast, kid-portion-sized, parent-permissible. Thickness mattered less; speed of service mattered more.

Demographic analysis ("our buyers are 35-45 male commuters") missed the entire causal chain. Job analysis surfaced it in one round of interviews. The redesigns that followed (thicker mornings, smaller-portion afternoons) doubled milkshake category revenue.

The pattern generalises: products succeed when they win a job; they fail when they target a demographic. The job-to-be-done is the causal force; demographics are correlations.

## The three dimensions of a job

Christensen and later JTBD practitioners (notably Bob Moesta and Chris Spiek, _Demand-Side Sales 101_, 2020) decompose every job into three dimensions:

1. **Functional job.** What measurable outcome does the user achieve? "Get a working web app deployed in 10 minutes." "Submit a tax return without errors." "Find a song to match this mood." The functional job is the easiest to articulate and the easiest to test.
2. **Social job.** How does the user want to be seen by others while doing this job? "Look like a competent technical founder to my non-technical co-founder." "Demonstrate to my team that I tried the AI tools we discussed." "Send my designer a clean Figma file." The social job is what makes the user choose the more visible alternative even when it is functionally weaker.
3. **Emotional job.** How does the user want to feel? "Feel that I am making real progress." "Feel that I have not wasted my afternoon." "Feel that I am not going to be embarrassed by tomorrow's demo." The emotional job is what drives churn and what drives ten-out-of-ten loyalty when met.

Skipping any of the three produces a product that is locally optimal but globally rejected. Many AI products win the functional job ("we can generate the code") and lose the emotional job ("the user does not feel they have a working product"), which is why retention craters.

## Why JTBD is Question 2

Question 2 of the 14 mandatory discovery questions reads: "Persona + pain (3)". The 3 is not arbitrary. The team is required to write three pains, structured implicitly along the three JTBD dimensions:

- **Functional pain.** "I cannot get a working URL in under an hour using existing tools."
- **Social pain.** "My co-founder thinks AI tools are not real engineering, and I want to disprove that with a demo I can hand him."
- **Emotional pain.** "Every time I try a new builder, I end up with a half-finished project that mocks me from my desktop."

A persona statement with one functional pain is failing JTBD. Two pains in the same dimension is failing JTBD. Three pains across the three dimensions is the minimum bar.

## What JTBD is not

JTBD is not a replacement for personas; it is a constraint on them. A persona without a job is a horoscope. A job without a persona is an abstract noun. The pair is what travels.

JTBD is not a license to skip user research. The jobs are discovered, not deduced. The Torres Continuous Discovery cadence (`continuous-discovery.md`) is the practice that surfaces real jobs over time; JTBD is the analysis frame for what surfaces.

JTBD is not the same as "user stories". A user story is a deliverable contract ("As a / I want / so that"). A job is a causal claim about the user. The story is downstream of the job.

## Anti-patterns

**The featurised job.** "The user wants to use our AI orchestrator." This is not a job; it is the product wearing a job costume. If the user could hire a different product to do the same job, name it. If they cannot, the job is too narrow.

**The aspirational job.** "The user wants to ship a billion-dollar SaaS." Real jobs are immediate, instrumented, and provable in a 10-minute success signal (Question 4). Billion-dollar is not a job; it is a brochure.

**The internal job.** "The user wants efficient code generation." Internal jobs describe how the team thinks about its tech stack, not what the user is hiring the product for. The user hires the product to ship a working URL today.

## How `audit_constitution.py` checks Q2

The audit looks for the keyword `persona` (case-insensitive) in PRODUCT.md. This is a low bar by design; the heavy lifting is human review. The audit is a tripwire that catches "we forgot to fill it in"; it cannot catch "we filled it in with a featurised job". The Gate 1 review meeting is where a teammate reads the persona+pain entry aloud and asks: "Could a different product do this job? Is the pain functional, social, AND emotional? Could we write this paragraph for any other product and have it still be true?". If yes to any, the answer goes back for revision.

## Reading list

- Christensen, _The Innovator's Solution_, ch. 3.
- Christensen, "Marketing Malpractice", _HBR_ 2005.
- Bob Moesta, _Demand-Side Sales 101_, Lioncrest, 2020.
- Tony Ulwick, _Jobs to be Done: Theory to Practice_, 2016 -- the more rigorous, outcomes-driven (ODI) version of JTBD.
- Alan Klement, _When Coffee and Kale Compete_, 2016 -- a working-day-to-day JTBD primer.
