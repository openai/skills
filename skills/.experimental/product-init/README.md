# product-init

**AI sets the goal. product-init makes sure you're shooting at the right one.**

> "Vibe-coding without a product spec isn't moving fast. It's building the wrong thing at the speed of AI."

Codex ships `/goal`. Cursor ships `/build`. Every AI tool now moves faster.  
43% of startups still die from the same cause: wrong product.

product-init is the gate before the gate — 9 hard stops between your idea and your deploy, each blocked by a Python audit script with real pass/fail criteria. CRITICAL findings stop the pipeline. No `--skip` flag.

Works on Claude Code, Codex CLI, and OpenClaw/Hermes.

---

## How it works

```
/product-init "build an HR assessment tool"
```

Three questions. AI drafts the rest. 9 gates run in sequence.

```
Gate 1  Discovery Constitution   JTBD + four-risk model
Gate 2  Statement of Work        Shape Up appetite + PR-FAQ
Gate 3  Design                   Every screen maps to a job from Gate 1
Gate 4  Build                    Commit-to-AC, no orphan TODOs
Gate 5  QA                       Unit + integration + E2E — all green
Gate 6  UAT                      Real human signs off on real URL
Gate 7  Deploy                   HTTP 200 to prod, smoke job, rollback drill
Gate 8  Handoff                  ADRs + runbook + DEBT.md — a contract, not a README
Gate 9  Warranty                 72h monitoring window: error rate, latency, uptime
```

Gate 1 is the one that matters most. It asks: *who gets fired if this fails, what job are they hiring it for, and what does failure look like in production?*  
That's the goal you're shooting at. Everything else is build speed.

---

## Install

```bash
curl -sSL https://raw.githubusercontent.com/mturac/product-init/main/install.sh | bash
```

That's it. The script detects which AI tools you have installed (Claude Code, Codex CLI, OpenClaw) and installs there automatically. Works on all of them at once if you have multiple.

---

## Usage

```bash
# Bootstrap a new project
python3 scripts/orchestrator.py --project-dir /path/to/project init "your idea"

# Run a specific gate
python3 scripts/orchestrator.py --project-dir /path/to/project gate 1

# Run all audits
python3 scripts/orchestrator.py --project-dir /path/to/project audit --json
```

Every audit accepts `--project-dir` and `--json`. JSON output: `{ findings: [...], exit_code: 0|1 }`.

---

## Runtime support

| Runtime | Adapter | Install dir |
|---------|---------|-------------|
| Claude Code | `runtime/claude-code.md` | `~/.claude/skills/product-init` |
| Codex CLI | `runtime/codex.md` | `~/.codex/skills/product-init` |
| OpenClaw + Hermes | `runtime/openclaw.md` | `~/.openclaw/skills/product-init` |

Orchestrator auto-detects path: `$PRODUCT_INIT_SKILL_DIR` → `~/.codex/` → `~/.openclaw/` → `~/.claude/`.

---

## What ships at the end

- `PRODUCT.md` — golden path, persona, outcome metric, kill criteria
- `SPEC.md` — scope, acceptance criteria
- `PLAN.md` — Shape Up pitch, appetite, deferred list
- `TASKS.md` — golden path tasks only (filter blocks scope creep)
- `COMPETITIVE_BENCHMARK.md` — v0/Bolt/Lovable/Railway targets
- `DEBT.md` — every TODO/FIXME named and owned
- `UAT_REPORT.md` — signed off, sha256-tagged
- `HANDOFF.md` — ADRs, runbook, rollback, credentials vault link
- `.github/workflows/ci.yml` — audit jobs as required checks

---

## Demo

HR assessment tool built in one session with product-init:
- Editorial landing page: "Hire on evidence, not on a feeling."
- Dark cinematic interview room — live AI sessions
- Dashboard with scored candidates
- PDF reports across 4 dimensions

Live: https://demorpoject.vercel.app

---

## CI

`.github/workflows/dogfood.yml` — self-audits on every push:
- Gate 1 + Gate 2 must exit 0 on known-good fixture
- Orchestrator `init`, `audit`, `gate` subcommands tested
- Runtime adapters frontmatter validated
- `install.sh` executable check
- Python syntax check on all 23 scripts
- `$PRODUCT_INIT_SKILL_DIR` env var override verified

---

## Research basis

| Source | Applied at |
|--------|-----------|
| CB Insights 2024 (43% PMF failure) | Gate 1 hard block |
| Christensen JTBD | Gate 1 Q2 |
| Cagan four-risk model | Gate 1 Q7 |
| Basecamp Shape Up | Gate 2 appetite + scope |
| Amazon PR-FAQ | Gate 2 user narrative |
| Torres Continuous Discovery | Gate 1 Q13 |
| Ries Lean Startup | Kill criteria + BML loop |

Full citations: `references/research-evidence.md`
