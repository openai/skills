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
$skill-installer install the ralph-wiggum-loop skill from the .experimental folder
```

Or provide the GitHub directory URL:

```
$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/ralph-wiggum-loop
```

After installing a skill, restart Codex to pick up new skills.

## Auditing skill integrity

For a quick repository audit, run:

```bash
for skill_dir in /opt/skills/skills/.curated/* /opt/skills/skills/.experimental/* /opt/skills/skills/.system/*; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  python3 /opt/skills/skills/.system/skill-creator/scripts/quick_validate.py "$skill_dir"
done

python3 /opt/skills/scripts/check_skill_references.py
```

## License

The license of an individual skill can be found directly inside the skill's directory inside the `LICENSE.txt` file.
