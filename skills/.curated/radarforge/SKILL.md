---
name: radarforge
description: Operate RadarForge, a Telegram-first local signal and interest radar sidecar app for Hermes Agent.
version: 0.1.0
author: Günter Weber
license: MIT
metadata:
  hermes:
    tags: [radarforge, hermes-agent, telegram, local-first, interest-radar, sqlite, cron]
---

# RadarForge

Use this skill when installing, operating, adapting, or troubleshooting RadarForge.

RadarForge is a local-first Hermes sidecar app that collects topic streams, ranks them with explicit reasons, sends Telegram cards, and learns from inline feedback. Security is the first dogfood profile, but the same pattern works for research, engineering blogs, markets, policy, and personal interests.

## Repo and paths

```text
Repo: https://github.com/gweber/radarforge
Recommended checkout: ~/.hermes/apps/radarforge
Runtime DB: ~/.hermes/data/radarforge/radarforge.sqlite
App manifest: hermes-app.yaml
```

## Install / update

```bash
git clone https://github.com/gweber/radarforge ~/.hermes/apps/radarforge
cd ~/.hermes/apps/radarforge
python -m pip install -e . pytest pyyaml
python -m pytest tests -q
python -m radarforge.cli init
python -m radarforge.cli doctor
```

For an existing checkout:

```bash
cd ~/.hermes/apps/radarforge
git pull --ff-only
python -m pytest tests -q
```

## Configure topics

Inspect and activate a profile:

```bash
python -m radarforge.cli profiles list
python -m radarforge.cli profiles show research
python -m radarforge.cli profiles activate research
python -m radarforge.cli prefs
```

Checked-in starting points:

- research
- engineering
- security
- personal

For ad-hoc source experiments, start with:

```bash
cp config.example.yaml config.yaml
# or: cp profiles/security.yaml config.yaml
```

Then edit `config.yaml` with feeds for the use case:

- security / infrastructure
- AI/ML research
- engineering blogs
- markets / policy
- personal hobbies

## Safe operation

Always dry-run before live Telegram sends:

```bash
python -m radarforge.cli cards --limit 5
python -m radarforge.cli send-cards --dry-run --limit 5
python -m radarforge.cli watch-tracked --dry-run
```

Only live-send after dry-run output looks sane and the Telegram environment is configured.

## Useful CLI commands

```bash
python -m radarforge.cli init
python -m radarforge.cli collect-rss --source-name "Demo Research" --from-file examples/feeds/research.xml
python -m radarforge.cli collect-cisa  # optional security-profile adapter
python -m radarforge.cli profiles list
python -m radarforge.cli profiles activate research
python -m radarforge.cli prefs
python -m radarforge.cli feedback summary
python -m radarforge.cli cards --limit 5
python -m radarforge.cli why <item_id>
python -m radarforge.cli saved
python -m radarforge.cli tracked
python -m radarforge.cli sources
python -m radarforge.cli watch-tracked --dry-run
python -m radarforge.cli send-cards --dry-run --limit 5
```

## Telegram/Gateway rules

- Telegram is a delivery adapter; keep business logic in the RadarForge package.
- `/radar` command handlers should authenticate the sender before invoking the sidecar CLI.
- Sidecar subprocess calls need timeouts and cleanup.
- Supported private Gateway commands mirror the CLI: `/radar profiles`, `/radar profiles show <name>`, `/radar profile <name>`, `/radar prefs`, `/radar feedback`, `/radar saved`, `/radar tracked`, `/radar why <item_id>`, `/radar watch dry-run`, `/radar sources`, and `/radar unmute <source>`.
- Do not restart Hermes Gateway from an active Telegram session unless explicitly asked and verified.
- Gateway activation may be deferred until the next planned restart.

## Verification checklist

Before reporting a RadarForge change as done:

```bash
python -m pytest tests -q
python -m py_compile radarforge/*.py
git diff --check
git status --short
```

If pushing to GitHub, verify CI after push:

```bash
gh run list --repo gweber/radarforge --limit 3
```

## Pitfalls

- Do not overfit wording or code to security only; security is a profile, not the product boundary.
- Do not live-send cards before dry-run.
- Do not treat feedback as opaque magic; keep ranking reasons inspectable.
- Do not put core ranking or watcher behavior into Telegram handlers.
- Escape feed-controlled Markdown before Telegram rendering.
- Neutralize hidden bot-command text from feeds before display: leading `/command` lines become inert `∕command` text, Telegram mentions are de-linked, HTML/script/control/Bidi tricks are stripped, and non-HTTP(S) RSS links are skipped.
