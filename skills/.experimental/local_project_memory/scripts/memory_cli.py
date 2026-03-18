#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MU_SCHEMA = "nh.memory.mu"
MU_SCHEMA_VERSION = 1
MAX_JSON_CHARS = 50_000
MEMORY_DB_DIR = ".memory"
GLOBAL_MEMORY_ENV = "LOCAL_PROJECT_MEMORY_GLOBAL_DIR"
DEFAULT_GLOBAL_MEMORY_DIR = Path.home() / ".local" / "share" / "local_project_memory" / "global"
SIMILARITY_LINK_TYPES = {"similar", "duplicate_candidate"}
LINK_TYPES = SIMILARITY_LINK_TYPES | {"related", "supersedes"}
MAX_LINK_CANDIDATES = 15
MAX_STORED_LINKS = 5
DEFAULT_NEIGHBORS_K = 3

MU_TYPES = {
  "ARCH_DECISION",
  "INTERFACE_SPEC",
  "CONSTRAINTS",
  "GLOSSARY",
  "WORKFLOW",
  "KNOWN_ISSUE",
  "TASK_CONTEXT",
}

SECRET_PATTERNS = [
  "API_KEY",
  "PRIVATE_KEY",
  "SECRET_KEY",
  "BEARER",
  "-----BEGIN",
]

VIEW_FIELDS = {
  "tiny": ["id", "type", "title", "validity.status", "updated_at"],
  "compact": [
    "id",
    "type",
    "title",
    "validity.status",
    "updated_at",
    "summary",
    "tags",
  ],
  "full": None,
}


def now_iso() -> str:
  return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def emit_json(payload: Any) -> None:
  print(json.dumps(payload, ensure_ascii=False))


def fail(message: str, code: int = 1) -> None:
  print(message, file=sys.stderr)
  sys.exit(code)


def find_memory_dir(start: Path) -> Path | None:
  current = start.resolve()
  while True:
    memory_dir = current / MEMORY_DB_DIR
    if memory_dir.exists() and memory_dir.is_dir():
      return memory_dir
    if current.parent == current:
      return None
    current = current.parent


def resolve_scope(args: argparse.Namespace) -> str:
  scope = getattr(args, "scope", "project")
  if scope not in {"project", "global"}:
    fail(f"Invalid --scope: '{scope}'. Must be 'project' or 'global'.")
  return scope


def resolve_namespace(args: argparse.Namespace) -> str | None:
  namespace = getattr(args, "namespace", None)
  if namespace is None:
    return None
  namespace = namespace.strip()
  if not namespace:
    fail("Invalid --namespace: expected non-empty string.")
  return namespace


def require_namespace(args: argparse.Namespace) -> str:
  namespace = resolve_namespace(args)
  if not namespace:
    fail("Global scope requires --namespace (example: --namespace user:git).")
  return namespace


def global_memory_root() -> Path:
  raw = os.environ.get(GLOBAL_MEMORY_ENV)
  if raw:
    return Path(raw).expanduser().resolve()
  return DEFAULT_GLOBAL_MEMORY_DIR


def namespace_db_path(namespace: str) -> Path:
  _ = namespace
  return global_memory_root() / "memory.db"


def storage_id_for(scope: str, namespace: str | None, mu_id: str) -> str:
  if scope == "global":
    if not namespace:
      fail("Global scope requires --namespace.")
    return f"ns:{namespace}::{mu_id}"
  return mu_id


def storage_id_prefix(scope: str, namespace: str | None) -> str | None:
  if scope != "global":
    return None
  if not namespace:
    fail("Global scope requires --namespace.")
  return f"ns:{namespace}::"


def external_id_from_storage(scope: str, namespace: str | None, storage_id: str) -> str:
  prefix = storage_id_prefix(scope, namespace)
  if prefix and storage_id.startswith(prefix):
    return storage_id[len(prefix):]
  return storage_id


def git_root(start: Path) -> Path | None:
  try:
    result = subprocess.run(
      ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
      check=True,
      capture_output=True,
      text=True,
    )
  except (subprocess.CalledProcessError, FileNotFoundError):
    return None

  output = result.stdout.strip()
  if not output:
    return None
  return Path(output)


def resolve_project_name(cwd: Path) -> str:
  memory_dir = find_memory_dir(cwd)
  if memory_dir:
    return memory_dir.parent.name

  root = git_root(cwd)
  if root:
    return root.name

  fail("No project context found. Run 'scripts/memory_cli.py init' in your project root.")


def resolve_project_root(cwd: Path) -> Path:
  memory_dir = find_memory_dir(cwd)
  if memory_dir:
    return memory_dir.parent

  root = git_root(cwd)
  if root:
    return root

  fail("No project context found. Run 'scripts/memory_cli.py init' in your project root.")


def target_label(scope: str, namespace: str | None, project: str | None) -> str:
  if scope == "global":
    return f"global:{namespace}"
  if project is None:
    fail("Internal error: missing project label for project scope.")
  return project


def db_path_for(scope: str, namespace: str | None, project: str | None) -> Path:
  if scope == "global":
    if not namespace:
      fail("Global scope requires --namespace.")
    return namespace_db_path(namespace)

  cwd = Path.cwd()
  project_root = resolve_project_root(cwd)
  memory_dir = project_root / MEMORY_DB_DIR
  return memory_dir / "memory.db"


def open_db(scope: str, namespace: str | None, project: str | None) -> sqlite3.Connection:
  db_path = db_path_for(scope, namespace, project)
  db_path.parent.mkdir(parents=True, exist_ok=True)
  conn = sqlite3.connect(db_path)
  conn.row_factory = sqlite3.Row
  conn.execute("PRAGMA journal_mode=WAL")
  conn.execute("PRAGMA synchronous=NORMAL")
  conn.execute("PRAGMA busy_timeout=2000")
  conn.execute("PRAGMA foreign_keys=ON")
  return conn


