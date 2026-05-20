# Luck Skill (黄历 Skill)

[English](README.md) | [简体中文](README_zh.md)

It is like an Eastern strategist and a Western Lady Luck in one: reading traditional almanac signals to help you choose timing, direction, colors, and a little extra good fortune for the day.

A Chinese almanac (黄历) skill for AI coding assistants. Get daily luck cards, outfit color guidance, and traditional almanac insights — translated into modern, practical advice.

If this skill is useful to you, please consider giving the repo a star. It really means a lot to me! 🌟

## Features

- **Daily Luck Card** — Today's almanac at a glance: day quality, lucky directions, clothing colors, dos and don'ts
- **Scenario Check** — Ask if a specific action is suitable: deploying code, signing contracts, interviews, travel, gaming, etc.
- **Clothing Colors** — What colors to wear today based on the Five Elements
- **Peng Zu Taboo** — Ancient cautions translated into modern daily tips
- **Hourly Luck** — Check which two-hour periods are auspicious
- **Multilingual** — Responds in your language. Ask in Chinese, get Chinese. Ask in English, get English.
- **Playful Tone** — Fun lines sprinkled in when the moment fits; ridiculous questions get a reality check with practical alternatives

## Installation

### Quick Install

Just tell your AI assistant:

> Install this skill from https://github.com/clllb/luck-skill

### Manual Install

**Claude Code**

```bash
git clone https://github.com/clllb/luck-skill.git ~/.claude/skills/luck-skill
```

**OpenAI Codex**

```bash
git clone https://github.com/clllb/luck-skill.git ~/.codex/skills/luck-skill
```

**OpenCode**

```bash
mkdir -p ~/.config/opencode/skill
git clone https://github.com/clllb/luck-skill.git ~/.config/opencode/skill/luck-skill
```

Then invoke with `/luck-skill` or just ask naturally — in Chinese, English, or any language you prefer.

## Usage

Just talk to your AI assistant naturally. Examples:

| You say | You get |
|---------|---------|
| `What's today's almanac?` | Full daily luck card |
| `Is tomorrow a good day to deploy?` | Deployment readiness check |
| `What colors should I wear today?` | Outfit color guide |
| `Is tonight good for gaming?` | Gaming timing advice |
| `Can I go to space tomorrow?` | Playful reality check + practical tips |
| `How does today look for signing a contract?` | Contract signing guidance |
| `What should I wear for an interview today?` | Interview outfit + direction tips |

The skill fetches real almanac data and gives grounded, modern advice — never deterministic fortune-telling.

## Data Sources

Almanac data is generated and hosted by [Toolbox](https://github.com/clllb/toolbox).

## Disclaimer

This skill provides traditional Chinese almanac content for **cultural and entertainment purposes only**. It does not predict outcomes or replace professional judgment. For medical, legal, financial, employment, or major contract decisions, rely on qualified professionals.

## License

MIT
