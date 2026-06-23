#!/usr/bin/env python3

"""Telegram triage skill.

Read-only CLI utility that summarizes unread/high-priority Telegram threads from a
locally stored session and supports keyword/match-based prioritization.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from getpass import getpass
from pathlib import Path
from typing import Iterable, List, Optional

try:
    from telethon import TelegramClient, errors
    from telethon.tl.types import Message
    from telethon.utils import get_display_name
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pip install -r requirements.txt (telethon is required)."
    ) from exc


MAX_SNIPPET_LEN = 160
DEFAULT_CHAT_LIMIT = 40
DEFAULT_MESSAGE_LIMIT = 12
DEFAULT_MAX_RESULTS = 20


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only Telegram triage for local sessions."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    login = subparsers.add_parser("login", help="Create or refresh a local Telegram session.")
    login.add_argument("--session-file", default=os.getenv("TELEGRAM_SESSION_FILE"))
    login.add_argument("--api-id", default=os.getenv("TELEGRAM_API_ID"))
    login.add_argument("--api-hash", default=os.getenv("TELEGRAM_API_HASH"))
    login.add_argument("--phone", default=os.getenv("TELEGRAM_PHONE"))
    login.add_argument("--force", action="store_true", help="Re-authorize even if session exists.")

    triage = subparsers.add_parser(
        "triage", help="Summarize unread/priority Telegram messages."
    )
    triage.add_argument("--session-file", default=os.getenv("TELEGRAM_SESSION_FILE"))
    triage.add_argument("--api-id", default=os.getenv("TELEGRAM_API_ID"))
    triage.add_argument("--api-hash", default=os.getenv("TELEGRAM_API_HASH"))
    triage.add_argument("--chat-limit", type=int, default=DEFAULT_CHAT_LIMIT)
    triage.add_argument("--message-limit", type=int, default=DEFAULT_MESSAGE_LIMIT)
    triage.add_argument(
        "--since",
        default=None,
        help="ISO time or duration: 30m, 2h, 1d, 3w. Defaults to 72h.",
    )
    triage.add_argument(
        "--keywords",
        default="",
        help="Comma-separated keywords to boost message priority.",
    )
    triage.add_argument(
        "--include-read", action="store_true", help="Include read chats when keyword matched."
    )
    triage.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS)
    triage.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON only.",
    )
    triage.set_defaults(json=False)

    return parser.parse_args()


def parse_since(raw: Optional[str]) -> datetime:
    now = datetime.now(timezone.utc)
    if not raw:
        return now - timedelta(hours=72)

    match = re.fullmatch(r"(\d+)([smhdw])", raw.strip().lower())
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        if unit == "s":
            return now - timedelta(seconds=value)
        if unit == "m":
            return now - timedelta(minutes=value)
        if unit == "h":
            return now - timedelta(hours=value)
        if unit == "d":
            return now - timedelta(days=value)
        return now - timedelta(weeks=value)

    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit(
            "Invalid --since value. Use 30m, 2h, 1d, 3w, or ISO-8601."
        ) from exc
    return parsed.astimezone(timezone.utc)


def split_keywords(raw: str) -> List[str]:
    return [s.strip().lower() for s in raw.split(",") if s.strip()]


def snippet(text: Optional[str], max_len: int = MAX_SNIPPET_LEN) -> str:
    if not text:
        return ""
    compact = " ".join(text.split())
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 1].rstrip() + "…"


@dataclass
class CandidateMessage:
    chat_id: int
    chat_title: str
    when: str
    sender: str
    message_id: int
    text: str
    mentioned_me: bool
    keyword_hits: List[str]
    priority: int
    unread_count: int
    unread_mentions: int

    @property
    def urgency(self) -> str:
        if self.mentioned_me:
            return "high"
        if self.priority >= 3 or self.keyword_hits:
            return "medium"
        return "low"


def priority_score(message: Message, keywords: Iterable[str], match_mentions: bool) -> List[str]:
    if message.message is None:
        return []
    lower = message.message.lower()
    hits: List[str] = []
    for k in keywords:
        if k and k in lower:
            hits.append(k)
    if match_mentions and message.mentioned:
        if "mentioned_you" not in hits:
            hits.append("mentioned_you")
    return hits


def load_env_file() -> None:
    env_path = Path.home() / ".config" / "env" / "global.env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key not in os.environ and value:
            os.environ[key.strip()] = value.strip()


def normalize_session_path(path_raw: Optional[str]) -> str:
    path = Path(path_raw or "~/.telegram-triage/session").expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


async def login_cmd(args: argparse.Namespace) -> None:
    load_env_file()
    session = normalize_session_path(args.session_file)
    api_id = args.api_id
    api_hash = args.api_hash
    phone = args.phone

    if not api_id or not api_hash:
        raise SystemExit(
            "Missing TELEGRAM_API_ID / TELEGRAM_API_HASH. Set env vars or pass --api-id/--api-hash."
        )
    if not phone and not args.force:
        phone = input("Phone (including country code, e.g. +15551234567): ").strip()
    if not phone:
        raise SystemExit("Phone number is required for login.")

    try:
        api_id_int = int(api_id)
    except ValueError as exc:
        raise SystemExit("TELEGRAM_API_ID must be an integer.") from exc

    client = TelegramClient(session, api_id_int, api_hash)
    if args.force and Path(session).exists():
        Path(session).unlink(missing_ok=True)

    try:
        await client.start(
            phone=lambda: phone,
            code_callback=lambda: input("Telegram login code: ").strip(),
            password=lambda: getpass("Telegram two-step password (if set): "),
        )
        me = await client.get_me()
        print(f"Login complete for {get_display_name(me)}")
        print(f"Session written to: {session}.session")
    except (errors.RPCError, ValueError) as exc:
        raise SystemExit(f"Login failed: {exc}") from exc
    finally:
        await client.disconnect()


async def triage_cmd(args: argparse.Namespace) -> None:
    load_env_file()
    session = normalize_session_path(args.session_file)
    api_id = args.api_id
    api_hash = args.api_hash
    if not Path(session).with_suffix(".session").exists():
        raise SystemExit(
            f"No session file found at {session}.session. Run login first."
        )
    if not api_id or not api_hash:
        raise SystemExit(
            "Missing TELEGRAM_API_ID / TELEGRAM_API_HASH. Set env vars or pass --api-id/--api-hash."
        )

    try:
        api_id_int = int(api_id)
    except ValueError as exc:
        raise SystemExit("TELEGRAM_API_ID must be an integer.") from exc

    client = TelegramClient(session, api_id_int, api_hash)
    try:
        await client.start()
        if not await client.is_user_authorized():
            raise SystemExit(f"Session at {session} is not authorized. Run login again.")

        cutoff = parse_since(args.since)
        keywords = split_keywords(args.keywords)
        dialogs = await client.get_dialogs(limit=args.chat_limit)
        candidates: List[CandidateMessage] = []

        for dialog in dialogs:
            unread_count = int(getattr(dialog, "unread_count", 0) or 0)
            unread_mentions = int(getattr(dialog, "unread_mentions_count", 0) or 0)
            title = dialog.name or "Unknown chat"
            include_read = args.include_read
            if not include_read and unread_count == 0 and unread_mentions == 0 and not keywords:
                continue

            messages = await client.get_messages(dialog.entity, limit=args.message_limit)
            for msg in messages:
                if msg.date is None or msg.date.replace(tzinfo=timezone.utc) < cutoff:
                    continue
                if msg.out:
                    continue
                hits = priority_score(
                    msg,
                    keywords,
                    unread_mentions > 0 or getattr(msg, "mentioned", False),
                )
                if not hits and not unread_count and not unread_mentions and not include_read:
                    continue

                sender = get_display_name(await msg.get_sender()) if msg.sender else "Unknown"
                candidate = CandidateMessage(
                    chat_id=int(dialog.id),
                    chat_title=title,
                    when=msg.date.isoformat(),
                    sender=sender,
                    message_id=msg.id,
                    text=snippet(msg.message),
                    mentioned_me=bool(msg.mentioned),
                    keyword_hits=hits,
                    priority=(3 if msg.mentioned else 0) + (2 if unread_mentions else 0) + len(hits),
                    unread_count=unread_count,
                    unread_mentions=unread_mentions,
                )
                candidates.append(candidate)

        urgency_rank = {"high": 3, "medium": 2, "low": 1}
        candidates.sort(
            key=lambda m: (urgency_rank[m.urgency], m.priority, m.when),
            reverse=True,
        )
        if args.max_results > 0:
            candidates = candidates[: args.max_results]

        if args.json:
            print(json.dumps([asdict(c) for c in candidates], indent=2))
            return

        if not candidates:
            print("No candidate messages found for triage window.")
            return

        counts = {"high": 0, "medium": 0, "low": 0}
        for c in candidates:
            counts[c.urgency] += 1

        print("# Telegram triage")
        print(f"Window: since {cutoff.isoformat()}")
        print(f"Total candidates: {len(candidates)} (high={counts['high']} medium={counts['medium']} low={counts['low']})")
        print("")

        for item in candidates:
            urgency_tag = f"[{item.urgency.upper()}]"
            print(f"{urgency_tag} {item.chat_title}")
            print(
                f"  • {item.sender} at {item.when}"
                f" | unread={item.unread_count} mentions={item.unread_mentions}"
            )
            if item.keyword_hits:
                print(f"  • matches: {', '.join(item.keyword_hits)}")
            print(f"  • {item.text}")
            print(f"  • message id: {item.message_id}")
            print("")
    finally:
        await client.disconnect()


async def main() -> None:
    args = parse_args()
    if args.command == "login":
        await login_cmd(args)
    elif args.command == "triage":
        await triage_cmd(args)
    else:
        raise SystemExit("Unknown command.")


if __name__ == "__main__":
    asyncio.run(main())
