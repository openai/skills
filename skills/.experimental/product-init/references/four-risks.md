---
name: four-risks
description: Marty Cagan's four product risks (Value, Usability, Feasibility, Viability) and how Question 7 enforces them.
type: reference
---

# The Four Risks

## Source

Marty Cagan, founder of Silicon Valley Product Group (SVPG) and author of _Inspired_ (2008, revised 2017) and _Empowered_ (2020, with Chris Jones), articulated the four risks that every product feature must address. The canonical post is "The Four Big Risks": https://www.svpg.com/four-big-risks/. The framework underlies the Sequoia Arc programme materials (https://www.sequoiacap.com/article/company-building-arc/) and is widely adopted across product orgs whose teams operate as "missionaries, not mercenaries" (Cagan's phrase).

The four risks are:

1. **Value risk.** Will the customer buy this, or use it?
2. **Usability risk.** Can the customer figure out how to use it?
3. **Feasibility risk.** Can our engineers build it, with the time, skills, and tech we have?
4. **Viability risk.** Does this work for our business -- legal, sales, marketing, finance, support?

Cagan's argument is that every feature has all four risks at all times. Failure in any one kills the feature. Most teams obsess over feasibility (because engineers are loud about it) and viability (because finance is loud about it) and underweight value and usability (because customers are not in the standup).

## Why Q7 demands a four-risk ledger

Question 7 of the 14 mandatory discovery questions requires the team to fill a four-row ledger for the MVP scope:

| Risk | Rating | Mitigation |
| --- | --- | --- |
| Value | high / med / low | how we will test |
| Usability | ... | ... |
| Feasibility | ... | ... |
| Viability | ... | ... |

The audit (`audit_constitution.py`) looks for "value", "usability", "feasibility", "viability" tokens in PRODUCT.md/PLAN.md and flags absence. The deeper review is human: does each risk row have a real mitigation, or is "high / TBD" being used to wave the risk past?

## Risk by risk

### Value risk

The hardest risk and the most-skipped. "Will customers buy?" cannot be answered by an exec saying yes; it can only be answered by customers behaving in a way that costs them something (signing up, paying, returning, telling a friend). Mitigations that count: pre-sales, paid pilot, signed LOI, working prototype with measured retention, Sean Ellis 40% PMF survey above threshold. Mitigations that do not count: positive feedback in user interviews ("interest is not intent" -- Erika Hall), exec gut feel, a Slack channel of fans.

For an AI product builder MVP, the value risk pivots on "would a real founder pay $50/month if the tool produced a working deploy by minute 10?". Until you have one founder paying, value risk is high.

### Usability risk

A subset of value risk but operationally distinct. Even if the customer wants the outcome, can they reach it? An AI builder where the user must write Cypress tests to verify their site has lost the usability fight. Mitigations: high-fidelity prototype with five-user usability studies per Nielsen Norman group's empirical 5-user-finds-85%-of-issues guideline (https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/). Mitigations that do not count: the team using the product themselves (selection bias).

### Feasibility risk

The risk engineers usually own. "Can we build this in the appetite (Q8)?" Mitigations: spike, prototype, third-party tech evaluation, capability check on the AI provider, latency test under realistic load. Feasibility risk often hides in AI products as "we assume the model will handle this" until the eval shows it does not. Run the eval before committing to scope.

### Viability risk

The "rest of the business" risk. Will sales price this without losing margin? Will support handle the volume? Will legal sign off on the data flows? Will marketing find the audience? The deferred-list-from-`deferred-until-proven.md` is mostly viability-risk debt: RBAC, compliance, marketplace, etc. are deferred because tackling them speculatively is a viability mis-bet, not because they do not matter.

## Common failure mode: the lopsided ledger

The most common Q7 failure is a ledger where three of the four risks read "low" and one reads "high". This usually means the team has thought about one risk and bracketed the others. Cagan's empirical claim is that if the ledger looks lopsided, you have not interrogated the low-rated risks; you have just assumed them. The audit cannot catch this; the human review must.

Healthy MVP ledgers tend to look like:

| Risk | Rating | Why |
| --- | --- | --- |
| Value | high | no paying customer yet; paid pilot is Q1 milestone |
| Usability | medium | five-user prototype study scheduled week 2 |
| Feasibility | medium | model latency under 8s on benchmark prompts; needs 3s; spike planned |
| Viability | medium | pricing TBD; legal review of generated-code IP scheduled |

If you write "low" anywhere, you owe a sentence per row explaining the evidence that makes it low. "Our team has built this before" is not evidence; it is selection bias.

## Risk and appetite: the cross-table

The four-risk ledger composes with the appetite (Q8). A small appetite plus a high-value-risk feature is a kill candidate: the appetite is too small to test the value question. A large appetite plus an all-low-risk feature is overspending: you are using six weeks where two would do. The Shape Up pitch (Q8/10/11) and the four-risk ledger should be read together at the start of every cycle.

## Mapping summary

| Risk | Owner | MVP mitigation pattern |
| --- | --- | --- |
| Value | PM + customer | paid pilot, pre-sales, retention measurement |
| Usability | designer + customer | 5-user prototype study, click tests |
| Feasibility | engineering | spike, eval, latency test |
| Viability | exec + cross-functional | pricing, legal, support load model |

## Reading list

- Cagan, _Inspired_, 2nd ed., 2017.
- Cagan, _Empowered_, 2020.
- Cagan, "The Four Big Risks", svpg.com.
- Erika Hall, _Just Enough Research_, 2nd ed., 2019.
- Sequoia, "Company Building: Arc", sequoiacap.com.
