---
name: deferred-until-proven
description: Six capability categories that are banned from MVP scope until specific evidence unlocks them; the why and the unlock condition for each.
type: reference
---

# Deferred Until Proven

Six categories of work are banned from MVP scope by default. They are not banned forever. They are banned **until specific evidence** justifies their inclusion. Until that evidence exists, every hour spent on them is an hour not spent moving the user along the golden path.

`audit_sow.py` checks PLAN.md's deferred list and requires at least three of these six categories to be explicitly named. `audit_sow.py` also scans TASKS.md for any of these terms and flags CRITICAL if found inside MVP scope.

The six categories below are listed with: **definition**, **why it leaks early**, **what unlocks it**.

## 1. RBAC (Role-Based Access Control)

**Definition.** Per-user, per-resource permission systems with roles, groups, policies, scopes, OAuth scopes, attribute-based rules, organisation/team hierarchies, delegated admin, audit-grade access logs.

**Why it leaks early.** RBAC is intellectually seductive because it sounds like "just data modelling". In practice it is six months of edge cases (impersonation, soft-delete, cross-org sharing, expired roles, transient grants, service accounts) that interact with every feature you build afterwards. Worse, RBAC built before the user's actual workflow is known almost always gets ripped out: the roles you guessed are not the roles real customers need.

**What unlocks it.** A paying or actively-piloting customer asks for it in writing, names two specific roles, and the lack of RBAC is blocking purchase or churning the account. Until then, two hardcoded roles ("user" and "admin") satisfy 95% of MVP needs. If you absolutely must, ship `is_admin: boolean` and move on.

## 2. Compliance / audit chain

**Definition.** SOC 2, ISO 27001, HIPAA, PCI, GDPR DSAR pipelines, immutable audit logs, evidence collection systems, data classification frameworks, data retention policies enforced in code.

**Why it leaks early.** Engineers and PMs treat compliance as a checklist they can pre-empt. They cannot. Real compliance is contextual: the auditor's interpretation, the customer's risk team, the actual data flows you have, not the ones you guess. Pre-built compliance scaffolding is almost always wrong on at least three axes by the time the auditor walks in.

**What unlocks it.** A signed customer contract that requires it, with an attestation deadline, with budget. Or a board mandate with a date. Or your data flows touch regulated data (PHI, cardholder, EU PII) for a real user, not a hypothetical one. Until then, write a one-page security note, encrypt at rest, encrypt in transit, do not log secrets, and ship.

## 3. Marketplace

**Definition.** Multi-tenant catalogues of third-party plugins, themes, integrations, extensions, with submission flows, review processes, revenue share, partner portals, sandbox environments.

**Why it leaks early.** Marketplaces are second-order products. They require (a) enough first-order customers to justify a marketplace and (b) enough second-order developers to populate it. Building one before either condition is met produces an empty marketplace, which is worse than no marketplace because it signals abandonment. Salesforce, Shopify, and Atlassian all built their marketplaces years after their core product had clear PMF.

**What unlocks it.** Three or more independent third parties have built unofficial integrations against your API and asked for an official channel. Or a pilot customer has explicitly said they will buy if and only if their existing partner is in your marketplace. Until then, a documented webhook + REST API is the marketplace.

## 4. Multi-region

**Definition.** Active-active or active-passive deployments across two or more cloud regions, geo-routing, region-local data residency, region-aware failover, replicated databases.

**Why it leaks early.** "What if we get popular in Asia?" is a great question to think about and a terrible question to build for. Multi-region adds 40-100% to operational cost, doubles your incident-blast-radius surface area, and requires data engineering you do not have until you have product. Most products that prematurely went multi-region rolled back to single-region within 18 months because the latency wins did not justify the operational cost.

**What unlocks it.** A specific paying customer in a specific region requires data residency by contract, OR your latency SLA is being broken for >5% of traffic from a specific geography. Until then, single region with a CDN in front gets you to ~95% of the world at acceptable latency.

## 5. Observability stack

**Definition.** Distributed tracing, full-fidelity APM, custom Prometheus / Datadog / Honeycomb dashboards, custom alerting taxonomies, log aggregation pipelines, error budgets, SLI/SLO frameworks.

**Why it leaks early.** Observability is "platform work that feels like product work". It is genuinely useful at scale and genuinely a distraction before scale. Building a Honeycomb-grade pipeline before you have users to observe produces dashboards no one looks at and alerts that fire on nothing.

**What unlocks it.** First production incident that took >30 minutes to root-cause because logs were insufficient. OR sustained traffic above the threshold where eyeballing logs stops working (~10 req/s sustained, ~1 incident/week). Until then, structured JSON logs to stdout + your platform's free log viewer + Sentry-equivalent error tracking is enough.

## 6. Enterprise integrations

**Definition.** SAML SSO, SCIM provisioning, custom audit log exports, IP allowlisting, on-prem deployment options, custom data residency, BAA-signing, custom contract negotiations baked into the product.

**Why it leaks early.** Enterprise features are high-margin and high-effort. Building them before you have an enterprise pipeline is building margin you cannot capture. Each enterprise integration is a six-week project that interacts non-trivially with auth, audit, and data layers. Doing them speculatively (a) ages badly because enterprise standards shift and (b) produces unused complexity in everyone else's experience.

**What unlocks it.** A specific enterprise lead with a specific integration requirement, a deal size that justifies six weeks, and a procurement timeline you can match. Or a partnership where the integration is the wedge. Until then, OIDC + email/password covers 90% of the SMB market that you should be selling to first.

## Common failure mode: the deferred list as theatre

The deferred list is only useful if it is honoured. The failure mode is "we put it on the deferred list and then quietly built it anyway". `audit_sow.py` catches the easy form (TASKS.md mentions a deferred term) but not the subtle form (the team rebuilds RBAC under a different name like "permissions service"). The defence is the weekly Gate 1 audit run by someone outside the build team, treating the list as a contract.

## Why three of six is the threshold

`audit_sow.py` requires at least three of these six categories to be named in PLAN.md's deferred list. The number is not arbitrary. Empirically, teams that name fewer than three of these categories tend to be teams that have not actually done the deferral work; they have just written "TBD" against scope. Three forces the team to think about which two or three of the six are most tempting for their product and to name them out loud, which is what the discipline of deferral requires.

## Re-litigating the deferral

Deferred items are not closed forever. Each gate-review meeting includes one question per deferred item: "Has anything changed?". If yes (a customer asked, a contract was signed, an SLA was broken), the item is moved into a future increment with a date. If no, it stays deferred. This is the discipline that prevents both premature inclusion and amnesia-driven re-implementation.
