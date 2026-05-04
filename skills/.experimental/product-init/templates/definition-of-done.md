---
name: Definition of Done
description: Per-feature DoD and Golden Path release-gate.
gate: 5
audit_script: audit_qa.py
---

<!-- INSTRUCTION: This template is filled by the QA Team and Developers during the QA phase because it defines the criteria for feature completion and release. -->

## Per-Feature DoD
- [ ] [FILL: Feature 1]
  - [ ] Tied to golden_path_step: [FILL: Step]
  - [ ] AC met: [FILL: AC ID]
  - [ ] Tests green: [FILL: Yes/No]
  - [ ] No new debt markers: [FILL: Yes/No]
- [ ] [FILL: Feature 2]
  - [ ] Tied to golden_path_step: [FILL: Step]
  - [ ] AC met: [FILL: AC ID]
  - [ ] Tests green: [FILL: Yes/No]
  - [ ] No new debt markers: [FILL: Yes/No]

## Golden Path Release Gate
- [ ] Single end-to-end E2E required green for any release

<!-- DONE WHEN: All sections are filled, and the audit script passes. -->
