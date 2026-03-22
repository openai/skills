#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from dotenv import load_dotenv
from telethon import TelegramClient, functions, types, utils
from telethon.sessions import StringSession
from telethon.tl.custom import Dialog, Draft, Message


SESSION_ENV_KEYS = ("TELEGRAM_SESSION_STRING", "TELEGRAM_USER_SESSION")


class CLIError(RuntimeError):
    pass


class ConfigError(ValueError):
    pass


@dataclass(slots=True)
class AppConfig:
    api_id: int
    api_hash: str
    session_string: str | None
    env_file: Path | None
    timeout: float


ServiceFactory = Callable[[AppConfig], Any]


def find_default_env_file(start_dir: str | Path | None = None) -> Path | None:
    current = Path(start_dir or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        env_file = candidate / ".env"
        if env_file.exists():
            return env_file
    return None


def load_runtime_env(env_file: str | None = None) -> Path | None:
    resolved = Path(env_file).expanduser().resolve() if env_file else find_default_env_file()
    if resolved and resolved.exists():
        load_dotenv(resolved, override=False)
        return resolved
    return None


def resolve_session_string(env: dict[str, str | None] | None = None) -> str | None:
    env_map = env or os.environ
    for key in SESSION_ENV_KEYS:
        value = str(env_map.get(key) or "").strip()
        if value:
            return value
    return None


def build_config(
    env_file: str | None,
    timeout: float,
    *,
    require_session: bool = True,
    env: dict[str, str | None] | None = None,
) -> "AppConfig":
    loaded_env_file = load_runtime_env(env_file)
    env_map = env or os.environ

    api_id_raw = str(env_map.get("TELEGRAM_API_ID") or "").strip()
    api_hash = str(env_map.get("TELEGRAM_API_HASH") or "").strip()
    session_string = resolve_session_string(env_map)

    try:
        api_id = int(api_id_raw)
    except ValueError as error:
        raise ConfigError("TELEGRAM_API_ID must be a positive integer") from error

    if api_id <= 0:
        raise ConfigError("TELEGRAM_API_ID must be a positive integer")
    if not api_hash:
        raise ConfigError("TELEGRAM_API_HASH is required")
    if require_session and not session_string:
        raise ConfigError(
            "Telegram session is required. Set TELEGRAM_SESSION_STRING or TELEGRAM_USER_SESSION, "
            "or run `python scripts/tg.py auth login` first."
        )

    return AppConfig(
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
        env_file=loaded_env_file,
        timeout=timeout,
    )


def normalize_global_flags(argv: Sequence[str]) -> list[str]:
    args = list(argv)
    front: list[str] = []
    remainder: list[str] = []
    value_options = {"--env-file", "--output", "--timeout", "--log-level"}
    index = 0

    while index < len(args):
        token = args[index]
        if token == "--json":
            front.append(token)
            index += 1
            continue
        if token in value_options:
            if index + 1 >= len(args):
                front.append(token)
                break
            front.extend([token, args[index + 1]])
            index += 2
            continue
        remainder.append(token)
        index += 1

    return [*front, *remainder]


def _normalize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, bytes):
        return {"type": "bytes", "length": len(value)}
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_normalize(item) for item in value]
    return value


def render_json(payload: Any) -> str:
    return json.dumps(_normalize(payload), ensure_ascii=False, indent=2, sort_keys=True)


def render_pretty(payload: Any) -> str:
    normalized = _normalize(payload)
    if isinstance(normalized, list):
        if not normalized:
            return "(empty)"
        return "\n\n".join(_render_block(item) for item in normalized)
    return _render_block(normalized)


def _render_block(payload: Any) -> str:
    if isinstance(payload, dict):
        lines: list[str] = []
        for key, value in payload.items():
            if isinstance(value, list):
                if not value:
                    lines.append(f"{key}: []")
                elif all(not isinstance(item, dict) for item in value):
                    lines.append(f"{key}: {', '.join(str(item) for item in value)}")
                else:
                    lines.append(f"{key}:")
                    for item in value:
                        lines.append(f"  - {_render_inline(item)}")
            else:
                lines.append(f"{key}: {_render_inline(value)}")
        return "\n".join(lines)
    return _render_inline(payload)


def _render_inline(value: Any) -> str:
    if isinstance(value, dict):
        preferred = []
        for key in ("title", "display_name", "username", "id", "kind", "text", "path", "status"):
            if key in value and value[key] not in (None, ""):
                preferred.append(f"{key}={value[key]}")
        return ", ".join(preferred) if preferred else render_json(value)
    if isinstance(value, list):
        return ", ".join(_render_inline(item) for item in value)
    return str(value)