def create_schema(conn: sqlite3.Connection) -> None:
  conn.executescript(
    """
    CREATE TABLE IF NOT EXISTS memory_units (
      id TEXT PRIMARY KEY,
      type TEXT NOT NULL,
      title TEXT NOT NULL,
      summary TEXT NOT NULL,
      content_json TEXT NOT NULL,
      tags_json TEXT NOT NULL,
      hints_json TEXT NOT NULL,
      provenance_json TEXT,
      validity_json TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );

    CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
      id UNINDEXED,
      title,
      summary,
      tags,
      hints,
      content,
      type
    );

    CREATE TABLE IF NOT EXISTS memory_links (
      source_id TEXT NOT NULL,
      target_id TEXT NOT NULL,
      link_type TEXT NOT NULL,
      score REAL NOT NULL,
      reason_json TEXT NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      PRIMARY KEY (source_id, target_id),
      FOREIGN KEY (source_id) REFERENCES memory_units(id) ON DELETE CASCADE,
      FOREIGN KEY (target_id) REFERENCES memory_units(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS memory_links_source_idx
    ON memory_links(source_id, link_type, score DESC);

    CREATE INDEX IF NOT EXISTS memory_links_target_idx
    ON memory_links(target_id, link_type, score DESC);

    CREATE TRIGGER IF NOT EXISTS memory_units_ai AFTER INSERT ON memory_units BEGIN
      INSERT INTO memory_fts(id, title, summary, tags, hints, content, type)
      VALUES (
        NEW.id,
        NEW.title,
        NEW.summary,
        NEW.tags_json,
        NEW.hints_json,
        NEW.content_json,
        NEW.type
      );
    END;

    CREATE TRIGGER IF NOT EXISTS memory_units_au AFTER UPDATE ON memory_units BEGIN
      DELETE FROM memory_fts WHERE id = OLD.id;
      INSERT INTO memory_fts(id, title, summary, tags, hints, content, type)
      VALUES (
        NEW.id,
        NEW.title,
        NEW.summary,
        NEW.tags_json,
        NEW.hints_json,
        NEW.content_json,
        NEW.type
      );
    END;

    CREATE TRIGGER IF NOT EXISTS memory_units_ad AFTER DELETE ON memory_units BEGIN
      DELETE FROM memory_fts WHERE id = OLD.id;
    END;
    """
  )
  conn.commit()


def parse_json_field(raw: str | None, default: Any) -> Any:
  if raw is None:
    return default
  try:
    return json.loads(raw)
  except json.JSONDecodeError:
    return default


def validity_from_mu(mu: dict[str, Any]) -> dict[str, Any]:
  return mu.get("validity", {"status": "active", "replaced_by": None})


def is_deprecated_mu(mu: dict[str, Any]) -> bool:
  validity = validity_from_mu(mu)
  return str(validity.get("status", "active")).lower() == "deprecated"


def row_to_mu(
  row: sqlite3.Row,
  *,
  scope: str = "project",
  namespace: str | None = None,
) -> dict[str, Any]:
  mu: dict[str, Any] = {
    "schema": MU_SCHEMA,
    "schema_version": MU_SCHEMA_VERSION,
    "id": external_id_from_storage(scope, namespace, row["id"]),
    "type": row["type"],
    "title": row["title"],
    "summary": row["summary"],
    "content": parse_json_field(row["content_json"], {}),
    "tags": parse_json_field(row["tags_json"], []),
    "retrieval_hints": parse_json_field(row["hints_json"], []),
    "validity": parse_json_field(
      row["validity_json"], {"status": "active", "replaced_by": None}
    ),
    "updated_at": row["updated_at"],
  }

  provenance = parse_json_field(row["provenance_json"], None)
  if provenance:
    mu["provenance"] = provenance

  return mu


def split_select(select: str | None) -> list[str] | None:
  if not select:
    return None
  paths = [p.strip() for p in select.split(",") if p.strip()]
  return paths or None


def set_nested(target: dict[str, Any], path: str, value: Any) -> None:
  parts = path.split(".")
  cursor = target
  for part in parts[:-1]:
    existing = cursor.get(part)
    if not isinstance(existing, dict):
      existing = {}
      cursor[part] = existing
    cursor = existing
  cursor[parts[-1]] = value


def get_nested(source: dict[str, Any], path: str) -> tuple[bool, Any]:
  parts = path.split(".")
  cursor: Any = source
  for part in parts:
    if not isinstance(cursor, dict) or part not in cursor:
      return (False, None)
    cursor = cursor[part]
  return (True, cursor)


def project_mu(mu: dict[str, Any], view: str, select: str | None) -> dict[str, Any]:
  paths = split_select(select)
  if paths is None:
    if view == "full":
      return mu
    paths = VIEW_FIELDS[view]

  projected: dict[str, Any] = {
    "schema": mu["schema"],
    "schema_version": mu["schema_version"],
  }

  for path in paths or []:
    found, value = get_nested(mu, path)
    if found:
      set_nested(projected, path, value)

  return projected


def normalize_string_list(value: Any, field_name: str) -> list[str]:
  if value is None:
    return []
  if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
    fail(f"Invalid '{field_name}': expected an array of strings.")
  return value


def has_secrets(payload_text: str) -> bool:
  upper = payload_text.upper()
  return any(pattern in upper for pattern in SECRET_PATTERNS)


def validate_mu(mu: dict[str, Any]) -> dict[str, Any]:
  if not isinstance(mu, dict):
    fail("Invalid MU: expected JSON object.")

  required_fields = ["id", "type", "title", "summary", "content"]
  for field in required_fields:
    if field not in mu:
      fail(f"Missing required field: '{field}'.")

  mu_id = mu["id"]
  if not isinstance(mu_id, str) or not re.fullmatch(r"[A-Za-z0-9._:-]+", mu_id):
    fail("Invalid 'id': use slug format with no spaces.")

  mu_type = mu["type"]
  if mu_type not in MU_TYPES:
    valid_types = ", ".join(sorted(MU_TYPES))
    fail(f"Invalid 'type': '{mu_type}'. Must be one of: {valid_types}")

  title = mu["title"]
  summary = mu["summary"]
  if not isinstance(title, str) or not title.strip():
    fail("Invalid 'title': expected non-empty string.")
  if not isinstance(summary, str) or not summary.strip():
    fail("Invalid 'summary': expected non-empty string.")

  content = mu["content"]
  if not isinstance(content, dict):
    fail("Invalid 'content': expected JSON object.")

  tags = normalize_string_list(mu.get("tags", []), "tags")
  hints = normalize_string_list(mu.get("retrieval_hints", []), "retrieval_hints")

  provenance = mu.get("provenance")
  if provenance is not None and not isinstance(provenance, dict):
    fail("Invalid 'provenance': expected object.")

  validity = mu.get("validity", {"status": "active", "replaced_by": None})
  if not isinstance(validity, dict):
    fail("Invalid 'validity': expected object.")

  status = validity.get("status", "active")
  if status not in {"active", "deprecated"}:
    fail("Invalid 'validity.status': expected 'active' or 'deprecated'.")
  replaced_by = validity.get("replaced_by")
  if status == "deprecated" and (not isinstance(replaced_by, str) or not replaced_by.strip()):
    fail("Invalid 'validity': deprecated items require 'replaced_by'.")

  summary_len = len(summary)
  content_text = json.dumps(content, ensure_ascii=False)
  if summary_len + len(content_text) > MAX_JSON_CHARS:
    fail("Payload too large: summary + content exceeds 50000 characters.")

  serialized_all = json.dumps(mu, ensure_ascii=False)
  if has_secrets(serialized_all):
    fail("Rejected: MU appears to contain secret material.")

  updated_at = mu.get("updated_at")
  if not isinstance(updated_at, str) or not updated_at.strip():
    updated_at = now_iso()

  normalized = {
    "schema": MU_SCHEMA,
    "schema_version": MU_SCHEMA_VERSION,
    "id": mu_id,
    "type": mu_type,
    "title": title,
    "summary": summary,
    "content": content,
    "tags": tags,
    "retrieval_hints": hints,
    "validity": {
      "status": status,
      "replaced_by": replaced_by if status == "deprecated" else None,
    },
    "updated_at": updated_at,
  }
  if provenance is not None:
    normalized["provenance"] = provenance

  return normalized


