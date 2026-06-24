# Plugin Organization

This directory proposes a plugin layer on top of the existing skills catalog.
Each plugin wrapper contains:

- `.codex-plugin/plugin.json` for Codex plugin metadata.
- `skills/<skill-name>` symlinks back to the canonical skill directories under
  `../skills/.curated` or `../skills/.system`.

The symlinked layout keeps `skills/` as the source of truth and avoids copying
the same skill content into multiple package locations. A release pipeline
should materialize the symlinks into copied folders before publishing or
validating a self-contained plugin archive, especially when skill agent metadata
references icons or other assets.

| Plugin | Skills |
| --- | --- |
| `openai-codex-toolsmith` | `define-goal`, `migrate-to-codex`, `plugin-creator`, `skill-creator`, `skill-installer` |
| `openai-developers` | `chatgpt-apps`, `openai-docs` |
| `figma` | `figma`, `figma-use`, `figma-create-new-file`, `figma-generate-design`, `figma-generate-library`, `figma-implement-design`, `figma-code-connect-components`, `figma-create-design-system-rules` |
| `github` | `gh-address-comments`, `gh-fix-ci`, `yeet` |
| `openai-deploy` | `cloudflare-deploy`, `netlify-deploy`, `render-deploy` |
| `vercel` | `vercel-deploy` |
| `openai-web-automation` | `playwright`, `playwright-interactive`, `screenshot` |
| `openai-creative-media` | `imagegen`, `speech`, `transcribe`, `hatch-pet` |
| `openai-documents-lab` | `pdf`, `jupyter-notebook` |
| `linear` | `linear` |
| `notion` | `notion-knowledge-capture`, `notion-meeting-intelligence`, `notion-research-documentation`, `notion-spec-to-implementation` |
| `openai-app-frameworks` | `aspnet-core`, `winui-app`, `cli-creator` |
| `openai-security` | `security-best-practices`, `security-ownership-map`, `security-threat-model` |
| `sentry` | `sentry` |

`openai-docs` appears in both `.curated` and `.system`. This proposal exposes
the curated copy through `openai-developers`; maintainers should reconcile the
duplicate before publishing both as separate plugin content.
