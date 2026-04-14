---
name: skill-improver
description: Evaluate and improve an already-installed Codex skill by forking it into an improver workspace, running paired rollouts with that skill versus no skill, and opening the generated review viewer for human comparison. Use this when the user names an installed skill and asks to test, compare, benchmark, roll out, iterate on, or improve it. New skill creation is out of scope for this skill.
---

# Skill Improver

Use this skill to evaluate an installed skill by comparing Codex behavior with that skill available against Codex behavior with no skill. Keep the workflow narrow and reliable: fork the installed skill into a workspace, run paired rollouts, generate the review viewer, and stop for human review.

New skill creation is out of scope. If the user wants to create a brand-new skill, tell them this improver is only for installed-skill evaluation and ask them to install or provide an existing skill first.

## Stage Gates and Approvals

This workflow is a user-reviewed loop. The agent should move work forward to the next review point, then stop for the user before continuing.

At the beginning:
1. The user asks to improve or evaluate an installed skill.
2. Resolve and read the target skill only enough to draft evals.
3. Draft eval prompts and assertions, then ask the user to review and confirm them before creating an improver workspace, snapshotting the skill, or running any rollout.

For each skill iteration:
1. Run the approved evals and ask the user to review the comparison outputs in the viewer.
2. Incorporate the user's review feedback into a drafted skill update, then ask the user to review and confirm the revised skill before the next rollout.

A user instruction customizes the workflow, but does not bypass a review point unless it explicitly approves the artifact or stage currently under review.

Examples:
- "Ignore existing test cases" means draft fresh evals; it does not approve those evals.
- "Use subagents" changes how approved rollouts run; it does not approve the rollout.
- "Continue" means proceed past the current completed gate only.
- "Looks good" approves the artifact currently under review if the context is clear.

Required gates:
- Before workspace setup or the first rollout: the user must approve the eval prompts and assertions, unless they already provided exact evals.
- After opening the review viewer: stop until the user submits reviews and asks to continue.
- After editing a skill revision: stop until the user confirms the revised skill before running the next round.

At each gate, state what the user should review, link the artifact, and say exactly what confirmation is needed.

## Non-Negotiable Flow

When this skill triggers, add these items to your task plan or checklist and drive them to completion unless blocked by missing information or a stage gate:

- Identify the installed skill and read it only enough to draft evals.
- Draft eval prompts and assertions for user approval.
- When working inside a repo that already contains a local skill fork, keep or create a repo-local fork there instead of treating `~/.codex/skills/...` as the only editable copy.
- After eval approval, fork the installed skill into an improver workspace and create evals JSON.
- In parallel with the improver workspace, create a per-skill reporting workspace under `skill-reporting/` and keep the canonical eval/report artifacts there.
- If the eval depends on live external or connector data, capture the shared source material once into workspace inputs before executor runs.
- Run paired rollouts: with `<skill name>` and without `<skill name>`.
- Create comparison artifacts, benchmark data when available, and run `eval-viewer/generate_review.py` so the human can review test cases.
- Open the served viewer so feedback is written to the current run directory, starting with `<workspace>/runs/original/feedback.json`.
- Keep `skill-reporting/<skill-name>/status.md` updated as the iteration proceeds.
- Once the user says they are done iterating and ready to finalize the skill, complete `skill-reporting/<skill-name>/report.md` and `skill-reporting/<skill-name>/slack-post.md`.
- Final message: link to the canonical `skill-reporting/<skill-name>/evals.json` file and the synced `<workspace>/runs/evals/evals.json` file used for the run, tell the user to press the viewer's "Submit All Reviews" button, then prompt you to continue.
- When continuing after viewer feedback, create the next skill revision under `<workspace>/skill-revisions/<revision-id>/`, then pause to summarize the skill updates, explain why they were made, link the updated revision `SKILL.md`, and ask for confirmation before running the next test round.

Do not continue revising the skill after the viewer opens. The viewer is the handoff point.

## Inputs

The user should name an installed skill and either provide exact eval prompts or approve proposed evals.

If the user only names the skill, or asks for fresh evals without providing exact prompts, inspect the skill and propose 5 realistic eval prompts with assertions. Stop for approval before creating the improver workspace, snapshotting the skill, or running rollouts.

