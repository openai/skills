# Test Quality Review Guide — Mode 4

**Purpose:** Diagnose the health of a test suite using six test-space decay risks.
Every finding must follow the Iron Law: Symptom → Source → Consequence → Remedy.

---

## Before You Start: Build the Test Suite Map

Before scanning for any risk, map the current test suite structure:

```
Unit tests:        X files, ~N tests
Integration tests: X files, ~N tests
E2E tests:         X files, ~N tests
Ratio:             Unit X%  :  Integration X%  :  E2E X%
Coverage areas:    [modules with tests] vs [modules without tests]
```

If you cannot access test files directly, ask the user **one question** — choose the
most relevant:
1. "Which module is hardest to test or has the least coverage?"
2. "When you make a change, how often do unrelated tests break?"
3. "Is there a part of the codebase your team avoids touching because it has no tests?"

After one answer, proceed. Do not ask more than one question.

---

## Analysis Process

Work through these five steps in order.

### Step 1: Scan for Test Obscurity

*Scan this first — the most visible risk and the one that determines whether the suite
is maintainable at all.*

Look for:
- Read 5–10 test names at random: can each one communicate subject + scenario + expected
  outcome without opening the test body?
- Are there tests where a failure gives no clue which behavior broke (multiple assertions,
  no message strings)?
- Does any test depend on external state (files, database rows, env variables, shared mutable
  fixtures) that is invisible from within the test body?
- Is there a single massive setUp or beforeEach that every test inherits regardless of
  what it actually needs?

If all test names are clear and setups are minimal → no finding.

### Step 2: Scan for Test Brittleness and Mock Abuse

*These two risks co-occur: over-mocking produces tests that are both fragile and vacuous.
Scan them together.*

Look for Test Brittleness:
- Ask (or check git history): did any recent refactor cause test failures with no
  behavior change?
- Are there test methods where the name contains "and" or that assert on 3 or more
  unrelated behaviors (Eager Test)?
- Do assertions specify mock call order or exact parameter values that are irrelevant
  to the observable behavior?

Look for Mock Abuse:
- Sample 3–5 tests: is mock setup longer than the test logic?
- Are the primary assertions `expect(mock).toHaveBeenCalledWith(...)` rather than
  assertions on outputs, state, or events?
- Are there methods in production classes that are only called from test files?
- Does any single test create more than 3 mock objects?

### Step 3: Scan for Test Duplication

Look for:
- Is the same setup block (same variables initialized the same way) repeated across
  5 or more test files without a shared helper?
- Are there multiple tests that pass identical inputs and assert identical outputs
  with no differentiation (Lazy Test)?
- Is the same business scenario covered at unit, integration, and E2E level with no
  difference in what each layer is testing?

If duplication is systemic (10 or more instances) → Critical.
If localized (3–5 instances) → Warning.

### Step 4: Scan for Coverage Illusion and Architecture Mismatch

Look for Coverage Illusion:
- Pick the most recently modified core module. Are its error-handling branches and
  null/boundary inputs covered by tests?
- Are there legacy areas (old functions, no test files nearby) that are actively
  being changed?
- Do the tests assert on side effects (DB writes, events emitted, state transitions)
  or only on return values?

Look for Architecture Mismatch:
- Compare the suite map from the start: is the ratio close to 70% unit / 20% integration / 10% E2E?
- If legacy code is being modified, are there Characterization Tests that captured
  behavior before the change?
- Is the full suite execution time known? If > 10 minutes, note as 🟡 Warning.
- Are high-risk modules tested at higher density than trivial utilities?

### Step 5: Apply Iron Law, Output Report

For every finding identified above, write it in this format:

```
**[Test Risk Name] — [Short title]**
Symptom: [the exact thing observed in the test files — quote file names or patterns]
Source: [Book title — Smell or Principle name]
Consequence: [what happens to the test suite if this is not addressed]
Remedy: [concrete, specific action]
```

Do not write a finding you cannot complete. If you can identify a symptom but cannot
state a consequence, re-read `test-decay-risks.md` for that risk before writing the finding.

---

## Output

Use the standard Report Template from `SKILL.md`.
Mode: Test Quality Review
Scope: the test files or directory reviewed.

Include the Test Suite Map as a code block before the Findings section,
labeled "Test Suite Map".
