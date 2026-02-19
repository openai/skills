# Agent Team Review Gate

Use this policy when `self-improve` is running inside a multi-agent protocol workflow.

## Reviewer separation
- The actor that authored the change cannot be the actor that finalizes acceptance.

## Decision policy
- Keep the existing dual gate:
  - smoke must pass
  - regression must pass
- If either fails, decision is `reject`.

## Escalation policy
- If reviewer feedback conflicts, set task to `failed` with blocker details and escalate to orchestrator.
- Do not perform speculative second change in the same iteration.