Installed skill resolution:

1. Prefer an exact match from the active skills list when available.
2. Otherwise search common skill roots:
   - `$CODEX_HOME/skills/<skill-name>/`
   - `$CODEX_HOME/skills/*/<skill-name>/`
   - repo-local skill directories if the user points at one
3. Confirm the chosen `SKILL.md` path before running paired rollouts if there is any ambiguity.

Do not edit the installed skill directly during rollout. Always fork it first.

## Workspace Layout

Create the improver workspace in the top-level of the current local working directory, not next to the installed skill. Installed skills may live under obscure cache or home-directory paths; keep improver workspaces easy to find in the active repo or local workspace root. If the current task has a clear repository root, use that root. Otherwise use the current working directory.

If the current repo already contains a local skill fork, also maintain a repo-local fork of the installed skill there. Prefer a stable path shaped like:

```text
<repo-or-cwd>/plugins/<skill-name>/skills/<skill-name>/
```

Use that repo-local fork for code review, packaging, and eventual installed-skill updates. The improver workspace remains disposable evaluation scratch space.

```text
<repo-or-cwd>/
  skill-reporting/
    <skill-name>/
      evals.json          # canonical editable eval definition
      report.md           # side-by-side artifact comparison and rubric notes
      status.md           # simple status, testing coverage, overall performance
      slack-post.md       # draft post for the broader team
  <skill-name>-<YYYYMMDD>-v_<N>-workspace/
    inputs/               # optional shared input snapshots for all runs
      source_snapshot/
    skill-revisions/
      original/           # copied from the installed skill
      iteration-1/        # first edited revision, after review
    runs/
      evals/
        evals.json        # synced copy of skill-reporting/<skill-name>/evals.json
      original/           # run-id; runs against skill-revisions/original
      feedback.json        # written by the viewer after Submit All Reviews
      revision_brief.md    # optional, generated from feedback
      benchmark.json       # when grading data exists
      benchmark.md         # when generated
      viewer.log           # when serving the viewer
      <eval-name>/
        eval_metadata.json
        with_skill/
          run_metadata.json
          grading.json
          timing.json        # optional
          outputs/
            final_message.md
            full_rollout.jsonl
            executor_stderr.log # optional
            <task-artifacts>
        without_skill/
          run_metadata.json
          grading.json
          timing.json        # optional
          outputs/
            final_message.md
            full_rollout.jsonl
            executor_stderr.log # optional
            <task-artifacts>
    iteration-1/           # run-id; runs against skill-revisions/iteration-1
      feedback.json
      revision_brief.md
      benchmark.json
      benchmark.md
      viewer.log
      <eval-name>/
        eval_metadata.json
        with_skill/
          run_metadata.json
          grading.json
          timing.json        # optional
          outputs/
            final_message.md
            full_rollout.jsonl
            executor_stderr.log # optional
            <task-artifacts>
        without_skill/
          run_metadata.json
          grading.json
          timing.json        # optional
          outputs/
            final_message.md
            full_rollout.jsonl
            executor_stderr.log # optional
            <task-artifacts>
```

Choose a readable collision-resistant workspace name. If `v_1` already exists, use `v_2`, then `v_3`, and so on.

Create the reporting workspace in parallel with the improver workspace. The reporting workspace is per skill, not per iteration, so prefer:

```bash
python <skill-improver-path>/scripts/init_reporting_workspace.py \
  <repo-or-cwd> \
  --skill-name <skill-name> \
  --improver-workspace <workspace> \
  --plugin-skill-path <repo-or-cwd>/plugins/<skill-name>/skills/<skill-name> \
  --installed-skill-path <installed-skill-directory-or-SKILL.md-path>
```

Use `skill-reporting/<skill-name>/evals.json` as the canonical eval definition. Before launching rollouts, sync that file into `<workspace>/runs/evals/evals.json` so existing viewer and benchmark tooling keeps working.

The bundled `init_reporting_workspace.py` script performs that sync automatically whenever `--improver-workspace <workspace>` is provided.

