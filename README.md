# Agent Skills

Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform at specific tasks. Write once, use everywhere.

Codex uses skills to help package capabilities that teams and individuals can use to complete specific tasks in a repeatable way. This repository catalogs skills for use and distribution with Codex.

Learn more:
- [Using skills in Codex](https://developers.openai.com/codex/skills)
- [Create custom skills in Codex](https://developers.openai.com/codex/skills/create-skill)
- [Agent Skills open standard](https://agentskills.io)

## Installing a skill

Skills in [`.system`](skills/.system/) are automatically installed in the latest version of Codex.

To install [curated](skills/.curated/) or [experimental](skills/.experimental/) skills, you can use the `$skill-installer` inside Codex.

Curated skills can be installed by name (defaults to `skills/.curated`):

```
$skill-installer gh-address-comments
```

For experimental skills, specify the skill folder. For example:

```
$skill-installer install the create-plan skill from the .experimental folder
```

Or provide the GitHub directory URL:

```
$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
```

After installing a skill, restart Codex to pick up new skills.

## License

The license of an individual skill can be found directly inside the skill's directory inside the `LICENSE.txt` file.
