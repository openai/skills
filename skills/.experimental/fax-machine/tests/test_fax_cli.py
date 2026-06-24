from __future__ import annotations

import importlib.util
import io
from pathlib import Path
from unittest.mock import Mock

import pytest
from pypdf import PdfReader


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fax_cli.py"
spec = importlib.util.spec_from_file_location("fax_cli", SCRIPT_PATH)
fax_cli = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(fax_cli)


def test_render_text_pdf_creates_readable_pdf(tmp_path: Path) -> None:
    out_path = tmp_path / "rendered.pdf"

    fax_cli.render_text_pdf("hello from codex", out_path)

    reader = PdfReader(str(out_path))
    assert len(reader.pages) == 1
    assert "hello from codex" in (reader.pages[0].extract_text() or "")


def test_overlay_text_pdf_preserves_pages_and_adds_text(tmp_path: Path) -> None:
    input_path = tmp_path / "input.pdf"
    out_path = tmp_path / "overlay.pdf"
    fax_cli.render_text_pdf("base document", input_path)

    fax_cli.overlay_text_pdf(input_path, "Approved", 72, 700, out_path)

    reader = PdfReader(str(out_path))
    assert len(reader.pages) == 1
    text = reader.pages[0].extract_text() or ""
    assert "base document" in text
    assert "Approved" in text


def test_phaxio_client_from_env_requires_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PHAXIO_API_KEY", raising=False)
    monkeypatch.delenv("PHAXIO_API_SECRET", raising=False)

    with pytest.raises(fax_cli.FaxCliError, match="must be set"):
        fax_cli.PhaxioClient.from_env()


def test_phaxio_client_from_env_reads_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PHAXIO_API_KEY", "key")
    monkeypatch.setenv("PHAXIO_API_SECRET", "secret")

    client = fax_cli.PhaxioClient.from_env()

    assert client.auth == ("key", "secret")


def test_send_fax_shapes_multipart_request(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pdf_path = tmp_path / "fax.pdf"
    pdf_path.write_bytes(fax_cli.build_text_pdf_bytes("hello"))
    response = Mock(status_code=200)
    response.json.return_value = {"success": True, "data": {"id": 123}}
    request = Mock(return_value=response)
    monkeypatch.setattr(fax_cli.requests, "request", request)
    client = fax_cli.PhaxioClient("key", "secret", base_url="https://api.example.test/v2")

    payload = client.send_fax(to="+14155551212", pdf_path=pdf_path, cover_page="Cover")

    assert payload == {"success": True, "data": {"id": 123}}
    request.assert_called_once()
    _, url = request.call_args.args
    assert url == "https://api.example.test/v2/faxes"
    assert request.call_args.kwargs["auth"] == ("key", "secret")
    assert request.call_args.kwargs["data"] == {"to": "+14155551212", "cover_page": "Cover"}
    assert request.call_args.kwargs["files"]["file"][0] == "fax.pdf"


def test_get_status_uses_expected_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Mock(status_code=200)
    response.json.return_value = {"success": True, "data": {"id": 123, "status": "queued"}}
    request = Mock(return_value=response)
    monkeypatch.setattr(fax_cli.requests, "request", request)
    client = fax_cli.PhaxioClient("key", "secret")

    payload = client.get_status("123")

    assert payload["data"]["status"] == "queued"
    assert request.call_args.args[:2] == ("GET", "https://api.phaxio.com/v2/faxes/123")


def test_fetch_file_returns_response_content(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Mock(status_code=200, content=b"%PDF-1.4")
    request = Mock(return_value=response)
    monkeypatch.setattr(fax_cli.requests, "request", request)
    client = fax_cli.PhaxioClient("key", "secret")

    content = client.fetch_file("123")

    assert content == b"%PDF-1.4"
    assert request.call_args.args[:2] == ("GET", "https://api.phaxio.com/v2/faxes/123/file")


def test_request_raises_for_http_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Mock(status_code=400, text="bad request")
    monkeypatch.setattr(fax_cli.requests, "request", Mock(return_value=response))
    client = fax_cli.PhaxioClient("key", "secret")

    with pytest.raises(fax_cli.FaxCliError, match="Phaxio API error 400"):
        client.get_status("123")


def test_wait_for_terminal_status_stops_on_success(monkeypatch: pytest.MonkeyPatch) -> None:
    client = Mock()
    client.get_status.side_effect = [
        {"data": {"status": "queued"}},
        {"data": {"status": "success"}},
    ]
    monkeypatch.setattr(fax_cli.time, "sleep", Mock())

    payload = fax_cli.wait_for_terminal_status(client, "123", interval=1, timeout=10)

    assert payload == {"data": {"status": "success"}}
    assert client.get_status.call_count == 2