Snapshot the installed skill before running it. The snapshot id and run id must match: run `<workspace>/runs/original` against `<workspace>/skill-revisions/original`, run `<workspace>/runs/iteration-1` against `<workspace>/skill-revisions/iteration-1`, and so on.

Keep this high-level structure clean. Do not create run artifacts, eval directories, `with_skill/`, `without_skill/`, `full_rollout.jsonl`, or task output files directly under the workspace root. Do not create ad hoc revision folders outside `skill-revisions/`, and do not write top-level files except when the user explicitly asks for a workspace-level note.

```bash
python <skill-improver-path>/scripts/snapshot_skill.py \
  <installed-skill-directory-or-SKILL.md-path> \
  <workspace> \
  --label original \
  --note "copied from <installed-skill-directory-or-SKILL.md-path>"
```

Use `<workspace>/skill-revisions/<revision-id>/` for the with-skill runs. Use no skill path for the baseline. This improver compares the named skill revision to no skill, not to an old version, unless the user explicitly asks for a version-to-version comparison.

The run metadata revision must be the snapshot label, such as `original` or `iteration-1`. Do not derive `skill_revision` from the workspace directory name and do not use `workspace` as the revision unless the user explicitly created a revision with that exact label.

When the task depends on remote tools or live connector reads, add a shared inputs area:

```text
<workspace>/
  inputs/
    source_snapshot/
```

Use it to store a single captured corpus, for example channel messages, fetched docs, or API results, that every rollout can read. Prefer this over repeating the same live reads in every executor run.

## Evals JSON

Create the canonical eval file at `skill-reporting/<skill-name>/evals.json` before launching rollouts, then copy it to `<workspace>/runs/evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 0,
      "name": "descriptive-name",
      "prompt": "The user's task prompt",
      "files": [],
      "assertions": [
        "Output uses the requested response format.",
        "Output satisfies the key task constraint.",
        "Output includes any required citations, fields, or artifacts."
      ]
    }
  ]
}
```

Assertions are required for every eval. Do not leave `assertions` empty.

The reporting workspace copy is the human-owned source of truth. The improver workspace copy is an execution snapshot for that run. If you revise evals later, update `skill-reporting/<skill-name>/evals.json` first, then resync it into the current improver workspace before rerunning.

Prefer using the same script for resyncs so the reporting workspace and improver workspace stay aligned:

```bash
python <skill-improver-path>/scripts/init_reporting_workspace.py \
  <repo-or-cwd> \
  --skill-name <skill-name> \
  --improver-workspace <workspace> \
  --status running
```

Eval prompts should be realistic user tasks, not harness explanations. Keep them as short and natural as a real user's request would be; do not over-specify obvious behavior that the skill under test should infer, such as preserving native document elements when asking to create a Google Doc from Markdown. Do not put skill-control text, comparison setup, grading expectations, or phrases like "static connector snapshot" into the eval prompt; add those only in the executor wrapper. Put specific success criteria only in `assertions`. Test cases must produce real artifacts that a human can review in the viewer, such as a created document, deck, spreadsheet, issue, report, edited file, or applied change record. Do not make evals easier by asking only for edit plans, proposed payloads, API request stubs, or other intermediate artifacts unless the skill's actual user-facing purpose is to produce that intermediate artifact.

Keep the assertion set simple and durable:

- Include at least 3 assertions per eval.
- Prefer plain, verifiable statements over clever grading logic.
- For subjective tasks, include structural assertions plus one or two task-specific checks.
- If you are unsure what to assert, start with format, completeness, and one core correctness check.

