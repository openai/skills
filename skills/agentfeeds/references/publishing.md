# Publishing

This repository includes development files for tests, docs, packaging, and GitHub presentation. A Skills Hub release should publish a clean skill bundle instead of the raw repo.

Build the publishable bundle from the repo root:

```bash
python3 scripts/bundle/build_skill_bundle.py
```

The bundle should include:

```text
SKILL.md
agents/
assets/
references/
scripts/
LICENSE
```

The bundle should exclude:

```text
README.md
docs/
tests/
dist/
build/
*.egg-info/
__pycache__/
.pytest_cache/
.venv/
```