def ensure_ready(scope: str, namespace: str | None, project: str | None) -> sqlite3.Connection:
  conn = open_db(scope, namespace, project)
  create_schema(conn)
  return conn


def fetch_mu(conn: sqlite3.Connection, mu_id: str) -> dict[str, Any] | None:
  row = conn.execute(
    "SELECT * FROM memory_units WHERE id = ?",
    (mu_id,),
  ).fetchone()
  if row is None:
    return None
  return row_to_mu(row)


def resolve_storage_target(args: argparse.Namespace, *, allow_project_autoresolve: bool = True) -> dict[str, Any]:
  scope = resolve_scope(args)
  namespace = resolve_namespace(args)
  project = None
  if scope == "global":
    namespace = require_namespace(args)
    label = target_label(scope, namespace, None)
  elif allow_project_autoresolve:
    project = resolve_project_name(Path.cwd())
    label = target_label(scope, None, project)
  else:
    label = "project:<pending-init>"
  return {
    "scope": scope,
    "namespace": namespace,
    "project": project,
    "label": label,
  }


def run_query(target: dict[str, Any]) -> tuple[sqlite3.Connection, Path]:
  conn = ensure_ready(target["scope"], target["namespace"], target["project"])
  return conn, db_path_for(target["scope"], target["namespace"], target["project"])


def fetch_mu_for_target(conn: sqlite3.Connection, target: dict[str, Any], mu_id: str) -> dict[str, Any] | None:
  storage_id = storage_id_for(target["scope"], target["namespace"], mu_id)
  row = conn.execute(
    "SELECT * FROM memory_units WHERE id = ?",
    (storage_id,),
  ).fetchone()
  if row is None:
    return None
  return row_to_mu(row, scope=target["scope"], namespace=target["namespace"])


def tokenize_text(value: str) -> list[str]:
  return re.findall(r"[a-z0-9]+", value.lower())


def fts_or_query_from_text(value: str) -> str:
  tokens = tokenize_text(value)
  unique_tokens: list[str] = []
  seen: set[str] = set()
  for token in tokens:
    if token in seen:
      continue
    unique_tokens.append(token)
    seen.add(token)
  if not unique_tokens:
    fail("Invalid search query: expected at least one alphanumeric token.")
  return " OR ".join(unique_tokens)


def mu_search_text(mu: dict[str, Any]) -> str:
  content = mu.get("content", {})
  parts = [
    mu.get("title", ""),
    mu.get("summary", ""),
    " ".join(mu.get("tags", [])),
    " ".join(mu.get("retrieval_hints", [])),
  ]
  if isinstance(content, dict):
    parts.append(" ".join(str(key) for key in content.keys()))
  return " ".join(part for part in parts if part)


def token_counter_for_mu(mu: dict[str, Any]) -> Counter[str]:
  return Counter(tokenize_text(mu_search_text(mu)))


def jaccard_strings(left: list[str], right: list[str]) -> float:
  left_set = {item.strip().lower() for item in left if item.strip()}
  right_set = {item.strip().lower() for item in right if item.strip()}
  if not left_set or not right_set:
    return 0.0
  union = left_set | right_set
  if not union:
    return 0.0
  return len(left_set & right_set) / len(union)


def weighted_token_overlap(left: Counter[str], right: Counter[str]) -> float:
  if not left or not right:
    return 0.0
  common = sum(min(left[token], right[token]) for token in left.keys() & right.keys())
  total = sum(left.values()) + sum(right.values()) - common
  if total <= 0:
    return 0.0
  return common / total


def similarity_breakdown(anchor: dict[str, Any], candidate: dict[str, Any]) -> tuple[float, dict[str, Any]]:
  text_overlap = weighted_token_overlap(token_counter_for_mu(anchor), token_counter_for_mu(candidate))
  tag_overlap = jaccard_strings(anchor.get("tags", []), candidate.get("tags", []))
  hint_overlap = jaccard_strings(anchor.get("retrieval_hints", []), candidate.get("retrieval_hints", []))

  anchor_keys = sorted(str(key) for key in anchor.get("content", {}).keys())
  candidate_keys = sorted(str(key) for key in candidate.get("content", {}).keys())
  content_key_overlap = jaccard_strings(anchor_keys, candidate_keys)
  same_type = 1.0 if anchor.get("type") == candidate.get("type") else 0.0

  score = (
    0.35 * text_overlap
    + 0.25 * tag_overlap
    + 0.20 * hint_overlap
    + 0.10 * same_type
    + 0.10 * content_key_overlap
  )
  reason = {
    "matched_tags": sorted(set(anchor.get("tags", [])) & set(candidate.get("tags", []))),
    "matched_hints": sorted(set(anchor.get("retrieval_hints", [])) & set(candidate.get("retrieval_hints", []))),
    "same_type": bool(same_type),
    "score_components": {
      "text_overlap": round(text_overlap, 6),
      "tag_overlap": round(tag_overlap, 6),
      "hint_overlap": round(hint_overlap, 6),
      "same_type": round(same_type, 6),
      "content_key_overlap": round(content_key_overlap, 6),
    },
  }
  return score, reason


def classify_link(score: float) -> str | None:
  if score >= 0.85:
    return "duplicate_candidate"
  if score >= 0.60:
    return "similar"
  return None


def candidate_query_for_mu(mu: dict[str, Any]) -> str | None:
  tokens = tokenize_text(mu_search_text(mu))
  unique_tokens: list[str] = []
  seen: set[str] = set()
  for token in tokens:
    if token not in seen:
      unique_tokens.append(token)
      seen.add(token)
    if len(unique_tokens) >= 12:
      break
  if not unique_tokens:
    return None
  return " OR ".join(unique_tokens)


def active_status_sql(column_name: str) -> str:
  return f"LOWER(COALESCE(json_extract({column_name}, '$.status'), 'active')) != 'deprecated'"


def deprecated_status_sql(column_name: str) -> str:
  return f"LOWER(COALESCE(json_extract({column_name}, '$.status'), 'active')) = 'deprecated'"


def storage_scope_clause(target: dict[str, Any], id_column: str) -> tuple[list[str], list[Any]]:
  prefix = storage_id_prefix(target["scope"], target["namespace"])
  if prefix:
    return ([f"{id_column} LIKE ?"], [f"{prefix}%"])
  return ([], [])


