#!/usr/bin/env python3
"""Smoke and unit tests for sync_bmad_method.py."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

import importlib.util

SCRIPT_PATH = Path(__file__).resolve().parent / "sync_bmad_method.py"
spec = importlib.util.spec_from_file_location("sync_bmad_method", SCRIPT_PATH)
sync_bmad_method = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(sync_bmad_method)  # type: ignore[attr-defined]


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text.encode("utf-8")

    def read(self):
        return self.text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class SyncBMADMethodTests(unittest.TestCase):
    def test_request_text_retries_then_succeeds(self):
        with patch.object(
            sync_bmad_method.urllib.request,
            "urlopen",
            side_effect=[urllib.error.URLError("temporary"), _FakeResponse("ok")],
        ):
            result = sync_bmad_method.request_text(
                "https://example.test/timeout",
                max_retries=1,
                retry_delay=0,
            )
        self.assertEqual(result, "ok")

    def test_build_warnings_for_version_mismatch(self):
        health = {
            "versions_match": False,
            "runtime_version": "1.0.0",
        }
        warnings = sync_bmad_method.build_warnings(
            health,
            first_run=False,
            runtime_before="1.0.1",
            release_changed=True,
            mode="check",
        )
        self.assertTrue(any("Wersja skilla" in item for item in warnings))
        self.assertTrue(any("Wersja Codex runtime" in item for item in warnings))

    def test_main_smoke_check_outputs_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_dir = root / "references"
            manifest_dir.mkdir()
            (manifest_dir / "skill-manifest.json").write_text(
                json.dumps(
                    {
                        "skill_version": "0.1.0",
                        "target_codex_profile": "codex-5.3",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            home = root / "codex-home"
            installed = home / ".codex" / "skills" / sync_bmad_method.SKILL_NAME
            installed.mkdir(parents=True)
            (installed / "SKILL.md").write_text("test", encoding="utf-8")
            installed_refs = installed / "references"
            installed_refs.mkdir()
            (installed_refs / "skill-manifest.json").write_text(
                json.dumps({"skill_version": "0.1.0"}, indent=2),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
                with patch.object(sync_bmad_method, "ROOT", root):
                    with patch.object(
                        sync_bmad_method,
                        "STATE_FILE",
                        root / "state" / "bmad-release-state.json",
                    ):
                        with patch.object(
                            sync_bmad_method,
                            "SNAPSHOT_DIR",
                            root / "references" / "upstream",
                        ):
                            with patch.object(
                                sync_bmad_method,
                                "MANIFEST_FILE",
                                manifest_dir / "skill-manifest.json",
                            ):
                                with patch.object(sync_bmad_method, "TRACKED_FILES", []):
                                    with patch.object(
                                        sync_bmad_method,
                                        "sync_snapshots",
                                        return_value=({}, []),
                                    ):
                                        with patch.object(
                                            sync_bmad_method,
                                            "write_release_summary",
                                            return_value=None,
                                        ):
                                            with patch.object(
                                                sync_bmad_method,
                                                "read_skill_health",
                                                return_value={
                                                    "local_version": "0.1.0",
                                                    "agent_version": "0.1.0",
                                                    "versions_match": True,
                                                    "agent_path": str(installed),
                                                    "runtime_profile": "codex-5.3",
                                                    "runtime_version": "",
                                                    "local_manifest": str(manifest_dir / "skill-manifest.json"),
                                                    "agent_manifest": str(installed_refs / "skill-manifest.json"),
                                                },
                                            ):
                                                with patch.object(
                                                    sync_bmad_method,
                                                    "request_json",
                                                    return_value={
                                                        "tag_name": "v1.0.0",
                                                        "name": "BMAD-METHOD",
                                                        "published_at": "2026-01-01T00:00:00Z",
                                                        "html_url": "https://example.com/release",
                                                        "body": "release notes",
                                                    },
                                                ):
                                                    with patch.object(sync_bmad_method.time, "sleep", lambda *_args, **_kwargs: None):
                                                        with patch.object(sync_bmad_method, "_now_iso", return_value="2026-01-01T00:00:00+00:00"):
                                                            out = io.StringIO()
                                                            with contextlib.redirect_stdout(out):
                                                                code = sync_bmad_method.main([
                                                                    "check",
                                                                    "--json",
                                                                    "--max-retries",
                                                                    "0",
                                                                    "--retry-delay",
                                                                    "0",
                                                                ])
                                                            payload = json.loads(out.getvalue())

            self.assertEqual(code, 0)
            self.assertEqual(payload["latest_release"]["tag"], "v1.0.0")
            self.assertIn("is_optimal", payload)


if __name__ == "__main__":
    unittest.main()
