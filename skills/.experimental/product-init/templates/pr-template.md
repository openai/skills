---
name: Pull Request Template
description: Template for pull requests.
gate: 4
audit_script: audit_build.py
---

<!-- INSTRUCTION: This template is filled by the Developers during the build phase because it standardizes the pull request process. -->

- **golden_path_step:** [FILL: 1-7]
- **AC ID (link to TASKS.md):** [FILL: AC ID]
- **DEBT introduced? (yes->link to DEBT.md row):** [FILL: Yes/No]
- **E2E test added? (link to test):** [FILL: Yes/No]
- **Console errors triggered? (must be no):** [FILL: Yes/No]
- **Preview URL (Vercel/Netlify link):** [FILL: Preview URL]

## Self-Checklist
- [ ] All tests pass
- [ ] Code is reviewed
- [ ] Documentation is updated
- [ ] Changes are committed and pushed

<!-- DONE WHEN: All sections are filled, and the audit script passes. -->
