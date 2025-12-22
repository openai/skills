# Agent Skills

Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform at specific tasks. Write once, use everywhere.

Codex uses skills to help package capabilities that teams and individuals can use to complete specific tasks in a repeatable way. This repository catalogs skills for use and distribution with Codex. Skills in Codex follow the open [Agent Skills specification](https://agentskills.io).

Learn more:
- [Using skills in Codex](https://developers.openai.com/codex/skills)
- [Official Agent Skills specification](https://agentskills.io)

## Installing a skill

Skills in the [`.system` directory](skills/.system/) directory are automatically installed in the latest version of Codex.

To install [curated](skills/.curated/) or [experimental](skills/.experimental/) skills, you can use the `$skill-installer` inside Codex. For example:

```
$skill-installer gh-address-comments
```

## License

The license of an individual skill can be found directly inside the skill's directory inside the `LICENSE.txt` file.
