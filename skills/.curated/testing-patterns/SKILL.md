---
name: testing-patterns
description: Plan and write effective tests across static checks, unit tests, integration tests, end-to-end flows, and visual regression. Use when the task is to add tests, improve coverage, choose a test strategy, fix brittle tests, decide what not to test, or set up test tooling for a repository or feature.
---

# Testing Patterns

## Overview

Use this skill to choose the smallest test that gives real confidence, reuse the repository's existing tooling, and keep tests anchored to behavior rather than implementation details. Start from the contract that matters, then pick the right layer.

## Workflow

1. Inspect the existing test stack first: manifests, lockfiles, CI config, test directories, and current naming conventions.
2. Reuse the repo's current framework unless it is clearly broken or missing for the target layer.
3. Decide which behavior matters and what the smallest proving test is.
4. Choose the test layer:
   - static checks for types, schemas, and obvious contract validation
   - unit tests for pure logic and narrow state transitions
   - integration tests for component boundaries, handlers, services, and data flow
   - end-to-end tests for critical user journeys or cross-system flows
   - visual regression for layout-sensitive UI where screenshot comparison is the right signal
5. Write or update the tests close to the changed code, keep fixtures lean, and prefer deterministic inputs.
6. Run the narrowest relevant test command first, then broaden only if the change touches shared behavior or the local signal is weak.

## Layer Selection

- Use static checks for compile-time guarantees, schema validation, serialization boundaries, and basic misuse prevention.
- Use unit tests for calculations, parsers, selectors, reducers, and small helpers.
- Use integration tests when confidence depends on multiple layers working together, such as API handlers plus storage, components plus data fetching, or command handlers plus side effects.
- Use end-to-end tests only for flows that really need the whole system to cooperate.
- Use visual regression when the acceptance criterion is visual stability, not just DOM shape.

## Test Writing Rules

- Test behavior the user, caller, or downstream system cares about.
- Prefer one clear expectation per test, even when setup is shared.
- Control time, randomness, and network behavior so failures are reproducible.
- Keep fixtures and factories small enough that the assertion is obvious.
- Name tests after expected behavior and the condition under which it holds.
- Prefer meaningful assertions over broad snapshots or mock-call bookkeeping.
- Do not test private methods or framework internals unless they are the only observable contract.

## Framework Guidance

- If the repo already has a test framework, stay consistent with it.
- For JavaScript or TypeScript repositories, load `references/javascript-typescript.md`.
- For repository-level browser automation or E2E tests, use the existing repo setup; if the task is terminal-driven browser work rather than adding test files, prefer the `$playwright` skill when it is available.
- For Python, prefer `pytest` unless the repo already standardizes elsewhere.
- For Go, prefer the standard `testing` package.
- For other stacks, follow the repository's conventions before introducing new tools.

## Anti-Patterns

- Do not add end-to-end tests for behavior that can be proven with a unit or integration test.
- Do not mock away the core logic you are actually trying to verify.
- Do not chase coverage percentages at the expense of high-value paths.
- Do not leave flaky waits, real-time sleeps, or environment-coupled assumptions in tests when a deterministic alternative exists.
- Do not convert unclear requirements into fragile tests; tighten the contract first.

## Deliverables

- New or updated tests at the right layer
- The minimal fixture, helper, or mock setup needed to support them
- The exact test command(s) run
- Any remaining gaps, especially if a higher-level test could not be added in the current environment
