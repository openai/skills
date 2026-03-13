# Question Bank

Use this bank to generate focused clarification rounds. Ask only what is needed to move readiness toward green.

## Table of Contents

1. Requirements and Scope
2. Project Route and Memory
3. Current Codebase Context
4. Constraints and Non-Goals
5. Naming Conventions (Micro)
6. Naming Conventions (Macro)
7. Acceptance and Verification
8. Round Construction by Aggressiveness

## Usage Rules

1. Pick at least one question from each unresolved dimension per round.
2. Increase depth according to `aggressiveness`.
3. Prefer concrete, answerable questions over broad open prompts.
4. Keep each round small enough for fast user response.

## Requirements and Scope

Blocking questions:

1. What exact output should be delivered, and in what format?
2. What is explicitly out of scope for this task?
3. What does success look like in one sentence?

Quality questions:

1. Which edge cases must be handled on day one?
2. Which tradeoff is preferred: speed, correctness, or maintainability?

Deep questions:

1. Which failure is unacceptable even if implementation is slower?
2. Which assumptions are safest to reject before coding?

## Project Route and Memory

Blocking questions:

1. Which project or repo should this task be routed to?
2. Is there an existing project memory source to trust for this task?
3. Should provisional startup memory be used if memory is missing?

Quality questions:

1. Which memory fields are most reliable right now, and which are stale?
2. Which project boundary signals confirm this route is correct?

Deep questions:

1. What evidence would force re-routing to another project?
2. Which memory assumption is most likely to be wrong for this task?

## Current Codebase Context

Blocking questions:

1. Which files or modules are the source of truth for this change?
2. Which interfaces must remain backward compatible?
3. Which existing tests or examples represent current behavior?

Quality questions:

1. What architectural boundaries must this change respect?
2. Which subsystem owner conventions should be preserved?

Deep questions:

1. What hidden coupling is most likely to break this change?
2. Which observability hooks are required before rollout?

## Constraints and Non-Goals

Blocking questions:

1. What deadlines, runtime limits, or policy constraints apply?
2. What should explicitly not be optimized right now?
3. What dependencies or tools are disallowed?

Quality questions:

1. Which constraints are hard vs negotiable?
2. Which risk should be accepted vs mitigated?

Deep questions:

1. Under what condition should this approach be abandoned?
2. What rollback criteria must be pre-defined?

## Naming Conventions (Micro)

Micro means symbol-level names: variables, functions, methods, classes, files.

Blocking questions:

1. What naming style should be followed for symbols in this codebase?
2. Which domain terms are mandatory in names?
3. Which abbreviations are forbidden?

Quality questions:

1. Should names optimize for brevity or explicitness?
2. How should temporary or experimental names be marked?

Deep questions:

1. Which ambiguous terms caused bugs before and should be banned?
2. Which naming pattern improves code review velocity most?

## Naming Conventions (Macro)

Macro means architecture-level names: packages, services, bounded contexts, API groups, major folders.

Blocking questions:

1. What taxonomy should govern module and service naming?
2. Which existing macro names must align with this change?
3. Which ownership boundaries should names encode?

Quality questions:

1. Should macro names reflect business domains or technical layers?
2. How should cross-team shared modules be prefixed or grouped?

Deep questions:

1. Which naming strategy minimizes future re-org churn?
2. Which macro name choices create accidental coupling?

## Acceptance and Verification

Blocking questions:

1. What test or check must pass before this is considered done?
2. What user-visible behavior must be demonstrably correct?
3. What regression must be explicitly prevented?

Quality questions:

1. What performance or reliability threshold is acceptable?
2. Which smoke tests are mandatory per milestone?

Deep questions:

1. Which metric should be tracked post-change to validate outcome?
2. What evidence would disprove the current plan?

## Round Construction by Aggressiveness

1. `1`: Ask one blocking question for each unresolved dimension.
2. `2`: Ask blocking questions plus one quality question for highest-risk dimension.
3. `3`: Ask blocking questions and quality questions for all unresolved dimensions.
4. `4`: Add deep questions for two highest-risk dimensions.
5. `5`: Add deep questions for every unresolved dimension and challenge assumptions.
