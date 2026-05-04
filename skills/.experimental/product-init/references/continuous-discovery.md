---
name: continuous-discovery
description: Teresa Torres's Opportunity Solution Tree and weekly cadence; how Question 13 locks the rhythm in.
type: reference
---

# Continuous Discovery

## Origin

Teresa Torres's _Continuous Discovery Habits_ (2021, Product Talk Press) is the canonical reference. Torres had been running discovery coaching at Product Talk since 2014, and the book consolidated practices observed across hundreds of product teams. The blog archive at https://www.producttalk.org is the running, opinionated commentary; the book is the structured frame.

Two ideas anchor the practice:

1. **Continuous discovery cadence.** A product trio (PM + engineer + designer) interviews at least one customer every week. Not every quarter, not every "discovery sprint". Every week. The cadence matters more than the technique.
2. **Opportunity Solution Tree (OST).** A visual map that ties the desired outcome (top) to opportunities (gaps in customer experience), to candidate solutions, to assumption tests. The tree is updated weekly as new interviews surface new opportunities or kill old ones.

## Why weekly

Torres's empirical claim: teams running monthly or quarterly discovery underweight customer evidence relative to internal opinion, because the gap between "what the engineer believes today" and "what the customer told us last quarter" widens with time. Weekly closes the gap. The corollary: weekly cadence forces the team to recruit a sustainable interview pipeline (Calendly+ recruiting service, a partner like UserInterviews.com, or in-product prompts) instead of one-shot recruiting drives. Sustainable recruiting is itself a forcing function for "are we still selling to a segment that exists?".

## The Opportunity Solution Tree

The OST has four levels:

1. **Outcome.** The business or user outcome the team is responsible for, e.g. "First-time users complete a deployed product within 10 minutes". Outcomes are not features; they are measurable changes in user behaviour.
2. **Opportunities.** Customer pains, desires, or unmet needs surfaced through interviews. Each opportunity is phrased in the customer's voice and is mappable to one outcome. "I tried four AI builders this month and gave up because each one half-finished the project" is an opportunity.
3. **Solutions.** Candidate ways to address the opportunity. Two or more per opportunity, to force comparison. A single-solution opportunity is a sign the team has stopped exploring.
4. **Assumption tests.** For each candidate solution, the smallest experiment that would falsify the most-load-bearing assumption. Tests are sized in hours, not weeks.

The OST is updated every week. Opportunities die when interviews stop surfacing them. Solutions die when assumption tests falsify them. Outcomes change rarely (quarterly at most). The tree is shared with the whole team and serves as the single source of truth for "what we are working on and why".

## How Question 13 locks it in

Question 13 of the 14 mandatory discovery questions reads: "Discovery cadence (weekly)?". The audit (`audit_constitution.py`) checks for the keyword `discovery cadence` or `weekly touchpoint` in PRODUCT.md or PLAN.md. The substantive answer must include:

- **Who interviews.** Named PM + engineer + designer trio, or a documented stand-in.
- **How often.** Weekly is the bar.
- **Where it lives.** The OST file or board path; an OST that is nowhere is an OST that does not exist.
- **What feeds the funnel.** Recruiting source (existing user list, Calendly+, partner). A weekly cadence with no recruiting plan is fiction.

A team that says "we will interview as needed" is failing Q13. As-needed = never.

## Cadence rituals

Torres recommends three artefacts per cadence cycle:

1. **Interview snapshot.** A one-page summary per interview: who, when, the verbatim "moment of struggle" (Bob Moesta's term, JTBD), the inferred opportunity, the surprise. Snapshots are filed in a discoverable location (Notion DB, GitHub, a shared Drive folder).
2. **OST diff.** Weekly: which opportunities did we add, which did we kill, which solutions advanced, which assumption tests ran. The diff is a 5-minute standup item, not a 1-hour meeting.
3. **Outcome trend.** The outcome metric (Q5) plotted against time. Without this, the OST has no feedback loop.

For an AI product builder MVP, a healthy week might look like: 2 customer interviews (one new, one returning), 1 prototype tested with 1 user, 1 OST diff (added "users want a one-click rollback after a generated deploy fails"), and the outcome metric (10-minute success rate) tracked against the previous week.

## Common anti-patterns

**The interview drought.** "We are heads-down this sprint, we will interview after launch." The launch never comes; the interviews never resume. By the time the team looks up, they have built features no current user has asked for. The defence: weekly cadence is a non-negotiable team commitment, not a phase.

**The opportunity hoard.** A 200-node opportunity tree where nothing is ever removed. Opportunities should expire if no interview surfaces them for two cycles. The OST is a living tree, not a graveyard.

**The single-solution opportunity.** Every opportunity has exactly one candidate solution, and that candidate is "the thing the engineer wants to build". The tree is now a roadmap with extra steps. Force two or more candidate solutions per opportunity.

**The unmeasured outcome.** The outcome at the top of the tree is "delight users" or "be the best". Unmeasurable outcomes mean the tree has no kill criteria; everything below it is justifiable forever. Outcomes must be a measurable user behaviour with a baseline and a target.

**The interview-without-listening.** The PM runs the interview, asks five leading questions, and gets the answers they expected. Torres's _Continuous Discovery Habits_ has a chapter on interview craft; the short version is "ask about specific past behaviour, not opinion or speculation".

## How OST integrates with the 9 gates

| Gate | OST artefact |
| --- | --- |
| 1 Discovery | Outcomes (PRODUCT.md), top-level opportunities (PLAN.md kill criteria mapping), Q13 cadence commitment. |
| 2 SoW | Selected solutions with assumption tests; appetite tied to the test. |
| 4 Build | Each in-flight ticket maps to a solution node on the tree. |
| 5 QA | E2E `@golden-path` tests verify the outcome at the top of the tree. |
| 7 Deploy | Outcome metric tracked post-launch; tree feedback loop closes. |

## Reading list

- Torres, _Continuous Discovery Habits_, Product Talk Press, 2021.
- Torres blog: https://www.producttalk.org -- especially the OST series (https://www.producttalk.org/opportunity-solution-tree/).
- Bob Moesta + Chris Spiek, _Demand-Side Sales 101_, Lioncrest, 2020 -- interview craft.
- Steve Portigal, _Interviewing Users_, 2nd ed., 2023 -- interview craft.
- Erika Hall, _Just Enough Research_, 2nd ed., 2019 -- recruiting and bias.
