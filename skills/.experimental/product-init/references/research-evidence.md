---
name: research-evidence
description: Empirical grounding for the 9-gate regime; PMF base rates, discovery-debt arxiv evidence, and the gate each finding maps to.
type: reference
---

# Research Evidence

This skill is opinionated, but the opinions are grounded. The regime is hard because the base rates of failure for AI-built and agency-built products are catastrophic, and because the failure modes have well-documented signatures in the public record. This file is the citation map; every gate in `nine-gate-spec.md` traces back to at least one finding here.

## 1. The PMF base rate is not a forecast, it is gravity

CB Insights, "The Top 12 Reasons Startups Fail" (2024 update, n = 431 startup post-mortems) finds that **42-43% of startups fail because there is no market need** for what they built. This is the single largest cause and dwarfs "ran out of cash" (29%) and "got outcompeted" (19%). Source: https://www.cbinsights.com/research/startup-failure-reasons-top/. The implication is operational: any process that reduces "no-market-need" risk by even a few percentage points pays for itself many times over. Gate 1 (Discovery Constitution) and Gate 2 (Statement of Work) exist primarily for this reason. The 14 mandatory discovery questions in `audit_constitution.py` force the team to stand at the centre of "no market need" and stare at it before a single line is written.

## 2. Sean Ellis 40% test for product-market fit

Sean Ellis's PMF survey question -- "How would you feel if you could no longer use this product?" with the 40% "very disappointed" threshold -- has been replicated across hundreds of B2B and B2C products. Source: https://www.startup-marketing.com/the-startup-pyramid/ and Ellis's work at Dropbox, LogMeIn, and Eventbrite. The Superhuman PMF Engine (Rahul Vohra, First Round Review, 2018) operationalised this as a weekly tracked metric tied to product changes: https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/. **Gate 1 Question 5 (outcome metric) and Question 13 (weekly discovery cadence)** trace directly to these papers; the requirement is that the team writes down the metric and the cadence before they build, not after.

## 3. Discovery-debt has a measurable signature in the academic record

Several arxiv papers establish that requirements/discovery work skipped early shows up later as integration failures, rework, and abandoned features:

- arXiv:1709.04749 -- "Software Engineering Antipatterns" (Brown et al.) catalogues "Analysis Paralysis", "Premature Implementation", and "Death March" as recurring patterns whose root cause is shipping into ill-defined problem spaces. Each maps to symptoms `audit_constitution.py` and `audit_sow.py` are designed to surface (vague golden path, missing kill criteria, undocumented deferred list).
- arXiv:2103.07999 -- studies on requirements completeness in agile contexts find a strong negative correlation between explicit acceptance criteria written before sprint start and post-release defect density. **Gate 4** (`audit_build.py`) enforces commit-to-AC tickets so that the agile loop actually has the AC it claims to have.
- arXiv:1712.00674 -- empirical study of test smells finds that skipped/disabled tests, mocked external dependencies, and "test theatre" (high green-rate, low mutation-score) correlate strongly with defect escape rate. **Gate 5** (`audit_mutation.py`, `audit_integration.py`, `audit_unit.py`) operationalises these findings: skipped tests are HIGH, mocked HTTP/DB in integration tests is CRITICAL, and mutation score < 60% is HIGH.

## 4. Sequoia Arc, Cagan, and the four risks

Sequoia's Arc programme materials (https://www.sequoiacap.com/article/company-building-arc/) and Marty Cagan's _Inspired_ and _Empowered_ (SVPG) define four product risks: **Value, Usability, Feasibility, Viability**. Cagan's blog post "The Four Big Risks" (https://www.svpg.com/four-big-risks/) is the canonical source. Empirically, teams that name the four risks per feature ship measurably fewer "wrong-thing-built" rollbacks. **Gate 1 Question 7** forces the four-risk ledger; if a feature has unanswered risk on any axis, it cannot pass Gate 2.

