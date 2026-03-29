#!/usr/bin/env python3
"""Static Supabase/Postgres security audit helper."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".next",
    ".turbo",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "vendor",
}
SQL_EXTENSIONS = {".sql"}
CODE_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
SYSTEM_SCHEMAS = {"pg_catalog", "information_schema", "pg_toast"}
RISKY_PUBLIC_ENV_RE = re.compile(
    r"\bNEXT_PUBLIC_[A-Z0-9_]*(?:SECRET|TOKEN|PRIVATE|SERVICE_ROLE|WEBHOOK)[A-Z0-9_]*\b"
)


@dataclass
class Finding:
    severity: str
    kind: str
    location: str
    message: str


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"--[^\n]*", "", text)


def split_sql_statements(text: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    i = 0
    in_single = False
    in_double = False
    dollar_tag: str | None = None

    while i < len(text):
        ch = text[i]

        if dollar_tag:
            if text.startswith(dollar_tag, i):
                current.append(dollar_tag)
                i += len(dollar_tag)
                dollar_tag = None
                continue
            current.append(ch)
            i += 1
            continue

        if in_single:
            current.append(ch)
            if ch == "'" and not text.startswith("''", i):
                in_single = False
            elif text.startswith("''", i):
                current.append("'")
                i += 2
                continue
            i += 1
            continue

        if in_double:
            current.append(ch)
            if ch == '"':
                in_double = False
            i += 1
            continue

        if ch == "'":
            in_single = True
            current.append(ch)
            i += 1
            continue

        if ch == '"':
            in_double = True
            current.append(ch)
            i += 1
            continue

        if ch == "$":
            match = re.match(r"\$[A-Za-z0-9_]*\$", text[i:])
            if match:
                dollar_tag = match.group(0)
                current.append(dollar_tag)
                i += len(dollar_tag)
                continue

        if ch == ";":
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements


def normalize_identifier(raw: str) -> str:
    parts = [part.strip().strip('"') for part in raw.strip().split(".") if part.strip()]
    if not parts:
        return raw.strip()
    if len(parts) == 1:
        return f"public.{parts[0]}"
    return ".".join(parts)


def collect_files(root: Path, suffixes: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() in suffixes:
            files.append(path)
    return sorted(files)


def audit_sql(root: Path) -> tuple[list[Finding], dict[str, dict[str, object]]]:
    findings: list[Finding] = []
    tables: dict[str, dict[str, object]] = {}

    create_table_re = re.compile(
        r"^create\s+table\s+(?:if\s+not\s+exists\s+)?([A-Za-z0-9_\".]+)",
        re.I,
    )
    enable_rls_re = re.compile(
        r"^alter\s+table\s+(?:if\s+exists\s+)?([A-Za-z0-9_\".]+)\s+enable\s+row\s+level\s+security$",
        re.I,
    )
    force_rls_re = re.compile(
        r"^alter\s+table\s+(?:if\s+exists\s+)?([A-Za-z0-9_\".]+)\s+force\s+row\s+level\s+security$",
        re.I,
    )
    create_policy_re = re.compile(
        r"^create\s+policy\s+.+?\s+on\s+([A-Za-z0-9_\".]+)\b",
        re.I | re.S,
    )
    create_function_re = re.compile(
        r"^create\s+(?:or\s+replace\s+)?function\s+([A-Za-z0-9_\".]+)\b",
        re.I,
    )
    grant_re = re.compile(
        r"^grant\s+(.+?)\s+on\s+(?:table\s+)?([A-Za-z0-9_\".]+)\s+to\s+(.+)$",
        re.I | re.S,
    )

    for sql_file in collect_files(root, SQL_EXTENSIONS):
        relative = sql_file.relative_to(root)
        text = strip_comments(sql_file.read_text())
        for statement in split_sql_statements(text):
            normalized = " ".join(statement.split())
            lower = normalized.lower()

            match = create_table_re.match(normalized)
            if match:
                name = normalize_identifier(match.group(1))
                schema = name.split(".", 1)[0]
                if schema not in SYSTEM_SCHEMAS:
                    tables.setdefault(
                        name,
                        {
                            "file": str(relative),
                            "rls": False,
                            "force": False,
                            "policies": [],
                        },
                    )
                continue

            match = enable_rls_re.match(normalized)
            if match:
                name = normalize_identifier(match.group(1))
                tables.setdefault(
                    name,
                    {"file": str(relative), "rls": False, "force": False, "policies": []},
                )["rls"] = True
                continue

            match = force_rls_re.match(normalized)
            if match:
                name = normalize_identifier(match.group(1))
                entry = tables.setdefault(
                    name,
                    {"file": str(relative), "rls": False, "force": False, "policies": []},
                )
                entry["force"] = True
                continue

            match = create_policy_re.match(normalized)
            if match:
                name = normalize_identifier(match.group(1))
                policy = {
                    "file": str(relative),
                    "command": "all",
                    "using_true": bool(re.search(r"\busing\s*\(\s*true\s*\)", lower)),
                    "with_check_true": bool(re.search(r"\bwith\s+check\s*\(\s*true\s*\)", lower)),
                }
                cmd_match = re.search(r"\bfor\s+(select|insert|update|delete|all)\b", lower)
                if cmd_match:
                    policy["command"] = cmd_match.group(1)
                tables.setdefault(
                    name,
                    {"file": str(relative), "rls": False, "force": False, "policies": []},
                )["policies"].append(policy)
                continue

            match = create_function_re.match(normalized)
            if match and "security definer" in lower:
                func_name = normalize_identifier(match.group(1))
                if "set search_path" in lower:
                    findings.append(
                        Finding(
                            "info",
                            "security-definer",
                            str(relative),
                            f"{func_name} uses SECURITY DEFINER and should be reviewed like privileged code.",
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "medium",
                            "security-definer",
                            str(relative),
                            f"{func_name} uses SECURITY DEFINER without an explicit search_path.",
                        )
                    )
                continue

            match = grant_re.match(normalized)
            if match:
                privileges = match.group(1).lower()
                object_name = normalize_identifier(match.group(2))
                roles = match.group(3).lower()
                if "anon" in roles or "authenticated" in roles or "public" in roles:
                    severity = (
                        "high"
                        if any(word in privileges for word in ("insert", "update", "delete", "all"))
                        else "medium"
                    )
                    findings.append(
                        Finding(
                            severity,
                            "grant-review",
                            str(relative),
                            f"Grant on {object_name} to {roles.strip()} should be reviewed: {privileges.strip()}",
                        )
                    )

    for table_name, entry in sorted(tables.items()):
        schema = table_name.split(".", 1)[0]
        if schema in SYSTEM_SCHEMAS:
            continue

        policies = entry["policies"]
        if not entry["rls"]:
            findings.append(
                Finding(
                    "high",
                    "missing-rls",
                    entry["file"],
                    f"{table_name} is created without row level security.",
                )
            )
            continue

        if not policies:
            findings.append(
                Finding(
                    "medium",
                    "no-policies",
                    entry["file"],
                    f"{table_name} has RLS enabled but no policies. Confirm deny-all is intentional.",
                )
            )

        if not entry["force"]:
            findings.append(
                Finding(
                    "info",
                    "rls-not-forced",
                    entry["file"],
                    f"{table_name} does not use FORCE ROW LEVEL SECURITY. Review whether owner bypass should remain possible.",
                )
            )

        for policy in policies:
            command = str(policy["command"])
            if policy["with_check_true"]:
                findings.append(
                    Finding(
                        "medium",
                        "broad-policy",
                        policy["file"],
                        f"{table_name} has a {command} policy with WITH CHECK (true). Confirm user-driven writes are really unrestricted.",
                    )
                )
            if policy["using_true"]:
                severity = "medium" if command in {"all", "update", "delete"} else "info"
                findings.append(
                    Finding(
                        severity,
                        "broad-policy",
                        policy["file"],
                        f"{table_name} has a {command} policy with USING (true). Confirm this wide read/write scope is intentional.",
                    )
                )

    return findings, tables


def audit_code(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for code_file in collect_files(root, CODE_EXTENSIONS):
        relative = code_file.relative_to(root)
        text = code_file.read_text()

        if RISKY_PUBLIC_ENV_RE.search(text):
            findings.append(
                Finding(
                    "high",
                    "public-secret",
                    str(relative),
                    "A NEXT_PUBLIC_* variable looks like a secret or privileged token.",
                )
            )

        lower = text.lower()
        is_client = '"use client"' in lower or "'use client'" in lower or "createbrowserclient" in lower
        if "supabase_service_role_key" in lower and is_client:
            findings.append(
                Finding(
                    "high",
                    "client-service-role",
                    str(relative),
                    "SUPABASE_SERVICE_ROLE_KEY appears in code that looks client-side.",
                )
            )

        if "dangerouslysetinnerhtml" in lower:
            findings.append(
                Finding(
                    "medium",
                    "dangerous-html",
                    str(relative),
                    "dangerouslySetInnerHTML is present. Verify sanitization and trusted content boundaries.",
                )
            )

        if re.search(r"\beval\s*\(", text) or re.search(r"\bnew\s+Function\s*\(", text):
            findings.append(
                Finding(
                    "medium",
                    "dynamic-code",
                    str(relative),
                    "Dynamic code execution is present. Confirm untrusted input cannot reach it.",
                )
            )

    return findings


def print_findings(findings: list[Finding], sql_files: int, code_files: int, tables_found: int) -> None:
    order = {"high": 0, "medium": 1, "info": 2}
    grouped = {"high": [], "medium": [], "info": []}
    for finding in sorted(findings, key=lambda item: (order[item.severity], item.location, item.kind, item.message)):
        grouped[finding.severity].append(finding)

    print(f"Scanned {sql_files} SQL files, {code_files} code files, and {tables_found} tables.")
    print()

    for severity in ("high", "medium", "info"):
        title = severity.upper()
        print(title)
        if not grouped[severity]:
            print("- none")
        else:
            for finding in grouped[severity]:
                print(f"- [{finding.kind}] {finding.location}: {finding.message}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Supabase/Postgres project for common security gaps.")
    parser.add_argument("root", nargs="?", default=".", help="Project root to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Path not found: {root}")
    if not root.is_dir():
        raise SystemExit(f"Path is not a directory: {root}")

    sql_files = collect_files(root, SQL_EXTENSIONS)
    code_files = collect_files(root, CODE_EXTENSIONS)
    sql_findings, tables = audit_sql(root)
    code_findings = audit_code(root)
    findings = sql_findings + code_findings

    print_findings(findings, len(sql_files), len(code_files), len(tables))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
