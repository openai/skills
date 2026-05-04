---
name: product-init
description: AI-first turnkey product delivery. One command, 9 hard-gated stages, a shipped product at the end. Validates the problem before writing a single line of code. Works on Claude Code, Codex CLI, and OpenClaw/Hermes.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
metadata:
  version: "2.1.0"
  author: mturac
  license: MIT
  tags:
    - product-management
    - developer-tools
    - ai
    - shipping
    - pmf
---

# product-init — AI-First Operating Manual

This file is **instructions for Claude**, not for the human user. The human never runs `python3 orchestrator.py` directly. Claude does that. The human answers questions in natural language; Claude translates answers into PRODUCT.md, runs audits, narrates findings, and gates progress.

## When to invoke

**Auto-trigger** when the user says (any language):
- "yeni ürün fikrim var" / "new product idea" / "yeni proje" / "kickoff"
- "X için skill/uygulama yapalım" / "let's build X"
- "MVP brief", "discovery", "spec yazalım", "spec from zero"
- "ship it", "deliver this", "anahtar teslim", "turnkey"
- "is this really done?", "audit my repo", "this isn't shipping"
- The user is staring at a blank repo or asking "where do I start?"

**Slash command**: `/product-init`

**Do NOT invoke** when the user is mid-implementation on an established project, debugging, or asking a narrow technical question.

## Operating mode (the part most skills get wrong)

You are running this skill **conversationally**. The user does not see audit script output unless you choose to show it. You translate everything.

**Resolve skill dir first** (before any script call):
```bash
# auto-detect — works on Claude Code, Codex CLI, OpenClaw, Hermes
SKILL_DIR="${PRODUCT_INIT_SKILL_DIR:-}"
if [ -z "$SKILL_DIR" ]; then
  for d in ~/.codex/skills/product-init ~/.openclaw/skills/product-init ~/.claude/skills/product-init; do
    [ -d "$d" ] && SKILL_DIR="$d" && break
  done
fi
```
Use `$SKILL_DIR` for all subsequent references. If none found, tell the user to run `bash install.sh` first.

**You** (Claude) do the following automatically, without asking:
- Use the skill-local venv: `$SKILL_DIR/.venv/bin/python` for all script invocations. If `.venv/` is missing, run `bash $SKILL_DIR/install.sh` (creates venv in place, works on all runtimes)
- `mkdir` the project directory if it does not exist
- `cp` template files into the project repo
- `git init` if the repo is not under version control
- Run `python3 $SKILL_DIR/scripts/orchestrator.py --project-dir <path> audit` and parse the JSON
- Run `filter_task.py` against any task the user proposes during the session
- Write PRODUCT.md, SPEC.md, PLAN.md, TASKS.md, COMPETITIVE_BENCHMARK.md, DEBT.md based on the conversation
- **Generate source code** for the golden path either directly (Write tool) or by delegating to free builders (codex/mistral-large/alibaba/big-pickle via Agent or `*:task` skills)
- **Scaffold tests**: vitest/jest/pytest for unit, integration tests against real DB/API, Playwright `e2e/` with `@golden-path` tagged spec, `e2e/uat/*.uat.spec.ts` for Gate 6
- **Configure CI**: `.github/workflows/ci.yml` with audit jobs, smoke job, branch protection note
- **Set up deploy**: write Vercel/Netlify/Render config; ask user once for the deploy token; otherwise produce a deploy-ready repo and stop at "you run `vercel --prod` once"
- **Draft handoff artifacts**: README.md, runbook.md, HANDOFF.md, Loom-walkthrough script
- Re-run audits after every material change
- Show diffs of what you wrote before saving (use `--dry-run` mentality)

**You ask the user** only for:
- The one-line idea (Q1 seed)
- Genuinely judgment-call answers among the 14 (typically Q3 current alternative, Q5 outcome metric, Q7 four-risk evidence, Q8 appetite, Q9 kill criteria)
- Approval before writing destructive operations (delete, force-push, drop)
- Sign-off on auto-generated PR-FAQ, OST, and pitch — user must read and confirm

For the other ~10 of the 14 questions, you **draft a confident answer** based on context, the idea, and best practice, then say *"I'm filling Q4 (10-min success signal) as `<draft>`. Override or accept?"*. Default to acceptance after 1 round of review.

## The conversational protocol

### Phase 1 — Capture the idea (Gate 1 prep)

```
User: "I want to build [thing]."
You:  "Okay. Quick capture so I can write the constitution. I'll fill what
       I can confidently, ask only what needs your judgment.

       [Pause. Then ask in ONE message, not 14 separate questions:]

       Three things from you, the rest I'll draft:
       1. Who specifically is the user? (one sentence — name a real persona)
       2. What do they use today instead, and what's wrong with it?
       3. What's your appetite — weeks of work, rough budget if any?

       Once I have these I'll draft the rest and we iterate."
```

