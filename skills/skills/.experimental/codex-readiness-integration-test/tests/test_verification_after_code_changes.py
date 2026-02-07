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


def write_run_dir(run_dir: Path, log_text: str, build_test_plan: list[dict] | None = None) -> None:
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    prompt = {
        "change_prompt": "x",
        "build_test_plan": build_test_plan or [],
    }
    (run_dir / "prompt.json").write_text(json.dumps(prompt), encoding="utf-8")
    (run_dir / "logs" / "agentic.log").write_text(log_text, encoding="utf-8")


def check(run_dir: Path) -> dict:
    return RULES.check_verification_after_code_changes(
        run_dir,
        {"prompt_path": "prompt.json", "agentic_log_path": "logs/agentic.log"},
    )


def test_verification_command_after_code_change_passes(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-pass"
    log_text = "\n".join(
        [
            "file update",
            "M src/app.py",
            "$ pytest -q",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "PASS"
    assert "after code changes" in result["rationale"]


def test_verification_only_before_code_change_fails(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-fail-order"
    log_text = "\n".join(
        [
            "$ pytest -q",
            "file update",
            "M src/app.py",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "FAIL"
    assert "No build/test/lint verification command detected" in result["rationale"]


def test_prompt_plan_command_counts_as_verification(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-pass-prompt-command"
    build_test_plan = [{"label": "verify", "cmd": "make check-all"}]
    log_text = "\n".join(
        [
            "file update",
            "M src/core.py",
            "$ make check-all",
        ]
    )
    write_run_dir(run_dir, log_text, build_test_plan=build_test_plan)

    result = check(run_dir)

    assert result["status"] == "PASS"


def test_codex_exec_lines_do_not_count_as_verification(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-fail-codex-line"
    log_text = "\n".join(
        [
            "file update",
            "M src/app.py",
            '$ codex exec -C /repo "please run tests after this change"',
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "FAIL"
    assert "No build/test/lint verification command detected" in result["rationale"]


def test_no_code_changes_warns(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-warn-no-code"
    log_text = "\n".join(
        [
            "file update",
            "M docs/notes.md",
            "$ pytest -q",
        ]
    )
    write_run_dir(run_dir, log_text)

    result = check(run_dir)

    assert result["status"] == "WARN"
    assert "ordering not evaluated" in result["rationale"]
