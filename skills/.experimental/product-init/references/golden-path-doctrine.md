---
name: golden-path-doctrine
description: The central question every task in this skill must answer; the doctrine the filter script enforces.
type: reference
---

# Golden Path Doctrine

## The central question

> **"Bu is kullaniciyi fikirden calisan deploy edilmis urune yaklastiriyor mu? Hayirsa MVP disi."**
>
> _Does this work move a user closer to a working, deployed product? If not, it is out of MVP scope._

This is the only question that matters. Every task, every story, every PR, every architectural decision is filtered through it. If the answer is "yes, and I can name the user, the product step, and the next deploy", the task is on path. If the answer requires a paragraph of justification, the task is off path and goes to the deferred list.

## Why this doctrine exists

The skill was born out of a specific failure mode. A team built an "AI product builder" platform. Jira showed dozens of closed tickets each sprint. Demos showed AI plans being generated, capabilities being unlocked, integrations going live. The team felt productive. The system was active.

The product never actually worked end-to-end. A real user could not start at "I have an idea" and finish at "I have a deployed working product". The frontend rendered, but it was wired to plans that were never executed. The tests were green, but they tested mocks of the things that had never been built. The Jira board was a fiction the team had agreed to believe in.

The root cause was not laziness. The root cause was that the team had stopped asking the central question. They had switched from "are we delivering the product?" to "are we shipping capabilities of the platform?". Every closed ticket was a real piece of work. None of them, in aggregate, produced the product.

The Golden Path Doctrine is the antidote. It is a forcing function: if a task cannot be tied to one of the seven golden path steps, it is not allowed to consume MVP time.

## The seven golden path steps

A user, in their own words, walks from idea to live product through exactly seven steps:

1. **Intake.** I tell the system my idea, my persona, my pain.
2. **Spec.** The system gives me back a specification I recognise as my idea, in a form I can edit.
3. **Code.** The system writes the code that implements that spec.
4. **Test.** The system tests the code against the spec, on real infrastructure, end-to-end.
5. **Deploy.** The system deploys the code to a URL the user can hit.
6. **Handoff.** The user gets the source, docs, credentials, and a walk-through.
7. **Support.** When something breaks, the user has a path to fix or escalate.

Anything that does not advance one of these seven steps is deferred. RBAC, compliance, marketplace, multi-region, observability stack, enterprise integrations -- all are post-MVP unless they are blocking the seven-step walk for the actual user being served.

## How `filter_task.py` enforces it

The filter script is intentionally simple. It tokenises the task description and scores tokens against keyword sets for each of the seven golden path steps:

| Step | Keywords (sample) |
| --- | --- |
| 1 Intake | intake, discovery, interview, persona, idea, brief, kickoff |
| 2 Spec | spec, specification, requirements, AC, acceptance, design, wireframe |
| 3 Code | code, implement, build, refactor, feature, endpoint, component |
| 4 Test | test, unit, integration, e2e, playwright, vitest, pytest, coverage |
| 5 Deploy | deploy, release, preview, staging, production, vercel, netlify |
| 6 Handoff | handoff, documentation, runbook, credentials, walkthrough |
| 7 Support | support, incident, monitor, alert, bugfix, hotfix, maintenance |

If the maximum score across all seven steps is below 0.3, the script prints `DEFER: no golden_path_step match` and exits non-zero. This is deliberately blunt. It is better to have a noisy false positive that forces a human to write a one-line justification than a silent off-path drift that costs a sprint.

The filter is not a substitute for judgement. It is a tripwire. When it fires, the human in the loop reads the task, decides whether the keywords are missing because the work is off-path or because the description is vague, and either rewrites the task description (so the filter passes) or moves the task to the deferred list. The filter cannot be made smarter without making it less useful.

## What the doctrine does not say

The doctrine does not say "ship sloppy". It says "ship narrow". The standard for what is on the path is high; the test of whether something is on the path is yes/no, not "kind of". A polished onboarding screen for a feature the user does not yet need is off-path. A flaky deploy of the feature the user does need is on-path-but-broken, which is a Gate 5 problem, not a Gate 1 problem.

The doctrine does not say "no platforms". Platforms are legitimate when the platform is the product. The failure mode is platform-as-displacement-activity: building platform features that no current user needs because they feel like progress. The doctrine cuts that.

The doctrine does not say "no debt". It says debt must be named. Every TODO/FIXME/HACK in a diff requires a DEBT.md row referencing `<file>:<line>` (`audit_build.py`). Naming the debt makes it possible to pay it; hiding it makes it compound.

## Daily ritual

At the start of every working session, the lead reads the Golden Path sentence from PRODUCT.md aloud. Yes, aloud. The doctrine is a habit, not a slogan. Every standup ends with a one-line answer to the central question for each task in flight: yes, on step N; or no, deferring. Anything that cannot answer in one line is decomposed until it can.

## Failure mode if the doctrine is dropped

When the Golden Path Doctrine is dropped, the visible signature is fast: backlog inflation, increasing rate of closed tickets, decreasing rate of working golden-path runs, a demo URL that becomes an empty shell, console errors that no one fixes, integration tests that mock the things that should be real. `audit_real_wiring.py`, `audit_console_clean.py`, `audit_integration.py`, and `audit_demo_url.py` exist precisely to detect that drift before it becomes the next post-mortem.