def parse_ref(value: str | int) -> str | int:
    raw = str(value).strip()
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def normalize_message_ids(ids: Sequence[int] | None) -> list[int]:
    return [int(item) for item in (ids or [])]


def isoformat_or_none(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.isoformat()
    return None


def entity_kind(entity: Any) -> str:
    if isinstance(entity, types.User):
        return "user"
    if isinstance(entity, types.Channel):
        if getattr(entity, "broadcast", False):
            return "channel"
        return "supergroup"
    if isinstance(entity, types.Chat):
        return "group"
    return type(entity).__name__


def entity_to_dict(entity: Any) -> dict[str, Any]:
    username = getattr(entity, "username", None)
    first_name = getattr(entity, "first_name", None)
    last_name = getattr(entity, "last_name", None)
    title = getattr(entity, "title", None)
    display_name = title or " ".join(part for part in (first_name, last_name) if part).strip() or username or ""
    return {
        "id": str(utils.get_peer_id(entity)),
        "kind": entity_kind(entity),
        "display_name": display_name,
        "title": title,
        "username": username,
        "phone": getattr(entity, "phone", None),
        "is_self": bool(getattr(entity, "is_self", False)),
        "is_bot": bool(getattr(entity, "bot", False)),
    }


def dialog_to_dict(dialog: Dialog) -> dict[str, Any]:
    entity = dialog.entity
    data = entity_to_dict(entity)
    data.update(
        {
            "name": dialog.name,
            "unread_count": dialog.unread_count,
            "archived": dialog.folder_id == 1,
            "folder_id": dialog.folder_id,
            "is_user": dialog.is_user,
            "is_group": dialog.is_group,
            "is_channel": dialog.is_channel,
            "last_message_id": getattr(dialog.message, "id", None),
            "last_message_date": isoformat_or_none(getattr(dialog.message, "date", None)),
        }
    )
    return data


def media_to_dict(media: Any) -> dict[str, Any] | None:
    if media is None:
        return None
    data = {
        "class": type(media).__name__,
        "has_photo": isinstance(media, types.MessageMediaPhoto),
        "has_document": isinstance(media, types.MessageMediaDocument),
    }
    document = getattr(media, "document", None)
    if document is not None:
        data["document_id"] = str(document.id)
        data["mime_type"] = getattr(document, "mime_type", None)
        data["size"] = getattr(document, "size", None)
    return data


def message_to_dict(message: Message) -> dict[str, Any]:
    peer_id = None
    if message.peer_id is not None:
        try:
            peer_id = str(utils.get_peer_id(message.peer_id))
        except Exception:
            peer_id = None
    sender_id = None
    if message.sender_id is not None:
        sender_id = str(message.sender_id)
    return {
        "id": message.id,
        "chat_id": peer_id,
        "sender_id": sender_id,
        "date": isoformat_or_none(message.date),
        "text": message.message or "",
        "raw_text": message.raw_text or "",
        "out": bool(message.out),
        "reply_to_msg_id": getattr(message.reply_to, "reply_to_msg_id", None),
        "views": getattr(message, "views", None),
        "forwards": getattr(message, "forwards", None),
        "grouped_id": str(message.grouped_id) if message.grouped_id is not None else None,
        "media": media_to_dict(message.media),
    }


def draft_to_dict(draft: Draft) -> dict[str, Any]:
    entity = getattr(draft, "entity", None)
    return {
        "chat_id": str(utils.get_peer_id(entity)) if entity is not None else None,
        "display_name": getattr(entity, "title", None)
        or " ".join(part for part in (getattr(entity, "first_name", None), getattr(entity, "last_name", None)) if part).strip()
        or getattr(entity, "username", None),
        "text": draft.text or "",
        "date": isoformat_or_none(getattr(draft, "date", None)),
        "reply_to_msg_id": getattr(draft, "reply_to_msg_id", None),
        "link_preview": getattr(draft, "link_preview", None),
    }


def parse_invite_hash(value: str) -> str | None:
    raw = value.strip()
    patterns = [
        r"(?:https?://)?t\.me/\+([A-Za-z0-9_-]+)",
        r"(?:https?://)?t\.me/joinchat/([A-Za-z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw)
        if match:
            return match.group(1)
    return None


class TelegramService:
    def __init__(self, client: TelegramClient, config: AppConfig):
        self.client = client
        self.config = config

    @classmethod
    async def connect(cls, config: AppConfig) -> "TelegramService":
        session = StringSession(config.session_string or "")
        client = TelegramClient(
            session,
            config.api_id,
            config.api_hash,
            request_retries=3,
            connection_retries=3,
            timeout=config.timeout,
        )
        await client.connect()
        return cls(client, config)

    async def close(self) -> None:
        await self.client.disconnect()

    @classmethod
    async def interactive_login(cls, config: AppConfig, phone: str | None = None) -> dict[str, Any]:
        client = TelegramClient(StringSession(config.session_string or ""), config.api_id, config.api_hash, timeout=config.timeout)
        await client.connect()
        try:
            if not await client.is_user_authorized():
                phone_value = phone or input("Telegram phone number: ").strip()

                async def code_callback() -> str:
                    return input("Telegram login code: ").strip()

                await client.start(
                    phone=lambda: phone_value,
                    code_callback=code_callback,
                    password=lambda: getpass.getpass("Telegram 2FA password (if enabled): ").strip(),
                )

            me = await client.get_me()
            return {
                "status": "ok",
                "account": entity_to_dict(me),
                "session_env_name": "TELEGRAM_SESSION_STRING",
                "session_string": client.session.save(),
            }
        finally:
            await client.disconnect()

    async def whoami(self) -> dict[str, Any]:
        me = await self.client.get_me()
        return entity_to_dict(me)

    async def validate_session(self) -> dict[str, Any]:
        authorized = await self.client.is_user_authorized()
        result: dict[str, Any] = {"authorized": authorized}
        if authorized:
            result["account"] = entity_to_dict(await self.client.get_me())
        return result

    async def resolve_entity(self, target: str | int) -> dict[str, Any]:
        entity = await self.client.get_entity(parse_ref(target))
        return entity_to_dict(entity)

    async def dialogs_list(self, query: str | None, limit: int, folder: str) -> list[dict[str, Any]]:
        if folder == "archived":
            archived: bool | None = True
        elif folder == "main":
            archived = False
        else:
            archived = None

        items: list[dict[str, Any]] = []
        async for dialog in self.client.iter_dialogs(limit=limit, archived=archived):
            data = dialog_to_dict(dialog)
            haystack = " ".join(
                filter(
                    None,
                    [
                        data.get("display_name"),
                        data.get("title"),
                        data.get("username"),
                        data.get("id"),
                    ],
                )
            ).lower()
            if query and query.lower() not in haystack:
                continue
            items.append(data)
        return items

    async def messages_list(
        self,
        chat: str | int,
        *,
        limit: int,
        search: str | None = None,
        offset_id: int = 0,
        from_user: str | None = None,
        reply_to: int | None = None,
        reverse: bool = False,
    ) -> list[dict[str, Any]]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        from_entity = await self.client.get_input_entity(parse_ref(from_user)) if from_user else None
        items: list[dict[str, Any]] = []
        async for message in self.client.iter_messages(
            entity,
            limit=limit,
            search=search,
            offset_id=offset_id,
            from_user=from_entity,
            reply_to=reply_to,
            reverse=reverse,
        ):
            items.append(message_to_dict(message))
        return items

    async def messages_get(self, chat: str | int, ids: Sequence[int]) -> list[dict[str, Any]]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        messages = await self.client.get_messages(entity, ids=list(ids))
        if not isinstance(messages, list):
            messages = [messages]
        return [message_to_dict(message) for message in messages if message is not None]

    async def messages_send(
        self,
        chat: str | int,
        *,
        text: str,
        reply_to: int | None = None,
        parse_mode: str = "md",
        silent: bool = False,
    ) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        message = await self.client.send_message(entity, text, reply_to=reply_to, parse_mode=parse_mode, silent=silent)
        return message_to_dict(message)

    async def messages_edit(self, chat: str | int, message_id: int, text: str, parse_mode: str = "md") -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        message = await self.client.edit_message(entity, message_id, text, parse_mode=parse_mode)
        return message_to_dict(message)

    async def messages_forward(
        self,
        *,
        source_chat: str | int,
        target_chat: str | int,
        ids: Sequence[int],
        silent: bool = False,
    ) -> list[dict[str, Any]]:
        source = await self.client.get_input_entity(parse_ref(source_chat))
        target = await self.client.get_input_entity(parse_ref(target_chat))
        forwarded = await self.client.forward_messages(target, list(ids), source, silent=silent)
        if not isinstance(forwarded, list):
            forwarded = [forwarded]
        return [message_to_dict(message) for message in forwarded if message is not None]

    async def messages_delete(
        self,
        chat: str | int,
        ids: Sequence[int],
        *,
        revoke: bool = True,
    ) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        deleted = await self.client.delete_messages(entity, list(ids), revoke=revoke)
        affected = len(deleted) if isinstance(deleted, Iterable) else len(list(ids))
        return {"deleted": affected, "ids": list(ids), "chat": str(chat), "revoke": revoke}

    async def messages_mark_read(self, chat: str | int, max_id: int | None = None) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        await self.client.send_read_acknowledge(entity, max_id=max_id)
        return {"status": "ok", "chat": str(chat), "max_id": max_id}

    async def messages_pin(self, chat: str | int, message_id: int, *, notify: bool = False) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        await self.client.pin_message(entity, message_id, notify=notify)
        return {"status": "ok", "chat": str(chat), "message_id": message_id, "notify": notify}

    async def messages_unpin(self, chat: str | int, message_id: int | None = None) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        await self.client.unpin_message(entity, message_id=message_id)
        return {"status": "ok", "chat": str(chat), "message_id": message_id}

    async def media_download(
        self,
        chat: str | int,
        message_id: int,
        *,
        output_dir: str | None = None,
        output_file: str | None = None,
    ) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        message = await self.client.get_messages(entity, ids=message_id)
        if message is None:
            raise ValueError(f"Message {message_id} not found")
        target: str | Path | None = output_file or output_dir
        downloaded = await self.client.download_media(message, file=target)
        return {
            "message": message_to_dict(message),
            "download_path": str(downloaded) if downloaded else None,
        }

    async def media_send_file(
        self,
        chat: str | int,
        files: Sequence[str],
        *,
        caption: str | None = None,
        reply_to: int | None = None,
        silent: bool = False,
        parse_mode: str = "md",
    ) -> list[dict[str, Any]]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        sent = await self.client.send_file(
            entity,
            list(files),
            caption=caption,
            reply_to=reply_to,
            silent=silent,
            parse_mode=parse_mode,
        )
        if not isinstance(sent, list):
            sent = [sent]
        return [message_to_dict(message) for message in sent if message is not None]

    async def chat_info(self, target: str | int) -> dict[str, Any]:
        entity = await self.client.get_entity(parse_ref(target))
        return entity_to_dict(entity)

    async def chat_participants(self, target: str | int, *, limit: int, search: str | None = None) -> list[dict[str, Any]]:
        entity = await self.client.get_entity(parse_ref(target))
        participants: list[dict[str, Any]] = []
        async for user in self.client.iter_participants(entity, search=search, limit=limit):
            participants.append(entity_to_dict(user))
        return participants

    async def join(self, target: str) -> dict[str, Any]:
        invite_hash = parse_invite_hash(target)
        if invite_hash:
            result = await self.client(functions.messages.ImportChatInviteRequest(invite_hash))
            return {"status": "ok", "action": "join", "result_type": type(result).__name__}
        entity = await self.client.get_input_entity(parse_ref(target))
        await self.client(functions.channels.JoinChannelRequest(entity))
        return {"status": "ok", "action": "join", "target": str(target)}

    async def leave(self, target: str | int) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(target))
        await self.client.delete_dialog(entity)
        return {"status": "ok", "action": "leave", "target": str(target)}

    async def archive(self, targets: Sequence[str]) -> dict[str, Any]:
        entities = [await self.client.get_input_entity(parse_ref(target)) for target in targets]
        await self.client.edit_folder(entities, folder=1)
        return {"status": "ok", "action": "archive", "targets": list(targets)}

    async def unarchive(self, targets: Sequence[str]) -> dict[str, Any]:
        entities = [await self.client.get_input_entity(parse_ref(target)) for target in targets]
        await self.client.edit_folder(entities, folder=0)
        return {"status": "ok", "action": "unarchive", "targets": list(targets)}

    async def mute(self, target: str | int, *, hours: int) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(target))
        mute_until = datetime.now(tz=timezone.utc) + timedelta(hours=hours)
        await self.client(
            functions.account.UpdateNotifySettingsRequest(
                peer=types.InputNotifyPeer(entity),
                settings=types.InputPeerNotifySettings(mute_until=int(mute_until.timestamp())),
            )
        )
        return {"status": "ok", "action": "mute", "target": str(target), "mute_until": mute_until.isoformat()}

    async def unmute(self, target: str | int) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(target))
        await self.client(
            functions.account.UpdateNotifySettingsRequest(
                peer=types.InputNotifyPeer(entity),
                settings=types.InputPeerNotifySettings(mute_until=0),
            )
        )
        return {"status": "ok", "action": "unmute", "target": str(target)}

    async def contacts_list(self, *, query: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        contacts = await self.client.get_contacts()
        items: list[dict[str, Any]] = []
        for contact in contacts[:limit]:
            data = entity_to_dict(contact)
            haystack = " ".join(filter(None, [data.get("display_name"), data.get("username"), data.get("phone")])).lower()
            if query and query.lower() not in haystack:
                continue
            items.append(data)
        return items

    async def contacts_add(
        self,
        *,
        target: str,
        first_name: str,
        last_name: str = "",
        phone: str = "",
    ) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(target))
        result = await self.client(
            functions.contacts.AddContactRequest(
                id=entity,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                add_phone_privacy_exception=False,
            )
        )
        return {"status": "ok", "action": "add-contact", "target": target, "result_type": type(result).__name__}

    async def contacts_remove(self, *, target: str) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(target))
        result = await self.client(functions.contacts.DeleteContactsRequest(id=[entity]))
        return {"status": "ok", "action": "remove-contact", "target": target, "result_type": type(result).__name__}

    async def drafts_list(self) -> list[dict[str, Any]]:
        drafts = await self.client.get_drafts()
        return [draft_to_dict(draft) for draft in drafts]

    async def drafts_get(self, chat: str | int) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        draft = await self.client.get_drafts(entity)
        if isinstance(draft, list):
            draft = draft[0] if draft else None
        return draft_to_dict(draft) if draft else {"chat": str(chat), "text": "", "status": "empty"}

    async def drafts_set(self, chat: str | int, *, text: str, reply_to: int | None = None) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        await self.client.edit_draft(entity, text=text, reply_to=reply_to)
        draft = await self.client.get_drafts(entity)
        if isinstance(draft, list):
            draft = draft[0] if draft else None
        return draft_to_dict(draft) if draft else {"chat": str(chat), "text": text}

    async def drafts_delete(self, chat: str | int) -> dict[str, Any]:
        entity = await self.client.get_input_entity(parse_ref(chat))
        await self.client.edit_draft(entity, text="")
        return {"status": "ok", "action": "delete-draft", "chat": str(chat)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tg", description="Bundled Telethon CLI for Codex skills")
    parser.add_argument("--env-file", help="Path to .env file")
    parser.add_argument("--timeout", type=float, default=30.0, help="Telegram request timeout in seconds")
    parser.add_argument("--output", choices=("pretty", "json"), default="pretty")
    parser.add_argument("--json", action="store_true", help="Shortcut for --output json")
    parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error"),
        default="warning",
        help="stderr logging level",
    )

    root = parser.add_subparsers(dest="group", required=True)

    auth = root.add_parser("auth", help="Authentication and session commands")
    auth_sub = auth.add_subparsers(dest="action", required=True)
    auth_login = auth_sub.add_parser("login", help="Interactive login and session export")
    auth_login.add_argument("--phone", help="Phone number to use during login")
    auth_sub.add_parser("validate", help="Validate current session")
    auth_sub.add_parser("whoami", help="Print current account identity")

    account = root.add_parser("account", help="Account inspection")
    account_sub = account.add_subparsers(dest="action", required=True)
    account_sub.add_parser("whoami", help="Print current account identity")

    dialogs = root.add_parser("dialogs", help="Dialog and entity commands")
    dialogs_sub = dialogs.add_subparsers(dest="action", required=True)
    dialogs_list = dialogs_sub.add_parser("list", help="List dialogs")
    dialogs_list.add_argument("--query")
    dialogs_list.add_argument("--limit", type=int, default=50)
    dialogs_list.add_argument("--folder", choices=("all", "main", "archived"), default="all")
    dialogs_target = dialogs_sub.add_parser("inspect", help="Inspect a single dialog/entity")
    dialogs_target.add_argument("--target", required=True)
    dialogs_resolve = dialogs_sub.add_parser("resolve", help="Resolve entity by id/username/link")
    dialogs_resolve.add_argument("--target", required=True)

    messages = root.add_parser("messages", help="Message management")
    messages_sub = messages.add_subparsers(dest="action", required=True)
    messages_list = messages_sub.add_parser("list", help="List message history")
    messages_list.add_argument("--chat", required=True)
    messages_list.add_argument("--limit", type=int, default=20)
    messages_list.add_argument("--search")
    messages_list.add_argument("--offset-id", type=int, default=0)
    messages_list.add_argument("--from-user")
    messages_list.add_argument("--reply-to", type=int)
    messages_list.add_argument("--reverse", action="store_true")

    messages_get = messages_sub.add_parser("get", help="Get one or more messages by id")
    messages_get.add_argument("--chat", required=True)
    messages_get.add_argument("--ids", type=int, nargs="+", required=True)

    messages_send = messages_sub.add_parser("send", help="Send a text message")
    messages_send.add_argument("--chat", required=True)
    messages_send.add_argument("--text", required=True)
    messages_send.add_argument("--reply-to", type=int)
    messages_send.add_argument("--parse-mode", default="md")
    messages_send.add_argument("--silent", action="store_true")

    messages_reply = messages_sub.add_parser("reply", help="Reply to a message")
    messages_reply.add_argument("--chat", required=True)
    messages_reply.add_argument("--message-id", type=int, required=True)
    messages_reply.add_argument("--text", required=True)
    messages_reply.add_argument("--parse-mode", default="md")
    messages_reply.add_argument("--silent", action="store_true")

    messages_edit = messages_sub.add_parser("edit", help="Edit a message")
    messages_edit.add_argument("--chat", required=True)
    messages_edit.add_argument("--message-id", type=int, required=True)
    messages_edit.add_argument("--text", required=True)
    messages_edit.add_argument("--parse-mode", default="md")

    messages_forward = messages_sub.add_parser("forward", help="Forward messages")
    messages_forward.add_argument("--source-chat", required=True)
    messages_forward.add_argument("--target-chat", required=True)
    messages_forward.add_argument("--ids", type=int, nargs="+", required=True)
    messages_forward.add_argument("--silent", action="store_true")

    messages_delete = messages_sub.add_parser("delete", help="Delete messages")
    messages_delete.add_argument("--chat", required=True)
    messages_delete.add_argument("--ids", type=int, nargs="+", required=True)
    messages_delete.add_argument("--local-only", action="store_true", help="Do not revoke for everyone")
    messages_delete.add_argument("--dry-run", action="store_true")
    messages_delete.add_argument("--yes", action="store_true")

    messages_mark_read = messages_sub.add_parser("mark-read", help="Mark dialog as read")
    messages_mark_read.add_argument("--chat", required=True)
    messages_mark_read.add_argument("--max-id", type=int)

    messages_pin = messages_sub.add_parser("pin", help="Pin a message")
    messages_pin.add_argument("--chat", required=True)
    messages_pin.add_argument("--message-id", type=int, required=True)
    messages_pin.add_argument("--notify", action="store_true")

    messages_unpin = messages_sub.add_parser("unpin", help="Unpin a message")
    messages_unpin.add_argument("--chat", required=True)
    messages_unpin.add_argument("--message-id", type=int)

    media = root.add_parser("media", help="Media operations")
    media_sub = media.add_subparsers(dest="action", required=True)
    media_inspect = media_sub.add_parser("inspect", help="Inspect message media")
    media_inspect.add_argument("--chat", required=True)
    media_inspect.add_argument("--message-id", type=int, required=True)

    media_download = media_sub.add_parser("download", help="Download message media")
    media_download.add_argument("--chat", required=True)
    media_download.add_argument("--message-id", type=int, required=True)
    media_download.add_argument("--output-dir")
    media_download.add_argument("--output-file")

    media_send = media_sub.add_parser("send-file", help="Send one or more files")
    media_send.add_argument("--chat", required=True)
    media_send.add_argument("--files", nargs="+", required=True)
    media_send.add_argument("--caption")
    media_send.add_argument("--reply-to", type=int)
    media_send.add_argument("--parse-mode", default="md")
    media_send.add_argument("--silent", action="store_true")

    chats = root.add_parser("chats", help="Chat-level operations")
    chats_sub = chats.add_subparsers(dest="action", required=True)
    chats_info = chats_sub.add_parser("info", help="Inspect chat info")
    chats_info.add_argument("--target", required=True)

    chats_participants = chats_sub.add_parser("participants", help="List chat participants")
    chats_participants.add_argument("--target", required=True)
    chats_participants.add_argument("--search")
    chats_participants.add_argument("--limit", type=int, default=100)

    chats_join = chats_sub.add_parser("join", help="Join chat by public username or invite link")
    chats_join.add_argument("--target", required=True)

    chats_leave = chats_sub.add_parser("leave", help="Leave or delete dialog")
    chats_leave.add_argument("--target", required=True)
    chats_leave.add_argument("--dry-run", action="store_true")
    chats_leave.add_argument("--yes", action="store_true")

    chats_archive = chats_sub.add_parser("archive", help="Archive dialogs")
    chats_archive.add_argument("--targets", nargs="+", required=True)

    chats_unarchive = chats_sub.add_parser("unarchive", help="Unarchive dialogs")
    chats_unarchive.add_argument("--targets", nargs="+", required=True)

    chats_mute = chats_sub.add_parser("mute", help="Mute chat notifications")
    chats_mute.add_argument("--target", required=True)
    chats_mute.add_argument("--hours", type=int, default=24)

    chats_unmute = chats_sub.add_parser("unmute", help="Unmute chat notifications")
    chats_unmute.add_argument("--target", required=True)

    contacts = root.add_parser("contacts", help="Contact operations")
    contacts_sub = contacts.add_subparsers(dest="action", required=True)
    contacts_list = contacts_sub.add_parser("list", help="List contacts")
    contacts_list.add_argument("--query")
    contacts_list.add_argument("--limit", type=int, default=100)

    contacts_add = contacts_sub.add_parser("add", help="Add contact")
    contacts_add.add_argument("--target", required=True)
    contacts_add.add_argument("--first-name", required=True)
    contacts_add.add_argument("--last-name", default="")
    contacts_add.add_argument("--phone", default="")

    contacts_remove = contacts_sub.add_parser("remove", help="Remove contact")
    contacts_remove.add_argument("--target", required=True)
    contacts_remove.add_argument("--dry-run", action="store_true")
    contacts_remove.add_argument("--yes", action="store_true")

    drafts = root.add_parser("drafts", help="Draft management")
    drafts_sub = drafts.add_subparsers(dest="action", required=True)
    drafts_sub.add_parser("list", help="List drafts")
    drafts_get = drafts_sub.add_parser("get", help="Get draft")
    drafts_get.add_argument("--chat", required=True)
    drafts_set = drafts_sub.add_parser("set", help="Set draft")
    drafts_set.add_argument("--chat", required=True)
    drafts_set.add_argument("--text", required=True)
    drafts_set.add_argument("--reply-to", type=int)
    drafts_delete = drafts_sub.add_parser("delete", help="Delete draft")
    drafts_delete.add_argument("--chat", required=True)
    drafts_delete.add_argument("--dry-run", action="store_true")
    drafts_delete.add_argument("--yes", action="store_true")

    return parser


