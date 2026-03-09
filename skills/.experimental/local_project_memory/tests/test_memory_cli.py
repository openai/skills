from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "memory_cli.py"


def base_mu(
  mu_id: str,
  title: str,
  summary: str,
  *,
  mu_type: str = "ARCH_DECISION",
  tags: list[str] | None = None,
  hints: list[str] | None = None,
  content: dict[str, object] | None = None,
) -> dict[str, object]:
  return {
    "id": mu_id,
    "type": mu_type,
    "title": title,
    "summary": summary,
    "content": content or {"decision": title, "rationale": summary},
    "tags": tags or [],
    "retrieval_hints": hints or [],
  }


class MemoryCliTest(unittest.TestCase):
  def setUp(self) -> None:
    self.tempdir = tempfile.TemporaryDirectory()
    self.cwd = Path(self.tempdir.name)
    self.env = os.environ.copy()
    self.global_dir = self.cwd / "global-memory"
    self.env["LOCAL_PROJECT_MEMORY_GLOBAL_DIR"] = str(self.global_dir)
    self.run_cli("init")

  def tearDown(self) -> None:
    self.tempdir.cleanup()

  def run_cli(self, *args: str, input_text: str | None = None) -> object:
    result = subprocess.run(
      [sys.executable, str(SCRIPT_PATH), *args],
      cwd=self.cwd,
      env=self.env,
      input=input_text,
      text=True,
      capture_output=True,
      check=False,
    )
    if result.returncode != 0:
      raise AssertionError(f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}")
    return json.loads(result.stdout)

  def upsert(self, mu: dict[str, object], *extra_args: str) -> object:
    return self.run_cli("upsert", *extra_args, "-", input_text=json.dumps(mu))

  def seed_auth_cluster(self) -> None:
    self.upsert(
      base_mu(
        "auth-jwt-v1",
        "JWT authentication for API",
        "Use JWT tokens for API login and authentication",
        tags=["auth", "jwt", "api"],
        hints=["login", "token", "authentication"],
        content={"decision": "jwt auth", "rationale": "stateless api"},
      )
    )
    self.upsert(
      base_mu(
        "auth-jwt-v2",
        "JWT authentication for service API",
        "Use JWT access tokens for API authentication and login",
        tags=["auth", "jwt", "api"],
        hints=["login", "token", "authentication"],
        content={"decision": "jwt auth", "rationale": "stateless api"},
      )
    )
    self.upsert(
      base_mu(
        "auth-session-v1",
        "Session authentication for admin",
        "Use session login flow for admin authentication",
        tags=["auth", "session", "admin"],
        hints=["login", "authentication", "session"],
        content={"decision": "session auth", "rationale": "admin console"},
      )
    )

  def test_search_compact_includes_neighborhood_even_with_select(self) -> None:
    self.seed_auth_cluster()

    results = self.run_cli("search", "authentication", "--select", "id,title")
    self.assertGreaterEqual(len(results), 1)
    auth_jwt = next(item for item in results if item["id"] == "auth-jwt-v1")
    self.assertIn("neighborhood", auth_jwt)
    self.assertTrue(auth_jwt["neighborhood"])
    self.assertEqual(auth_jwt["neighborhood"][0]["id"], "auth-jwt-v2")

  def test_tiny_view_omits_neighborhood_by_default(self) -> None:
    self.seed_auth_cluster()

    results = self.run_cli("search", "authentication", "--view", "tiny")
    self.assertGreaterEqual(len(results), 1)
    self.assertNotIn("neighborhood", results[0])

  def test_dedupe_returns_unique_pair(self) -> None:
    self.seed_auth_cluster()

    pairs = self.run_cli("dedupe", "--k", "10")
    self.assertEqual(len(pairs), 1)
    pair = pairs[0]
    self.assertEqual({pair["source_id"], pair["target_id"]}, {"auth-jwt-v1", "auth-jwt-v2"})

  def test_relink_removes_stale_links_after_edit(self) -> None:
    self.seed_auth_cluster()
    related_before = self.run_cli("related", "auth-jwt-v1", "--k", "10")
    self.assertTrue(any(item["id"] == "auth-jwt-v2" for item in related_before))

    self.upsert(
      base_mu(
        "auth-jwt-v1",
        "Payments ledger retention",
        "Retention workflow for finance ledgers and audit archive",
        mu_type="WORKFLOW",
        tags=["finance", "ledger", "retention"],
        hints=["archive", "finance", "retention"],
        content={"steps": "archive ledger", "cadence": "monthly"},
      )
    )

    self.run_cli("relink", "--all")
    related_after = self.run_cli("related", "auth-jwt-v1", "--k", "10")
    self.assertFalse(any(item["id"] == "auth-jwt-v2" for item in related_after))

  def test_deprecate_and_vacuum_cleanup_links(self) -> None:
    self.seed_auth_cluster()

    self.run_cli("deprecate", "auth-jwt-v2", "--replaced-by", "auth-jwt-v1")
    search_results = self.run_cli("search", "authentication")
    neighborhoods = [item.get("neighborhood", []) for item in search_results]
    flat_ids = {entry["id"] for group in neighborhoods for entry in group}
    self.assertNotIn("auth-jwt-v2", flat_ids)

    self.run_cli("vacuum")
    stats = self.run_cli("stats")
    self.assertEqual(stats["counts"]["deprecated"], 0)

  def test_global_namespace_isolation(self) -> None:
    shared_mu = base_mu(
      "workflow-auth",
      "Shared auth workflow",
      "Authentication workflow guidance for login and tokens",
      mu_type="WORKFLOW",
      tags=["auth", "workflow"],
      hints=["login", "token"],
      content={"steps": ["login", "refresh"]},
    )
    self.upsert(shared_mu, "--scope", "global", "--namespace", "user:alpha")
    self.upsert(
      base_mu(
        "workflow-auth",
        "Billing auth workflow",
        "Billing namespace workflow for invoices",
        mu_type="WORKFLOW",
        tags=["billing", "workflow"],
        hints=["invoice", "billing"],
        content={"steps": ["bill", "reconcile"]},
      ),
      "--scope",
      "global",
      "--namespace",
      "user:beta",
    )

    alpha_results = self.run_cli("search", "authentication", "--scope", "global", "--namespace", "user:alpha")
    beta_results = self.run_cli("search", "billing", "--scope", "global", "--namespace", "user:beta")
    self.assertEqual([item["id"] for item in alpha_results], ["workflow-auth"])
    self.assertEqual([item["id"] for item in beta_results], ["workflow-auth"])


if __name__ == "__main__":
  unittest.main()
