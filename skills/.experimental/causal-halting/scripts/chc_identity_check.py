#!/usr/bin/env python3
"""Validate identity-resolution metadata emitted by CHC analyzers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_KEYS = ("resolved", "ambiguous", "missing", "conflicts", "assumptions")


def validate_identity_resolution(data: dict[str, Any]) -> list[str]:
    report = data.get("identity_resolution")
    if not isinstance(report, dict):
        return ["identity_resolution must be an object"]
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if not isinstance(report.get(key), list):
            errors.append(f"identity_resolution.{key} must be a list")
    if data.get("classification") == "valid_acyclic":
        if report.get("ambiguous") or report.get("missing") or report.get("conflicts"):
            errors.append("valid_acyclic cannot contain ambiguous, missing, or conflicting identity evidence")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate CHC identity-resolution output.")
    parser.add_argument("input")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        errors = validate_identity_resolution(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors = [str(exc)]
    result = {"valid": not errors, "errors": errors}
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif errors:
        print("invalid")
        for error in errors:
            print(f"- {error}")
    else:
        print("valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