def candidate_rows_for_mu(conn: sqlite3.Connection, target: dict[str, Any], storage_id: str, mu: dict[str, Any]) -> list[sqlite3.Row]:
  query = candidate_query_for_mu(mu)
  if not query:
    return []

  where_clauses = ["memory_fts MATCH ?", "m.id != ?", active_status_sql("m.validity_json")]
  params: list[Any] = [query, storage_id]
  scope_clauses, scope_params = storage_scope_clause(target, "m.id")
  where_clauses.extend(scope_clauses)
  params.extend(scope_params)

  sql = f"""
    SELECT m.*
    FROM memory_fts f
    JOIN memory_units m ON m.id = f.id
    WHERE {' AND '.join(where_clauses)}
    ORDER BY bm25(memory_fts), m.updated_at DESC
    LIMIT ?
  """
  params.append(MAX_LINK_CANDIDATES)
  return conn.execute(sql, params).fetchall()


def delete_similarity_links_for_mu(conn: sqlite3.Connection, storage_id: str) -> None:
  placeholders = ", ".join("?" for _ in sorted(SIMILARITY_LINK_TYPES))
  params = [storage_id, storage_id, *sorted(SIMILARITY_LINK_TYPES)]
  conn.execute(
    f"""
    DELETE FROM memory_links
    WHERE (source_id = ? OR target_id = ?)
      AND link_type IN ({placeholders})
    """,
    params,
  )


def upsert_link_pair(
  conn: sqlite3.Connection,
  source_id: str,
  target_id: str,
  link_type: str,
  score: float,
  reason: dict[str, Any],
  timestamp: str,
) -> None:
  payload = (
    source_id,
    target_id,
    link_type,
    score,
    json.dumps(reason, ensure_ascii=False),
    timestamp,
    timestamp,
  )
  conn.execute(
    """
    INSERT INTO memory_links(
      source_id, target_id, link_type, score, reason_json, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(source_id, target_id) DO UPDATE SET
      link_type=excluded.link_type,
      score=excluded.score,
      reason_json=excluded.reason_json,
      updated_at=excluded.updated_at
    """,
    payload,
  )


def recompute_links_for_mu(
  conn: sqlite3.Connection,
  target: dict[str, Any],
  storage_id: str,
  mu: dict[str, Any],
) -> list[dict[str, Any]]:
  delete_similarity_links_for_mu(conn, storage_id)
  rows = candidate_rows_for_mu(conn, target, storage_id, mu)
  candidates: list[dict[str, Any]] = []
  for row in rows:
    candidate_mu = row_to_mu(row, scope=target["scope"], namespace=target["namespace"])
    score, reason = similarity_breakdown(mu, candidate_mu)
    link_type = classify_link(score)
    if link_type is None:
      continue
    candidates.append(
      {
        "storage_id": row["id"],
        "mu": candidate_mu,
        "score": score,
        "link_type": link_type,
        "reason": reason,
      }
    )

  candidates.sort(key=lambda item: (-item["score"], item["mu"]["updated_at"], item["mu"]["id"]))
  chosen = candidates[:MAX_STORED_LINKS]
  timestamp = now_iso()

  for item in chosen:
    reason = {
      **item["reason"],
      "generated_from": "upsert_similarity",
      "anchor_id": mu["id"],
      "candidate_id": item["mu"]["id"],
    }
    reverse_reason = {
      **reason,
      "anchor_id": item["mu"]["id"],
      "candidate_id": mu["id"],
    }
    upsert_link_pair(conn, storage_id, item["storage_id"], item["link_type"], item["score"], reason, timestamp)
    upsert_link_pair(conn, item["storage_id"], storage_id, item["link_type"], item["score"], reverse_reason, timestamp)

  return chosen


def query_score_by_storage_id(
  conn: sqlite3.Connection,
  target: dict[str, Any],
  query: str,
  storage_ids: list[str],
  *,
  include_deprecated: bool,
) -> dict[str, float]:
  if not storage_ids:
    return {}

  placeholders = ", ".join("?" for _ in storage_ids)
  where_clauses = ["memory_fts MATCH ?", f"m.id IN ({placeholders})"]
  params: list[Any] = [query, *storage_ids]
  scope_clauses, scope_params = storage_scope_clause(target, "m.id")
  where_clauses.extend(scope_clauses)
  params.extend(scope_params)
  if not include_deprecated:
    where_clauses.append(active_status_sql("m.validity_json"))

  sql = f"""
    SELECT m.id, bm25(memory_fts) AS rank
    FROM memory_fts f
    JOIN memory_units m ON m.id = f.id
    WHERE {' AND '.join(where_clauses)}
  """
  rows = conn.execute(sql, params).fetchall()
  if not rows:
    return {}
  raw_scores = {row["id"]: float(-row["rank"]) for row in rows}
  minimum = min(raw_scores.values())
  maximum = max(raw_scores.values())
  if maximum == minimum:
    return {storage_id: 1.0 for storage_id in raw_scores}
  scores: dict[str, float] = {}
  for row in rows:
    raw_score = raw_scores[row["id"]]
    scores[row["id"]] = (raw_score - minimum) / (maximum - minimum)
  return scores


def neighborhood_for_mu(
  conn: sqlite3.Connection,
  target: dict[str, Any],
  storage_id: str,
  query: str,
  neighbors_k: int,
  include_deprecated: bool,
) -> list[dict[str, Any]]:
  if neighbors_k <= 0:
    return []

  params: list[Any] = [storage_id]
  where_clauses = ["l.source_id = ?"]
  scope_clauses, scope_params = storage_scope_clause(target, "m.id")
  where_clauses.extend(scope_clauses)
  params.extend(scope_params)
  if not include_deprecated:
    where_clauses.append(active_status_sql("m.validity_json"))

  sql = f"""
    SELECT l.target_id, l.link_type, l.score, l.reason_json, m.*
    FROM memory_links l
    JOIN memory_units m ON m.id = l.target_id
    WHERE {' AND '.join(where_clauses)}
    ORDER BY l.score DESC, m.updated_at DESC
  """
  rows = conn.execute(sql, params).fetchall()
  if not rows:
    return []

  target_ids = [row["target_id"] for row in rows]
  query_scores = query_score_by_storage_id(
    conn,
    target,
    query,
    target_ids,
    include_deprecated=include_deprecated,
  )

  ranked: list[dict[str, Any]] = []
  for row in rows:
    candidate_mu = row_to_mu(row, scope=target["scope"], namespace=target["namespace"])
    link_score = float(row["score"])
    query_score = query_scores.get(row["target_id"], 0.0)
    combined_score = 0.6 * query_score + 0.4 * link_score
    ranked.append(
      {
        "id": candidate_mu["id"],
        "type": candidate_mu["type"],
        "title": candidate_mu["title"],
        "summary": candidate_mu["summary"],
        "validity": {"status": validity_from_mu(candidate_mu).get("status", "active")},
        "link_type": row["link_type"],
        "link_score": round(link_score, 6),
        "query_score": round(query_score, 6),
        "combined_score": round(combined_score, 6),
      }
    )

  ranked.sort(key=lambda item: (-item["combined_score"], -item["query_score"], -item["link_score"], item["id"]))
  return ranked[:neighbors_k]


