# Runtime Setup

Run setup from the skill root before doing real work from a fresh checkout:

```bash
python3 scripts/setup.py
```

The setup script installs an editable Python runtime into:

```text
~/.agentfeeds/runtime-venv/
```

The script wrappers re-exec through that virtual environment when it exists:

```bash
python3 scripts/agentfeeds.py --help
python3 scripts/agentfeeds_fetch.py --help
```

If Python cannot create a venv with `pip`, `scripts/setup.py` falls back to `uv pip install` when `uv` is available. If both `pip` and `uv` are missing, install one of them and rerun setup.

Console entry points installed by the package remain acceptable for local development:

```bash
agentfeeds --help
agentfeeds-fetch --help
```

For portable skill usage, prefer the bundled scripts.

After setup, verify or install background refresh:

```bash
python3 scripts/agentfeeds.py admin polling status --json
python3 scripts/agentfeeds.py admin polling install
python3 scripts/agentfeeds.py streams health --json
```

At session start, generate the compact prompt brief:

```bash
python3 scripts/agentfeeds.py brief
```

Use the default brief for stable prompt/context slots. It intentionally avoids volatile timestamps; use `--include-freshness` only for freshness debugging.

When a user prompt may be covered by existing ambient context, search local state before rerunning source-specific work:

```bash
python3 scripts/agentfeeds.py search <topic> --json
```
