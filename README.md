# Agent Skills

Agent Skills are portable folders of instructions, scripts, and resources that AI agents can discover and use to perform specific tasks reliably.  
**Write once, use everywhere.**

This repository is the public catalog of skills designed for **Codex** (CLI, IDE extension, and Codex app), and it follows the **Agent Skills open standard**.

---

## Learn more

- Using skills in Codex  
  https://developers.openai.com/codex/skills

- Create custom skills  
  https://developers.openai.com/codex/skills/create-skill

- Agent Skills open standard  
  https://agentskills.io

---

## What is a skill?

A skill is a directory that teaches an AI agent how to perform a repeatable task.

At minimum, a skill contains a `SKILL.md` file with structured metadata and instructions.  
Skills may also include scripts, templates, documentation, and assets.

Typical structure:

```

my-skill/
SKILL.md            # required
scripts/            # optional helpers / tools
references/         # optional documentation
assets/             # optional templates or media
agents/openai.yaml  # optional UI + MCP metadata

```

### SKILL.md (required)

`SKILL.md` includes:

1. YAML frontmatter (name + description)
2. Markdown instructions the agent follows

The **description is agent-facing** and determines when Codex automatically chooses the skill.

---

## How Codex uses skills

Codex uses **progressive disclosure**:

1. Codex indexes each skill’s metadata (name, description, location).
2. When a task matches the description, Codex loads the full instructions.
3. The skill is executed only when needed.

Skills can be triggered in two ways:

### Explicit invocation
Use the skill directly from the skill picker or run:

```

/skills

```

or type `$` and select a skill.

### Automatic invocation
Codex may choose a skill automatically when your request matches the skill’s description.

---

## Repository structure

This repository groups skills by stability level:

```

skills/
.system/
.curated/
.experimental/

```

### `.system`
Skills bundled with Codex.

### `.curated`
Stable skills recommended for general use.

### `.experimental`
Early-stage skills that may change frequently.

---

## Where Codex looks for skills

Codex automatically discovers skills from multiple locations.

| Scope | Location | Purpose |
|------|----------|---------|
| Repo | `$CWD/.agents/skills` | Skills specific to the current project |
| Repo | Parent folders' `.agents/skills` | Shared across nested folders |
| Repo | `$REPO_ROOT/.agents/skills` | Shared across entire repository |
| User | `$HOME/.agents/skills` | Personal global skills |
| Admin | `/etc/codex/skills` | Shared machines or containers |
| System | Bundled with Codex | Built-in skills |

Notes:

- Symlinked skill folders are supported.
- Duplicate skill names are allowed.
- `~/.codex/skills` still works but `~/.agents/skills` is preferred.

---

## Installing skills

Use the built-in installer **inside Codex**.

### Install curated skill by name

```

$skill-installer gh-address-comments

```

### Install experimental skill

```

$skill-installer install the create-plan skill from the .experimental folder

```

### Install from GitHub directory URL

```

$skill-installer install [https://github.com/openai/skills/tree/main/skills/.experimental/create-plan](https://github.com/openai/skills/tree/main/skills/.experimental/create-plan)

```

Restart Codex after installation if the skill does not appear.

---

## Manual installation

You can manually install a skill by copying the folder.

### Repo-scoped install

```

mkdir -p .agents/skills/my-skill

# copy skill files here

```

### User-scoped install

```

mkdir -p ~/.agents/skills/my-skill

# copy skill files here

```

Restart Codex if the skill does not appear immediately.

---

## Enable or disable a skill

You can disable a skill without deleting it.

Edit:

```

~/.codex/config.toml

````

Add:

```toml
[[skills.config]]
path = "/absolute/path/to/skill/SKILL.md"
enabled = false
````

Restart Codex after changes.

---

## Optional UI metadata and MCP dependencies

To customize how a skill appears in the Codex app, add:

```
agents/openai.yaml
```

Example:

```yaml
interface:
  display_name: "My Skill"
  short_description: "User facing description"
  icon_small: "./assets/icon-small.svg"
  icon_large: "./assets/icon-large.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional wrapper prompt"

dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

This file is optional but recommended for polished skills.

---

## Creating your own skill

Fastest way:

```
$skill-creator
```

Manual approach:

1. Create a folder inside `.agents/skills/`
2. Add `SKILL.md`
3. Add optional scripts/resources

Full guide:
[https://developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill)

---

## Security and trust

Treat skills like code:

* Review scripts before installing.
* Prefer instruction-only skills unless automation is required.
* Keep descriptions precise to avoid unintended triggering.

---

## License

Each skill has its own license.

The license for a skill is located in that skill’s directory in:

```
LICENSE.txt
```
---
## Contributing

Contributions are welcome.
Please read `contributing.md` before opening a pull request.