def cmd_init(args: argparse.Namespace) -> None:
  target = resolve_storage_target(args, allow_project_autoresolve=False)
  cwd = Path.cwd()

  if target["scope"] == "project":
    memory_dir = cwd / MEMORY_DB_DIR
    if memory_dir.exists() and not memory_dir.is_dir():
      fail(f"Invalid {MEMORY_DB_DIR}: expected a directory.")
    memory_dir.mkdir(parents=True, exist_ok=True)
    target["project"] = cwd.name
    target["label"] = target_label("project", None, target["project"])
  else:
    target["namespace"] = require_namespace(args)
    target["label"] = target_label("global", target["namespace"], None)

  conn = ensure_ready(target["scope"], target["namespace"], target["project"])
  conn.close()

  db_path = db_path_for(target["scope"], target["namespace"], target["project"])
  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "db_path": str(db_path.resolve()),
    }
  )


def cmd_upsert(args: argparse.Namespace) -> None:
  file_or_dash = args.file_or_dash
  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  try:
    if file_or_dash == "-":
      raw = sys.stdin.read()
    else:
      raw = Path(file_or_dash).read_text(encoding="utf-8")
  except FileNotFoundError:
    conn.close()
    fail(f"File not found: {file_or_dash}")

  try:
    payload = json.loads(raw)
  except json.JSONDecodeError as exc:
    conn.close()
    fail(f"Invalid JSON: {exc}")

  mu = validate_mu(payload)
  storage_id = storage_id_for(target["scope"], target["namespace"], mu["id"])

  conn.execute(
    """
    INSERT INTO memory_units(
      id, type, title, summary, content_json, tags_json, hints_json,
      provenance_json, validity_json, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
      type=excluded.type,
      title=excluded.title,
      summary=excluded.summary,
      content_json=excluded.content_json,
      tags_json=excluded.tags_json,
      hints_json=excluded.hints_json,
      provenance_json=excluded.provenance_json,
      validity_json=excluded.validity_json,
      updated_at=excluded.updated_at
    """,
    (
      storage_id,
      mu["type"],
      mu["title"],
      mu["summary"],
      json.dumps(mu["content"], ensure_ascii=False),
      json.dumps(mu["tags"], ensure_ascii=False),
      json.dumps(mu["retrieval_hints"], ensure_ascii=False),
      json.dumps(mu["provenance"], ensure_ascii=False) if "provenance" in mu else None,
      json.dumps(mu["validity"], ensure_ascii=False),
      mu["updated_at"],
    ),
  )

  links = []
  if not is_deprecated_mu(mu):
    links = recompute_links_for_mu(conn, target, storage_id, mu)
  else:
    delete_similarity_links_for_mu(conn, storage_id)
  conn.commit()
  conn.close()

  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "id": mu["id"],
      "updated_at": mu["updated_at"],
      "linked_count": len(links),
      "link_ids": [item["mu"]["id"] for item in links],
    }
  )


def cmd_get(args: argparse.Namespace) -> None:
  mu_id = args.mu_id
  view = args.view
  select = args.select
  if view not in VIEW_FIELDS:
    valid_views = ", ".join(sorted(VIEW_FIELDS.keys()))
    fail(f"Invalid --view: '{view}'. Must be one of: {valid_views}")

  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  mu = fetch_mu_for_target(conn, target, mu_id)
  conn.close()

  if mu is None:
    fail(f"Memory unit not found: {mu_id}")

  emit_json(project_mu(mu, view=view, select=select))


def should_include_neighborhood(args: argparse.Namespace, view: str) -> bool:
  if args.include_neighborhood is not None:
    return bool(args.include_neighborhood)
  return view in {"compact", "full"}


def cmd_search(args: argparse.Namespace) -> None:
  query = args.query
  k = args.k
  type = args.type
  tag = args.tag
  include_deprecated = args.include_deprecated
  view = args.view
  select = args.select
  include_neighborhood = should_include_neighborhood(args, view)
  neighbors_k = args.neighbors_k
  if view not in VIEW_FIELDS:
    valid_views = ", ".join(sorted(VIEW_FIELDS.keys()))
    fail(f"Invalid --view: '{view}'. Must be one of: {valid_views}")
  if k <= 0:
    fail("Invalid --k. Must be > 0.")
  if neighbors_k <= 0:
    fail("Invalid --neighbors-k. Must be > 0.")
  if type is not None and type not in MU_TYPES:
    valid_types = ", ".join(sorted(MU_TYPES))
    fail(f"Invalid --type: '{type}'. Must be one of: {valid_types}")
  fts_query = fts_or_query_from_text(query)

  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  where_clauses = ["memory_fts MATCH ?"]
  params: list[Any] = [fts_query]

  prefix = storage_id_prefix(target["scope"], target["namespace"])
  if prefix:
    where_clauses.append("m.id LIKE ?")
    params.append(f"{prefix}%")

  if type:
    where_clauses.append("m.type = ?")
    params.append(type)

  if tag:
    where_clauses.append("LOWER(m.tags_json) LIKE ?")
    params.append(f"%{tag.lower()}%")

  if not include_deprecated:
    where_clauses.append(active_status_sql("m.validity_json"))

  sql = f"""
    SELECT m.*
    FROM memory_fts f
    JOIN memory_units m ON m.id = f.id
    WHERE {' AND '.join(where_clauses)}
    ORDER BY bm25(memory_fts), m.updated_at DESC
    LIMIT ?
  """
  params.append(k)

  rows = conn.execute(sql, params).fetchall()

  results = []
  for row in rows:
    mu = row_to_mu(row, scope=target["scope"], namespace=target["namespace"])
    projected = project_mu(mu, view=view, select=select)
    if include_neighborhood:
      projected["neighborhood"] = neighborhood_for_mu(
        conn,
        target,
        row["id"],
        fts_query,
        neighbors_k,
        include_deprecated,
      )
    results.append(projected)

  conn.close()
  emit_json(results)


def cmd_deprecate(args: argparse.Namespace) -> None:
  mu_id = args.mu_id
  replaced_by = args.replaced_by
  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  mu = fetch_mu_for_target(conn, target, mu_id)
  if mu is None:
    conn.close()
    fail(f"Memory unit not found: {mu_id}")

  validity = mu.get("validity", {})
  validity["status"] = "deprecated"
  validity["replaced_by"] = replaced_by
  updated_at = now_iso()

  storage_id = storage_id_for(target["scope"], target["namespace"], mu_id)
  conn.execute(
    """
    UPDATE memory_units
    SET validity_json = ?, updated_at = ?
    WHERE id = ?
    """,
    (json.dumps(validity, ensure_ascii=False), updated_at, storage_id),
  )
  delete_similarity_links_for_mu(conn, storage_id)
  conn.commit()
  conn.close()

  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "id": mu_id,
      "status": "deprecated",
      "replaced_by": replaced_by,
      "updated_at": updated_at,
    }
  )


