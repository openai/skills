#!/usr/bin/env python3
"""Automated evaluation runner for Conductor skill.

Uses Claude as both the agent-under-test and the judge.
Requires ANTHROPIC_API_KEY env var.

Usage:
    # Run all evals
    python3 scripts/run_evals.py

    # Run specific eval(s)
    python3 scripts/run_evals.py evaluations/install-and-connect.json

    # Run with a specific model
    python3 scripts/run_evals.py --model claude-sonnet-4-20250514

    # Run with verbose output
    python3 scripts/run_evals.py --verbose

    # Output JSON report
    python3 scripts/run_evals.py --json --output report.json
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "claude-sonnet-4-20250514"
JUDGE_MODEL = "claude-sonnet-4-20250514"
API_URL = "https://api.anthropic.com/v1/messages"
SKILL_DIR = Path(__file__).resolve().parent.parent
EVAL_DIR = SKILL_DIR / "evaluations"


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def call_claude(api_key, model, system, user_message, max_tokens=4096):
    """Call Claude API via urllib (stdlib only)."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user_message}],
    }).encode()

    req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")

    retries = 3
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                return data["content"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  [RETRY] HTTP {e.code}, waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            error_body = ""
            try:
                error_body = e.read().decode()
            except Exception:
                pass
            print(f"API error: HTTP {e.code} {e.reason}\n{error_body}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"Connection error: {e.reason}", file=sys.stderr)
            sys.exit(1)


# ---------------------------------------------------------------------------
# Skill context loader
# ---------------------------------------------------------------------------

def load_skill_context():
    """Load SKILL.md, references, and examples as context for the agent."""
    parts = []

    skill_md = SKILL_DIR / "SKILL.md"
    if skill_md.exists():
        parts.append(f"# SKILL.md\n\n{skill_md.read_text()}")

    refs_dir = SKILL_DIR / "references"
    if refs_dir.exists():
        for ref_file in sorted(refs_dir.glob("*.md")):
            parts.append(f"# {ref_file.name}\n\n{ref_file.read_text()}")

    examples_dir = SKILL_DIR / "examples"
    if examples_dir.exists():
        for ex_file in sorted(examples_dir.glob("*.md")):
            parts.append(f"# Example: {ex_file.stem}\n\n{ex_file.read_text()}")

    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# Eval runner
# ---------------------------------------------------------------------------

def run_agent(api_key, model, skill_context, query, verbose=False):
    """Send the eval query to Claude acting as an agent with the skill."""
    system = f"""You are an AI coding agent with access to the Conductor workflow skill. Your tools include: Bash (shell commands), Read/Write/Edit (files), Grep/Glob (search).

You must follow the skill instructions precisely. Key rules:
- ALWAYS install the `conductor` CLI proactively if missing — RUN `npm install -g @conductor-oss/conductor-cli` yourself, do NOT just tell the user to install it. If npm is missing, install Node.js first (brew install node on macOS, nodesource on Linux) BEFORE installing the CLI. Only fall back to `scripts/conductor_api.py` if Node.js/npm truly cannot be installed.
- When setting up a server connection, ALWAYS ask the user to choose between local and remote — do not assume one or the other.
- Request auth credentials ONLY when the server returns 401/403 — never ask for auth preemptively.
- ALWAYS save the connection as a named profile using `conductor config save` so it persists for reuse.
- ALWAYS verify the setup works with a final connectivity check (e.g. `conductor workflow list`).
- NEVER use `python3 -c` for any purpose.
- NEVER echo auth tokens, keys, or secrets in output — use env vars or CLI flags, and redact any sensitive values.
- Write workflow JSON to a file first, then pass the file path to CLI commands.
- After registering a workflow, you MUST check `conductor taskDef list` to verify all SIMPLE tasks have registered workers. For any SIMPLE task missing from the task definitions, flag it to the user and offer to create the task definition and scaffold a worker.
- When writing workers, always include a comment or docstring noting the worker must be idempotent (safe to retry on failure/timeout).
- Use `--profile` flag when the user mentions an environment (dev, prod, staging).
- Use `--json` flags when available for structured output.

When responding, describe the exact steps you would take:
1. Show the exact bash commands you would run (real commands, not placeholders)
2. Show the exact file contents you would write (complete JSON, not truncated)
3. Explain your decision logic at EVERY branching point — cover ALL paths, not just the happy path. For example:
   - If the user needs a server: present both local and remote options and let them choose
   - If a command returns 401/403: describe how you would handle auth
   - If a tool/CLI is missing: show the fallback approach
4. Show what you would communicate to the user at each step

Follow the patterns from the examples in the skill context. Be thorough — cover prerequisites, the main action, all conditional branches, verification, and cleanup/next-steps.

--- SKILL INSTRUCTIONS ---

{skill_context}"""

    user_msg = f"""User query: {query}

Describe in detail the complete sequence of steps you would take to handle this request. Show exact commands, exact file contents, and exact user communications. Follow the skill rules strictly."""

    if verbose:
        print(f"  [AGENT] Sending query to {model}...")

    return call_claude(api_key, model, system, user_msg, max_tokens=8192)


def judge_response(api_key, judge_model, query, agent_response, expected_behavior, success_criteria, verbose=False):
    """Use Claude as judge to evaluate the agent response."""
    system = """You are an evaluation judge for an AI coding agent. The agent was given a task and described the steps it WOULD take (a plan), without actually executing anything.

You must evaluate EACH success criterion individually based on the agent's described plan.

Evaluation guidelines:
- The agent is describing a PLAN, not showing actual execution output. Judge whether the plan WOULD satisfy each criterion if executed.
- "CLI is installed automatically" means the plan includes running the install command proactively (not just suggesting the user do it).
- "Auth tokens are never echoed" means the plan does not include printing/logging actual token values, and uses env vars or redacted placeholders appropriately.
- "Workflow definition is fetched from the server" means the plan includes a command to fetch it (e.g., `conductor workflow get ...`), even though no actual server response is shown.
- "Commands are shown" means the agent wrote out the actual CLI commands it would run, not vague descriptions.
- If the agent describes a conditional path (e.g., "if 401 then request auth"), credit the criterion if the relevant branch is covered.
- Be lenient on exact formatting but strict on whether the correct commands and approach are used.

Return a JSON object with this exact structure:
{
  "criteria_results": [
    {
      "criterion": "the criterion text",
      "pass": true or false,
      "reason": "brief explanation"
    }
  ],
  "overall_pass": true or false,
  "overall_score": 0.0 to 1.0,
  "summary": "1-2 sentence overall assessment"
}

Set overall_score to the fraction of criteria that passed (passed / total). Set overall_pass to true if at least 80% of criteria pass.
Return ONLY valid JSON, no other text."""

    user_msg = f"""## User Query
{query}

## Agent Response
{agent_response}

## Expected Behavior (for reference, not scored)
{json.dumps(expected_behavior, indent=2)}

## Success Criteria (score each one)
{json.dumps(success_criteria, indent=2)}

Evaluate each success criterion. Return JSON only."""

    if verbose:
        print(f"  [JUDGE] Evaluating with {judge_model}...")

    raw = call_claude(api_key, judge_model, system, user_msg)

    # Extract JSON from response (handle markdown code blocks)
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]  # remove opening ```json
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "criteria_results": [],
            "overall_pass": False,
            "overall_score": 0.0,
            "summary": f"Judge returned invalid JSON: {raw[:200]}",
        }


