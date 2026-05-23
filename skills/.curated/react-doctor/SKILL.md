---
name: react-doctor
description: Scan a React, React Native, Next.js, Vite, Remix, or TanStack Start codebase for security, performance, accessibility, architecture, and correctness issues using the `react-doctor` CLI, and report a 0-100 health score. Use after finishing a React feature or bug fix, before committing React code, when the user asks for a "React health check / score / audit / review" or mentions react-doctor, or when the user wants to clean up an existing React codebase by severity. Skip for projects that do not depend on `react`, `react-dom`, `react-native`, or an Expo / Next / Vite / TanStack / Remix framework that pulls them in.
---

# React Doctor

Run [`react-doctor`](https://github.com/millionco/react-doctor) to produce a 0-100 health score plus categorized diagnostics for any React codebase. Rules toggle automatically based on the detected framework (Next.js, Vite, Remix, TanStack Start, Expo, React Native) and React version, so you do not need to configure anything before the first run.

## When to use

- The user finished a React feature or bug fix and wants to verify nothing regressed before committing.
- The user asks for a "React health check / score / audit / code review" or names `react-doctor` directly.
- The user wants to clean up an existing React codebase by severity (errors first, then warnings).
- A pre-commit or pre-push checkpoint, when changed files are `.tsx` / `.jsx` / `.ts` / `.js` inside a React project.

## Default workflow (recently-changed files only)

Run inside the project root:

```bash
npx react-doctor@latest --verbose --diff
```

- `--diff` auto-detects `main` / `master`. Pass an explicit base when needed: `--diff develop`.
- `--verbose` prints every rule fired with file paths and line numbers (default shows top 3 rules).

Read the printed diagnostics top-down — they are already sorted by severity. Compare the printed score with any earlier score the user mentioned to detect a regression. If the score dropped, fix the new diagnostics this branch introduced before committing.

## Full-codebase cleanup

When the user wants to harden the whole project, drop `--diff` so every file is scanned:

```bash
npx react-doctor@latest --verbose
```

Resolve issues in this order:

1. `error` severity, ranked by category (Security → Correctness → React Native → Performance → Architecture → Accessibility).
2. `warning` severity in the same category order.
3. Re-run the command after each batch of fixes to confirm the score moved up.

## Reading the score

| Score   | Label      | Meaning                                  |
| ------: | ---------- | ---------------------------------------- |
| 75+     | Great      | Healthy baseline; focus on regressions.  |
| 50 - 74 | Needs work | Material issues to fix.                  |
| < 50    | Critical   | Address top-severity findings first.     |

Formula: `100 - (unique_error_rules * 1.5) - (unique_warning_rules * 0.75)`. The score penalizes **unique rules triggered**, not total instances — fixing the last violation of a rule is what removes its penalty. Pin a specific `react-doctor` version in CI if you need stable scores across upgrades.

## Useful flags

| Flag                    | Purpose                                                                  |
| ----------------------- | ------------------------------------------------------------------------ |
| `--verbose`             | Print every rule fired with file paths and line numbers.                 |
| `--diff [base]`         | Scan only files changed vs the base branch.                              |
| `--staged`              | Scan only files in the git index (use inside a pre-commit hook).         |
| `--score`               | Print only the numeric score — useful for threshold checks.              |
| `--json`                | Emit a structured JSON report on stdout (`ok: false` on error).          |
| `--fail-on <level>`     | Exit non-zero on `error`, `warning`, or `none`.                          |
| `--explain <file:line>` | Diagnose why a rule fired or why a nearby suppression did not apply.     |
| `--offline`             | Skip the score API entirely (no network, no score, no share URL).        |

`--staged` and `--diff` cannot be combined.

## Suppressing a finding

When a diagnostic is intentional, prefer **inline suppression** over editing config:

```tsx
// react-doctor-disable-next-line react-doctor/no-cascading-set-state
useEffect(() => {
  setA(value);
  setB(value);
}, [value]);
```

When two rules fire on the same line, comma-separate the ids on one comment or stack one comment per rule directly above the diagnostic (nothing but other `react-doctor-disable-next-line` comments may sit between them and the target line). If a suppression looks adjacent but the rule still fires, run `npx react-doctor@latest --explain <file:line>` to find out why.

For multi-file exemptions, add an entry to `react-doctor.config.json` (or the `"reactDoctor"` key in `package.json`):

```json
{
  "ignore": {
    "rules": ["react-doctor/no-danger"],
    "files": ["src/generated/**"],
    "overrides": [
      {
        "files": ["components/Highlight.tsx"],
        "rules": ["react-doctor/no-danger"]
      }
    ]
  }
}
```

`ignore.overrides` is the narrowest knob — it silences the listed rules only on the matched files and leaves every other rule active. Reach for it before `ignore.files`, which silences every rule on the matched paths.

## Notes

- React Doctor honors `.gitignore`, `.eslintignore`, `.oxlintignore`, `.prettierignore`, and inline `// eslint-disable*` / `// oxlint-disable*` comments.
- When the project already has an `.oxlintrc.json` or `.eslintrc.json`, its rules are merged into the scan automatically and count toward the score. Set `"adoptExistingLintConfig": false` in `react-doctor.config.json` to opt out.
- The same binary can post sticky PR comments and GitHub Actions annotations in CI — see the composite action documented in [`millionco/react-doctor`](https://github.com/millionco/react-doctor).
- Network is only used for the score API and the share URL. The rest of the report works fully offline; pass `--offline` to skip the network entirely.