def cmd_vacuum(args: argparse.Namespace) -> None:
  dry_run = args.dry_run
  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  rows = conn.execute(
    (
      f"""
      SELECT id FROM memory_units
      WHERE {deprecated_status_sql('validity_json')}
        AND id LIKE ?
      ORDER BY id
      """
      if storage_id_prefix(target["scope"], target["namespace"])
      else
      f"""
      SELECT id FROM memory_units
      WHERE {deprecated_status_sql('validity_json')}
      ORDER BY id
      """
    ),
    ((f"{storage_id_prefix(target['scope'], target['namespace'])}%"),)
    if storage_id_prefix(target["scope"], target["namespace"])
    else (),
  ).fetchall()

  deprecated_ids = [
    external_id_from_storage(target["scope"], target["namespace"], row["id"])
    for row in rows
  ]

  if dry_run:
    conn.close()
    emit_json(
      {
        "ok": True,
        "scope": target["scope"],
        "target": target["label"],
        "namespace": target["namespace"],
        "project": target["project"],
        "dry_run": True,
        "deprecated_count": len(deprecated_ids),
        "would_delete_ids": deprecated_ids[:100],
      }
    )
    return

  deleted_count = len(deprecated_ids)
  prefix = storage_id_prefix(target["scope"], target["namespace"])
  if prefix:
    conn.execute(
      f"""
      DELETE FROM memory_units
      WHERE {deprecated_status_sql('validity_json')}
        AND id LIKE ?
      """,
      (f"{prefix}%",),
    )
  else:
    conn.execute(
      f"""
      DELETE FROM memory_units
      WHERE {deprecated_status_sql('validity_json')}
      """
    )
  conn.commit()
  conn.execute("VACUUM")
  conn.commit()
  conn.close()

  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "dry_run": False,
      "deleted_count": deleted_count,
      "vacuumed": True,
    }
  )


def related_rows(
  conn: sqlite3.Connection,
  target: dict[str, Any],
  storage_id: str,
  *,
  include_deprecated: bool,
  link_type: str | None = None,
  limit: int | None = None,
) -> list[sqlite3.Row]:
  where_clauses = ["l.source_id = ?"]
  params: list[Any] = [storage_id]
  scope_clauses, scope_params = storage_scope_clause(target, "m.id")
  where_clauses.extend(scope_clauses)
  params.extend(scope_params)

  if link_type is not None:
    where_clauses.append("l.link_type = ?")
    params.append(link_type)

  if not include_deprecated:
    where_clauses.append(active_status_sql("m.validity_json"))

  sql = f"""
    SELECT l.target_id, l.link_type, l.score, l.reason_json, l.updated_at AS link_updated_at, m.*
    FROM memory_links l
    JOIN memory_units m ON m.id = l.target_id
    WHERE {' AND '.join(where_clauses)}
    ORDER BY l.score DESC, m.updated_at DESC
  """
  if limit is not None:
    sql += " LIMIT ?"
    params.append(limit)
  return conn.execute(sql, params).fetchall()


def cmd_related(args: argparse.Namespace) -> None:
  if args.k <= 0:
    fail("Invalid --k. Must be > 0.")
  if args.link_type is not None and args.link_type not in LINK_TYPES:
    valid = ", ".join(sorted(LINK_TYPES))
    fail(f"Invalid --link-type: '{args.link_type}'. Must be one of: {valid}")

  target = resolve_storage_target(args)
  conn, _ = run_query(target)
  mu = fetch_mu_for_target(conn, target, args.mu_id)
  if mu is None:
    conn.close()
    fail(f"Memory unit not found: {args.mu_id}")

  storage_id = storage_id_for(target["scope"], target["namespace"], args.mu_id)
  rows = related_rows(
    conn,
    target,
    storage_id,
    include_deprecated=args.include_deprecated,
    link_type=args.link_type,
    limit=args.k,
  )
  results = []
  for row in rows:
    neighbor = row_to_mu(row, scope=target["scope"], namespace=target["namespace"])
    results.append(
      {
        "id": neighbor["id"],
        "type": neighbor["type"],
        "title": neighbor["title"],
        "summary": neighbor["summary"],
        "validity": {"status": validity_from_mu(neighbor).get("status", "active")},
        "link_type": row["link_type"],
        "link_score": round(float(row["score"]), 6),
        "reason": parse_json_field(row["reason_json"], {}),
        "updated_at": neighbor["updated_at"],
      }
    )
  conn.close()
  emit_json(results)


def cmd_dedupe(args: argparse.Namespace) -> None:
  if args.k <= 0:
    fail("Invalid --k. Must be > 0.")

  target = resolve_storage_target(args)
  conn, _ = run_query(target)
  source_scope_clauses, source_scope_params = storage_scope_clause(target, "l.source_id")
  target_scope_clauses, target_scope_params = storage_scope_clause(target, "l.target_id")
  where_clauses = ["l.link_type = 'duplicate_candidate'"]
  params: list[Any] = []
  where_clauses.extend(source_scope_clauses)
  where_clauses.extend(target_scope_clauses)
  params.extend(source_scope_params)
  params.extend(target_scope_params)
  if not args.include_deprecated:
    where_clauses.append(active_status_sql("m1.validity_json"))
    where_clauses.append(active_status_sql("m2.validity_json"))

  sql = f"""
    SELECT l.source_id, l.target_id, l.score, m1.validity_json AS source_validity_json,
           m2.validity_json AS target_validity_json, m1.updated_at AS source_updated_at,
           m2.updated_at AS target_updated_at
    FROM memory_links l
    JOIN memory_units m1 ON m1.id = l.source_id
    JOIN memory_units m2 ON m2.id = l.target_id
    WHERE {' AND '.join(where_clauses)}
    ORDER BY l.score DESC, l.source_id, l.target_id
  """
  rows = conn.execute(sql, params).fetchall()
  seen: set[tuple[str, str]] = set()
  results = []
  for row in rows:
    left = external_id_from_storage(target["scope"], target["namespace"], row["source_id"])
    right = external_id_from_storage(target["scope"], target["namespace"], row["target_id"])
    pair = tuple(sorted((left, right)))
    if pair in seen:
      continue
    seen.add(pair)
    results.append(
      {
        "source_id": pair[0],
        "target_id": pair[1],
        "link_type": "duplicate_candidate",
        "link_score": round(float(row["score"]), 6),
      }
    )
    if len(results) >= args.k:
      break
  conn.close()
  emit_json(results)


def iter_target_storage_ids(conn: sqlite3.Connection, target: dict[str, Any], include_deprecated: bool) -> list[str]:
  where_clauses = ["1 = 1"]
  params: list[Any] = []
  scope_clauses, scope_params = storage_scope_clause(target, "id")
  where_clauses.extend(scope_clauses)
  params.extend(scope_params)
  if not include_deprecated:
    where_clauses.append(active_status_sql("validity_json"))
  rows = conn.execute(
    f"""
    SELECT id
    FROM memory_units
    WHERE {' AND '.join(where_clauses)}
    ORDER BY updated_at DESC, id
    """,
    params,
  ).fetchall()
  return [row["id"] for row in rows]


