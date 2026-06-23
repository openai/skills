#!/usr/bin/env python3
"""Detect project stack and generate Docker artifacts."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


STACK_PRIORITY = ["node", "python", "go", "rust"]


@dataclass
class Detection:
    stack: str
    framework: str | None
    package_manager: str | None
    port: int
    start_command: str
    dev_command: str
    notes: list[str] = field(default_factory=list)
    scripts: dict[str, str] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8", errors="ignore").lstrip("\ufeff")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def normalize_package_manager(value: str | None) -> str | None:
    if not value:
        return None
    lowered = value.lower().strip()
    if "@" in lowered:
        lowered = lowered.split("@", 1)[0]
    if lowered in {"pnpm", "npm", "yarn"}:
        return lowered
    return None


def choose_package_manager(repo: Path, package_json: dict[str, Any]) -> str:
    by_field = normalize_package_manager(str(package_json.get("packageManager", "")))
    if by_field:
        return by_field
    if (repo / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (repo / "yarn.lock").exists():
        return "yarn"
    return "npm"


def pm_run_script(pm: str, script: str, extra_args: list[str] | None = None) -> str:
    base = f"{pm} run {script}"
    if not extra_args:
        return base
    suffix = " ".join(extra_args)
    return f"{base} -- {suffix}"


def detect_node_framework(package_json: dict[str, Any]) -> str | None:
    deps: dict[str, Any] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package_json.get(key)
        if isinstance(value, dict):
            deps.update(value)
    names = {str(name).lower() for name in deps.keys()}
    if "next" in names:
        return "nextjs"
    if "vite" in names:
        return "vite"
    if "@nestjs/core" in names or "@nestjs/common" in names:
        return "nest"
    if "express" in names:
        return "express"
    return None


def detect_python_framework(repo: Path) -> str | None:
    requirements = read_text_if_exists(repo / "requirements.txt").lower()
    pyproject = read_text_if_exists(repo / "pyproject.toml").lower()
    combined = "\n".join([requirements, pyproject])
    if "fastapi" in combined:
        return "fastapi"
    if "django" in combined:
        return "django"
    return None


def detect_stack_candidates(repo: Path) -> list[str]:
    candidates: list[str] = []
    if (repo / "package.json").exists():
        candidates.append("node")
    if (repo / "requirements.txt").exists() or (repo / "pyproject.toml").exists():
        candidates.append("python")
    if (repo / "go.mod").exists():
        candidates.append("go")
    if (repo / "Cargo.toml").exists():
        candidates.append("rust")
    return candidates


def detect_fastapi_module(repo: Path) -> str:
    candidates = [
        ("app/main.py", "app.main"),
        ("main.py", "main"),
        ("app.py", "app"),
        ("src/main.py", "src.main"),
    ]
    for rel, module in candidates:
        if (repo / rel).exists():
            content = read_text_if_exists(repo / rel).lower()
            if "fastapi(" in content or "from fastapi import" in content:
                return module
    return "main"


def detect_django_manage_path(repo: Path) -> str:
    root_manage = repo / "manage.py"
    if root_manage.exists():
        return "manage.py"
    for path in repo.glob("*/manage.py"):
        if path.is_file():
            return str(path.relative_to(repo)).replace("\\", "/")
    return "manage.py"


def detect_python_entrypoint(repo: Path) -> str:
    for rel in ("main.py", "app.py", "src/main.py"):
        if (repo / rel).exists():
            return rel
    return "main.py"


def detect_go_target(repo: Path) -> str:
    if (repo / "main.go").exists():
        return "."
    cmd_dir = repo / "cmd"
    if cmd_dir.is_dir():
        mains = [p for p in cmd_dir.glob("*/main.go") if p.is_file()]
        if len(mains) == 1:
            target = mains[0].parent.relative_to(repo).as_posix()
            return f"./{target}"
    return "."


def parse_rust_bin_name(repo: Path) -> str:
    cargo_toml = read_text_if_exists(repo / "Cargo.toml")
    match = re.search(r'(?m)^\s*name\s*=\s*"([^"]+)"\s*$', cargo_toml)
    if match:
        return match.group(1).strip().replace("-", "_")
    return "app"


def detect_project(repo: Path) -> Detection:
    package_json = read_json_if_exists(repo / "package.json")
    candidates = detect_stack_candidates(repo)
    if not candidates:
        raise RuntimeError(
            "Could not detect project stack. Expected one of: package.json, requirements.txt, "
            "pyproject.toml, go.mod, Cargo.toml."
        )

    notes: list[str] = []
    if len(candidates) > 1:
        notes.append(
            "Multiple stack signals found: "
            + ", ".join(candidates)
            + ". Using priority: "
            + " > ".join(STACK_PRIORITY)
            + "."
        )
    stack = sorted(candidates, key=lambda item: STACK_PRIORITY.index(item))[0]

    if stack == "node":
        pm = choose_package_manager(repo, package_json)
        framework = detect_node_framework(package_json)
        scripts = package_json.get("scripts", {})
        scripts = scripts if isinstance(scripts, dict) else {}

        port = 5173 if framework == "vite" else 3000

        if framework == "nextjs":
            dev_command = (
                pm_run_script(pm, "dev", ["--hostname", "0.0.0.0", "--port", str(port)])
                if "dev" in scripts
                else f"next dev --hostname 0.0.0.0 --port {port}"
            )
            start_command = (
                pm_run_script(pm, "start")
                if "start" in scripts
                else f"next start --hostname 0.0.0.0 --port {port}"
            )
        elif framework == "vite":
            dev_command = (
                pm_run_script(pm, "dev", ["--host", "0.0.0.0", "--port", str(port)])
                if "dev" in scripts
                else f"vite --host 0.0.0.0 --port {port}"
            )
            if "preview" in scripts:
                start_command = pm_run_script(
                    pm, "preview", ["--host", "0.0.0.0", "--port", str(port)]
                )
            elif "start" in scripts:
                start_command = pm_run_script(pm, "start")
            else:
                start_command = f"vite preview --host 0.0.0.0 --port {port}"
        elif framework == "nest":
            dev_command = (
                pm_run_script(pm, "start:dev")
                if "start:dev" in scripts
                else pm_run_script(pm, "dev")
                if "dev" in scripts
                else "nest start --watch"
            )
            start_command = (
                pm_run_script(pm, "start:prod")
                if "start:prod" in scripts
                else pm_run_script(pm, "start")
                if "start" in scripts
                else "node dist/main.js"
            )
        else:
            dev_script = "dev" if "dev" in scripts else "start:dev" if "start:dev" in scripts else "start"
            dev_command = (
                pm_run_script(pm, dev_script)
                if dev_script in scripts
                else "node --watch ."
            )
            start_command = (
                pm_run_script(pm, "start")
                if "start" in scripts
                else "node server.js"
                if framework == "express"
                else "node ."
            )

        return Detection(
            stack=stack,
            framework=framework,
            package_manager=pm,
            port=port,
            start_command=start_command,
            dev_command=dev_command,
            notes=notes,
            scripts={str(k): str(v) for k, v in scripts.items()},
        )

    if stack == "python":
        framework = detect_python_framework(repo)
        port = 8000
        install_mode = "requirements"
        if (repo / "poetry.lock").exists():
            install_mode = "poetry"
        elif (repo / "pyproject.toml").exists() and "[tool.poetry]" in read_text_if_exists(
            repo / "pyproject.toml"
        ):
            install_mode = "poetry"
        elif (repo / "pyproject.toml").exists() and not (repo / "requirements.txt").exists():
            install_mode = "pyproject"

        if framework == "fastapi":
            module = detect_fastapi_module(repo)
            start_command = f"uvicorn {module}:app --host 0.0.0.0 --port {port}"
            dev_command = f"uvicorn {module}:app --host 0.0.0.0 --port {port} --reload"
            notes.append(f"Using FastAPI module '{module}'.")
        elif framework == "django":
            manage = detect_django_manage_path(repo)
            start_command = f"python {manage} runserver 0.0.0.0:{port}"
            dev_command = start_command
            notes.append(f"Using Django manage path '{manage}'.")
        else:
            entry = detect_python_entrypoint(repo)
            start_command = f"python {entry}"
            dev_command = start_command
            notes.append(f"Using Python entrypoint '{entry}'.")

        return Detection(
            stack=stack,
            framework=framework,
            package_manager=None,
            port=port,
            start_command=start_command,
            dev_command=dev_command,
            notes=notes,
            details={"python_install_mode": install_mode},
        )

    if stack == "go":
        target = detect_go_target(repo)
        port = 8080
        return Detection(
            stack=stack,
            framework=None,
            package_manager=None,
            port=port,
            start_command="/app/bin/app",
            dev_command=f"go run {target}",
            notes=notes + [f"Using Go build target '{target}'."],
            details={"go_target": target},
        )

    if stack == "rust":
        bin_name = parse_rust_bin_name(repo)
        port = 8080
        return Detection(
            stack=stack,
            framework=None,
            package_manager=None,
            port=port,
            start_command=f"/usr/local/bin/{bin_name}",
            dev_command="cargo run",
            notes=notes + [f"Using Rust binary name '{bin_name}'."],
            details={"rust_bin_name": bin_name},
        )

    raise RuntimeError(f"Unsupported detected stack: {stack}")


def node_install_command(det: Detection, repo: Path) -> str:
    pm = det.package_manager or "npm"
    if pm == "pnpm":
        return "corepack enable && pnpm install --frozen-lockfile"
    if pm == "yarn":
        return "corepack enable && yarn install --frozen-lockfile"
    if (repo / "package-lock.json").exists():
        return "npm ci"
    return "npm install"


def python_install_command(repo: Path, det: Detection) -> str:
    mode = str(det.details.get("python_install_mode", "requirements"))
    if mode == "poetry":
        return (
            "pip install --no-cache-dir --upgrade pip poetry && "
            "poetry config virtualenvs.create false && "
            "poetry install --no-interaction --no-ansi"
        )
    if mode == "pyproject":
        return "pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir ."
    return "pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt"


def generate_dockerfile(repo: Path, det: Detection) -> str:
    if det.stack == "node":
        install_cmd = node_install_command(det, repo)
        build_cmd = (
            pm_run_script(det.package_manager or "npm", "build") + " || true"
            if "build" in det.scripts
            else "echo \"No build script detected; skipping build step\""
        )
        return f"""FROM node:20-alpine