For each eval directory, also write:

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name",
  "prompt": "The user's task prompt",
  "assertions": [
    "Output uses the requested response format.",
    "Output satisfies the key task constraint.",
    "Output includes any required citations, fields, or artifacts."
  ]
}
```

Use descriptive eval directory names such as `summarize-customer-tickets`, not bare `eval-0`, when practical.

## Reporting Workspace

Keep a sibling reporting workspace at `skill-reporting/<skill-name>/`. This workspace exists to track the eval during iteration and to produce the final review/share artifacts once the user says they are done iterating and ready to finalize the skill.

Required files:

- `evals.json`: canonical prompt and assertion set for the current iteration. This is the file you edit first.
- `report.md`: finalized report with the rubric, a per-eval comparison table, and 3-5 hero side-by-side artifacts. Flesh this out once the user says they are done iterating.
- `status.md`: simple status note describing where the eval stands, how much testing happened, and how it performed overall. Keep this updated throughout the iteration.
- `slack-post.md`: finalized Slack draft describing what the skill does, how it compares to baseline, and any useful iteration insights worth sharing. Write this once the user says they are done iterating and ready to finalize.

`report.md` requirements when finalizing:

- Include a rubric table with these weighted dimensions:
  - Task success: 35%
  - Output quality: 35%
  - Context retrieval quality: 10%
  - Skill orchestration: 10%
  - Efficiency: 10%
- Include a comparison table with one row per eval prompt and columns for:
  - eval prompt
  - use case
  - expected skills
  - with skill output
  - without skill output
  - preference
  - rubric notes
  - status
- Keep the table simple. Short phrases and links are better than long prose inside cells.
- Document 3-5 hero prompts per use case when possible. Where appropriate, include some cases that avoid connectors and instead use uploaded files or public information.

`status.md` requirements during iteration:

- Keep it simple.
- State the current phase, for example `draft`, `approved`, `running`, `under review`, `update ready`, or `complete`.
- State how much testing was done, for example `5 prompts run: 3 connector, 2 file/public-info`.
- State overall performance in one or two sentences, for example whether the skill beat baseline clearly, only on connector-heavy prompts, or not yet reliably.

`slack-post.md` requirements when finalizing:

- Describe what the skill does in plain language.
- Summarize how it compares to baseline.
- Call out any iteration insights worth sharing with the broader team.
- Keep it short enough to post with minimal editing.

Default assertion recipe:

- `Format`: the output shape matches the requested structure.
- `Coverage`: the output includes all required sections, fields, or artifacts.
- `Core correctness`: the output satisfies the most important task-specific requirement.

Examples:

- Digest task:
  - `Output contains exactly 3 numbered items.`
  - `Each item includes a Citation line and a Why it matters line.`
  - `No headline exceeds 10 words.`
- File-generation task:
  - `The expected output file exists at the requested path.`
  - `The file contains the required sections or columns.`
  - `The final message references the generated artifact.`
- Analysis task:
  - `The answer addresses the requested time window or scope.`
  - `The answer cites the required sources or evidence.`
  - `The answer clearly states the main recommendation or conclusion.`

## Performance Defaults

Assume the evaluator wants the fastest reliable comparison, not the most literal replay of live reads in each run.

When this skill is triggered, the user's request to evaluate or improve a skill counts as explicit authorization to delegate the independent rollout matrix to subagents. Use subagents by default for every independent eval/configuration cell unless subagents are unavailable or the user explicitly asks not to use them. This authorization is scoped only to skill-improver rollout and evaluation work for the named skill; do not generalize it to unrelated tasks.

- Prefer a two-phase flow for live-data evals:
  1. Capture shared source material once into `<workspace>/inputs/source_snapshot/`.
  2. Run all executor comparisons against that fixed snapshot.
- Treat repeated connector fetches across `with_skill` and `without_skill` as a bug unless the live-read behavior itself is what you are evaluating.
- Before the smoke run, classify the executor path and permission needs. If the run will use nested `codex exec` and is expected to touch Codex auth, model/network state, plugin sync, shell snapshots, or files under `~/.codex`, request elevated execution before the smoke run. Do not start with a sandboxed smoke run when the likely failure mode is already knowable from those requirements.
- Treat any smoke run as environment validation, not as a serialized eval cell. For the subagent path, prefer no eval-cell smoke run: once subagents are available, launch every independent eval/configuration subagent concurrently. If you must validate the environment first, use a separate lightweight smoke task and do not count it as part of the matrix.
- Always launch the full comparison matrix in parallel once the executor environment is ready. Every independent eval/configuration pair should run concurrently unless a concrete connector rate limit, machine limit, or isolation requirement forces a lower cap. Do not serialize the matrix merely because a shell runner is easier to write.
- Prefer subagents for the rollout matrix whenever the runtime supports them. Treat subagents as the default execution path for independent `with_skill` and `without_skill` runs because they give each eval fresh context, parallel thinking budget, and isolated output ownership without repeatedly spawning cold `codex exec` processes.
- When using subagents for rollouts, spawn them with `fork_context: false`. Do not leak the main conversation, evaluator discussion, expected output, or grading assertions into executor context. Use the same model and reasoning effort as the parent rollout unless the user explicitly requests a different model.
- If policy or runtime constraints block subagents, use the best available isolated executor and still run all independent eval/configuration pairs in parallel. Serial execution is a fallback only when parallelism is materially unsafe or impossible, and the reason must be recorded in the workspace or transcript.
- If you must use `codex exec`, minimize startup overhead:
  - bias toward the permission level needed for the nested executor to start cleanly. If sandboxed startup is likely to require network access, plugin/auth refresh, or writes under `~/.codex`, request elevated permissions before the smoke run instead of burning time on a predictable false start.
  - if a sandboxed smoke run fails or stalls on network, plugin sync, auth, shell snapshots, or `~/.codex` state access, stop that run and rerun immediately with elevated permissions.
  - keep the smoke run's stdout/stderr observable while it starts; once it has emitted a real task action after startup, start the remaining executor runs in parallel while the smoke run continues.
  - reuse a prepared `CODEX_HOME` with auth already present
  - set approval policy in that prepared `CODEX_HOME/config.toml`; do not assume your local `codex exec` build supports CLI approval flags such as `-a`
  - if you are scripting `codex exec`, verify the supported flags with `codex exec --help` before hard-coding them
  - keep only the plugins, MCP servers, and skills required for the eval
  - avoid unrelated startup work such as extra marketplaces or unused connectors
  - preserve `codex exec --json` stdout as clean JSONL in `full_rollout.jsonl`; write stderr, plugin sync warnings, Cloudflare/HTML responses, and other non-JSON logs to a separate file such as `executor_stderr.log`
- When the user does not provide exact evals, default to drafting 5 focused eval prompts so the first comparison has enough breadth to expose weak spots. If the skill or environment makes 5 impractical, say why and propose the best smaller set before any rollout.

## Running Paired Rollouts

Run every eval in two configurations. For the first round, use `revision-id=original` and `run-id=original`; after the first reviewed edit, use `revision-id=iteration-1` and `run-id=iteration-1`.

- `with_skill`: Codex has access to `<workspace>/skill-revisions/<revision-id>/`
- `without_skill`: the same task with no access to the named skill

Launch paired runs in the same turn where the environment supports subagents. Use subagents as the preferred path for the rollout matrix. If subagents are not available, use the best available isolated executor, such as `codex exec`, and capture the full output. Do not silently do only the with-skill run.

Default concurrency policy:

- If the runtime supports subagents, use them for the rollout matrix and launch every independent `with_skill` and `without_skill` eval cell simultaneously. Spawn each with `fork_context: false`, the same model as the parent, and the same reasoning effort as the parent. Give each subagent a distinct label and output directory, and tell it that other agents may be writing elsewhere in the same workspace.
- Start all evals for both configurations simultaneously immediately after environment validation, unless the machine or connector rate limits force a lower cap.
- If a cap is needed, prefer the highest safe cap and state the exact configured parallelism, for example `parallelism=6 for 3 evals x 2 configurations` or `parallelism=3 due to connector rate limits`.
- If full concurrency is risky, cap concurrency explicitly and still interleave both configurations. Do not run the entire `with_skill` set first and then the entire `without_skill` set unless there is a real isolation requirement.
- Keep a short note in the workspace or transcript explaining any deliberate concurrency cap.

Executor prompt discipline:

- The executor prompt must be minimal and representative of a real user task. Do not include assertions, expected-output text, grading criteria, benchmark rationale, scoring rubrics, or hidden implementation hints in the executor prompt.
- The only required skill-control line is one of:
  - `You must use this skill: <workspace>/skill-revisions/<revision-id>`
  - `You must not use any skills to complete this task.`
- Include only operational paths the executor truly needs, such as the input file path and output directory. Keep those paths neutral and do not reveal the grader's assertions.
- Save the exact prompt sent to each executor at `<workspace>/runs/<run-id>/<eval-name>/<configuration>/executor_prompt.txt` before launching the run.
- Store assertions only in `eval_metadata.json` and use them only after execution for grading.

For live-data tasks, point both configurations at the same captured inputs, but keep the task wording representative. Example:

```text
<eval prompt, including any user-realistic reference to input files such as:
"Use the Markdown file at <workspace>/inputs/source_snapshot/input.md to create the requested artifact.">

