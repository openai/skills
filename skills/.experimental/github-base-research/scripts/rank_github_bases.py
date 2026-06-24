#!/usr/bin/env python3
"""Rank GitHub repositories and propose a single-base or multi-repo foundation."""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ALIAS_MAP = {
    "auth": "authentication",
    "authentication": "authentication",
    "oauth": "authentication",
    "login": "authentication",
    "rbac": "authorization",
    "authorization": "authorization",
    "acl": "authorization",
    "permission": "authorization",
    "payment": "billing",
    "payments": "billing",
    "stripe": "billing",
    "billing": "billing",
    "subscription": "billing",
    "audit": "audit-log",
    "auditlog": "audit-log",
    "audit-log": "audit-log",
    "telemetry": "observability",
    "metrics": "observability",
    "observability": "observability",
    "queue": "messaging",
    "messaging": "messaging",
    "search": "search",
    "vector": "search",
    "websocket": "realtime",
    "realtime": "realtime",
    "admin": "admin-ui",
    "dashboard": "admin-ui",
    "admin-ui": "admin-ui",
    "api": "api",
    "rest": "api",
    "graphql": "api",
}
KNOWN_CAPABILITIES = set(ALIAS_MAP.values())


@dataclass
class RepoScore:
    repo: dict
    score: float
    capability_coverage: float
    matched_capabilities: list[str]
    capabilities: set[str]
    score_breakdown: dict[str, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank GitHub repositories for base-project selection."
    )
    parser.add_argument("--input", required=True, help="JSON file with repository objects.")
    parser.add_argument(
        "--required-capabilities",
        default="",
        help="Comma-separated required capabilities (e.g. auth,billing,rbac).",
    )
    parser.add_argument(
        "--preferred-language",
        default="",
        help="Preferred implementation language (e.g. TypeScript).",
    )
    parser.add_argument("--top", type=int, default=10, help="Number of ranked repos to show.")
    parser.add_argument(
        "--combo-max",
        type=int,
        default=3,
        help="Maximum repositories in multi-repo recommendation.",
    )
    parser.add_argument(
        "--emit-markdown",
        default="",
        help="Optional path to write a markdown report.",
    )
    parser.add_argument(
        "--emit-json",
        default="",
        help="Optional path to write structured output JSON.",
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=50,
        help="Hard-gate minimum star threshold (default: 50).",
    )
    parser.add_argument(
        "--max-inactive-days",
        type=int,
        default=730,
        help="Hard-gate max days since push (default: 730).",
    )
    parser.add_argument(
        "--require-license",
        action="store_true",
        help="Hard-gate repositories without SPDX license metadata.",
    )
    parser.add_argument(
        "--no-hard-gate",
        action="store_true",
        help="Disable hard-gate filtering before scoring.",
    )
    return parser.parse_args()


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def canonicalize(token: str) -> str:
    t = token.strip().lower()
    if not t:
        return ""
    return ALIAS_MAP.get(t, t)


def normalize_text(value: object, max_len: int = 800) -> str:
    if not isinstance(value, str):
        return ""
    sanitized = value.replace("\x00", " ").strip()
    return sanitized[:max_len]


def tokenize_text(value: str) -> Iterable[str]:
    return re.findall(r"[a-z0-9][a-z0-9.+-]*", value.lower())


def extract_capabilities(repo: dict) -> set[str]:
    caps: set[str] = set()

    topics = repo.get("topics") or []
    if isinstance(topics, list):
        for topic in topics:
            if isinstance(topic, str):
                canonical = canonicalize(topic)
                if canonical:
                    caps.add(canonical)

    repo_caps = repo.get("capabilities") or []
    if isinstance(repo_caps, list):
        for capability in repo_caps:
            if isinstance(capability, str):
                canonical = canonicalize(capability)
                if canonical:
                    caps.add(canonical)

    text_fields = [
        normalize_text(repo.get("name")),
        normalize_text(repo.get("full_name")),
        normalize_text(repo.get("description"), max_len=1000),
    ]
    for field in text_fields:
        if field:
            for token in tokenize_text(field):
                canonical = canonicalize(token)
                if canonical and canonical in KNOWN_CAPABILITIES:
                    caps.add(canonical)

    return caps


