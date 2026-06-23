---
name: adversarial-testing
description: Review implementations for failure modes, resilience gaps, and destructive edge cases before shipping. Use when the task is to stress test a service or workflow, simulate failures, red-team operational behavior, validate restart or recovery logic, or answer "what will break?" before deploy or merge.
---

# Adversarial Testing

## Overview

Use this skill to pressure-test systems before they surprise you in production. Focus on realistic failure paths, evidence-backed risk, and the smallest set of tests that proves whether the implementation can survive bad inputs, missing dependencies, retries, restarts, and degraded environments.

## Workflow

1. Define the target clearly: service, job, script, deployment, cron, queue worker, or end-to-end workflow.
2. Identify the highest-risk failure axes:
   - malformed or empty input
   - authentication, authorization, and secret handling
   - dependency loss or API changes
   - retries, idempotency, and duplicate execution
   - concurrency and race conditions
   - restarts, crashes, and reboot behavior
   - disk, memory, or network pressure
3. Separate safe checks from destructive simulations.
4. Run or propose tests in this order:
   - static review and configuration review
   - safe local or staging checks
   - integration and recovery tests
   - destructive simulations only after explicit user approval
5. Report findings with severity, evidence, likely impact, and concrete mitigation.

## What To Look For

- Does the system fail safely when inputs are missing, malformed, late, duplicated, or oversized?
- Does it restart cleanly without corrupting state or replaying work unexpectedly?
- Are timeouts, retries, and backoff behavior explicit and bounded?
- Are secrets, tokens, and sensitive logs handled safely under failure conditions?
- Does the system degrade clearly when a dependency is down, slow, or partially broken?
- Can operators tell what happened from logs, metrics, and state files?

## Guardrails

- Never run destructive commands without explicit approval from the user.
- Treat reboot tests, process kills, disk-fill tests, firewall drops, and credential rotation as destructive.
- Prefer staged reproduction or dry runs when production behavior can be learned safely there.
- Do not inflate risk with generic hypotheticals; keep findings tied to the actual system.
- Prioritize unattended systems and automations, where silent failure is especially costly.

## Reporting Format

Summarize findings in a compact structure:

```text
Issue:
Severity:
Evidence:
Failure scenario:
Mitigation:
```

If no serious issues are found, say so explicitly and note what was and was not tested.