You must use this skill: <workspace>/skill-revisions/<revision-id>

Save your final response and artifact references under: <workspace>/runs/<run-id>/<eval-name>/with_skill/outputs/
```

Use this task shape for the with-skill run:

```text
<eval prompt>

You must use this skill: <workspace>/skill-revisions/<revision-id>

Save your final response and artifact references under: <workspace>/runs/<run-id>/<eval-name>/with_skill/outputs/
```

Use this task shape for the baseline. Do not provide a skill path. Avoid putting the skill name in the task text unless needed to describe the output directory; the baseline should behave like a normal Codex run without the target skill.

```text
<same eval prompt>

You must not use any skills to complete this task.

Save your final response and artifact references under: <workspace>/runs/<run-id>/<eval-name>/without_skill/outputs/
```

If the target skill is a local installed skill and you control the executor home, prefer a true isolated baseline by omitting the skill from the baseline executor's skill registry entirely instead of relying only on the prompt warning.

For each run, write `run_metadata.json`. The review viewer uses this for labels and for summary chips above `full_rollout.jsonl`, so include the concrete comparison identity rather than only generic values:

```json
{
  "configuration": "with_skill",
  "configuration_label": "with example-skill",
  "skill_name": "example-skill",
  "skill_revision": "original",
  "skill_path": "/absolute/path/to/workspace/skill-revisions/original",
  "skills_used": ["example-skill"]
}
```

For `without_skill`, set:

```json
{
  "configuration": "without_skill",
  "configuration_label": "without example-skill",
  "skill_name": "example-skill",
  "skill_revision": "none",
  "skill_path": "",
  "skills_used": []
}
```

If completion notifications include `total_tokens` and `duration_ms`, save them immediately to the run's `timing.json`. The review viewer reads this file and surfaces timing/token chips above `full_rollout.jsonl`, alongside metadata from `run_metadata.json`. If timing is unavailable, omit the file or write:

```json
{"timing_unavailable": true, "reason": "runner did not provide duration_ms or total_tokens"}
```

## Grading and Benchmark

Grade every run and save `grading.json` beside the run's `outputs/`. The viewer expects this shape:

```json
{
  "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
  "expectations": [
    {"text": "Clear assertion text", "passed": true, "evidence": "Short evidence from the output."}
  ]
}
```

Do not use empty `expectations`. If an eval draft is missing assertions, stop and add them before launching rollouts or before grading.

Then run:

```bash
cd <skill-improver-path>
python -m scripts.aggregate_benchmark <workspace>/runs/<run-id> --skill-name <skill-name> --skill-path <workspace>/skill-revisions/<revision-id>
```

If aggregation fails, treat it as an improver setup bug and fix the missing metadata or malformed grading files. Do not intentionally ship zero-assertion runs.

## Generate the Review Viewer

Always use the bundled viewer generator. Do not write custom HTML.

Served viewer:

```bash
nohup python <skill-improver-path>/eval-viewer/generate_review.py \
  <workspace>/runs/<run-id> \
  --skill-name "<skill-name>" \
  --benchmark <workspace>/runs/<run-id>/benchmark.json \
  > <workspace>/runs/<run-id>/viewer.log 2>&1 &
