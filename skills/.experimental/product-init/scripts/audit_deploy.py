#!/usr/bin/env python3
"""Gate 7 - Deploy audit. prod_url returns 200, has <title>, smoke job present, rollback drill <14d."""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402
from lib.tool_runner import run  # noqa: E402

try:
    import frontmatter
except ImportError:
    frontmatter = None

try:
    import requests
except ImportError:
    requests = None


def get_prod_url(project_dir: Path):
    p = project_dir / "PRODUCT.md"
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8", errors="ignore")
    if frontmatter:
        try:
            post = frontmatter.loads(text)
            return post.metadata.get("prod_url")
        except Exception:
            pass
    m = re.search(r"^prod_url\s*:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


TBD_RE = re.compile(r"^TBD[-_].+", re.IGNORECASE)


def find_debt_ack(project_dir: Path):
    """Return (debt_id, row_text) of an infra DEBT row that acknowledges the
    prod_url placeholder, or None."""
    p = project_dir / "DEBT.md"
    if not p.exists():
        return None
    keyword_re = re.compile(r"prod_url|gate\s*7|deploy", re.IGNORECASE)
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[3].lower() != "infra":
            continue
        if keyword_re.search(line):
            return cells[0], line.strip()
    return None


def audit(project_dir: Path) -> Report:
    rep = Report(name="gate7-deploy")
    gate = "Gate 7: Deploy"

    prod_url = get_prod_url(project_dir)
    is_tbd = isinstance(prod_url, str) and bool(TBD_RE.match(prod_url.strip()))
    if is_tbd:
        ack = find_debt_ack(project_dir)
        if ack:
            debt_id, _ = ack
            rep.add_finding(Severity.HIGH, gate, "prod-url-tbd",
                            f"prod_url is placeholder `{prod_url}`; acknowledged by DEBT row {debt_id} (infra).",
                            "Replace prod_url with a real URL after Gate 7 deploy; close DEBT row.")
        else:
            rep.add_finding(Severity.CRITICAL, gate, "prod-url-tbd",
                            f"prod_url is placeholder `{prod_url}` and no infra DEBT row acknowledges it",
                            "Either deploy and set prod_url, or add an infra DEBT row referencing prod_url/gate 7/deploy.")
        prod_url = None  # skip live fetch checks below
    if not prod_url and not is_tbd:
        rep.add_finding(Severity.CRITICAL, gate, "prod-url",
                        "no `prod_url` in PRODUCT.md frontmatter",
                        "Add `prod_url: https://...` to PRODUCT.md frontmatter.")
    elif not prod_url:
        pass  # TBD case already reported above
    elif not requests:
        rep.add_finding(Severity.MEDIUM, gate, "requests-missing",
                        "requests library not installed",
                        "pip install requests")
    else:
        ok = False
        last_err = ""
        for _ in range(3):
            try:
                r = requests.head(prod_url, timeout=10, allow_redirects=True)
                if r.status_code == 200:
                    ok = True
                    break
                last_err = f"HTTP {r.status_code}"
            except Exception as e:
                last_err = str(e)
        if not ok:
            rep.add_finding(Severity.CRITICAL, gate, "prod-url-200",
                            f"{prod_url}: {last_err}",
                            "Make production reachable; HEAD must return 200.")
        else:
            try:
                r = requests.get(prod_url, timeout=15)
                m = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.IGNORECASE | re.DOTALL)
                if not m or not m.group(1).strip():
                    rep.add_finding(Severity.HIGH, gate, "prod-title",
                                    f"{prod_url}: empty <title>",
                                    "Production page has no title; likely an empty shell.")
            except Exception as e:
                rep.add_finding(Severity.HIGH, gate, "prod-get",
                                f"GET failed: {e}",
                                "Investigate prod URL.")

    workflows = list((project_dir / ".github" / "workflows").glob("*.yml")) if (project_dir / ".github" / "workflows").exists() else []
    smoke_seen = any("smoke" in w.read_text(encoding="utf-8", errors="ignore").lower() for w in workflows)
    if not smoke_seen:
        rep.add_finding(Severity.HIGH, gate, "smoke-job",
                        "no `smoke` keyword in .github/workflows/*.yml",
                        "Add a post-deploy smoke job that hits prod_url.")

    today = dt.date.today()
    drill_recent = False
    res = run(["git", "-C", str(project_dir), "tag", "--list", "rollback-drill-*"])
    if res.ok:
        for tag in res.stdout.split():
            m = re.match(r"rollback-drill-(\d{4}-\d{2}-\d{2})", tag)
            if m:
                try:
                    d = dt.date.fromisoformat(m.group(1))
                    if (today - d).days <= 14:
                        drill_recent = True
                        break
                except ValueError:
                    pass
    if not drill_recent:
        runbook = project_dir / "runbooks" / "rollback-drills.md"
        if runbook.exists():
            mtime = dt.date.fromtimestamp(runbook.stat().st_mtime) if False else dt.datetime.fromtimestamp(runbook.stat().st_mtime).date()
            if (today - mtime).days <= 14:
                drill_recent = True
    if not drill_recent:
        rep.add_finding(Severity.HIGH, gate, "rollback-drill",
                        "no `rollback-drill-YYYY-MM-DD` tag or recent runbooks/rollback-drills.md within 14 days",
                        "Run a rollback drill, document it, and tag/commit the result.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Gate 7: Deploy audit")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