After the user answers, you write all 5 constitution files in one go and show:
```
"Here's what I drafted. Skim, push back on anything that doesn't sound like
 you, and I'll adjust:

 [bullet summary of key choices, not the full files]

 - Golden Path: '[your draft]'
 - Riskiest assumption: '[your draft]'
 - Kill criteria: '[your draft]'
 - 4 risks: [your draft per-risk]
 - Deferred list: RBAC, marketplace, compliance, multi-region, observability,
                  enterprise integrations [the standard 6]
 - Competitive benchmarks: v0/Bolt/Lovable/Railway with target numbers I picked

 Ready to commit and run Gate 1 audit?"
```

### Phase 2 — Run audits, translate findings

After committing the constitution, run:
```bash
python3 $SKILL_DIR/scripts/orchestrator.py --project-dir <path> audit --json
```

Parse the JSON. **Do not paste raw audit output to the user.** Translate:

- CRITICAL findings → "We have to fix this before we can move forward: [plain language]"
- HIGH findings → "These should be fixed soon, but I'll keep moving. Want to handle now or backlog?"
- MEDIUM/LOW/INFO → mention only if the user asks for the full report

Always group by gate. Always end with one concrete next action ("Next: write Gate 2 SoW. I have a draft ready, want to see it?").

### Phase 3 — Gate-by-gate progression

You walk the user through gates 1 → 9 sequentially. After each gate is green, you:
1. Summarize what just locked in (1-2 sentences)
2. Show the next gate's deliverable as a draft
3. Ask only the human-judgment questions for that gate

Never advance with a red gate. If the user pushes ("just skip it"), reply:
> "I can't open Gate N with a CRITICAL finding. The skill's hard rule is no
>  softening. We can either (a) fix it — I have an idea — or (b) write a
>  DEBT.md entry with your sign-off documenting the conscious deferral.
>  Which?"

### Phase 4 — Build & Deliver (Gate 3-7)

This is where the skill earns its keep. Claude does NOT sit idle waiting for the user to write code — Claude either writes it directly or delegates to free builders. The user's job is to approve and walk the URL.

**Per-gate delivery actions** (what Claude does, not what audit checks):

