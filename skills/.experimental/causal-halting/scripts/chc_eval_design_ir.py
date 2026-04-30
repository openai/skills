#!/usr/bin/env python3
"""Evaluate DesignIR corpus fixtures without analyzing prose.

The corpus contains natural-language descriptions for humans and expected
DesignIR JSON for verification. This script intentionally does not classify or
parse prose. It only checks that expected DesignIR artifacts are valid and that
the deterministic analyzer returns the expected classification.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_design_analyzer():
    script = Path(__file__).resolve().with_name("chc_design_analyze.py")
    spec = importlib.util.spec_from_file_location("chc_design_analyze", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load design analyzer from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["chc_design_analyze"] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def evaluate_case(case_dir: Path, analyzer: Any) -> dict[str, Any]:
    design_path = case_dir / "expected.design-ir.json"
    analysis_path = case_dir / "expected.analysis.json"
    description_path = case_dir / "description.md"
    missing = [str(path.name) for path in (design_path, analysis_path, description_path) if not path.is_file()]
    if missing:
        return {
            "case": case_dir.name,
            "status": "failed",
            "classification": None,
            "expected_classification": None,
            "errors": [f"missing required file(s): {', '.join(missing)}"],
        }

    design_ir, design_error = load_json(design_path)
    expected, expected_error = load_json(analysis_path)
    errors = [error for error in (design_error, expected_error) if error]
    if errors:
        return {
            "case": case_dir.name,
            "status": "failed",
            "classification": None,
            "expected_classification": None,
            "errors": errors,
        }
    if not isinstance(design_ir, dict) or not isinstance(expected, dict):
        return {
            "case": case_dir.name,
            "status": "failed",
            "classification": None,
            "expected_classification": None,
            "errors": ["expected.design-ir.json and expected.analysis.json must be JSON objects"],
        }

    result = analyzer.analyze_design(json.dumps(design_ir))
    expected_classification = expected.get("classification")
    errors = []
    if result.get("classification") != expected_classification:
        errors.append(
            f"classification mismatch: expected {expected_classification!r}, got {result.get('classification')!r}"
        )
    if result.get("classification") == "parse_error":
        errors.append(result.get("explanation", "parse_error"))

    return {
        "case": case_dir.name,
        "status": "passed" if not errors else "failed",
        "classification": result.get("classification"),
        "expected_classification": expected_classification,
        "errors": errors,
    }


def evaluate_corpus(corpus_dir: Path) -> dict[str, Any]:
    analyzer = load_design_analyzer()
    cases = [
        evaluate_case(case_dir, analyzer)
        for case_dir in sorted(corpus_dir.iterdir())
        if case_dir.is_dir()
    ]
    failed = [case for case in cases if case["status"] != "passed"]
    return {
        "status": "passed" if not failed else "failed",
        "case_count": len(cases),
        "passed_count": len(cases) - len(failed),
        "failed_count": len(failed),
        "cases": cases,
        "explanation": (
            "All expected DesignIR fixtures matched their expected classifications."
            if not failed
            else "One or more expected DesignIR fixtures failed validation."
        ),
    }


def format_human(result: dict[str, Any]) -> str:
    lines = [
        f"status: {result['status']}",
        f"case_count: {result['case_count']}",
        f"passed_count: {result['passed_count']}",
        f"failed_count: {result['failed_count']}",
        f"explanation: {result['explanation']}",
    ]
    for case in result["cases"]:
        lines.append(
            f"- {case['case']}: {case['status']} "
            f"({case['classification']} expected {case['expected_classification']})"
        )
        for error in case["errors"]:
            lines.append(f"  error: {error}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate DesignIR corpus fixtures.")
    parser.add_argument("corpus", nargs="?", default="examples/design-ir-corpus", help="DesignIR corpus directory.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    corpus_dir = Path(args.corpus).expanduser()
    if not corpus_dir.is_dir():
        result = {
            "status": "failed",
            "case_count": 0,
            "passed_count": 0,
            "failed_count": 0,
            "cases": [],
            "explanation": f"Corpus directory not found: {corpus_dir}",
        }
    else:
        result = evaluate_corpus(corpus_dir)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_human(result))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
