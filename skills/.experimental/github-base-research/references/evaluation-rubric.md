# Evaluation Rubric

## Hard reject signals

- Repository is archived or disabled.
- No clear license when commercial usage is expected.
- Last meaningful update is older than 24 months without clear stability rationale.
- Missing basic project documentation (install/run instructions).

## Strong positive signals

- Active maintenance in the last 90 days.
- Clear architecture and setup docs.
- Test suite or CI workflow present.
- Release cadence or tagged versions.
- Healthy contributor and issue response activity.

## Scoring interpretation

- `0.75 - 1.00`: Strong foundation candidate.
- `0.60 - 0.74`: Usable with targeted gap work.
- `0.45 - 0.59`: Risky, only use for narrow subsystems.
- `< 0.45`: Usually not suitable as a base.

## Single-base recommendation rule

Recommend a single base when:
- Coverage of required capabilities is at least 70%, and
- No high-risk red flags exist.

## Multi-repo recommendation rule

Recommend composition when:
- No single repo reaches acceptable capability coverage, and
- Two or three repositories together cover key capabilities with manageable integration boundaries.

Define boundaries explicitly:
- Primary shell (routing/runtime)
- Domain subsystem (billing/auth/search)
- Shared infra layer (SDK, queue, persistence, observability)