WORKDIR /app

COPY package.json ./
COPY package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN {install_cmd}

COPY . .
RUN {build_cmd}

EXPOSE {det.port}
CMD ["sh", "-c", "{det.start_command}"]
"""

    if det.stack == "python":
        install_cmd = python_install_command(repo, det)
        return f"""FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements*.txt pyproject.toml poetry.lock* ./
RUN {install_cmd}

COPY . .

EXPOSE {det.port}
CMD ["sh", "-c", "{det.start_command}"]
"""

    if det.stack == "go":
        target = str(det.details.get("go_target", "."))
        return f"""FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum* ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/bin/app {target}

FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/bin/app /app/bin/app

EXPOSE {det.port}
CMD ["/app/bin/app"]
"""

    if det.stack == "rust":
        bin_name = str(det.details.get("rust_bin_name", "app"))
        return f"""FROM rust:1.77 AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock* ./
RUN mkdir src && echo "fn main() {{}}" > src/main.rs && cargo build --release || true
RUN rm -rf src

COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/{bin_name} /usr/local/bin/{bin_name}

EXPOSE {det.port}
CMD ["/usr/local/bin/{bin_name}"]
"""

    raise RuntimeError(f"Unsupported stack: {det.stack}")


def generate_dockerignore(det: Detection) -> str:
    entries = [
        ".git",
        ".git/*",
        "__pycache__",
        "*.py[cod]",
        "*.log",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".DS_Store",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        ".env",
        ".env.*",
        "coverage",
        "dist",
        "build",
        "target",
    ]
    if det.stack == "node":
        entries.extend(["node_modules", ".next", ".turbo", ".pnpm-store"])
    if det.stack == "python":
        entries.extend([".tox", "*.sqlite3"])
    return "\n".join(dict.fromkeys(entries)) + "\n"


def generate_compose(det: Detection) -> str:
    return f"""services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env
    ports:
      - "${{PORT:-{det.port}}}:{det.port}"
    command: sh -c "{det.dev_command}"
