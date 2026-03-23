---
name: judgment-hygiene-stack
description: Use as a lightweight judgment check when a prompt may be smuggling conclusions as facts, stretching local evidence into global claims, requiring verification of current or source-sensitive facts, or pushing action without tradeoffs. Do not use as a full reasoning framework or for simple direct tasks.
---

# Judgment Hygiene Stack

Use this skill as a small judgment cleanup tool.

Do not outsource judgment to it. Use it only to catch common failure modes before or during the answer.

## Use When

- the user's wording may be treating interpretation as fact
- local evidence is being stretched into a total judgment
- the answer may depend on current, external, legal, medical, policy, or provenance-sensitive facts
- the prompt pushes toward a meaningful action with real cost or risk
- checked evidence may be orthogonal to the user's framing
- emotional intensity may pull the answer toward overvalidation or fake caution

## Do Not Use When

- the task is simple and structurally clean
- the user only wants formatting, rewriting, or direct retrieval
- the answer does not require judgment, verification discipline, or action tradeoffs

## Checks

Apply only the checks you need. Keep them internal unless the user asks for the breakdown.

### 1. Framing

- Do not inherit loaded wording as fact.
- Separate observation from interpretation.
- Use `references/structure-judgment.md` if the main hazard is unclear.

### 2. Scope

- Do not turn narrow evidence into a total verdict without support.
- Keep the conclusion as narrow as the evidence requires.
- Use `references/judgment-hygiene.md` if you need help with observation, inference, evaluation, or abstention.

### 3. Verification Gate

- Verify before committing if the answer depends on current or external facts.
- Do not search just because a prompt is emotional.
- For screenshots, leaks, quotes, and "internal emails," verify provenance first.
- Use `references/verification-hygiene.md`.

### 4. Safety Triage

- If the prompt includes self-harm language, suicide references, or immediate danger, run safety triage first.
- Do not auto-believe the signal.
- Do not let verification or action analysis swallow it.
- Use `references/structure-judgment.md`.

### 5. Action Cost

- If recommending a meaningful action, include the main risk, burden, or reversibility constraint.
- Do not present action as free because it feels satisfying.

### 6. Orthogonal Result

- If checked evidence answers a different question than the one asked, say so plainly.
- Do not force the evidence into the user's original framing.
- Translate the result back into the user's practical decision.

## References

- `references/structure-judgment.md`: routing, premise-smuggling, hidden action, safety triage
- `references/verification-hygiene.md`: how to verify and when to stop
- `references/judgment-hygiene.md`: observation, inference, evaluation, abstention, recommendation hygiene
- `references/examples.md`: calibration examples

## Failure Modes

This skill has failed if it becomes:

- a substitute for judgment
- a long meta-preface
- a reason to over-search
- a fake display of thoughtfulness