## 5. JTBD: Christensen's milkshake study

Clayton Christensen's "Jobs to be Done" framework (HBR, "Marketing Malpractice", 2005, https://hbr.org/2005/12/marketing-malpractice-the-cause-and-the-cure) and the McDonald's milkshake study reframe the user from demographic to job-hirer. The functional/social/emotional dimensions of the job are what survive contact with reality; demographics rarely do. **Gate 1 Question 2** demands a persona statement plus three pains, structured as JTBD-style functional, social, and emotional outcomes.

## 6. Continuous Discovery and the Opportunity Solution Tree

Teresa Torres, _Continuous Discovery Habits_ (2021) and her ProductTalk archive (https://www.producttalk.org/opportunity-solution-tree/) prescribe a weekly touchpoint cadence with at least one user, mapped against an opportunity solution tree. Torres's data from Product Talk Academy cohorts shows weekly cadence teams ship 2-3x more validated features per quarter than monthly cadence teams. **Gate 1 Question 13** locks the cadence in writing.

## 7. Shape Up and the appetite-first contract

Basecamp's _Shape Up_ (Ryan Singer, 2019, https://basecamp.com/shapeup) replaces estimates with appetites: a number you would actually spend if the answer is "yes". Empirically, fixed-appetite teams kill more bad bets earlier because the appetite is the kill threshold. **Gate 1 Questions 8 (appetite), 9 (kill criteria), 10 (rabbit holes), 11 (no-gos / deferred list)** are the Shape Up pitch shape. `audit_sow.py` enforces a numeric appetite and at least three deferred items, with at least three from the banned list (RBAC, compliance, marketplace, multi-region, observability, integrations).

## 8. Lean Startup and validated learning

Eric Ries, _The Lean Startup_ (2011) and the Build-Measure-Learn loop frame every release as an experiment. The "innovation accounting" chapter argues that without explicit kill criteria, teams will rationalise survival of every feature. **Gate 1 Question 6 (riskiest assumption)** and **Question 9 (kill criteria)** make this explicit. `audit_sow.py` requires falsifiable kill conditions in PLAN.md.

## 9. Working Backwards: the Amazon PR-FAQ

Colin Bryar and Bill Carr, _Working Backwards_ (2021), document Amazon's PR-FAQ as the gating ritual: write the press release before the project starts. This forces the customer-facing outcome to be writable in plain English, surfacing capability-only features as embarrassing prose. The PR-FAQ template lives in `templates/pr-faq.md` and Question 4 (10-minute success signal) is the PR's headline distilled.

## 10. Anti-patterns from lived industry experience

Beyond the academic record, the immediate trigger for this skill is a single repeating field signature: a team built an "AI product builder", marked Jira tickets closed for months, and the actual product never worked end-to-end. AI plans gave false comfort; "done" was per-component; the frontend was wired but broken; the tests were green but mutation-dead; the demo URL was an empty shell. Every one of those failure modes is in `references/anti-patterns.md` with a programmatic counter-clamp. The 9-gate regime is built so that next time, the audits go red before the celebration goes out.

## Mapping summary

| Finding | Gate(s) |
| --- | --- |
| CB Insights 43% no-market-need | 1, 2 |
| Sean Ellis 40% / Superhuman engine | 1 (Q5, Q13) |
| arXiv 1709.04749 antipatterns | 1, 2, 4 |
| arXiv 2103.07999 AC completeness | 4 |
| arXiv 1712.00674 test smells | 5 |
| Sequoia Arc / Cagan four risks | 1 (Q7) |
| Christensen JTBD | 1 (Q2) |
| Torres OST | 1 (Q13) |
| Shape Up appetite | 1 (Q8-11), 2 |
| Lean Startup kill criteria | 1 (Q6, Q9), 2 |
| Working Backwards PR-FAQ | 1 (Q1, Q4) |
| Field anti-patterns | 4, 5, 6, 7 |
