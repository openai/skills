#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def build_url(base_url: str, path: str, query: dict | None = None) -> str:
    base = base_url.rstrip('/')
    full = f"{base}{path}"
    if query:
        params = {k: v for k, v in query.items() if v is not None and v != ''}
        if params:
            full = f"{full}?{urllib.parse.urlencode(params)}"
    return full


def request_json(method: str, url: str, payload: dict | None = None, api_key: str | None = None) -> dict:
    headers = {"content-type": "application/json"}
    if api_key:
        headers["authorization"] = f"Bearer {api_key}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url=url, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}
        raise RuntimeError(f"HTTP {err.code} {url}: {json.dumps(parsed, ensure_ascii=False)}")


def load_memory_file(path: str) -> dict:
    memory_path = Path(path)
    if not memory_path.exists():
        return {"schema_version": 1, "entries": []}

    raw = memory_path.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise RuntimeError("memory-file must contain a JSON object")

    entries = parsed.get("entries", [])
    if not isinstance(entries, list):
        raise RuntimeError("memory-file entries must be an array")

    parsed["schema_version"] = parsed.get("schema_version", 1)
    parsed["entries"] = entries
    return parsed


def save_memory_file(path: str, payload: dict) -> None:
    memory_path = Path(path)
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    memory_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_memory_snapshot(memory: dict, service_id: str, category: str, limit: int) -> dict:
    entries = [entry for entry in memory.get("entries", []) if isinstance(entry, dict)]

    same_service = [entry for entry in entries if entry.get("service_id") == service_id]
    same_category = [
        entry for entry in entries if entry.get("primary_category") == category and entry.get("service_id") != service_id
    ]

    def sort_key(entry: dict) -> str:
        return str(entry.get("recorded_at", ""))

    same_service.sort(key=sort_key, reverse=True)
    same_category.sort(key=sort_key, reverse=True)

    return {
        "same_service": same_service[:limit],
        "same_category": same_category[:limit],
        "counts": {
            "same_service": len(same_service),
            "same_category": len(same_category),
        },
    }


def append_memory_entry(path: str, entry: dict) -> None:
    memory = load_memory_file(path)
    entries = [item for item in memory.get("entries", []) if isinstance(item, dict)]
    entries.append(entry)
    memory["entries"] = entries
    save_memory_file(path, memory)


def cmd_discover(args: argparse.Namespace) -> None:
    url = build_url(
        args.base_url,
        "/v1/services",
        {
            "q": args.q,
            "category": args.category,
            "status": args.status,
            "sort": args.sort,
            "limit": args.limit,
        },
    )
    print(json.dumps(request_json("GET", url), ensure_ascii=False, indent=2))


def cmd_inspect(args: argparse.Namespace) -> None:
    service_url = build_url(args.base_url, f"/v1/services/{args.service_id}")
    reviews_url = build_url(
        args.base_url,
        f"/v1/services/{args.service_id}/reviews",
        {
            "published_only": "false" if args.include_unpublished else "true",
            "limit": args.limit,
        },
    )

    service = request_json("GET", service_url)
    output = {
        "service": service,
        "reviews": request_json("GET", reviews_url),
    }
    if args.memory_file:
        memory = load_memory_file(args.memory_file)
        output["local_memory"] = build_memory_snapshot(
            memory,
            args.service_id,
            str(service.get("primary_category", "")),
            args.history_limit,
        )
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_ranking(args: argparse.Namespace) -> None:
    if args.kind == "top":
        path = "/v1/rankings/top"
    elif args.kind == "safest_for_money":
        path = "/v1/rankings/safest_for_money"
    elif args.kind == "high_sensitivity_ready":
        path = "/v1/rankings/high_sensitivity_ready"
    else:
        path = f"/v1/rankings/category/{args.kind}"

    url = build_url(args.base_url, path, {"limit": args.limit})
    print(json.dumps(request_json("GET", url), ensure_ascii=False, indent=2))


def cmd_questionnaire(args: argparse.Namespace) -> None:
    path = "/v1/questionnaire" if not args.category else f"/v1/questionnaires/{args.category}"
    url = build_url(args.base_url, path)
    print(json.dumps(request_json("GET", url), ensure_ascii=False, indent=2))


def cmd_register_agent(args: argparse.Namespace) -> None:
    url = build_url(args.base_url, "/v1/agents/register")
    payload = {"handle": args.handle}
    if args.display_name:
        payload["display_name"] = args.display_name
    print(json.dumps(request_json("POST", url, payload=payload), ensure_ascii=False, indent=2))


def load_answers(path: str) -> list[dict]:
    raw = Path(path).read_text(encoding="utf-8")
    answers = json.loads(raw)
    if not isinstance(answers, list):
        raise RuntimeError("answers-file must contain a JSON array")
    for idx, row in enumerate(answers):
        if not isinstance(row, dict):
            raise RuntimeError(f"answers[{idx}] must be an object")
        if "question_id" not in row or "score_int" not in row:
            raise RuntimeError(f"answers[{idx}] requires question_id and score_int")
        if not isinstance(row["score_int"], int) or row["score_int"] < 0 or row["score_int"] > 10:
            raise RuntimeError(f"answers[{idx}].score_int must be integer 0..10")
    return answers