def run_single_eval(api_key, model, judge_model, skill_context, eval_file, verbose=False):
    """Run a single evaluation and return results."""
    with open(eval_file) as f:
        eval_data = json.load(f)

    name = eval_data["name"]
    query = eval_data["query"]
    expected_behavior = eval_data.get("expected_behavior", [])
    success_criteria = eval_data.get("success_criteria", [])

    print(f"\n{'='*60}")
    print(f"  EVAL: {name}")
    print(f"  FILE: {Path(eval_file).name}")
    print(f"  MODEL: {model}")
    print(f"{'='*60}")

    # Step 1: Run agent
    agent_response = run_agent(api_key, model, skill_context, query, verbose)

    if verbose:
        print(f"\n  --- Agent Response ---")
        print(f"  {agent_response[:500]}...")
        print(f"  --- End Response ---\n")

    # Step 2: Judge response
    judgment = judge_response(
        api_key, judge_model, query, agent_response,
        expected_behavior, success_criteria, verbose
    )

    # Step 3: Display results
    criteria_results = judgment.get("criteria_results", [])
    passed = sum(1 for c in criteria_results if c.get("pass"))
    total = len(criteria_results)
    score = judgment.get("overall_score", 0.0)
    overall = judgment.get("overall_pass", False)

    for cr in criteria_results:
        status = "PASS" if cr.get("pass") else "FAIL"
        icon = "+" if cr.get("pass") else "-"
        print(f"  [{icon}] {status}: {cr.get('criterion', '?')}")
        if not cr.get("pass") and verbose:
            print(f"         Reason: {cr.get('reason', '')}")

    print(f"\n  Score: {passed}/{total} criteria passed ({score:.0%})")
    print(f"  Overall: {'PASS' if overall else 'FAIL'}")
    print(f"  Summary: {judgment.get('summary', '')}")

    return {
        "name": name,
        "file": str(Path(eval_file).name),
        "model": model,
        "overall_pass": overall,
        "overall_score": score,
        "passed": passed,
        "total": total,
        "summary": judgment.get("summary", ""),
        "criteria_results": criteria_results,
        "agent_response": agent_response,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run automated evaluations for the Conductor skill"
    )
    parser.add_argument(
        "files", nargs="*",
        help="Specific eval JSON files to run (default: all in evaluations/)"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Model for agent-under-test (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--judge-model", default=JUDGE_MODEL,
        help=f"Model for judge (default: {JUDGE_MODEL})"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output JSON report")
    parser.add_argument("--output", "-o", default=None, help="Write JSON report to file")

    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        print("Get your key at https://console.anthropic.com/", file=sys.stderr)
        sys.exit(1)

    judge_model = args.judge_model

    # Collect eval files
    if args.files:
        eval_files = [Path(f) for f in args.files]
    else:
        eval_files = sorted(EVAL_DIR.glob("*.json"))

    if not eval_files:
        print("No evaluation files found.", file=sys.stderr)
        sys.exit(1)

    # Load skill context once
    print("Loading skill context...")
    skill_context = load_skill_context()
    print(f"Loaded {len(skill_context)} chars of skill context")
    print(f"Running {len(eval_files)} evaluation(s) with model: {args.model}")

    # Run evals
    results = []
    for eval_file in eval_files:
        if not eval_file.exists():
            print(f"Warning: {eval_file} not found, skipping.", file=sys.stderr)
            continue
        if eval_file.name == "README.md":
            continue

        result = run_single_eval(api_key, args.model, judge_model, skill_context, eval_file, args.verbose)
        results.append(result)

    # Summary
    total_evals = len(results)
    passed_evals = sum(1 for r in results if r["overall_pass"])
    total_criteria = sum(r["total"] for r in results)
    passed_criteria = sum(r["passed"] for r in results)
    avg_score = sum(r["overall_score"] for r in results) / total_evals if total_evals else 0

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Evals:    {passed_evals}/{total_evals} passed")
    print(f"  Criteria: {passed_criteria}/{total_criteria} passed")
    print(f"  Avg score: {avg_score:.0%}")
    print()

    for r in results:
        icon = "+" if r["overall_pass"] else "-"
        print(f"  [{icon}] {r['name']}: {r['passed']}/{r['total']} ({r['overall_score']:.0%})")

    print()

    # JSON report
    report = {
        "model": args.model,
        "judge_model": judge_model,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": {
            "total_evals": total_evals,
            "passed_evals": passed_evals,
            "total_criteria": total_criteria,
            "passed_criteria": passed_criteria,
            "avg_score": round(avg_score, 3),
        },
        "results": results,
    }

    if args.json_output:
        # Strip agent_response from console JSON to keep it readable
        slim = json.loads(json.dumps(report))
        for r in slim["results"]:
            r.pop("agent_response", None)
        print(json.dumps(slim, indent=2))

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"  Report written to {args.output}")

    # Exit code: fail if any eval failed
    sys.exit(0 if passed_evals == total_evals else 1)


if __name__ == "__main__":
    main()