VIEWER_PID=$!
```

After launching, check that the process is still running and that `viewer.log` contains a usable URL. Open the URL for the user when possible.

If `benchmark.json` does not exist, omit the `--benchmark` argument.

## Final Message After Opening the Viewer

After the served viewer opens, stop and report only what the user needs:

- The viewer URL.
- The workspace path.
- A link to the exact evals file at `<workspace>/runs/evals/evals.json` so the user can review the test prompts and assertions.
- A link to `skill-reporting/<skill-name>/report.md` and `skill-reporting/<skill-name>/status.md`.
- A short note that the Results tab compares `with <skill-name>` against `without <skill-name>`.
- Clear next step: "After you press Submit All Reviews in the viewer, prompt me to continue. I will read feedback from `<workspace>/runs/<run-id>/feedback.json`."

Do not revise, package, or reinstall the skill before the user reviews the comparison.

## Continuing After User Feedback

When the user prompts you to continue, read the previous run's feedback file, starting with `<workspace>/runs/original/feedback.json` after the first viewer. The served viewer writes that file directly in the run workspace when the user presses Submit All Reviews. If it is missing, treat that as a viewer or server problem to debug rather than asking the user to supply feedback manually.

Read the feedback, summarize the user's preference and concrete complaints, then create the next skill revision by copying the previous revision. For example, after `runs/original`, create and edit `<workspace>/skill-revisions/iteration-1/`.

After editing the next skill revision, write or update `<previous-run-workspace>/revision_brief.md`. The brief must include:

- The user's viewer feedback summary.
- The rationale for each skill update.
- The exact unified diff applied to the updated skill, comparing the previous revision's `SKILL.md` to `<workspace>/skill-revisions/<next-revision-id>/SKILL.md`.

After editing `<workspace>/skill-revisions/<next-revision-id>/`, always pause before running the next paired iteration. In that pause message:

- Summarize each skill update made.
- Explain why each update was made, grounded in the user's viewer feedback.
- Link to the updated `<workspace>/skill-revisions/<next-revision-id>/SKILL.md` file for final review.
- Link to the updated `<previous-run-workspace>/revision_brief.md` file so the user can inspect the exact diff.
- Ask the user to confirm that the skill changes look right before proceeding with the next round of tests.

Do not run rollouts, grade outputs, or generate the next viewer until the user confirms the updated skill file.

To create the next revision from the previous one, run:

```bash
python <skill-improver-path>/scripts/snapshot_skill.py \
  <workspace>/skill-revisions/original \
  <workspace> \
  --label iteration-1 \
  --parent original \
  --note "short summary of changes"
