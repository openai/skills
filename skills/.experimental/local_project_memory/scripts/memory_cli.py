#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MU_SCHEMA = "nh.memory.mu"
MU_SCHEMA_VERSION = 1
MAX_JSON_CHARS = 50_000
MEMORY_DB_DIR = ".memory"

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
  return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def db_path_for(project: str) -> Path:
  cwd = Path.cwd()
  project_root = resolve_project_root(cwd)
  memory_dir = project_root / MEMORY_DB_DIR
  return memory_dir / "memory.db"


def open_db(project: str) -> sqlite3.Connection:
  db_path = db_path_for(project)
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


def row_to_mu(row: sqlite3.Row) -> dict[str, Any]:
  mu: dict[str, Any] = {
    "schema": MU_SCHEMA,
    "schema_version": MU_SCHEMA_VERSION,
    "id": row["id"],
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


def ensure_ready(project: str) -> sqlite3.Connection:
  conn = open_db(project)
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


def run_query(project: str) -> tuple[sqlite3.Connection, Path]:
  conn = ensure_ready(project)
  return conn, db_path_for(project)


def cmd_init(args: argparse.Namespace) -> None:
  cwd = Path.cwd()
  memory_dir = cwd / MEMORY_DB_DIR
  if memory_dir.exists() and not memory_dir.is_dir():
    fail(f"Invalid {MEMORY_DB_DIR}: expected a directory.")
  memory_dir.mkdir(parents=True, exist_ok=True)
  project = cwd.name

  conn = ensure_ready(project)
  conn.close()

  emit_json(
    {
      "ok": True,
      "project": project,
      "db_path": str(db_path_for(project).resolve()),
    }
  )


def cmd_upsert(args: argparse.Namespace) -> None:
  file_or_dash = args.file_or_dash
  project = resolve_project_name(Path.cwd())
  conn, _ = run_query(project)

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
      mu["id"],
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

  emit_json({"ok": True, "id": mu["id"], "updated_at": mu["updated_at"]})


def cmd_get(args: argparse.Namespace) -> None:
  mu_id = args.mu_id
  view = args.view
  select = args.select
  if view not in VIEW_FIELDS:
    valid_views = ", ".join(sorted(VIEW_FIELDS.keys()))
    fail(f"Invalid --view: '{view}'. Must be one of: {valid_views}")

  project = resolve_project_name(Path.cwd())
  conn, _ = run_query(project)

  mu = fetch_mu(conn, mu_id)
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

  project = resolve_project_name(Path.cwd())
  conn, _ = run_query(project)

  where_clauses = ["memory_fts MATCH ?"]
  params: list[Any] = [query]

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

  results = [project_mu(row_to_mu(row), view=view, select=select) for row in rows]
  emit_json(results)


def cmd_deprecate(args: argparse.Namespace) -> None:
  mu_id = args.mu_id
  replaced_by = args.replaced_by
  project = resolve_project_name(Path.cwd())
  conn, _ = run_query(project)

  mu = fetch_mu(conn, mu_id)
  if mu is None:
    conn.close()
    fail(f"Memory unit not found: {mu_id}")

  validity = mu.get("validity", {})
  validity["status"] = "deprecated"
  validity["replaced_by"] = replaced_by
  updated_at = now_iso()

  conn.execute(
    """
    UPDATE memory_units
    SET validity_json = ?, updated_at = ?
    WHERE id = ?
    """,
    (json.dumps(validity, ensure_ascii=False), updated_at, mu_id),
  )
  conn.commit()
  conn.close()

  emit_json(
    {
      "ok": True,
      "id": mu_id,
      "status": "deprecated",
      "replaced_by": replaced_by,
      "updated_at": updated_at,
    }
  )


def cmd_vacuum(args: argparse.Namespace) -> None:
  dry_run = args.dry_run
  project = resolve_project_name(Path.cwd())
  conn, _ = run_query(project)

  rows = conn.execute(
    """
    SELECT id FROM memory_units
    WHERE LOWER(COALESCE(json_extract(validity_json, '$.status'), 'active')) = 'deprecated'
    ORDER BY id
    """
  ).fetchall()

  deprecated_ids = [row["id"] for row in rows]

  if dry_run:
    conn.close()
    emit_json(
      {
        "ok": True,
        "dry_run": True,
        "deprecated_count": len(deprecated_ids),
        "would_delete_ids": deprecated_ids[:100],
      }
    )
    return

  deleted_count = len(deprecated_ids)
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
      "dry_run": False,
      "deleted_count": deleted_count,
      "vacuumed": True,
    }
  )


def cmd_stats(args: argparse.Namespace) -> None:
  project = resolve_project_name(Path.cwd())
  conn, db_path = run_query(project)

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
      "project": project,
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
    description="Local per-project structured memory with SQLite"
  )
  subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

  # init command
  parser_init = subparsers.add_parser("init", help="Initialize project memory")
  parser_init.set_defaults(func=cmd_init)

  # upsert command
  parser_upsert = subparsers.add_parser("upsert", help="Insert or update a memory unit")
  parser_upsert.add_argument("file_or_dash", help="JSON file path or '-' for stdin")
  parser_upsert.set_defaults(func=cmd_upsert)

  # get command
  parser_get = subparsers.add_parser("get", help="Retrieve a memory unit by ID")
  parser_get.add_argument("mu_id", help="Memory unit ID")
  parser_get.add_argument("--view", default="full", choices=["tiny", "compact", "full"], help="Output view format")
  parser_get.add_argument("--select", default=None, help="Comma-separated field paths to project")
  parser_get.set_defaults(func=cmd_get)

  # search command
  parser_search = subparsers.add_parser("search", help="Search memory units")
  parser_search.add_argument("query", help="Search query")
  parser_search.add_argument("--k", type=int, default=8, help="Number of results to return")
  parser_search.add_argument("--type", default=None, help="Filter by MU type")
  parser_search.add_argument("--tag", default=None, help="Filter by tag")
  parser_search.add_argument("--include-deprecated", action="store_true", help="Include deprecated units")
  parser_search.add_argument("--view", default="compact", choices=["tiny", "compact", "full"], help="Output view format")
  parser_search.add_argument("--select", default=None, help="Comma-separated field paths to project")
  parser_search.set_defaults(func=cmd_search)

  # deprecate command
  parser_deprecate = subparsers.add_parser("deprecate", help="Mark a memory unit as deprecated")
  parser_deprecate.add_argument("mu_id", help="Memory unit ID")
  parser_deprecate.add_argument("--replaced-by", required=True, help="ID of replacement memory unit")
  parser_deprecate.set_defaults(func=cmd_deprecate)

  # vacuum command
  parser_vacuum = subparsers.add_parser("vacuum", help="Remove deprecated memory units and vacuum database")
  parser_vacuum.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
  parser_vacuum.set_defaults(func=cmd_vacuum)

  # stats command
  parser_stats = subparsers.add_parser("stats", help="Show database statistics")
  parser_stats.set_defaults(func=cmd_stats)

  try:
    args = parser.parse_args()
    args.func(args)
  except Exception as exc:  # pragma: no cover
    fail(str(exc))


if __name__ == "__main__":
  main()
