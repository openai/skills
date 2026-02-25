#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MU_SCHEMA = "nh.memory.mu"
MU_SCHEMA_VERSION = 1
MAX_JSON_CHARS = 50_000
MEMORY_DB_DIR = ".memory"
GLOBAL_MEMORY_ENV = "LOCAL_PROJECT_MEMORY_GLOBAL_DIR"
DEFAULT_GLOBAL_MEMORY_DIR = Path.home() / ".local" / "share" / "local_project_memory" / "global"

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


def cmd_search(args: argparse.Namespace) -> None:
  query = args.query
  k = args.k
  type = args.type
  tag = args.tag
  include_deprecated = args.include_deprecated
  view = args.view
  select = args.select
  if view not in VIEW_FIELDS:
    valid_views = ", ".join(sorted(VIEW_FIELDS.keys()))
    fail(f"Invalid --view: '{view}'. Must be one of: {valid_views}")
  if k <= 0:
    fail("Invalid --k. Must be > 0.")
  if type is not None and type not in MU_TYPES:
    valid_types = ", ".join(sorted(MU_TYPES))
    fail(f"Invalid --type: '{type}'. Must be one of: {valid_types}")

  target = resolve_storage_target(args)
  conn, _ = run_query(target)

  where_clauses = ["memory_fts MATCH ?"]
  params: list[Any] = [query]

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
    where_clauses.append(
      "LOWER(COALESCE(json_extract(m.validity_json, '$.status'), 'active')) != 'deprecated'"
    )

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
  conn.close()

  results = [
    project_mu(
      row_to_mu(row, scope=target["scope"], namespace=target["namespace"]),
      view=view,
      select=select,
    )
    for row in rows
  ]
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
      """
      SELECT id FROM memory_units
      WHERE LOWER(COALESCE(json_extract(validity_json, '$.status'), 'active')) = 'deprecated'
        AND id LIKE ?
      ORDER BY id
      """
      if storage_id_prefix(target["scope"], target["namespace"])
      else
      """
      SELECT id FROM memory_units
      WHERE LOWER(COALESCE(json_extract(validity_json, '$.status'), 'active')) = 'deprecated'
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
      """
      DELETE FROM memory_units
      WHERE LOWER(COALESCE(json_extract(validity_json, '$.status'), 'active')) = 'deprecated'
        AND id LIKE ?
      """,
      (f"{prefix}%",),
    )
  else:
    conn.execute(
      """
      DELETE FROM memory_units
      WHERE LOWER(COALESCE(json_extract(validity_json, '$.status'), 'active')) = 'deprecated'
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

  for row in rows:
    mu_type = row["type"]
    by_type[mu_type] = by_type.get(mu_type, 0) + 1

    validity = parse_json_field(row["validity_json"], {"status": "active"})
    status = str(validity.get("status", "active")).lower()
    if status == "deprecated":
      deprecated += 1
    else:
      active += 1

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

  conn.close()

  db_size = db_path.stat().st_size if db_path.exists() else 0

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

  # init command
  parser_init = subparsers.add_parser(
    "init",
    parents=[common],
    help="Initialize memory storage",
    description="Initialize project-local or global namespaced memory storage.",
  )
  parser_init.set_defaults(func=cmd_init)

  # upsert command
  parser_upsert = subparsers.add_parser(
    "upsert",
    parents=[common],
    help="Insert or update a memory unit",
    description="Insert or update a memory unit from a JSON file path or stdin ('-').",
  )
  parser_upsert.add_argument("file_or_dash", help="JSON file path or '-' for stdin")
  parser_upsert.set_defaults(func=cmd_upsert)

  # get command
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

  # search command
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
  parser_search.set_defaults(func=cmd_search)

  # deprecate command
  parser_deprecate = subparsers.add_parser(
    "deprecate",
    parents=[common],
    help="Mark a memory unit as deprecated",
    description="Mark a memory unit as deprecated and link it to a replacement ID.",
  )
  parser_deprecate.add_argument("mu_id", help="Memory unit ID")
  parser_deprecate.add_argument("--replaced-by", required=True, help="ID of replacement memory unit")
  parser_deprecate.set_defaults(func=cmd_deprecate)

  # vacuum command
  parser_vacuum = subparsers.add_parser(
    "vacuum",
    parents=[common],
    help="Remove deprecated memory units and vacuum database",
    description="Delete deprecated memory units in the selected scope and compact the SQLite database.",
  )
  parser_vacuum.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
  parser_vacuum.set_defaults(func=cmd_vacuum)

  # stats command
  parser_stats = subparsers.add_parser(
    "stats",
    parents=[common],
    help="Show database statistics",
    description="Show counts, sizes, and tag summaries for the selected scope.",
  )
  parser_stats.set_defaults(func=cmd_stats)

  try:
    args = parser.parse_args()
    args.func(args)
  except Exception as exc:  # pragma: no cover
    fail(str(exc))


if __name__ == "__main__":
  main()
