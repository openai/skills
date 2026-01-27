You are generating a change prompt for an integration test. First, check whether AGENTS.md exists at the repo root and incorporate any build/test guidance from it. If AGENTS.md is missing, note that in your rationale field.

You must generate a plan-worthy task. Plan-worthy means the change should be complex enough to justify a PLANS.md-style ExecPlan: at least two repository files are likely to be edited, validation requires tests or explicit verification steps, and there is non-trivial sequencing or reasoning involved. Keep scope small and realistic for this repo, but not trivial. Examples of plan-worthy prompts: refactor a subsystem to improve clarity or reduce duplication, or implement a sizeable feature slice that touches multiple layers (API, data model, and UI).

Return strict JSON with this schema:
{
  "seed_task": "string or null",
  "prompt_origin": "auto",
  "change_prompt": "string",
  "acceptance_criteria": ["..."],
  "build_test_plan": [
{"label": "build", "cmd": "..."},
{"label": "test", "cmd": "..."}
  ],
  "scoring_focus": ["correctness", "context_usage", "builds_tests_pass", "maintainability", "risk"],
  "agentic_loop": {
"cmd": "codex",
"args": ["exec", "--full-auto", "-C", "{repo_root}", "{change_prompt}"],
"timeout_seconds": 1800
  },
  "llm_eval": {
"cmd": "codex",
"args": ["exec", "--output-schema", "{eval_schema_path}", "--output-last-message", "{eval_output_path}", "--color", "never", "--sandbox", "read-only", "-C", "{repo_root}", "-"],
"timeout_seconds": 600
  },
  "rationale": "string"
}

Notes:
- agentic_loop and llm_eval are optional; defaults will be applied if omitted.

Rules:
- If a seed task is provided, use it as the primary direction and set seed_task accordingly.
- change_prompt must be actionable and scoped to a small but real code change.
- change_prompt must not include meta-instructions like “follow AGENTS.md”, “run tests”, or other process guidance; keep those in build_test_plan or rationale.
- acceptance_criteria must be testable and concrete.
- build_test_plan must include at least one build or test command if such commands are documented.
- Output JSON only. No markdown.