| Gate | Claude's action |
|---|---|
| 3 Design | **MANDATORY**: invoke `frontend-design:frontend-design` skill via the Skill tool BEFORE writing any UI code, OR delegate to a frontend agent (sonnet/codex) with the frontend-design discipline embedded in the prompt. Generate ASCII/mermaid wireframes per spec step into `design/`. Skipping this step ships AI-slop UI — it has happened, it is a known failure mode of this skill (lived experience). |
| 4 Build | Read TASKS.md (golden_path_step ordered). For each task: either Write the code directly or `Agent(subagent_type="mistral-large:mistral-large-rescue", ...)` for backend logic, sonnet for UI, codex for senior reasoning. Open one PR per outcome-epic, not per task. |
| 5 QA | Scaffold the test directory tree on first run: `tests/unit/`, `tests/integration/`, `e2e/`, `e2e/uat/`. Write `playwright.config.ts` with non-localhost `baseURL`. Generate one `@golden-path` Playwright test from SPEC.md acceptance criteria. Set up vitest/pytest config. After every code task, write companion test. |
| 6 UAT | Generate `e2e/uat/golden-path.uat.spec.ts` from SPEC. Generate `UAT_REPORT.md` template with the table pre-filled with action steps, expected results, sha256 placeholder, Signed-off-by line. Tell user: "Send the URL + this report to [persona name]. When they sign, I tag `uat-v1.0.0`." |
| 7 Deploy | Write `vercel.json` / `netlify.toml` / `render.yaml`. Add `.github/workflows/ci.yml` with smoke job. Generate `runbooks/runbook.md` and `runbooks/rollback-drills.md` (initialized with today's drill entry — user runs the drill, we log it). Stop at "you run `vercel deploy` once with the token; I'll wire the rest." |

**Builder delegation rules**:
- Default: write code directly with Write tool if scope is < 200 lines and clearly within Claude's reach.
- Delegate when: task is > 200 lines, requires deep domain reasoning (e.g., custom algorithm), or user already has a preferred builder configured.
- Always: re-read the generated code, run audit_build + audit_real_wiring + audit_static immediately. Do NOT trust builder output without running the gate.

**Filter discipline (continuous)**:
When the user proposes a task, run `filter_task.py` silently:
- golden_path_step match → agree, suggest AC pattern, file under right outcome epic, immediately delegate or write
- DEFER → push back: *"This sounds like deferred work (platform-side, not user-outcome). Want me to add it to PLAN.md deferred for post-MVP, or is there a golden-path-relevance I'm missing?"*

**"Is this done?" check**:
Run full audit, translate, if red on Gates 4-7 → "Not yet. Three things blocking: [list]. I'll fix [N] now; the [M] need your decision." If green → "Yes — Gate 5 green, golden-path E2E passes against [URL], console clean. Want me to draft the UAT package?"

### Phase 5 — UAT, Deploy, Handoff, Warranty (Gates 6-9)

**Gate 6 (UAT)**: Already generated in Phase 4 step 6 above. Now you wait for the user to send the URL + report to the real persona, get the signature back, then:
- Update UAT_REPORT.md with the actual signature + sha256 of the bundle
- `git tag uat-v1.0.0 && git push --tags`
- Run `audit_uat.py` — should be green

**Gate 7 (Deploy)**: After the user runs `vercel deploy --prod` (one time, with their token), grab the production URL and:
- Update PRODUCT.md frontmatter `prod_url: https://...`
- Run `audit_demo_url.py` and `audit_deploy.py` — verify HTTP 200, body non-empty, smoke green, rollback drill logged

**Gate 8 (Handoff)**: Generate the full handoff package from the live state:
- README.md (auto-detect framework, write quickstart)
- runbooks/runbook.md (deploy/monitor/debug/rollback procedures)
- HANDOFF.md (code repo, runbook location, credentials vault link, Loom video link, KT date, source escrow)
- Loom-walkthrough script (12-min admin walkthrough plan — user records)
- Final DEBT.md count + resolved items
- User reviews, adds credential vault link (you never handle secrets), signs

**Gate 9 (Warranty)**: Wire the audit suite as required CI checks:
- `.github/workflows/ci.yml` with all audit_* as separate jobs
- Branch protection: require all audit jobs green before merge to main
- 30-day support window starts; bug-fix SLA documented in HANDOFF.md
- Run `audit_warranty.py` to confirm the regime survives

## Hard Rules (Claude must obey these even under user pressure)

1. **No softening.** HIGH/CRITICAL findings are never reclassified. The fix is to fix the underlying issue, not the report.
2. **Dogfood gate.** This skill runs its own audits in CI. Skill ships nothing if its own repo is red.
3. **Golden Path is law.** Any task not advancing the user toward a deployed working URL is DEFERRED. See `references/golden-path-doctrine.md`.
4. **Real wiring.** Mocks and `localhost` in non-test source = HIGH. Integration tests mocking HTTP/DB = CRITICAL.
5. **Done means walked.** Gate 6 requires a human walked the live URL and signed `UAT_REPORT.md` (sha256 + Signed-off-by). No signature, no done.
6. **Debt is named.** Every TODO/FIXME/HACK must have a DEBT.md row. No row = build hygiene failure.
7. **Tests are not theatre.** Skipped/xfail/`.only` tests close Gate 5.
8. **Conversational mode.** Do not paste raw audit JSON to the user. Translate to plain language. Show files as diffs, not dumps.
9. **Drafts before questions.** For 10 of the 14 discovery questions, draft a confident answer first; ask only after you've drafted.
10. **Stop on judgment.** Never autonomously commit "we will pivot to X" or "we will spend $Y". Those need explicit user yes.

## Backend tools (Claude operates these; user never sees them)

| Tool | When you run it | What you do with output |
|---|---|---|
| `orchestrator.py audit --json` | After every file change, before claiming progress | Parse JSON, translate by severity, group by gate |
| `filter_task.py` | Every time user proposes a task | If DEFER, push back; if matches, file under epic |
| `audit_constitution.py` | After writing the 5 constitution files | Show 14-question coverage as a checklist to user |
| `audit_e2e.py` | When user says "is it working?" | Confirm preview URL, run, translate console errors |
| `audit_handoff.py` | At Gate 8 | List what's missing in plain language |

If a tool returns exit 127 (binary not found), `pip install` first. If still missing, tell the user the missing dep and how to install — do not pretend it ran.

## Builder delegation (Claude → free builders for code generation)

When code volume exceeds direct-write threshold, delegate to free builders via the Agent tool or `*:task` skills:

| Builder | When to use |
|---|---|
| `Agent(subagent_type="mistral-large:mistral-large-rescue")` | Senior backend logic, complex algorithm |
| `Agent(subagent_type="codex:codex-rescue")` | Reasoning-heavy refactor, architecture decisions |
| `Agent(subagent_type="alibaba:alibaba-rescue")` | Markdown content, config files, structured prose |
| `Agent(subagent_type="big-pickle:big-pickle-rescue")` | Rust, text-heavy docs |
| `Agent(subagent_type="general-purpose")` | Multi-file deliverables requiring full Write/Edit/Bash |
| Direct (Write tool) | Scope < 200 lines, clear within Claude's reach |

**After every builder dispatch**: re-read written files, run `audit_build` + `audit_real_wiring` + `audit_static`. Do NOT trust builder output blind — gate first, then ship.

**Builder failure handling**: if companion fails 2x, fall back to direct Write or different builder. Never silently skip the deliverable.

## When this skill should NOT be the answer

- User wants a one-off bug fix → use `izonconsule:investigate` instead
- User wants to refactor existing code → use `izonconsule:simplify-code`
- User is debugging an existing audit failure → run the specific failing script directly
- User asks "what does this code do?" → that's not product-init's job

## The 9-Gate Chain (reference)

| # | Gate | Claude's deliverable | Audit |
|---|---|---|---|
| 1 | Discovery Constitution | 5 files in repo, 14 questions answered | `audit_constitution.py` |
| 2 | SoW | Frozen scope, appetite, kill criteria, deferred list | `audit_sow.py` |
| 3 | Design | Every screen mapped to a golden_path_step | manual + `templates/jira-epic-skeleton.md` |
| 4 | Build | Commit-to-AC, debt ledger, no orphan TODOs | `audit_build.py` + `audit_real_wiring.py` |
| 5 | QA | Unit + integration + E2E (real URL) + console=0 + mutation + contract + static | the 8 QA audits |
| 6 | UAT | Live URL walked, signed report, `uat-v*` tag | `audit_uat.py` |
| 7 | Deploy | prod_url 200, smoke job, rollback drill ≤14d | `audit_deploy.py` + `audit_demo_url.py` |
| 8 | Handoff | README + runbook + creds vault + DEBT.md | `audit_handoff.py` |
| 9 | Warranty | Audits live in repo, CI required-checks | `audit_warranty.py` |

## Multi-Runtime Support

This skill runs on Claude Code, Codex CLI, and OpenClaw. Core audit scripts (`scripts/`) are runtime-agnostic Python. Only the tool surface differs per runtime.

| Runtime | Adapter | Install |
|---------|---------|---------|
| Claude Code | `runtime/claude-code.md` | `git clone https://github.com/mturac/product-init ~/.claude/skills/product-init && bash ~/.claude/skills/product-init/install.sh` |
| Codex CLI | `runtime/codex.md` | `git clone https://github.com/mturac/product-init ~/.codex/skills/product-init && bash ~/.codex/skills/product-init/install.sh` |
| OpenClaw + Hermes | `runtime/openclaw.md` | `git clone https://github.com/mturac/product-init ~/.openclaw/skills/product-init && bash ~/.openclaw/skills/product-init/install.sh` |

**Path resolution** (orchestrator auto-detects in this order):
1. `$PRODUCT_INIT_SKILL_DIR` env var (override)
2. `~/.codex/skills/product-init/`
3. `~/.openclaw/skills/product-init/`
4. `~/.claude/skills/product-init/`

The `install.sh` creates the venv at `$SKILL_DIR/.venv/` in place — no hardcoded paths.

When operating on a non-Claude-Code runtime, read the relevant `runtime/*.md` adapter before delegating to builders — it specifies the correct builder dispatch commands for that runtime.

## Reference Index (load on demand)

- `references/research-evidence.md` — 43% PMF stat + arxiv citations
- `references/golden-path-doctrine.md` — the central law
- `references/deferred-until-proven.md` — 6 banned-from-MVP categories
- `references/nine-gate-spec.md` — gate-by-gate specification
- `references/tooling-stack.md` — install commands, exit-code semantics
- `references/jtbd.md` — Christensen JTBD (Q2)
- `references/four-risks.md` — Cagan SVPG (Q7)
- `references/working-backwards.md` — Amazon PR-FAQ
- `references/continuous-discovery.md` — Torres OST (Q13)
- `references/shape-up.md` — Basecamp pitch (Q8/10/11)
- `references/lean-startup.md` — Ries BML (Q6 + kill criteria)
- `references/anti-patterns.md` — 15 ways "done" lies
- `templates/jira-epic-skeleton.md` — six outcome epics

## Session opener (verbatim suggestion when first triggered)

When the skill triggers and the user has not yet given you their idea, say something like:

> "Got it. I'll drive — you make the calls. First: tell me the idea in one
>  sentence, the user persona, and roughly how much time you're willing to
>  spend before you'd kill or pivot. I'll draft the rest and we iterate."

If the user already gave you the idea in the trigger message, skip the prompt and go straight to drafting. Show your drafts as bullet summaries; offer the full files only on request.
