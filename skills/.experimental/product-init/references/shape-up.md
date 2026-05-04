---
name: shape-up
description: Basecamp's Shape Up pitch (Problem, Appetite, Solution, Rabbit Holes, No-gos) and how it powers Q8/10/11.
type: reference
---

# Shape Up

## Origin

_Shape Up_ by Ryan Singer (2019, free at https://basecamp.com/shapeup) documents the product development methodology Basecamp evolved over fifteen years and used to build Basecamp 3 and Hey. Singer was Head of Product Strategy at Basecamp and wrote the book to externalise practices that were, until then, informal. The methodology has since been adopted by hundreds of small product teams who reject Scrum's estimate-driven cadence in favour of fixed-time, variable-scope cycles.

## The five-section pitch

The Shape Up pitch is the artefact every initiative produces before being scheduled into a six-week cycle. It has five sections:

1. **Problem.** The raw user pain or business need. One paragraph, in user-vocabulary, with a specific instance.
2. **Appetite.** How much time the team is willing to spend on this. A small batch is two weeks; a big batch is six weeks. The appetite is fixed; the scope flexes around it.
3. **Solution.** A "fat-marker sketch" of the solution: enough fidelity to communicate the shape, not so much that engineering loses optionality. Singer is explicit that the sketch is intentionally underspecified.
4. **Rabbit holes.** The places where the team could spend the entire appetite if not warned off. Listed explicitly so the team can route around them.
5. **No-gos.** What is explicitly out of scope. The deferred list.

Together, the five sections make the pitch a contract: the team will spend X time on this problem, attempt this shape of solution, avoid these rabbit holes, and not build these no-gos. If the appetite is exceeded, the work is killed -- not extended.

## Why Shape Up powers Q8, Q10, and Q11

The 14 mandatory discovery questions adopt three Shape Up sections directly:

- **Q8 -- numeric appetite.** "What is your appetite in weeks or budget?" `audit_sow.py` regex-greps PLAN.md for `appetite\s*[:=]?\s*\d+\s*(week|day|sprint|hour|\$)`. Without a number, the appetite is a wish.
- **Q10 -- rabbit holes.** "What rabbit holes will eat the appetite?" Examples for an AI product builder: state synchronisation between agent runs, cross-cloud deploy abstractions, semantic diffing of generated code. Naming them upfront lets the team build trip-wires (timeboxes, escape hatches, "just hardcode it for v1").
- **Q11 -- deferred list / no-gos.** "What is explicitly out of v1?" Must include three or more of the banned MVP categories (`deferred-until-proven.md`).

## The fixed-time, variable-scope contract

The deepest Shape Up commitment is that **time is fixed and scope is flexible**, never the inverse. The team does not "estimate how long it will take and then do all of it". The team takes the appetite, picks the scope it can ship in that appetite, and ships exactly that. If the appetite runs out, the work is shipped at whatever-state-it-is-in or killed. There is no "we just need two more weeks". Two more weeks is a new cycle, requiring a new pitch.

This contract is incompatible with most velocity-based agile rituals. Shape Up has no story points, no burndown chart, no daily standup as ceremony. It has the pitch, the betting table (where pitches are selected for the next cycle), the cycle itself (six weeks of focused work), and the cool-down (two weeks of cleanup, exploration, debt). The cycle is the unit; the sprint is not.

For this skill, the appetite (Q8) is the kill threshold. If the team is consistently shipping past appetite, either the appetites are wrong or the scope is wrong; either way, the pitch contract is broken.

## Hill chart, not burndown

Shape Up replaces burndown with the **hill chart**: every work item is plotted on an "uphill / downhill" curve. Uphill = "still figuring out how to do it". Downhill = "now executing the known plan". The chart is updated by ICs themselves, not by a project manager pulling tickets. Items stuck uphill are the rabbit holes (Q10) that the pitch warned about; they are escalation candidates.

This skill does not enforce hill charts (that would be over-prescription), but the pattern matters: the audit suite is built so that gates fail when the work is "obviously stuck" -- a stuck Gate 5 is the audit's version of "stuck uphill on testing". The signal is the same; the artefact differs.

## Common anti-patterns

**The infinite appetite.** "We will spend whatever it takes." This is not Shape Up; it is a death march. Real appetites are uncomfortable; they force scope choices.

**The estimate disguised as appetite.** "Appetite: 6 weeks (we estimate it will take 6 weeks)." The appetite is what you are willing to spend, not what you predict it will cost. If the estimate equals the appetite, you have not made a bet; you have copied a guess.

**The expanding solution.** The fat-marker sketch becomes a Figma mock, becomes a 30-page spec. By the time engineering starts, the optionality has been spent. Singer's rule: keep the sketch genuinely fat-marker; let the team make local decisions.

**The unspecified no-gos.** "Out of scope: TBD." The no-gos must be enumerated. If it is not on the no-gos list, an engineer is allowed to assume it is in scope. Audit (`audit_sow.py`) catches the empty deferred list.

## Worked example: AI product builder MVP pitch

```yaml
problem: |
  Solo technical founders trying to ship a B2B SaaS MVP spend 4-6 weekends
  on infrastructure and CRUD scaffolding before any customer-facing
  feature. They give up before they reach a paying customer.

appetite: 6 weeks

solution_sketch: |
  A single-page intake form -> AI generates spec -> user edits -> AI
  generates code -> tests run on a real preview URL -> one-click deploy
  to Vercel/Fly. The user gets a working URL within 10 minutes of intake.

rabbit_holes:
  - Multi-cloud deploy abstraction. Use Vercel only in v1.
  - Generic spec editor. Pre-fill from a small template library.
  - Custom auth. Use NextAuth or equivalent provider in v1.
  - Cross-agent state sync. Use a single agent in v1; multi-agent v2.

no_gos:
  - RBAC; one user per project.
  - Compliance / SOC2 evidence collection.
  - Marketplace of templates; ship 5 hardcoded templates.
  - Multi-region.
  - Observability dashboard; structured logs only.
  - SAML / SCIM enterprise integrations.
```

This pitch passes `audit_sow.py`: numeric appetite, named rabbit holes, deferred list with five of the six banned categories.

## Reading list

- Singer, _Shape Up_, Basecamp, 2019, free online: https://basecamp.com/shapeup.
- "Shape Up FAQ" on Basecamp's site for adoption questions.
- "Three Levels of Product Hierarchy", Singer's follow-up on Substack, for the appetite -- pitch -- cycle relationship.
- David Heinemeier Hansson's "Reconsider" essay (https://world.hey.com/dhh/reconsider-41f44e9c) for the cultural backdrop.
