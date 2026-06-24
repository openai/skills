# OpenAI Skills Plugin Marketplace

This directory proposes a Codex-compatible marketplace shape for the skill
catalog. The marketplace groups related skills into installable plugins while
keeping the canonical skill source under `skills/`.

The entries in `marketplace.json` point at lightweight wrappers under
`plugins/<plugin-name>`. Each wrapper has a `.codex-plugin/plugin.json` manifest
and a `skills/` directory with symlinks back to the canonical skill folders.
This avoids duplicating skill content in the repository while making the
intended plugin boundaries explicit.

If a distribution process requires self-contained plugin archives, replace the
symlinked `plugins/<plugin-name>/skills/<skill-name>` entries with copied skill
directories during packaging before running ingestion validation. This is
especially important for skills with `agents/openai.yaml` icon references,
because those assets must live inside the final plugin archive.