"""


def generate_compose_override(det: Detection) -> str:
    lines = [
        "services:",
        "  app:",
        "    volumes:",
        "      - ./:/app",
    ]
    if det.stack == "node":
        lines.append("      - /app/node_modules")
    return "\n".join(lines) + "\n"


def generate_env_example(det: Detection) -> str:
    lines = [
        "# Copy this file to .env and adjust values for your machine.",
        f"PORT={det.port}",
    ]
    if det.stack == "node":
        lines.append("NODE_ENV=development")
    elif det.stack == "python":
        lines.append("PYTHONUNBUFFERED=1")
    elif det.stack == "go":
        lines.append("GO_ENV=development")
    elif det.stack == "rust":
        lines.append("RUST_LOG=info")
    return "\n".join(lines) + "\n"


def write_or_print(
    path: Path,
    content: str,
    *,
    dry_run: bool,
    force: bool,
) -> str:
    if path.exists() and not force:
        return "skipped (exists)"
    if dry_run:
        print(f"\n--- {path.name} ---")
        print(content.rstrip())
        return "previewed"
    path.write_text(content, encoding="utf-8")
    return "written"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect stack and generate Docker artifacts."
    )
    parser.add_argument("--repo", default=".", help="Path to the repository root.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file content instead of writing files.",
    )
    parser.add_argument(
        "--with-env-example",
        action="store_true",
        help="Create .env.example when it is missing.",
    )
    parser.add_argument(
        "--with-compose-override",
        action="store_true",
        help="Create compose.override.yml when it is missing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        raise RuntimeError(f"Repository path is invalid: {repo}")

    det = detect_project(repo)

    print(f"Detected stack: {det.stack}")
    if det.framework:
        print(f"Detected framework: {det.framework}")
    if det.package_manager:
        print(f"Detected package manager: {det.package_manager}")
    for note in det.notes:
        print(f"Note: {note}")

    outputs: list[tuple[Path, str]] = [
        (repo / "Dockerfile", generate_dockerfile(repo, det)),
        (repo / ".dockerignore", generate_dockerignore(det)),
        (repo / "docker-compose.yml", generate_compose(det)),
    ]

    if args.with_env_example and not (repo / ".env.example").exists():
        outputs.append((repo / ".env.example", generate_env_example(det)))
    if args.with_compose_override and not (repo / "compose.override.yml").exists():
        outputs.append((repo / "compose.override.yml", generate_compose_override(det)))

    print("\nGeneration plan:")
    for path, content in outputs:
        status = write_or_print(path, content, dry_run=args.dry_run, force=args.force)
        print(f"- {path.name}: {status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