def requires_confirmation(args: argparse.Namespace) -> bool:
    return (args.group, args.action) in {
        ("messages", "delete"),
        ("chats", "leave"),
        ("contacts", "remove"),
        ("drafts", "delete"),
    }


def ensure_confirmed(args: argparse.Namespace, action_label: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    if not requires_confirmation(args):
        return None
    if getattr(args, "dry_run", False):
        return {"status": "dry-run", "action": action_label, **payload}
    if not getattr(args, "yes", False):
        raise CLIError(f"{action_label} is destructive. Re-run with --yes or use --dry-run first.")
    return None


async def dispatch(args: argparse.Namespace, service_factory: ServiceFactory) -> Any:
    output_mode = "json" if args.json else args.output
    setattr(args, "output", output_mode)

    if args.group == "auth" and args.action == "login":
        config = build_config(args.env_file, args.timeout, require_session=False)
        return await TelegramService.interactive_login(config, phone=args.phone)

    if args.group == "messages" and args.action == "delete":
        preview = ensure_confirmed(
            args,
            "messages.delete",
            {"chat": args.chat, "ids": normalize_message_ids(args.ids), "revoke": not args.local_only},
        )
        if preview is not None:
            return preview
    if args.group == "chats" and args.action == "leave":
        preview = ensure_confirmed(args, "chats.leave", {"target": args.target})
        if preview is not None:
            return preview
    if args.group == "contacts" and args.action == "remove":
        preview = ensure_confirmed(args, "contacts.remove", {"target": args.target})
        if preview is not None:
            return preview
    if args.group == "drafts" and args.action == "delete":
        preview = ensure_confirmed(args, "drafts.delete", {"chat": args.chat})
        if preview is not None:
            return preview

    require_session = not (args.group == "auth" and args.action == "login")
    config = build_config(args.env_file, args.timeout, require_session=require_session)
    service = await service_factory(config)
    try:
        if args.group == "auth" and args.action == "validate":
            return await service.validate_session()
        if args.group == "auth" and args.action == "whoami":
            return await service.whoami()
        if args.group == "account" and args.action == "whoami":
            return await service.whoami()

        if args.group == "dialogs" and args.action == "list":
            return await service.dialogs_list(args.query, args.limit, args.folder)
        if args.group == "dialogs" and args.action in {"inspect", "resolve"}:
            return await service.resolve_entity(args.target)

        if args.group == "messages" and args.action == "list":
            return await service.messages_list(
                args.chat,
                limit=args.limit,
                search=args.search,
                offset_id=args.offset_id,
                from_user=args.from_user,
                reply_to=args.reply_to,
                reverse=args.reverse,
            )
        if args.group == "messages" and args.action == "get":
            return await service.messages_get(args.chat, args.ids)
        if args.group == "messages" and args.action == "send":
            return await service.messages_send(
                args.chat,
                text=args.text,
                reply_to=args.reply_to,
                parse_mode=args.parse_mode,
                silent=args.silent,
            )
        if args.group == "messages" and args.action == "reply":
            return await service.messages_send(
                args.chat,
                text=args.text,
                reply_to=args.message_id,
                parse_mode=args.parse_mode,
                silent=args.silent,
            )
        if args.group == "messages" and args.action == "edit":
            return await service.messages_edit(args.chat, args.message_id, args.text, parse_mode=args.parse_mode)
        if args.group == "messages" and args.action == "forward":
            return await service.messages_forward(
                source_chat=args.source_chat,
                target_chat=args.target_chat,
                ids=args.ids,
                silent=args.silent,
            )
        if args.group == "messages" and args.action == "delete":
            return await service.messages_delete(args.chat, args.ids, revoke=not args.local_only)
        if args.group == "messages" and args.action == "mark-read":
            return await service.messages_mark_read(args.chat, args.max_id)
        if args.group == "messages" and args.action == "pin":
            return await service.messages_pin(args.chat, args.message_id, notify=args.notify)
        if args.group == "messages" and args.action == "unpin":
            return await service.messages_unpin(args.chat, args.message_id)

        if args.group == "media" and args.action == "inspect":
            result = await service.messages_get(args.chat, [args.message_id])
            return result[0] if result else {"status": "empty"}
        if args.group == "media" and args.action == "download":
            return await service.media_download(
                args.chat,
                args.message_id,
                output_dir=args.output_dir,
                output_file=args.output_file,
            )
        if args.group == "media" and args.action == "send-file":
            return await service.media_send_file(
                args.chat,
                args.files,
                caption=args.caption,
                reply_to=args.reply_to,
                silent=args.silent,
                parse_mode=args.parse_mode,
            )

        if args.group == "chats" and args.action == "info":
            return await service.chat_info(args.target)
        if args.group == "chats" and args.action == "participants":
            return await service.chat_participants(args.target, limit=args.limit, search=args.search)
        if args.group == "chats" and args.action == "join":
            return await service.join(args.target)
        if args.group == "chats" and args.action == "leave":
            return await service.leave(args.target)
        if args.group == "chats" and args.action == "archive":
            return await service.archive(args.targets)
        if args.group == "chats" and args.action == "unarchive":
            return await service.unarchive(args.targets)
        if args.group == "chats" and args.action == "mute":
            return await service.mute(args.target, hours=args.hours)
        if args.group == "chats" and args.action == "unmute":
            return await service.unmute(args.target)

        if args.group == "contacts" and args.action == "list":
            return await service.contacts_list(query=args.query, limit=args.limit)
        if args.group == "contacts" and args.action == "add":
            return await service.contacts_add(
                target=args.target,
                first_name=args.first_name,
                last_name=args.last_name,
                phone=args.phone,
            )
        if args.group == "contacts" and args.action == "remove":
            return await service.contacts_remove(target=args.target)

        if args.group == "drafts" and args.action == "list":
            return await service.drafts_list()
        if args.group == "drafts" and args.action == "get":
            return await service.drafts_get(args.chat)
        if args.group == "drafts" and args.action == "set":
            return await service.drafts_set(args.chat, text=args.text, reply_to=args.reply_to)
        if args.group == "drafts" and args.action == "delete":
            return await service.drafts_delete(args.chat)

        raise CLIError(f"Unsupported command: {args.group} {args.action}")
    finally:
        await service.close()


def configure_logging(level: str) -> None:
    logging.basicConfig(level=getattr(logging, level.upper()), format="%(levelname)s %(message)s")


async def async_main(argv: Sequence[str] | None = None, service_factory: ServiceFactory = TelegramService.connect) -> int:
    parser = build_parser()
    parsed_argv = normalize_global_flags(list(argv) if argv is not None else sys.argv[1:])
    args = parser.parse_args(parsed_argv)
    configure_logging(args.log_level)

    try:
        result = await dispatch(args, service_factory)
        renderer = render_json if args.output == "json" or args.json else render_pretty
        print(renderer(result))
        return 0
    except (CLIError, ConfigError, ValueError) as error:
        payload = {"status": "error", "error": str(error)}
        if getattr(args, "output", "pretty") == "json" or getattr(args, "json", False):
            print(render_json(payload), file=sys.stderr)
        else:
            print(f"error: {error}", file=sys.stderr)
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    return asyncio.run(async_main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
