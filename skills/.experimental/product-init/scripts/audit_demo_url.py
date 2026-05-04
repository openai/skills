#!/usr/bin/env python3
"""Cross-cutting: prod_url returns HTTP 200, body > 500 bytes, has non-empty <title>."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.report import Report, Severity  # noqa: E402

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
    rep = Report(name="cross-demo-url")
    gate = "Cross: Demo URL"

    url = get_prod_url(project_dir)
    if not url:
        rep.add_finding(Severity.HIGH, gate, "prod-url-missing",
                        "no prod_url in PRODUCT.md frontmatter",
                        "Add prod_url to PRODUCT.md.")
        return rep
    if isinstance(url, str) and TBD_RE.match(url.strip()):
        ack = find_debt_ack(project_dir)
        if ack:
            debt_id, _ = ack
            rep.add_finding(Severity.HIGH, gate, "prod-url-tbd",
                            f"prod_url is placeholder `{url}`; acknowledged by DEBT row {debt_id} (infra).",
                            "Replace prod_url with a real URL after Gate 7 deploy; close DEBT row.")
        else:
            rep.add_finding(Severity.CRITICAL, gate, "prod-url-tbd",
                            f"prod_url is placeholder `{url}` and no infra DEBT row acknowledges it",
                            "Either deploy and set prod_url, or add an infra DEBT row referencing prod_url/gate 7/deploy.")
        return rep
    if not requests:
        rep.add_finding(Severity.MEDIUM, gate, "requests-missing",
                        "requests library not installed",
                        "pip install requests")
        return rep
    try:
        r = requests.get(url, timeout=15)
    except Exception as e:
        rep.add_finding(Severity.CRITICAL, gate, "fetch-error",
                        f"{url}: {e}", "Make prod URL reachable.")
        return rep
    if r.status_code != 200:
        rep.add_finding(Severity.CRITICAL, gate, "http-status",
                        f"{url} returned {r.status_code}", "Fix prod deploy.")
        return rep
    if len(r.content) < 500:
        rep.add_finding(Severity.HIGH, gate, "empty-shell",
                        f"body length {len(r.content)} bytes < 500",
                        "Looks like an empty shell; verify rendered content.")
    m = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.IGNORECASE | re.DOTALL)
    if not m or not m.group(1).strip():
        rep.add_finding(Severity.HIGH, gate, "empty-title",
                        f"{url} has no <title>",
                        "Set the <title>.")
    return rep


def main() -> int:
    p = argparse.ArgumentParser(description="Cross: demo URL")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rep = audit(Path(args.project_dir).resolve())
    print(rep.to_json() if args.json else rep.to_markdown())
    return rep.exit_code


if __name__ == "__main__":
    sys.exit(main())