```

Then edit `<workspace>/skill-revisions/iteration-1/`, pause for user confirmation, and repeat the paired `with_skill` versus `without_skill` rollout and viewer generation in `<workspace>/runs/iteration-1/`, passing `--previous-workspace <workspace>/runs/original` to `generate_review.py`. For later rounds, advance both ids together: `skill-revisions/iteration-2` produces `runs/iteration-2`, and so on.

At the same time, update the reporting workspace:

- Refresh `skill-reporting/<skill-name>/status.md` with the new testing scope and overall result after each reviewed run.
- Do not spend time fully writing `skill-reporting/<skill-name>/report.md` or `skill-reporting/<skill-name>/slack-post.md` during intermediate iterations unless the user explicitly asks for them early.

If `benchmark.json` exists, refresh `status.md` with:

```bash
python <skill-improver-path>/scripts/init_reporting_workspace.py \
  <repo-or-cwd> \
  --skill-name <skill-name> \
  --improver-workspace <workspace> \
  --run-dir <workspace>/runs/<run-id> \
  --benchmark <workspace>/runs/<run-id>/benchmark.json \
  --status "under review" \
  --replace
```

Only reinstall or package the improved skill after the user explicitly says the reviewed behavior is good.

## Reporting Workspace Finalization

When the user says they are done iterating, happy with the skill changes, or ready to install/finalize the updated skill, finish the reporting workspace before or alongside packaging/install work.

In that finalization step:

- Complete `skill-reporting/<skill-name>/report.md` with:
  - eval scope
  - final status
  - side-by-side baseline vs latest approved revision examples
  - hero artifacts
  - concise notes on what changed during the iteration
- Complete `skill-reporting/<skill-name>/slack-post.md` with a short shareable summary:
  - what the skill does
  - how it compared to baseline
  - useful iteration insights
  - the recommended next step
- Refresh `skill-reporting/<skill-name>/status.md` to `update ready` or `complete`, depending on whether install/package work is still pending.

Use the latest approved revision as the default “final” skill version in `report.md` and `slack-post.md`, and compare it against the corresponding baseline run unless the user asks for a different comparison.
