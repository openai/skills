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


def read_description(case_dir: Path) -> str:
    path = case_dir / "description.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def language_guess(text: str) -> str:
    lowered = text.lower()
    if "execucao" in lowered or "rodada" in lowered or "avaliacao" in lowered:
        return "pt"
    if "ejecucion" in lowered or "evaluacion" in lowered or "misma" in lowered:
        return "es"
    return "en"


def evaluate_suite(corpus_dir: Path) -> dict[str, Any]:
    evaluator = load_eval_design_ir()
    result = evaluator.evaluate_corpus(corpus_dir)
    languages: dict[str, int] = {}
    for case_dir in corpus_dir.iterdir():
        if not case_dir.is_dir():
            continue
        language = language_guess(read_description(case_dir))
        languages[language] = languages.get(language, 0) + 1
    result["coverage"] = {
        "language_counts": languages,
        "minimum_case_target": 50,
        "meets_minimum_case_target": result["case_count"] >= 50,
        "natural_language_parsed_by_scripts": False,
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
        print(f"coverage: {result['coverage']}")
        print(f"explanation: {result['explanation']}")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