def cmd_relink(args: argparse.Namespace) -> None:
  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  if args.all:
    storage_ids = iter_target_storage_ids(conn, target, include_deprecated=False)
  else:
    if not args.mu_id:
      conn.close()
      fail("relink requires <mu_id> or --all.")
    mu = fetch_mu_for_target(conn, target, args.mu_id)
    if mu is None:
      conn.close()
      fail(f"Memory unit not found: {args.mu_id}")
    storage_ids = [storage_id_for(target["scope"], target["namespace"], args.mu_id)]

  refreshed = 0
  for storage_id in storage_ids:
    current = fetch_mu(conn, storage_id)
    if current is None or is_deprecated_mu(current):
      delete_similarity_links_for_mu(conn, storage_id)
      continue
    scoped_mu = row_to_mu(
      conn.execute("SELECT * FROM memory_units WHERE id = ?", (storage_id,)).fetchone(),
      scope=target["scope"],
      namespace=target["namespace"],
    )
    recompute_links_for_mu(conn, target, storage_id, scoped_mu)
    refreshed += 1
  conn.commit()
  conn.close()

  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "refreshed_count": refreshed,
      "mode": "all" if args.all else "single",
      "id": None if args.all else args.mu_id,
    }
  )


def canonical_candidate_rank(mu: dict[str, Any], duplicate_score_sum: float) -> tuple[int, float, str]:
  deprecated_rank = 0 if is_deprecated_mu(mu) else 1
  updated_at = mu.get("updated_at", "")
  return (deprecated_rank, duplicate_score_sum, updated_at)


def cmd_merge_suggest(args: argparse.Namespace) -> None:
  target = resolve_storage_target(args)
  conn, _ = run_query(target)
  anchor = fetch_mu_for_target(conn, target, args.mu_id)
  if anchor is None:
    conn.close()
    fail(f"Memory unit not found: {args.mu_id}")

  storage_id = storage_id_for(target["scope"], target["namespace"], args.mu_id)
  rows = related_rows(
    conn,
    target,
    storage_id,
    include_deprecated=args.include_deprecated,
    link_type=None,
    limit=None,
  )
  candidates = [anchor]
  duplicate_score_sum: dict[str, float] = {anchor["id"]: 0.0}
  duplicate_ids: list[str] = []

  for row in rows:
    if row["link_type"] != "duplicate_candidate":
      continue
    mu = row_to_mu(row, scope=target["scope"], namespace=target["namespace"])
    candidates.append(mu)
    duplicate_score_sum[mu["id"]] = duplicate_score_sum.get(mu["id"], 0.0) + float(row["score"])
    duplicate_score_sum[anchor["id"]] = duplicate_score_sum.get(anchor["id"], 0.0) + float(row["score"])
    duplicate_ids.append(mu["id"])

  unique_candidates = {mu["id"]: mu for mu in candidates}
  canonical_id = max(
    unique_candidates.keys(),
    key=lambda mu_id: canonical_candidate_rank(unique_candidates[mu_id], duplicate_score_sum.get(mu_id, 0.0)),
  )
  suggest_deprecate_ids = sorted(mu_id for mu_id in unique_candidates if mu_id != canonical_id)

  conn.close()
  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "anchor_id": args.mu_id,
      "canonical_id": canonical_id,
      "duplicate_candidate_ids": sorted(set(duplicate_ids)),
      "suggest_deprecate_ids": suggest_deprecate_ids,
    }
  )


def cmd_stats(args: argparse.Namespace) -> None:
  target = resolve_storage_target(args)
  conn, db_path = run_query(target)

  prefix = storage_id_prefix(target["scope"], target["namespace"])
  if prefix:
    rows = conn.execute(
      """
      SELECT id, type, summary, content_json, tags_json, validity_json, updated_at
      FROM memory_units
      WHERE id LIKE ?
      """,
      (f"{prefix}%",),
    ).fetchall()
  else:
    rows = conn.execute(
      "SELECT id, type, summary, content_json, tags_json, validity_json, updated_at FROM memory_units"
    ).fetchall()

  total = len(rows)
  active = 0
  deprecated = 0
  by_type: dict[str, int] = {mu_type: 0 for mu_type in sorted(MU_TYPES)}
  tag_counts: dict[str, int] = {}
  sum_summary_chars = 0
  sum_content_chars = 0
  sum_tags_chars = 0
  last_updated_at = None
  active_storage_ids: list[str] = []

  for row in rows:
    mu_type = row["type"]
    by_type[mu_type] = by_type.get(mu_type, 0) + 1

    validity = parse_json_field(row["validity_json"], {"status": "active"})
    status = str(validity.get("status", "active")).lower()
    if status == "deprecated":
      deprecated += 1
    else:
      active += 1
      active_storage_ids.append(row["id"])

    tags = parse_json_field(row["tags_json"], [])
    if isinstance(tags, list):
      for item in tags:
        if isinstance(item, str) and item:
          tag_counts[item] = tag_counts.get(item, 0) + 1

    summary = row["summary"] if isinstance(row["summary"], str) else ""
    content_json = row["content_json"] if isinstance(row["content_json"], str) else ""
    tags_json = row["tags_json"] if isinstance(row["tags_json"], str) else ""

    sum_summary_chars += len(summary)
    sum_content_chars += len(content_json)
    sum_tags_chars += len(tags_json)

    updated_at = row["updated_at"]
    if isinstance(updated_at, str) and updated_at:
      if last_updated_at is None or updated_at > last_updated_at:
        last_updated_at = updated_at

  top_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))[:20]
  db_size = db_path.stat().st_size if db_path.exists() else 0

  source_link_where, source_link_params = storage_scope_clause(target, "source_id")
  target_link_where, target_link_params = storage_scope_clause(target, "target_id")
  link_where = source_link_where + target_link_where
  link_params = source_link_params + target_link_params
  link_sql = "SELECT source_id, target_id, link_type, score FROM memory_links"
  if link_where:
    link_sql += f" WHERE {' AND '.join(link_where)}"
  link_rows = conn.execute(link_sql, link_params).fetchall()
  links_by_type: dict[str, int] = {link_type: 0 for link_type in sorted(LINK_TYPES)}
  linked_sources = set()
  for row in link_rows:
    links_by_type[row["link_type"]] = links_by_type.get(row["link_type"], 0) + 1
    linked_sources.add(row["source_id"])

  orphan_memories = len([storage_id for storage_id in active_storage_ids if storage_id not in linked_sources])
  duplicate_pairs = len({
    tuple(sorted((
      external_id_from_storage(target["scope"], target["namespace"], row["source_id"]),
      external_id_from_storage(target["scope"], target["namespace"], row["target_id"]),
    )))
    for row in link_rows
    if row["link_type"] == "duplicate_candidate"
  })
  total_links = len(link_rows)
  avg_links = round(total_links / active, 6) if active else 0.0

  conn.close()

  emit_json(
    {
      "ok": True,
      "scope": target["scope"],
      "target": target["label"],
      "namespace": target["namespace"],
      "project": target["project"],
      "db_path": str(db_path.resolve()),
      "counts": {
        "total": total,
        "active": active,
        "deprecated": deprecated,
        "by_type": by_type,
      },
      "links": {
        "total": total_links,
        "by_type": links_by_type,
        "orphan_memories": orphan_memories,
        "avg_links_per_active_memory": avg_links,
        "duplicate_candidate_pairs": duplicate_pairs,
      },
      "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
      "sizes": {
        "db_file_bytes": db_size,
        "sum_summary_chars": sum_summary_chars,
        "sum_content_chars": sum_content_chars,
        "sum_tags_chars": sum_tags_chars,
      },
      "last_updated_at": last_updated_at,
    }
  )