def to_repo_list(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        items = payload.get("items")
        if isinstance(items, list):
            return [x for x in items if isinstance(x, dict)]
    return []


def activity_score(repo: dict) -> float:
    age_days = activity_age_days(repo)
    if age_days is None:
        return 0.15
    if age_days <= 14:
        return 1.0
    if age_days <= 45:
        return 0.9
    if age_days <= 90:
        return 0.75
    if age_days <= 180:
        return 0.55
    if age_days <= 365:
        return 0.35
    if age_days <= 730:
        return 0.2
    return 0.05


def activity_age_days(repo: dict) -> int | None:
    pushed = parse_iso(repo.get("pushed_at") or repo.get("pushedAt"))
    if not pushed:
        return None
    return max((datetime.now(timezone.utc) - pushed).days, 0)


def popularity_score(repo: dict) -> tuple[float, float, float]:
    stars = float(repo.get("stargazers_count") or repo.get("stargazersCount") or 0)
    forks = float(repo.get("forks_count") or repo.get("forksCount") or 0)
    watchers = float(
        repo.get("subscribers_count")
        or repo.get("watchers_count")
        or repo.get("watchersCount")
        or 0
    )
    stars_n = clamp(math.log10(stars + 1) / 5.0)
    forks_n = clamp(math.log10(forks + 1) / 4.5)
    watchers_n = clamp(math.log10(watchers + 1) / 3.5) if watchers > 0 else 0.2
    return stars_n, forks_n, watchers_n


def maintenance_score(repo: dict) -> float:
    open_issues = float(repo.get("open_issues_count") or repo.get("openIssuesCount") or 0)
    issue_health = 1.0 - clamp(open_issues / 300.0)

    license_data = repo.get("license")
    has_license = isinstance(license_data, dict) and bool(license_data.get("spdx_id"))
    license_n = 1.0 if has_license else 0.2

    archived = bool(repo.get("archived") or repo.get("isArchived"))
    disabled = bool(repo.get("disabled"))
    status_n = 0.0 if (archived or disabled) else 1.0

    has_issues = repo.get("has_issues")
    has_wiki = repo.get("has_wiki")
    tooling_n = 0.5 + (0.25 if has_issues else 0.0) + (0.25 if has_wiki else 0.0)

    return clamp(0.35 * issue_health + 0.25 * license_n + 0.3 * status_n + 0.1 * tooling_n)


def compatibility_score(
    repo: dict, required_capabilities: list[str], preferred_language: str
) -> tuple[float, float, list[str], set[str]]:
    capabilities = extract_capabilities(repo)
    required = set(required_capabilities)
    matched = sorted(required & capabilities)

    if required:
        coverage = len(matched) / max(len(required), 1)
    else:
        coverage = 0.6

    language = (repo.get("language") or "").strip().lower()
    preferred = preferred_language.strip().lower()
    if preferred:
        lang_match = 1.0 if language == preferred else 0.0
    else:
        lang_match = 0.5

    compatibility = clamp(0.8 * coverage + 0.2 * lang_match)
    return compatibility, coverage, matched, capabilities


def score_repo(repo: dict, required_capabilities: list[str], preferred_language: str) -> RepoScore:
    stars_n, forks_n, watchers_n = popularity_score(repo)
    activity_n = activity_score(repo)
    maintenance_n = maintenance_score(repo)
    compatibility_n, coverage, matched, capabilities = compatibility_score(
        repo, required_capabilities, preferred_language
    )

    total = (
        0.22 * stars_n
        + 0.08 * forks_n
        + 0.1 * watchers_n
        + 0.2 * activity_n
        + 0.18 * maintenance_n
        + 0.22 * compatibility_n
    )

    return RepoScore(
        repo=repo,
        score=round(total, 4),
        capability_coverage=round(coverage, 4),
        matched_capabilities=matched,
        capabilities=capabilities,
        score_breakdown={
            "stars": round(stars_n, 4),
            "forks": round(forks_n, 4),
            "watchers": round(watchers_n, 4),
            "activity": round(activity_n, 4),
            "maintenance": round(maintenance_n, 4),
            "compatibility": round(compatibility_n, 4),
        },
    )


def normalize_capability_list(value: str) -> list[str]:
    out = []
    for part in value.split(","):
        canonical = canonicalize(part)
        if canonical and canonical not in out:
            out.append(canonical)
    return out


def has_license(repo: dict) -> bool:
    license_data = repo.get("license")
    return isinstance(license_data, dict) and bool(license_data.get("spdx_id"))


def hard_gate(
    repo: dict, min_stars: int, max_inactive_days: int, require_license: bool
) -> tuple[bool, str]:
    archived = bool(repo.get("archived") or repo.get("isArchived"))
    disabled = bool(repo.get("disabled"))
    if archived or disabled:
        return False, "archived_or_disabled"

    stars = int(repo.get("stargazers_count") or repo.get("stargazersCount") or 0)
    if stars < min_stars:
        return False, "below_min_stars"

    age_days = activity_age_days(repo)
    if age_days is None:
        return False, "missing_activity"
    if age_days > max_inactive_days:
        return False, "stale_activity"

    if require_license and not has_license(repo):
        return False, "missing_license"

    return True, ""


def choose_combo(
    ranked: list[RepoScore], required_capabilities: list[str], combo_max: int
) -> tuple[list[RepoScore], set[str]]:
    required = set(required_capabilities)
    if not required:
        return [], set()

    uncovered = set(required)
    selected: list[RepoScore] = []
    pool = ranked[: min(len(ranked), 20)]

    while uncovered and len(selected) < combo_max:
        best: RepoScore | None = None
        best_gain = -1
        best_score = -1.0

        for candidate in pool:
            if candidate in selected:
                continue
            gain = len(candidate.capabilities & uncovered)
            if gain > best_gain or (gain == best_gain and candidate.score > best_score):
                best = candidate
                best_gain = gain
                best_score = candidate.score

        if not best or best_gain <= 0:
            break

        selected.append(best)
        uncovered -= best.capabilities

    covered = required - uncovered
    return selected, covered


def repo_id(repo: dict) -> str:
    return repo.get("full_name") or repo.get("fullName") or repo.get("name") or "unknown"


def to_output_payload(
    ranked: list[RepoScore],
    total_candidates: int,
    input_candidates: int,
    filtered_out_count: int,
    filter_reasons: dict[str, int],
    hard_gate_enabled: bool,
    required_capabilities: list[str],
    preferred_language: str,
    combo: list[RepoScore],
    combo_covered: set[str],
) -> dict:
    top = ranked[:]
    single = top[0] if top else None
    single_coverage = single.capability_coverage if single else 0.0

    return {
        "summary": {
            "candidate_count": total_candidates,
            "input_candidate_count": input_candidates,
            "filtered_out_count": filtered_out_count,
            "hard_gate_enabled": hard_gate_enabled,
            "filter_reasons": filter_reasons,
            "required_capabilities": required_capabilities,
            "preferred_language": preferred_language,
            "single_base_recommended": bool(single),
            "single_base_coverage": single_coverage,
            "combo_recommended": bool(combo),
            "combo_coverage": (
                len(combo_covered) / len(required_capabilities) if required_capabilities else 0.0
            ),
        },
        "ranked": [
            {
                "repo": repo_id(item.repo),
                "url": item.repo.get("html_url") or item.repo.get("url"),
                "score": item.score,
                "coverage": item.capability_coverage,
                "matched_capabilities": item.matched_capabilities,
                "language": item.repo.get("language"),
                "stars": item.repo.get("stargazers_count", item.repo.get("stargazersCount", 0)),
                "forks": item.repo.get("forks_count", item.repo.get("forksCount", 0)),
                "updated_at": item.repo.get("updated_at", item.repo.get("updatedAt")),
                "score_breakdown": item.score_breakdown,
            }
            for item in top
        ],
        "single_base": (
            {
                "repo": repo_id(single.repo),
                "url": single.repo.get("html_url") or single.repo.get("url"),
                "score": single.score,
                "coverage": single.capability_coverage,
                "matched_capabilities": single.matched_capabilities,
            }
            if single
            else None
        ),
        "combo_base": [
            {
                "repo": repo_id(item.repo),
                "url": item.repo.get("html_url") or item.repo.get("url"),
                "score": item.score,
                "contributes_capabilities": sorted(
                    set(required_capabilities) & item.capabilities
                ),
            }
            for item in combo
        ],
    }


def render_markdown(payload: dict) -> str:
    summary = payload["summary"]
    ranked = payload["ranked"]
    single = payload["single_base"]
    combo = payload["combo_base"]
    required = summary["required_capabilities"]

    lines = ["# GitHub Base Research Report", ""]
    lines.append(
        f"- Candidate repositories scored: **{summary['candidate_count']}** "
        f"(from {summary['input_candidate_count']} collected)."
    )
    if summary["hard_gate_enabled"]:
        lines.append(f"- Hard-gate filtered out: **{summary['filtered_out_count']}**")
        reasons = summary.get("filter_reasons") or {}
        if reasons:
            reason_parts = [f"{k}={v}" for k, v in sorted(reasons.items())]
            lines.append(f"- Hard-gate reasons: **{', '.join(reason_parts)}**")
    lines.append(
        f"- Required capabilities: **{', '.join(required) if required else 'none provided'}**"
    )
    lines.append(
        f"- Preferred language: **{summary['preferred_language'] or 'none provided'}**"
    )
    lines.append("")

    lines.append("## Ranked Shortlist")
    lines.append("")
    lines.append("| Rank | Repository | Score | Coverage | Stars | Language |")
    lines.append("|---|---|---:|---:|---:|---|")
    for idx, item in enumerate(ranked[:10], start=1):
        repo_text = item["repo"]
        url = item["url"]
        linked = f"[{repo_text}]({url})" if url else repo_text
        cov = f"{item['coverage'] * 100:.0f}%"
        lines.append(
            f"| {idx} | {linked} | {item['score']:.3f} | {cov} | "
            f"{item['stars']} | {item['language'] or 'n/a'} |"
        )
    lines.append("")

    lines.append("## Recommendation")
    lines.append("")
    if single:
        lines.append(
            f"- Single-base pick: **[{single['repo']}]({single['url']})** "
            f"(score {single['score']:.3f}, coverage {single['coverage'] * 100:.0f}%)."
        )
        if single["matched_capabilities"]:
            lines.append(
                f"- Capabilities covered directly: **{', '.join(single['matched_capabilities'])}**."
            )
    else:
        lines.append("- Single-base pick: **none** (no viable candidates).")

    if combo:
        lines.append("- Multi-repo composition option:")
        for repo in combo:
            cap_text = ", ".join(repo["contributes_capabilities"]) or "general support"
            lines.append(
                f"  - **[{repo['repo']}]({repo['url']})** for {cap_text} "
                f"(score {repo['score']:.3f})."
            )
    else:
        lines.append("- Multi-repo composition option: **none required or insufficient coverage**.")

    lines.append("")
    lines.append("## Risks and Gaps")
    lines.append("")
    if required:
        top = ranked[0] if ranked else None
        unmatched = []
        if top:
            matched = set(top["matched_capabilities"])
            unmatched = [cap for cap in required if cap not in matched]
        if unmatched:
            lines.append(f"- Uncovered by top single-base repo: **{', '.join(unmatched)}**.")
        else:
            lines.append("- All required capabilities are covered by the top single-base repo.")
    else:
        lines.append("- Capability requirements were not provided; validate fit manually.")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    payload = json.loads(input_path.read_text())
    repos = to_repo_list(payload)
    if not repos:
        raise SystemExit("No repository objects found in input JSON.")

    required_capabilities = normalize_capability_list(args.required_capabilities)
    preferred_language = args.preferred_language.strip()

    working_repos = repos
    filtered_out_count = 0
    filter_reasons: dict[str, int] = {}
    hard_gate_enabled = not args.no_hard_gate

    if hard_gate_enabled:
        gated = []
        for repo in repos:
            allowed, reason = hard_gate(
                repo,
                min_stars=max(args.min_stars, 0),
                max_inactive_days=max(args.max_inactive_days, 1),
                require_license=args.require_license,
            )
            if allowed:
                gated.append(repo)
            else:
                filter_reasons[reason] = filter_reasons.get(reason, 0) + 1
        filtered_out_count = len(repos) - len(gated)
        working_repos = gated

        if not working_repos:
            raise SystemExit(
                "Hard-gate filtered all repos. Lower --min-stars, increase "
                "--max-inactive-days, or rerun with --no-hard-gate."
            )

    ranked_all = sorted(
        (score_repo(repo, required_capabilities, preferred_language) for repo in working_repos),
        key=lambda item: item.score,
        reverse=True,
    )
    ranked = ranked_all[: max(args.top, 1)]

    combo, covered = choose_combo(ranked_all, required_capabilities, max(args.combo_max, 1))
    output_payload = to_output_payload(
        ranked,
        len(ranked_all),
        len(repos),
        filtered_out_count,
        filter_reasons,
        hard_gate_enabled,
        required_capabilities,
        preferred_language,
        combo,
        covered,
    )

    if args.emit_json:
        out_path = Path(args.emit_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output_payload, indent=2) + "\n")

    markdown = render_markdown(output_payload)
    if args.emit_markdown:
        out_path = Path(args.emit_markdown)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown)

    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
