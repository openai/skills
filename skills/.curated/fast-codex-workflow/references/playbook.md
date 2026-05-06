# Playbook: Task Recipes, Verification Budget, Coding Defaults

Reference content for the `fast-codex-workflow` operating loop. Codex loads this on demand when the active task matches one of the recipes below or when escalation requires the deeper budget.

## Task Recipes

- **Bug fix** - read the exact error or failing behavior, inspect the smallest owning code path, search for the existing pattern, patch the root cause, run the narrowest regression check.
- **Feature or change** - identify owning files and existing pattern, make the smallest complete implementation, avoid optional polish, verify the touched behavior.
- **Review or audit** - map the surface quickly, inspect high-risk paths first, lead with evidence-backed findings, then note test gaps and residual risk.
- **Frontend or UI** - inspect the component and styling path, run build/typecheck when relevant, use browser/screenshot checks when layout or interaction can regress.
- **Environment or tooling** - check versions/config/list output first, run a direct smoke test before changing config, patch the smallest setting, then verify with the same command that exposed the issue.
- **Recommendation or research** - verify current sources when facts can drift, choose the best option, state why it beats the alternatives.

## Verification Budget

- **Tiny tasks** - one direct command, exact answer, or no tool call when the answer is already known and stable.
- **Normal code changes** - targeted test, typecheck, lint, or build command that covers the touched behavior.
- **UI changes** - run or inspect the app when feasible; use Playwright or screenshot checks for layout, rendering, and interaction risks.
- **Deep audits or security work** - broaden verification intentionally, but still parallelize independent reads and avoid unrelated cleanup.
- **Environment or tooling slowness** - prefer narrow diagnostics first. Only widen to environment-level maintenance when local bloat or slow startup is the proven cause.

## Coding Defaults

- Read before editing.
- Match existing style and local helpers.
- Make the smallest complete change.
- Re-read touched code for obvious mistakes.
- Run the relevant verification command and report exactly what passed or failed.