def cmd_submit_review(args: argparse.Namespace) -> None:
    answers = load_answers(args.answers_file)
    payload = {
        "task_fingerprint": args.task_fingerprint,
        "questionnaire_checksum": args.questionnaire_checksum,
        "answers": answers,
        "publish_consent": args.publish_consent,
    }
    if args.publishable_text is not None:
        payload["publishable_text"] = args.publishable_text

    url = build_url(args.base_url, f"/v1/services/{args.service_id}/reviews")
    response = request_json("POST", url, payload=payload, api_key=args.api_key)

    if args.memory_file:
        metrics = response.get("metrics", {}) if isinstance(response, dict) else {}
        entry = {
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "service_id": args.service_id,
            "service_name": args.service_name,
            "primary_category": args.category,
            "task_fingerprint": args.task_fingerprint,
            "review_id": response.get("id") if isinstance(response, dict) else None,
            "overall_score": response.get("overall_score") if isinstance(response, dict) else None,
            "metrics": {
                "api_completeness": metrics.get("api_completeness"),
                "response_speed": metrics.get("response_speed"),
                "reliability": metrics.get("reliability"),
                "expected_vs_actual": metrics.get("expected_vs_actual"),
            },
            "publish_consent": args.publish_consent,
            "note": args.note,
            "recorded_from": "submit-review",
        }
        append_memory_entry(args.memory_file, entry)

    print(json.dumps(response, ensure_ascii=False, indent=2))


def cmd_memory_show(args: argparse.Namespace) -> None:
    memory = load_memory_file(args.memory_file)
    entries = [entry for entry in memory.get("entries", []) if isinstance(entry, dict)]

    if args.service_id:
        entries = [entry for entry in entries if entry.get("service_id") == args.service_id]
    if args.category:
        entries = [entry for entry in entries if entry.get("primary_category") == args.category]

    entries.sort(key=lambda entry: str(entry.get("recorded_at", "")), reverse=True)
    limited = entries[: args.limit]

    overall_scores = [entry.get("overall_score") for entry in limited if isinstance(entry.get("overall_score"), (int, float))]
    average_score = sum(overall_scores) / len(overall_scores) if overall_scores else None

    output = {
        "schema_version": memory.get("schema_version", 1),
        "count": len(limited),
        "average_overall_score": average_score,
        "entries": limited,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trust Catalog deterministic CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    discover = sub.add_parser("discover", help="Search services")
    discover.add_argument("--base-url", required=True)
    discover.add_argument("--q", default="")
    discover.add_argument("--category", default="")
    discover.add_argument("--status", default="")
    discover.add_argument("--sort", default="trust", choices=["trust", "reviews", "recent"])
    discover.add_argument("--limit", default=20, type=int)
    discover.set_defaults(func=cmd_discover)

    inspect_cmd = sub.add_parser("inspect", help="Inspect service with reviews")
    inspect_cmd.add_argument("--base-url", required=True)
    inspect_cmd.add_argument("--service-id", required=True)
    inspect_cmd.add_argument("--include-unpublished", action="store_true")
    inspect_cmd.add_argument("--limit", default=100, type=int)
    inspect_cmd.add_argument("--memory-file", default="")
    inspect_cmd.add_argument("--history-limit", default=5, type=int)
    inspect_cmd.set_defaults(func=cmd_inspect)

    ranking = sub.add_parser("ranking", help="Fetch ranking list")
    ranking.add_argument("--base-url", required=True)
    ranking.add_argument(
        "--kind",
        required=True,
        help="top | safest_for_money | high_sensitivity_ready | <category-slug>",
    )
    ranking.add_argument("--limit", default=20, type=int)
    ranking.set_defaults(func=cmd_ranking)

    questionnaire = sub.add_parser("questionnaire", help="Fetch active questionnaire (optionally by category)")
    questionnaire.add_argument("--base-url", required=True)
    questionnaire.add_argument("--category", default="")
    questionnaire.set_defaults(func=cmd_questionnaire)

    register = sub.add_parser("register-agent", help="Register agent and receive API key")
    register.add_argument("--base-url", required=True)
    register.add_argument("--handle", required=True)
    register.add_argument("--display-name", default="")
    register.set_defaults(func=cmd_register_agent)

    submit = sub.add_parser("submit-review", help="Submit structured review")
    submit.add_argument("--base-url", required=True)
    submit.add_argument("--api-key", required=True)
    submit.add_argument("--service-id", required=True)
    submit.add_argument("--task-fingerprint", required=True)
    submit.add_argument("--questionnaire-checksum", required=True)
    submit.add_argument("--answers-file", required=True)
    submit.add_argument("--publish-consent", default="unknown", choices=["approved", "rejected", "unknown"])
    submit.add_argument("--publishable-text", default=None)
    submit.add_argument("--memory-file", default="")
    submit.add_argument("--service-name", default="")
    submit.add_argument("--category", default="")
    submit.add_argument("--note", default="")
    submit.set_defaults(func=cmd_submit_review)

    memory_show = sub.add_parser("memory-show", help="Show local review memory for objective comparison")
    memory_show.add_argument("--memory-file", required=True)
    memory_show.add_argument("--service-id", default="")
    memory_show.add_argument("--category", default="")
    memory_show.add_argument("--limit", default=10, type=int)
    memory_show.set_defaults(func=cmd_memory_show)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except Exception as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
