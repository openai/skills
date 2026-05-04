---
name: lean-startup
description: Eric Ries's Build-Measure-Learn loop, validated learning, and innovation accounting; the source of Q6 and the kill criteria discipline.
type: reference
---

# Lean Startup

## Origin

Eric Ries published _The Lean Startup_ in 2011 (Crown Business). The book synthesised three lineages: Toyota's lean manufacturing (Womack and Jones), Steve Blank's customer development (_The Four Steps to the Epiphany_, 2005), and the agile/XP software movement. Ries had previously been CTO and co-founder of IMVU, where the practices that became Lean Startup were field-tested under conditions of extreme uncertainty.

Three central ideas anchor the framework:

1. **Validated learning.** Progress is measured in "what we have learned about what customers want", not in "code shipped" or "features built".
2. **Build-Measure-Learn loop.** The smallest possible product is built, measured against a hypothesis, and the result feeds the next loop. The loop is the unit of work.
3. **Innovation accounting.** A reporting framework that tracks per-cohort metrics so a team can tell whether its product is genuinely improving or whether headline metrics are being inflated by mix shift, vanity selection, or growth.

## Why Lean Startup powers Q6 and kill criteria (Q9)

Question 6 of the 14 mandatory discovery questions reads: "What is the riskiest assumption?" The answer is the seed of the next Build-Measure-Learn loop. The riskiest assumption is the one that, if false, kills the product; everything else is downstream of it. For an AI product builder MVP the riskiest assumption is often: "A solo technical founder, given a working URL in 10 minutes, will pay $50/month within a week." If that assumption is false, no amount of better orchestration matters.

Question 9 reads: "Kill criteria?" Lean Startup's contribution is the insistence that the criteria be falsifiable and pre-committed. Ries's argument in the "Innovation Accounting" chapter is that without pre-committed kill criteria, teams will rationalise survival of every feature post hoc. The criteria must be: numeric, time-bound, and tied directly to the riskiest assumption.

`audit_sow.py` enforces the structural form (at least one kill criterion bullet under `## Kill Criteria` in PLAN.md). The substantive review is human: is the criterion actually falsifiable? "Users will love it" is not falsifiable. "If fewer than 3 of 10 paid pilot users complete the golden path within 10 minutes, we kill the v1 architecture and re-shape" is falsifiable.

## The Build-Measure-Learn loop

Each loop is a structured experiment:

1. **Build.** The smallest product or change that exposes the riskiest assumption to a real test.
2. **Measure.** Cohort-based, leading-indicator metrics that distinguish the experiment cohort from the baseline.
3. **Learn.** A written, signed-off conclusion: assumption confirmed, refuted, or inconclusive (and what we will do next).

The cycle is short by design. Ries advocates loops measured in days for early-stage products and weeks for mature ones. Teams that run quarterly loops have stopped being lean; they are doing waterfall in a hoodie.

For this skill, the loop maps onto the 9 gates as follows. Gates 1-2 set the hypothesis. Gates 3-5 build and instrument. Gates 6-7 measure with real users on the live URL. Gate 8 captures the learning in HANDOFF.md and DEBT.md. Gate 9 makes the regime survive.

## Validated learning vs. activity

Ries's most-cited observation: "If we are building the wrong thing, then optimising the product or its marketing won't yield significant results." The corollary is that hours spent building the wrong thing are not just wasted; they are negative-progress, because they entrench commitments to the wrong thing.

Validated learning means the team explicitly distinguishes:

- **Output.** Tickets closed, lines of code, sprint velocity. Internal-facing.
- **Outcome.** Cohort retention, conversion, NPS, the Sean Ellis 40% test, golden-path completion rate. Customer-facing.
- **Learning.** Which assumptions were confirmed or refuted; what the team now believes that it did not believe last cycle.

A high-output, low-outcome, no-learning quarter is the catastrophic case. The 9-gate regime is built to make it loud: Gate 1's outcome metric, Gate 5's real-URL E2E, Gate 6's signed UAT, and Gate 7's prod_url 200 check are all outcome anchors.

## Innovation accounting

Ries proposes three steps to graduating from "leap-of-faith" to "validated":

1. **Use a minimum viable product to establish real data on where the company is right now.** Not what you think; what is true today.
2. **Tune the engine** -- iterate on the product to improve the metrics from baseline toward the goal.
3. **Pivot or persevere** -- if iteration is not closing the gap, change strategy.

The "pivot or persevere" decision is made on a fixed cadence (Ries suggests monthly; this skill recommends per-cycle). Without a fixed cadence, the persevere choice becomes a default and the pivot never happens.

For Gate 1's outcome metric (Q5), the team writes the baseline AND the target AND the cadence on which the team will look at the gap. "Improve conversion" without those three is not an outcome metric; it is a wish.

## Pivot taxonomy

Ries names ten pivot types in chapter 8. The most operationally useful for AI product builders are:

- **Zoom-in pivot.** A single feature of the product becomes the whole product. (Most successful AI tool pivots are zoom-ins.)
- **Customer-segment pivot.** Same product, different customer. (When the engineer-tool became a designer-tool.)
- **Customer-need pivot.** Different problem. (The hardest pivot; usually a near-restart.)
- **Platform pivot.** App-to-platform or platform-to-app. (Often capability-led; often wrong.)
- **Engine-of-growth pivot.** Switch growth model (viral / sticky / paid). Late-stage.

Naming the candidate pivot in the kill-criteria section makes the pivot a real option, not a panic move. "If we miss the kill criteria, we pivot to a customer-segment pivot toward [specific segment]" is a pre-committed plan; the team is not improvising under stress.

## Common anti-patterns

**Vanity metrics.** Total signups, total page views, total stars. None of them tell you whether you are making validated progress on the riskiest assumption. Replace with cohort retention, paid conversion, golden-path completion rate.

**The MVP that is not minimum.** "MVP" gets pattern-matched to "v1.0 with three features". A real MVP is the smallest experiment that exposes the riskiest assumption. A landing page can be an MVP. A Figma click-through can be an MVP. The actual product, if it costs six months, is not an MVP; it is the bet.

**Persevere by default.** The team has not articulated kill criteria, so every cycle the answer to "should we pivot?" is "let's give it another cycle". After four cycles, the sunk cost is too large to confront. Pre-committed kill criteria break this.

**Learning without writing it down.** A loop that ends with "we learned a lot" but produces no written conclusion did not learn anything; it ran a vibe. Each loop ends with a one-page learnings doc filed alongside the OST.

## Reading list

- Ries, _The Lean Startup_, Crown Business, 2011.
- Steve Blank, _The Four Steps to the Epiphany_, 2nd ed., 2013.
- Steve Blank and Bob Dorf, _The Startup Owner's Manual_, 2012.
- Ash Maurya, _Running Lean_, 3rd ed., 2022 (operational primer).
- Ries, "Innovation Accounting" -- chapter 7 of _The Lean Startup_, also summarised at http://theleanstartup.com/principles.
