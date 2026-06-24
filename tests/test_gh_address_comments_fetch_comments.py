from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / ".curated"
    / "gh-address-comments"
    / "scripts"
    / "fetch_comments.py"
)


spec = importlib.util.spec_from_file_location("fetch_comments", SCRIPT_PATH)
assert spec is not None
fetch_comments = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(fetch_comments)


class GetCurrentPrRefTest(unittest.TestCase):
    def test_parses_pr_url(self) -> None:
        self.assertEqual(
            fetch_comments.parse_pr_url("https://github.com/openai/skills/pull/495"),
            ("openai", "skills", 495),
        )

    def test_uses_base_repository_from_pr_url_for_fork_prs(self) -> None:
        with patch.object(
            fetch_comments,
            "gh_pr_view_json",
            return_value={
                "number": 7582,
                "url": "https://github.com/JanDeDobbeleer/oh-my-posh/pull/7582",
                "headRepositoryOwner": {"login": "Nick2bad4u"},
                "headRepository": {"name": "oh-my-posh"},
            },
        ) as gh_pr_view_json:
            self.assertEqual(
                fetch_comments.get_current_pr_ref(),
                ("JanDeDobbeleer", "oh-my-posh", 7582),
            )
            gh_pr_view_json.assert_called_once_with("number,url")

    def test_rejects_unexpected_pr_url_shape(self) -> None:
        with self.assertRaises(RuntimeError):
            fetch_comments.parse_pr_url("https://github.com/openai/skills/issues/495")


if __name__ == "__main__":
    unittest.main()
