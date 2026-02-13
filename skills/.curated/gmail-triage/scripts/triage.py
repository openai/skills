#!/usr/bin/env python3
"""Read-only Gmail triage helper for Codex."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import imaplib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email import message_from_bytes
from email.header import decode_header
from email.message import Message
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Sequence


DEFAULT_IMAP_HOST = "imap.gmail.com"
DEFAULT_IMAP_PORT = 993
MAX_PREVIEW_CHARS = 220

URGENT_PATTERNS: Sequence[str] = (
    r"\burgent\b",
    r"asap",
    r"reply by",
    r"action required",
    r"response needed",
    r"important",
    r"deadline",
    r"verify\s+now",
    r"payment\s+overdue",
    r"billing issue",
    r"suspicious",
)

REPLY_PATTERNS: Sequence[str] = (
    r"\breply\b",
    r"\bconfirm\b",
    r"\bapprove\b",
    r"\bschedule\b",
    r"\brequire\b",
)

NOISE_PATTERNS: Sequence[str] = (
    r"\bno[- ]?reply\b",
    r"\bnewsletter\b",
    r"\bunsubscribe\b",
)


@dataclass
class TriageItem:
    uid: str
    subject: str
    sender: str
    sender_email: str
    date: str
    age: str
    snippet: str
    score: int
    priority: str
    action_hint: str
    raw_date: datetime | None


def load_env_file() -> None:
    path = Path.home() / ".config" / "env" / "global.env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and value and key.strip() not in os.environ:
            os.environ[key.strip()] = value.strip()


def decode_header_value(value: str | None) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    return " ".join(
        part.decode(charset or "utf-8", errors="replace") if isinstance(part, bytes) else str(part)
        for part, charset in parts
    ).strip()


def parse_subject(msg: Message) -> str:
    return decode_header_value(msg.get("Subject", ""))


def parse_sender(msg: Message) -> tuple[str, str]:
    raw_sender = decode_header_value(msg.get("From", ""))
    name, email = parseaddr(raw_sender)
    sender_name = name or raw_sender
    sender_email = email or raw_sender
    return sender_name, sender_email


def parse_date(msg: Message) -> datetime | None:
    raw_date = msg.get("Date")
    if not raw_date:
        return None
    try:
        return parsedate_to_datetime(raw_date)
    except Exception:
        return None


def body_text(msg: Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if isinstance(payload, (bytes, bytearray)):
                    return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if isinstance(payload, (bytes, bytearray)):
            return payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
    return ""


def snippet(text: str, max_len: int = MAX_PREVIEW_CHARS) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return "(no preview)"
    return compact[:max_len] + ("..." if len(compact) > max_len else "")


def compute_score(text: str, keywords: Sequence[str]) -> int:
    lower = text.lower()
    score = 0
    for pattern in URGENT_PATTERNS:
        if re.search(pattern, lower):
            score += 3
    for pattern in REPLY_PATTERNS:
        if re.search(pattern, lower):
            score += 1
    for keyword in keywords:
        if keyword and keyword in lower:
            score += 2
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, lower):
            score -= 1
    return score


def priority_from_score(score: int) -> str:
    if score >= 6:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def action_hint(text: str, score: int) -> str:
    if score >= 6:
        return "Reply today"
    if score >= 3:
        return "Review soon"
    if "invoice" in text or "receipt" in text:
        return "Handle billing"
    return "Read when convenient"


def format_age(when: datetime | None) -> str:
    if not when:
        return "unknown"
    now = datetime.now(timezone.utc)
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    age = now - when
    hours = int(age.total_seconds() // 3600)
    if hours < 1:
        return "< 1h"
    if hours < 24:
        return f"{hours}h"
    days = hours // 24
    if days < 7:
        return f"{days}d"
    return f"{days // 7}w"


def parse_since_days(raw: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=max(raw, 0))).strftime("%d-%b-%Y")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only Gmail triage")
    parser.add_argument("--username", default=os.environ.get("GMAIL_USERNAME"), help="Gmail address")
    parser.add_argument(
        "--password",
        default=os.environ.get("GMAIL_APP_PASSWORD"),
        help="Gmail app password (2SV required)",
    )
    parser.add_argument("--server", default=os.environ.get("GMAIL_IMAP_SERVER", DEFAULT_IMAP_HOST))
    parser.add_argument("--port", type=int, default=int(os.environ.get("GMAIL_IMAP_PORT", DEFAULT_IMAP_PORT)))
    parser.add_argument("--mailbox", default="INBOX", help="Mailbox name")
    parser.add_argument("--max", type=int, default=40, help="Max items to output")
    parser.add_argument("--since-days", type=int, default=1, help="Lookback window in days")
    parser.add_argument("--query", default="", help='Extra IMAP query terms, e.g. "FROM billing"')
    parser.add_argument("--include-read", action="store_true", help="Include read messages")
    parser.add_argument("--keywords", default="", help="Comma-separated boost keywords")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--mark-read", action="store_true", help="Mark returned emails as read")
    return parser.parse_args()


def require_credentials(username: str | None, password: str | None) -> tuple[str, str]:
    if not username or not password:
        raise SystemExit(
            "Missing GMAIL_USERNAME or GMAIL_APP_PASSWORD. Set them in env or pass --username/--password."
        )
    return username, password


def build_search_terms(args: argparse.Namespace) -> list[str]:
    terms: list[str] = []
    if not args.include_read:
        terms.append("UNSEEN")
    terms.extend(["SINCE", parse_since_days(args.since_days)])
    if args.query:
        terms.extend(args.query.split())
    return terms


def format_markdown(items: List[TriageItem]) -> str:
    lines = [
        "# Gmail triage",
        "",
        f"- Items: {len(items)}",
        "",
        "| priority | score | age | from | subject | action | snippet |",
        "| --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        subject = item.subject.replace("|", "\\|")
        sender = f"{item.sender} <{item.sender_email}>".replace("|", "\\|")
        snippet_escaped = item.snippet.replace("|", "\\|")
        lines.append(
            f"| {item.priority} | {item.score} | {item.age} | {sender} | {subject or '(no subject)'} "
            f"| {item.action_hint} | {snippet_escaped} |"
        )
    return "\n".join(lines)


def format_json(items: List[TriageItem]) -> str:
    payload: Dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(items),
        "items": [
            {
                "uid": item.uid,
                "priority": item.priority,
                "score": item.score,
                "age": item.age,
                "from": item.sender,
                "from_email": item.sender_email,
                "subject": item.subject,
                "date": item.date,
                "action_hint": item.action_hint,
                "snippet": item.snippet,
            }
            for item in items
        ],
    }
    return json.dumps(payload, indent=2)


def rank(items: List[TriageItem], max_items: int) -> List[TriageItem]:
    return sorted(
        items,
        key=lambda item: (item.score, item.raw_date or datetime.min.replace(tzinfo=timezone.utc)),
        reverse=True,
    )[:max_items]


def main() -> int:
    load_env_file()
    args = parse_args()
    username, password = require_credentials(args.username, args.password)
    keywords = [k.strip().lower() for k in args.keywords.split(",") if k.strip()]

    try:
        conn = imaplib.IMAP4_SSL(args.server, args.port)
        conn.login(username, password)
        status, _ = conn.select(args.mailbox)
        if status != "OK":
            raise RuntimeError(f"Cannot open mailbox {args.mailbox}")

        status, ids_data = conn.search(None, *build_search_terms(args))
        if status != "OK":
            raise RuntimeError("IMAP search failed")

        ids = ids_data[0].split()
        if not ids:
            print("No messages matched your triage filters.")
            return 0

        items: List[TriageItem] = []
        sample_ids = ids[-(args.max * 2):]
        for raw_uid in sample_ids:
            status, payload = conn.fetch(raw_uid, "(RFC822)")
            if status != "OK":
                continue
            data = next((part for part in payload if isinstance(part, tuple) and part[1]), None)
            if not data:
                continue

            msg = message_from_bytes(data[1])
            msg_subject = parse_subject(msg)
            sender_name, sender_email = parse_sender(msg)
            when = parse_date(msg)
            msg_snippet = snippet(body_text(msg))

            text = f"{msg_subject} {sender_name} {sender_email} {msg_snippet}".lower()
            item_score = compute_score(text, keywords)

            items.append(
                TriageItem(
                    uid=raw_uid.decode(),
                    subject=msg_subject,
                    sender=sender_name or sender_email,
                    sender_email=sender_email,
                    date=msg.get("Date", ""),
                    age=format_age(when),
                    snippet=msg_snippet,
                    score=item_score,
                    priority=priority_from_score(item_score),
                    action_hint=action_hint(text, item_score),
                    raw_date=when,
                )
            )

        ranked = rank(items, args.max)
        if args.format == "json":
            print(format_json(ranked))
        else:
            print(format_markdown(ranked))

        if args.mark_read and ranked:
            conn.store(",".join(item.uid for item in ranked), "+FLAGS", "\\Seen")

        conn.logout()
        return 0
    except imaplib.IMAP4.error as exc:
        print(f"IMAP error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Gmail triage failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
