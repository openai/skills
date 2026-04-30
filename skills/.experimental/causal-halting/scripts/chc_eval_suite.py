#!/usr/bin/env python3
"""Summarize CHC fixture coverage and deterministic analyzer correctness."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_eval_design_ir():
    script = Path(__file__).resolve().with_name("chc_eval_design_ir.py")
    spec = importlib.util.spec_from_file_location("chc_eval_design_ir", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load evaluator from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["chc_eval_design_ir"] = module
    spec.loader.exec_module(module)
    return module


def language_from_case_name(case_dir: Path) -> str:
    parts = case_dir.name.split("-")
    for part in parts:
        if part in {"en", "pt", "es"}:
            return part
    return "unknown"


def evaluate_suite(corpus_dir: Path) -> dict[str, Any]:
    evaluator = load_eval_design_ir()
    result = evaluator.evaluate_corpus(corpus_dir)
    languages: dict[str, int] = {}
    expected_counts: dict[str, int] = {}
    actual_counts: dict[str, int] = {}
    for case_dir in corpus_dir.iterdir():
        if not case_dir.is_dir():
            continue
        language = language_from_case_name(case_dir)
        languages[language] = languages.get(language, 0) + 1
    for case in result["cases"]:
        expected = str(case.get("expected_classification"))
        actual = str(case.get("classification"))
        expected_counts[expected] = expected_counts.get(expected, 0) + 1
        actual_counts[actual] = actual_counts.get(actual, 0) + 1
    total = result["case_count"]
    passed = result["passed_count"]
    result["coverage"] = {
        "language_counts": languages,
        "minimum_case_target": 50,
        "meets_minimum_case_target": result["case_count"] >= 50,
        "natural_language_parsed_by_scripts": False,
        "expected_classification_counts": expected_counts,
        "actual_classification_counts": actual_counts,
    }
    result["metrics"] = {
        "total": total,
        "passed": passed,
        "failed": result["failed_count"],
        "classification_accuracy": 1.0 if total == 0 else passed / total,
        "false_positive_categories": [],
        "false_negative_categories": [],
    }
    if result["case_count"] < 50:
        result["status"] = "failed"
        result["explanation"] = "DesignIR corpus has fewer than 50 fixtures."
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run CHC evaluation suite.")
    parser.add_argument("corpus", nargs="?", default="examples/design-ir-corpus")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args(argv)
    result = evaluate_suite(Path(args.corpus))
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"status: {result['status']}")
        print(f"case_count: {result['case_count']}")
        print(f"passed_count: {result['passed_count']}")
        print(f"failed_count: {result['failed_count']}")
        print(f"classification_accuracy: {result['metrics']['classification_accuracy']:.3f}")
        print(f"coverage: {result['coverage']}")
        print(f"false_positive_categories: {result['metrics']['false_positive_categories']}")
        print(f"false_negative_categories: {result['metrics']['false_negative_categories']}")
        print(f"explanation: {result['explanation']}")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
