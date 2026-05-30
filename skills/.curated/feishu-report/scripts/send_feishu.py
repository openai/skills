#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env(path):
    config = {}
    if not path.exists():
        return config

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip().strip('"').strip("'")
    return config


def mask_webhook(url):
    if len(url) <= 12:
        return "***"
    return f"{url[:32]}...{url[-6:]}"


def build_message(title, text, keyword):
    parts = [part.strip() for part in (title, text) if part and part.strip()]
    if not parts:
        raise ValueError("Provide --text or --file")

    message = "\n\n".join(parts)
    if keyword and keyword not in message:
        message = f"{keyword}\n\n{message}"
    return message


def send_text(webhook, message):
    payload = {
        "msg_type": "text",
        "content": {
            "text": message,
        },
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read().decode("utf-8", "replace")
        return response.status, body


def is_success(response_body):
    try:
        payload = json.loads(response_body)
    except json.JSONDecodeError:
        return False, response_body

    ok = payload.get("code") == 0 or payload.get("StatusCode") == 0
    return ok, payload


def main():
    parser = argparse.ArgumentParser(description="Send a text report to Feishu.")
    parser.add_argument("--title", default="", help="Report title.")
    parser.add_argument("--text", default="", help="Report body text.")
    parser.add_argument("--file", help="Read report body from a UTF-8 text file.")
    parser.add_argument("--webhook", help="Override FEISHU_WEBHOOK_URL.")
    parser.add_argument("--keyword", help="Override FEISHU_KEYWORD.")
    args = parser.parse_args()

    config = load_env(ENV_PATH)
    webhook = args.webhook or os.getenv("FEISHU_WEBHOOK_URL") or config.get("FEISHU_WEBHOOK_URL")
    keyword = args.keyword or os.getenv("FEISHU_KEYWORD") or config.get("FEISHU_KEYWORD") or ""

    if not webhook:
        print("FEISHU_WEBHOOK_URL is not configured", file=sys.stderr)
        return 2

    try:
        text = args.text
        if args.file:
            text = Path(args.file).read_text(encoding="utf-8")
        message = build_message(args.title, text, keyword)
        status, body = send_text(webhook, message)
        ok, parsed = is_success(body)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        print(json.dumps({
            "ok": False,
            "http_status": error.code,
            "webhook": mask_webhook(webhook),
            "response": body,
        }, ensure_ascii=False))
        return 1
    except Exception as error:
        print(json.dumps({
            "ok": False,
            "webhook": mask_webhook(webhook),
            "error": str(error),
        }, ensure_ascii=False))
        return 1

    print(json.dumps({
        "ok": ok,
        "http_status": status,
        "webhook": mask_webhook(webhook),
        "response": parsed,
    }, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
