#!/usr/bin/env python3
"""Regression tests for PR reference resolution in fetch_comments.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("fetch_comments.py")
MODULE_SPEC = importlib.util.spec_from_file_location("fetch_comments", MODULE_PATH)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError(f"Failed to load module spec from {MODULE_PATH}")
fetch_comments = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(fetch_comments)


class FetchCommentsPrResolutionTests(unittest.TestCase):
    """Lock down base-repository resolution for fork-backed pull requests."""

    def test_parse_pr_url_extracts_base_repository(self) -> None:
        self.assertEqual(
            fetch_comments.parse_pr_url("https://github.com/openai/skills/pull/406"),
            ("openai", "skills", 406),
        )

    def test_current_pr_ref_uses_pr_url_not_head_repository(self) -> None:
        response = {
            "number": 406,
            "url": "https://github.com/openai/skills/pull/406",
            "headRepositoryOwner": {"login": "TheCookieLab"},
            "headRepository": {"name": "skills"},
        }

        with patch.object(fetch_comments, "gh_pr_view_json", return_value=response):
            self.assertEqual(fetch_comments.get_current_pr_ref(), ("openai", "skills", 406))


if __name__ == "__main__":
    unittest.main()