def main() -> None:
  parser = argparse.ArgumentParser(
    description=(
      "Structured memory CLI with two storage scopes:\n"
      "  project (default): nearest .memory/ or git repo root\n"
      "  global: namespaced shared memory (requires --namespace)"
    ),
    formatter_class=argparse.RawTextHelpFormatter,
  )
  subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
  common = argparse.ArgumentParser(add_help=False)
  common.add_argument(
    "--scope",
    choices=["project", "global"],
    default="project",
    help="Storage scope (default: project). Use 'global' for shared namespaced memory.",
  )
  common.add_argument(
    "--namespace",
    default=None,
    help="Namespace for global scope (required with --scope global), e.g. user:git or project:backend",
  )

  parser_init = subparsers.add_parser(
    "init",
    parents=[common],
    help="Initialize memory storage",
    description="Initialize project-local or global namespaced memory storage.",
  )
  parser_init.set_defaults(func=cmd_init)

  parser_upsert = subparsers.add_parser(
    "upsert",
    parents=[common],
    help="Insert or update a memory unit",
    description="Insert or update a memory unit from a JSON file path or stdin ('-').",
  )
  parser_upsert.add_argument("file_or_dash", help="JSON file path or '-' for stdin")
  parser_upsert.set_defaults(func=cmd_upsert)

  parser_get = subparsers.add_parser(
    "get",
    parents=[common],
    help="Retrieve a memory unit by ID",
    description="Retrieve one memory unit by ID from the selected scope.",
  )
  parser_get.add_argument("mu_id", help="Memory unit ID")
  parser_get.add_argument("--view", default="full", choices=["tiny", "compact", "full"], help="Output view format")
  parser_get.add_argument("--select", default=None, help="Comma-separated field paths to project in output")
  parser_get.set_defaults(func=cmd_get)

  parser_search = subparsers.add_parser(
    "search",
    parents=[common],
    help="Search memory units",
    description="Full-text search memory units in the selected scope.",
  )
  parser_search.add_argument("query", help="Search query")
  parser_search.add_argument("--k", type=int, default=8, help="Number of results to return")
  parser_search.add_argument(
    "--type",
    default=None,
    help=f"Filter by MU type ({', '.join(sorted(MU_TYPES))})",
  )
  parser_search.add_argument("--tag", default=None, help="Filter by tag")
  parser_search.add_argument("--include-deprecated", action="store_true", help="Include deprecated units")
  parser_search.add_argument("--view", default="compact", choices=["tiny", "compact", "full"], help="Output view format")
  parser_search.add_argument("--select", default=None, help="Comma-separated field paths to project in output")
  parser_search.add_argument("--include-neighborhood", dest="include_neighborhood", action="store_true", default=None, help="Include neighborhood links in each search result")
  parser_search.add_argument("--no-include-neighborhood", dest="include_neighborhood", action="store_false", help="Omit neighborhood links from each search result")
  parser_search.add_argument("--neighbors-k", type=int, default=DEFAULT_NEIGHBORS_K, help="Number of neighborhood memories to include per search result")
  parser_search.set_defaults(func=cmd_search)

  parser_deprecate = subparsers.add_parser(
    "deprecate",
    parents=[common],
    help="Mark a memory unit as deprecated",
    description="Mark a memory unit as deprecated and link it to a replacement ID.",
  )
  parser_deprecate.add_argument("mu_id", help="Memory unit ID")
  parser_deprecate.add_argument("--replaced-by", required=True, help="ID of replacement memory unit")
  parser_deprecate.set_defaults(func=cmd_deprecate)

  parser_related = subparsers.add_parser(
    "related",
    parents=[common],
    help="Inspect related memory links",
    description="Show stored relationship links for one memory unit.",
  )
  parser_related.add_argument("mu_id", help="Memory unit ID")
  parser_related.add_argument("--k", type=int, default=8, help="Number of linked memories to return")
  parser_related.add_argument("--link-type", default=None, help=f"Filter by link type ({', '.join(sorted(LINK_TYPES))})")
  parser_related.add_argument("--include-deprecated", action="store_true", help="Include deprecated linked memories")
  parser_related.set_defaults(func=cmd_related)

  parser_dedupe = subparsers.add_parser(
    "dedupe",
    parents=[common],
    help="List likely duplicate memories",
    description="Show duplicate-candidate memory pairs in the selected scope.",
  )
  parser_dedupe.add_argument("--k", type=int, default=8, help="Number of duplicate pairs to return")
  parser_dedupe.add_argument("--include-deprecated", action="store_true", help="Include deprecated memories in duplicate results")
  parser_dedupe.set_defaults(func=cmd_dedupe)

  parser_relink = subparsers.add_parser(
    "relink",
    parents=[common],
    help="Recompute similarity links",
    description="Recompute similarity links for one memory unit or all active memories.",
  )
  parser_relink.add_argument("mu_id", nargs="?", default=None, help="Memory unit ID to relink")
  parser_relink.add_argument("--all", action="store_true", help="Relink all active memories in scope")
  parser_relink.set_defaults(func=cmd_relink)

  parser_merge_suggest = subparsers.add_parser(
    "merge-suggest",
    parents=[common],
    help="Suggest merge/deprecation candidates",
    description="Recommend a canonical memory unit among duplicate candidates without mutating data.",
  )
  parser_merge_suggest.add_argument("mu_id", help="Memory unit ID")
  parser_merge_suggest.add_argument("--include-deprecated", action="store_true", help="Include deprecated candidates in the suggestion")
  parser_merge_suggest.set_defaults(func=cmd_merge_suggest)

  parser_vacuum = subparsers.add_parser(
    "vacuum",
    parents=[common],
    help="Remove deprecated memory units and vacuum database",
    description="Delete deprecated memory units in the selected scope and compact the SQLite database.",
  )
  parser_vacuum.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
  parser_vacuum.set_defaults(func=cmd_vacuum)

  parser_stats = subparsers.add_parser(
    "stats",
    parents=[common],
    help="Show database statistics",
    description="Show counts, sizes, tag summaries, and link summaries for the selected scope.",
  )
  parser_stats.set_defaults(func=cmd_stats)

  try:
    args = parser.parse_args()
    args.func(args)
  except Exception as exc:  # pragma: no cover
    fail(str(exc))


if __name__ == "__main__":
  main()
