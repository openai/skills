#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import textwrap
from pathlib import Path
from typing import Any

import requests
from pypdf import PdfReader, PdfWriter


LETTER_WIDTH = 612
LETTER_HEIGHT = 792
TERMINAL_STATES = {"success", "failure", "canceled", "cancelled", "busy", "no-answer"}


class FaxCliError(Exception):
    pass


def pdf_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", "")
    )


def wrap_text(text: str, width: int = 90) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines() or [""]:
        if not raw_line:
            lines.append("")
            continue
        lines.extend(textwrap.wrap(raw_line, width=width, replace_whitespace=False))
    return lines


def build_text_pdf_bytes(
    text: str,
    *,
    width: float = LETTER_WIDTH,
    height: float = LETTER_HEIGHT,
    x: float = 72,
    y: float = 720,
    font_size: int = 12,
    line_gap: int = 16,
) -> bytes:
    lines = wrap_text(text)
    stream_lines = ["BT", f"/F1 {font_size} Tf", f"{x} {y} Td"]
    for index, line in enumerate(lines):
        if index:
            stream_lines.append(f"0 -{line_gap} Td")
        stream_lines.append(f"({pdf_escape(line)}) Tj")
    stream_lines.append("ET")
    stream = "\n".join(stream_lines).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    output = io.BytesIO()
    output.write(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(output.tell())
        output.write(f"{index} 0 obj\n".encode("ascii"))
        output.write(obj)
        output.write(b"\nendobj\n")

    xref_offset = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.write(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return output.getvalue()


def render_text_pdf(text: str, out_path: Path) -> None:
    out_path.write_bytes(build_text_pdf_bytes(text))


def overlay_text_pdf(input_path: Path, text: str, x: float, y: float, out_path: Path) -> None:
    writer = PdfWriter(clone_from=str(input_path))
    if not writer.pages:
        raise FaxCliError(f"PDF has no pages: {input_path}")

    first_page = writer.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)
    overlay_reader = PdfReader(io.BytesIO(build_text_pdf_bytes(text, width=width, height=height, x=x, y=y)))

    first_page.merge_page(overlay_reader.pages[0])

    with out_path.open("wb") as handle:
        writer.write(handle)


class PhaxioClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.phaxio.com/v2"):
        self.auth = (api_key, api_secret)
        self.base_url = base_url.rstrip("/")

    @classmethod
    def from_env(cls) -> PhaxioClient:
        api_key = os.environ.get("PHAXIO_API_KEY")
        api_secret = os.environ.get("PHAXIO_API_SECRET")
        if not api_key or not api_secret:
            raise FaxCliError("PHAXIO_API_KEY and PHAXIO_API_SECRET must be set")
        return cls(api_key=api_key, api_secret=api_secret)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        response = requests.request(method, f"{self.base_url}{path}", auth=self.auth, timeout=30, **kwargs)
        if response.status_code >= 400:
            raise FaxCliError(f"Phaxio API error {response.status_code}: {response.text}")
        return response

    def send_fax(
        self,
        *,
        to: str,
        pdf_path: Path,
        cover_page: str | None = None,
        callback_url: str | None = None,
    ) -> dict[str, Any]:
        data = {"to": to}
        if cover_page:
            data["cover_page"] = cover_page
        if callback_url:
            data["callback_url"] = callback_url

        with pdf_path.open("rb") as handle:
            response = self._request(
                "POST",
                "/faxes",
                data=data,
                files={"file": (pdf_path.name, handle, "application/pdf")},
            )
        return response.json()

    def get_status(self, fax_id: str) -> dict[str, Any]:
        return self._request("GET", f"/faxes/{fax_id}").json()

    def fetch_file(self, fax_id: str) -> bytes:
        return self._request("GET", f"/faxes/{fax_id}/file").content


def wait_for_terminal_status(client: PhaxioClient, fax_id: str, interval: int, timeout: int) -> dict[str, Any]:
    deadline = time.time() + timeout
    while True:
        payload = client.get_status(fax_id)
        status = str(payload.get("data", {}).get("status", "")).lower()
        if status in TERMINAL_STATES:
            return payload
        if time.time() >= deadline:
            raise FaxCliError(f"Timed out waiting for fax {fax_id}; last status={status or 'unknown'}")
        time.sleep(interval)


def print_payload(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(json.dumps(payload, sort_keys=True))


def cmd_render(args: argparse.Namespace) -> int:
    render_text_pdf(args.text, Path(args.out))
    return 0


def cmd_overlay(args: argparse.Namespace) -> int:
    overlay_text_pdf(Path(args.pdf), args.text, args.x, args.y, Path(args.out))
    return 0


def cmd_send(args: argparse.Namespace) -> int:
    client = PhaxioClient.from_env()
    payload = client.send_fax(
        to=args.to,
        pdf_path=Path(args.pdf),
        cover_page=args.cover,
        callback_url=args.callback_url,
    )
    if args.wait:
        fax_id = str(payload.get("data", {}).get("id") or payload.get("id"))
        if not fax_id:
            raise FaxCliError(f"Unable to determine fax id from response: {payload}")
        payload = wait_for_terminal_status(client, fax_id, args.interval, args.timeout)
    print_payload(payload, args.json)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    client = PhaxioClient.from_env()
    print_payload(client.get_status(args.fax_id), args.json)
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    client = PhaxioClient.from_env()
    Path(args.out).write_bytes(client.fetch_file(args.fax_id))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render PDFs and send outbound faxes via Phaxio")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="Render text to a PDF")
    render_parser.add_argument("--text", required=True)
    render_parser.add_argument("--out", required=True)
    render_parser.set_defaults(func=cmd_render)

    overlay_parser = subparsers.add_parser("overlay", help="Stamp text onto the first page of a PDF")
    overlay_parser.add_argument("--pdf", required=True)
    overlay_parser.add_argument("--text", required=True)
    overlay_parser.add_argument("--x", type=float, required=True)
    overlay_parser.add_argument("--y", type=float, required=True)
    overlay_parser.add_argument("--out", required=True)
    overlay_parser.set_defaults(func=cmd_overlay)

    send_parser = subparsers.add_parser("send", help="Send a PDF as a fax")
    send_parser.add_argument("--to", required=True)
    send_parser.add_argument("--pdf", required=True)
    send_parser.add_argument("--cover")
    send_parser.add_argument("--callback-url")
    send_parser.add_argument("--wait", action="store_true")
    send_parser.add_argument("--interval", type=int, default=5)
    send_parser.add_argument("--timeout", type=int, default=300)
    send_parser.add_argument("--json", action="store_true")
    send_parser.set_defaults(func=cmd_send)

    status_parser = subparsers.add_parser("status", help="Check fax delivery status")
    status_parser.add_argument("fax_id")
    status_parser.add_argument("--json", action="store_true")
    status_parser.set_defaults(func=cmd_status)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch the transmitted PDF")
    fetch_parser.add_argument("fax_id")
    fetch_parser.add_argument("--out", required=True)
    fetch_parser.set_defaults(func=cmd_fetch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except FaxCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
