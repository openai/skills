import unittest
from unittest.mock import patch

from fetch_comments import get_current_pr_ref, parse_pr_url


class ParsePrUrlTest(unittest.TestCase):
    def test_parses_base_repo_pr_url(self) -> None:
        self.assertEqual(
            parse_pr_url("https://github.com/JanDeDobbeleer/oh-my-posh/pull/7582"),
            ("JanDeDobbeleer", "oh-my-posh", 7582),
        )

    def test_rejects_non_pr_url(self) -> None:
        with self.assertRaises(RuntimeError):
            parse_pr_url("https://github.com/Nick2bad4u/oh-my-posh")

    def test_get_current_pr_ref_uses_base_repo_url(self) -> None:
        with patch(
            "fetch_comments.gh_pr_view_json",
            return_value={"url": "https://github.com/base-owner/base-repo/pull/42"},
        ):
            self.assertEqual(get_current_pr_ref(), ("base-owner", "base-repo", 42))


if __name__ == "__main__":
    unittest.main()
