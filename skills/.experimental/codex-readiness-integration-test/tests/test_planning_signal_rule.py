from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_rules_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "deterministic_rules.py"
    spec = importlib.util.spec_from_file_location("deterministic_rules", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load deterministic_rules module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RULES = load_rules_module()


def write_run_dir(run_dir: Path, log_text: str) -> None:
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    (run_dir / "prompt.json").write_text(json.dumps({"change_prompt": "x"}), encoding="utf-8")
    (run_dir / "logs" / "agentic.log").write_text(log_text, encoding="utf-8")


def check(run_dir: Path) -> dict:
    return RULES.check_exec_plan_before_code_changes(
        run_dir,
        {"prompt_path": "prompt.json", "agentic_log_path": "logs/agentic.log"},
    )


def test_planning_signal_before_code_change_passes(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-pass"
    log_text = "\n".join(
        [
            "Plan: inspect code paths",
            "file update",
            "M src/app.py",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "PASS"
    assert "before code changes" in result["rationale"]


def test_planning_signal_after_code_change_fails(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-fail-ordering"
    log_text = "\n".join(
        [
            "file update",
            "M src/app.py",
            "Plan: now I will describe the approach",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "FAIL"
    assert "after code changes" in result["rationale"]


def test_plan_file_path_does_not_count_as_planning_signal(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-plan-path"
    log_text = "\n".join(
        [
            "file update",
            "M docs/exec-plan.md",
            "file update",
            "M src/app.py",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "FAIL"
    assert "No planning signal detected" in result["rationale"]


def test_no_code_changes_warns(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-warn-no-code"
    log_text = "\n".join(
        [
            "Plan: investigate the issue",
            "file update",
            "M docs/notes.md",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "WARN"
    assert "ordering not evaluated" in result["rationale"]
