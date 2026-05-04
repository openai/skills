#!/usr/bin/env python3
"""Gate 5 - E2E (Playwright) audit. Demands a non-localhost baseURL and a green @golden-path test."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402


def find_pw_config(project: Path):
    for name in ("playwright.config.ts", "playwright.config.js", "playwright.config.mjs", "playwright.config.cjs"):
        p = project / name
        if p.exists():
            return p
    return None


def parse_baseurl(text: str):
    """Return (literal_url, env_var_name) tuple. Either may be None."""
    # Capture the full RHS of `baseURL:` (or `=`) up to a comma/newline/closing brace.
    m = re.search(r"baseURL\s*[:=]\s*([^,\n}]+)", text)
    if not m:
        return (None, None)
    rhs = m.group(1).strip().rstrip(",")
    literal = None
    env_var = None
    lit_m = re.search(r"['\"]([^'\"]+)['\"]", rhs)
    if lit_m:
        literal = lit_m.group(1)
    env_m = re.search(r"process\.env\.([A-Z_][A-Z0-9_]*)", rhs)
    if env_m:
        env_var = env_m.group(1)
    return (literal, env_var)


def env_var_documented(project_dir: Path, var: str) -> bool:
    # Check .env.example or any .env* file
    for envfile in list(project_dir.glob(".env*")):
        try:
            txt = envfile.read_text(encoding="utf-8", errors="ignore")
            if re.search(rf"^{re.escape(var)}\s*=", txt, re.MULTILINE):
                return True
        except OSError:
            pass
    # Check workflow files
    wf_dir = project_dir / ".github" / "workflows"
    if wf_dir.exists():
        for wf in wf_dir.glob("*.yml"):
            try:
                txt = wf.read_text(encoding="utf-8", errors="ignore")
                if re.search(rf"{re.escape(var)}\s*:\s*https?://", txt):
                    return True
            except OSError:
                pass
        for wf in wf_dir.glob("*.yaml"):
            try:
                txt = wf.read_text(encoding="utf-8", errors="ignore")
                if re.search(rf"{re.escape(var)}\s*:\s*https?://", txt):
                    return True
            except OSError:
                pass
    return False


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate5-e2e")
    gate = "Gate 5: QA / E2E"
    cfg = find_pw_config(project_dir)
    if not cfg:
        rep.add_finding(Severity.HIGH, gate, "playwright-config",
                        "no playwright.config.* found",
                        "Add Playwright with a real preview/staging baseURL.")
        return rep
    cfg_text = cfg.read_text(encoding="utf-8", errors="ignore")
    literal, env_var = parse_baseurl(cfg_text)
    if not literal and not env_var:
        rep.add_finding(Severity.CRITICAL, gate, "baseurl",
                        "baseURL not set in playwright config",
                        "Set baseURL to a real preview deploy URL.")
    elif literal and ("localhost" in literal or "127.0.0.1" in literal):
        rep.add_finding(Severity.CRITICAL, gate, "baseurl-localhost",
                        f"baseURL is local: {literal}",
                        "Point baseURL at the deployed preview URL, not localhost.")
    elif literal and literal.startswith(("http://", "https://")):
        # literal HTTPS (or HTTP non-localhost) URL — accepted; env-var fallback is fine
        pass
    elif env_var:
        # Bare env-var reference: require documentation in .env* or workflow
        if not env_var_documented(project_dir, env_var):
            rep.add_finding(Severity.HIGH, gate, "baseurl-env-undocumented",
                            f"baseURL uses process.env.{env_var} with no documented value",
                            f"Document {env_var} in .env.example or set it in a workflow.")

    pw_bin = project_dir / "node_modules" / ".bin" / "playwright"
    if pw_bin.exists():
        res = run([str(pw_bin), "test", "--reporter=json"], cwd=str(project_dir), timeout=900)
        try:
            data = json.loads(res.stdout)
        except Exception:
            rep.add_finding(Severity.HIGH, gate, "playwright-run",
                            "could not parse playwright JSON",
                            "Run `npx playwright test --reporter=json` locally to debug.")
            data = None
        if data:
            golden_seen = False
            failed = 0
            for suite in data.get("suites", []):
                _walk(suite, rep, gate, locals_obj := {"golden": False, "failed": 0})
                golden_seen = golden_seen or locals_obj["golden"]
                failed += locals_obj["failed"]
            if not golden_seen:
                rep.add_finding(Severity.CRITICAL, gate, "golden-path-tag",
                                "no test tagged @golden-path",
                                "Tag the end-to-end happy path test with @golden-path.")
            if failed:
                rep.add_finding(Severity.CRITICAL, gate, "e2e-failed",
                                f"{failed} failing e2e tests", "Fix all e2e failures.")
    else:
        rep.add_finding(Severity.MEDIUM, gate, "playwright-not-installed",
                        "node_modules/.bin/playwright missing",
                        "Install Playwright: `npm i -D @playwright/test`.")

    # console error scan in trace dirs
    for d in ("test-results", "playwright-report"):
        root = project_dir / d
        if not root.exists():
            continue
        for f in root.rglob("*.json"):
            try:
                txt = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(r'"type"\s*:\s*"console".*"(error|warning)"', txt):
                rep.add_finding(Severity.HIGH, gate, "console-pollution",
                                f"console error/warning in {f.relative_to(project_dir)}",
                                "Drive console.error/warn count to 0 on the golden path.")
                break
    return rep


def _walk(suite, rep, gate, acc):
    for t in suite.get("specs", []):
        title = t.get("title", "")
        if "@golden-path" in title:
            acc["golden"] = True
        for run_obj in t.get("tests", []):
            for r in run_obj.get("results", []):
                if r.get("status") not in ("passed", "skipped"):
                    acc["failed"] += 1
    for child in suite.get("suites", []):
        _walk(child, rep, gate, acc)


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 5: E2E audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
