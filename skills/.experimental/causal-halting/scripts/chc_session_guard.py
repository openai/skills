#!/usr/bin/env python3
"""UserPromptSubmit hook for low-cost Causal Halting context injection.

This script does not classify natural-language prompts. It always emits a
compact structural guard, and it emits a stronger guard when explicit session
mode is enabled for the current session_id.
"""

from __future__ import annotations

import json
import re
import sys
import argparse
import importlib.util
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_GUARD = (
    "Silently check whether the prompt involves prediction, observation, "
    "simulation, or evaluation about an execution that may control that same "
    "execution. If yes, apply CHC-0 hygiene and distinguish causal_paradox "
    "from unproved. If no, ignore this instruction and answer normally. Do "
    "not mention CHC-0 unless it materially improves the answer."
)

SESSION_GUARD = (
    "Causal Halting session mode is active. For every answer, silently check "
    "for prediction-feedback structure. When relevant, identify Code, Exec, "
    "H, and HaltResult; classify structural feedback as causal_paradox and "
    "unresolved semantic cases as unproved. If unrelated, answer normally "
    "without forcing CHC terminology."
)

ENABLE_COMMANDS = {
    "causal-halting session on",
    "causal halting session on",
    "use causal-halting for this session",
    "enable causal-halting for this session",
}

DISABLE_COMMANDS = {
    "causal-halting session off",
    "causal halting session off",
    "stop causal-halting for this session",
    "disable causal-halting for this session",
}


def normalize_command(prompt: str) -> str:
    return " ".join(prompt.strip().lower().split())


def safe_session_id(session_id: str | None) -> str | None:
    if not session_id:
        return None
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id.strip())[:128]
    return safe or None


def project_root(event: dict[str, Any]) -> Path:
    cwd = event.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return Path(cwd).expanduser()
    return Path.cwd()


def state_path(root: Path, session_id: str) -> Path:
    return root / ".codex" / "causal-halting" / "sessions" / f"{session_id}.json"


def project_state_path(root: Path) -> Path:
    return root / ".codex" / "causal-halting" / "session-mode.json"


def read_session_enabled(root: Path, session_id: str | None) -> bool:
    if session_id is None:
        return False
    path = state_path(root, session_id)
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return bool(data.get("enabled"))


def read_project_enabled(root: Path) -> bool:
    path = project_state_path(root)
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return bool(data.get("enabled"))


def write_session_state(root: Path, session_id: str, enabled: bool) -> None:
    path = state_path(root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "enabled": enabled,
        "session_id": session_id,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_project_state(root: Path, enabled: bool) -> Path:
    path = project_state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "enabled": enabled,
        "scope": "project",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def parse_hook_input(raw: str) -> dict[str, Any]:
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if isinstance(data, dict):
        return data
    return {}


def prompt_text(event: dict[str, Any]) -> str:
    value = event.get("user_prompt")
    if isinstance(value, str):
        return value
    value = event.get("prompt")
    if isinstance(value, str):
        return value
    return ""


def hook_response(system_message: str) -> dict[str, Any]:
    return {
        "continue": True,
        "suppressOutput": True,
        "systemMessage": system_message,
    }


def handle_event(event: dict[str, Any]) -> dict[str, Any]:
    root = project_root(event)
    session_id = safe_session_id(event.get("session_id") if isinstance(event.get("session_id"), str) else None)
    command = normalize_command(prompt_text(event))

    if session_id and command in ENABLE_COMMANDS:
        write_session_state(root, session_id, True)
        return hook_response(SESSION_GUARD)

    if session_id and command in DISABLE_COMMANDS:
        write_session_state(root, session_id, False)
        return hook_response(DEFAULT_GUARD)

    if read_session_enabled(root, session_id) or read_project_enabled(root):
        return hook_response(SESSION_GUARD)

    return hook_response(DEFAULT_GUARD)


def handle_raw_input(raw: str) -> dict[str, Any]:
    return handle_event(parse_hook_input(raw))


def explain_result(root: Path) -> dict[str, Any]:
    return {
        "mode": "explain",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": "Causal Halting uses a low-cost structural guard, not keyword matching.",
        "structural_trigger": "Obs/Pred(E) -> Result -> Control(E)",
        "default_guard": DEFAULT_GUARD,
        "session_guard": SESSION_GUARD,
    }


def check_file(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return {
            "mode": "check",
            "enabled": read_project_enabled(root),
            "scope": "project",
            "state_path": str(project_state_path(root)),
            "message": "Missing file path. Usage: /causal-halting check <file>",
        }

    path = Path(target).expanduser()
    if not path.is_absolute():
        path = root / path
    if not path.exists() or not path.is_file():
        return {
            "mode": "check",
            "enabled": read_project_enabled(root),
            "scope": "project",
            "state_path": str(project_state_path(root)),
            "message": f"File not found: {path}",
        }

    chc_check = load_chc_check()

    result = chc_check.analyze_text(path.read_text(encoding="utf-8"))
    return {
        "mode": "check",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Checked {path}",
        "file": str(path),
        "classification": result["classification"],
        "semantic_status": result["semantic_status"],
        "checker_output": chc_check.format_human(result),
    }


def analyze_design(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "analyze-design", "Missing design text or file path. Usage: /causal-halting analyze-design <text-or-file>")

    chc_design = load_script_module("chc_design_analyze")
    text = read_target_or_literal(root, target)
    result = chc_design.analyze_design(text)
    message = "Analyzed DesignIR." if result["classification"] != "needs_design_ir" else "DesignIR required before analysis."
    return {
        "mode": "analyze-design",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": message,
        "classification": result["classification"],
        "analysis_output": chc_design.format_human(result),
        "analysis_json": result,
    }


def analyze_trace(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "analyze-trace", "Missing trace file path. Usage: /causal-halting analyze-trace <jsonl-file>")

    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, "analyze-trace", f"File not found: {root / target}")

    chc_trace = load_script_module("chc_trace_check")
    result = chc_trace.analyze_text(path.read_text(encoding="utf-8"))
    return {
        "mode": "analyze-trace",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Analyzed trace {path}",
        "classification": result["classification"],
        "analysis_output": chc_trace.format_human(result),
        "analysis_json": result,
    }


def analyze_json_file(root: Path, target: str | None, script_name: str, function_name: str, mode: str, usage: str) -> dict[str, Any]:
    if not target:
        return command_file_error(root, mode, usage)
    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, mode, f"File not found: {root / target}")
    module = load_script_module(script_name)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return command_file_error(root, mode, f"Invalid JSON: {exc}")
    result = getattr(module, function_name)(payload if isinstance(payload, dict) else {})
    return {
        "mode": mode,
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Analyzed {path}",
        "classification": result["classification"],
        "analysis_output": json.dumps(result, indent=2, sort_keys=True),
        "analysis_json": result,
    }


def analyze_temporal(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "analyze-temporal", "Missing temporal trace file path.")
    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, "analyze-temporal", f"File not found: {root / target}")
    module = load_script_module("chc_temporal_check")
    result = module.analyze_temporal_text(path.read_text(encoding="utf-8"))
    return {
        "mode": "analyze-temporal",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Analyzed temporal trace {path}",
        "classification": result["classification"],
        "analysis_output": json.dumps(result, indent=2, sort_keys=True),
        "analysis_json": result,
    }


def repair_file(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "repair", "Missing analysis JSON file path. Usage: /causal-halting repair <analysis-json>")

    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, "repair", f"File not found: {root / target}")

    chc_repair = load_script_module("chc_repair")
    try:
        analysis = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return command_file_error(root, "repair", f"Invalid analysis JSON: {exc}")
    result = chc_repair.repair_analysis(analysis if isinstance(analysis, dict) else {})
    return {
        "mode": "repair",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Generated repair report for {path}",
        "classification": result["classification"],
        "analysis_output": chc_repair.format_human(result),
        "analysis_json": result,
    }


def adapt_workflow(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "adapt-workflow", "Missing workflow JSON file path. Usage: /causal-halting adapt-workflow <workflow-json>")

    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, "adapt-workflow", f"File not found: {root / target}")

    adapter = load_script_module("chc_workflow_adapter")
    try:
        workflow = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return command_file_error(root, "adapt-workflow", f"Invalid workflow JSON: {exc}")
    errors = adapter.validate_workflow(workflow if isinstance(workflow, dict) else {})
    if errors:
        return command_file_error(root, "adapt-workflow", "; ".join(errors))
    events = adapter.workflow_to_events(workflow)
    return {
        "mode": "adapt-workflow",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Converted workflow {path} to CHC trace events.",
        "classification": "not_analyzed",
        "analysis_output": adapter.format_jsonl(events),
        "analysis_json": {"events": events},
    }


def adapt_structured(root: Path, target: str | None, adapter_name: str, mode: str, usage: str) -> dict[str, Any]:
    if not target:
        return command_file_error(root, mode, usage)

    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, mode, f"File not found: {root / target}")

    adapter = load_script_module(adapter_name)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return command_file_error(root, mode, f"Invalid JSON: {exc}")

    if adapter_name == "chc_otel_adapter":
        events = adapter.otel_to_events(payload)
        errors = adapter.validate_events(events)
    elif adapter_name == "chc_temporal_airflow_adapter":
        if not isinstance(payload, dict):
            return command_file_error(root, mode, "Input must be a JSON object.")
        errors = adapter.validate_payload(payload)
        events = adapter.temporal_airflow_to_events(payload)
    else:
        if not isinstance(payload, dict):
            return command_file_error(root, mode, "Input must be a JSON object.")
        errors = adapter.validate_payload(payload)
        events = adapter.langgraph_to_events(payload)
    if errors:
        return command_file_error(root, mode, "; ".join(errors))
    return {
        "mode": mode,
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Converted {path} to CHC trace events.",
        "classification": "not_analyzed",
        "analysis_output": adapter.format_jsonl(events),
        "analysis_json": {"events": events},
    }


def eval_design_ir(root: Path, target: str | None) -> dict[str, Any]:
    corpus = resolve_existing_dir(root, target or "examples/design-ir-corpus")
    if corpus is None:
        return command_file_error(root, "eval-design-ir", "Corpus directory not found.")

    evaluator = load_script_module("chc_eval_design_ir")
    result = evaluator.evaluate_corpus(corpus)
    return {
        "mode": "eval-design-ir",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Evaluated DesignIR corpus {corpus}",
        "classification": result["status"],
        "analysis_output": evaluator.format_human(result),
        "analysis_json": result,
    }


def eval_suite(root: Path, target: str | None) -> dict[str, Any]:
    corpus = resolve_existing_dir(root, target or "examples/design-ir-corpus")
    if corpus is None:
        return command_file_error(root, "eval-suite", "Corpus directory not found.")
    evaluator = load_script_module("chc_eval_suite")
    result = evaluator.evaluate_suite(corpus)
    return {
        "mode": "eval-suite",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Evaluated CHC suite {corpus}",
        "classification": result["status"],
        "analysis_output": json.dumps(result, indent=2, sort_keys=True),
        "analysis_json": result,
    }


def verify_repair(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "verify-repair", "Missing trace paths. Usage: /causal-halting verify-repair <before-jsonl> <after-jsonl> [repair-json]")

    parts = target.split()
    if len(parts) not in {2, 3}:
        return command_file_error(root, "verify-repair", "verify-repair requires two trace file paths and optional repair JSON.")
    before = resolve_existing_file(root, parts[0])
    after = resolve_existing_file(root, parts[1])
    if before is None or after is None:
        return command_file_error(root, "verify-repair", "One or both trace files were not found.")
    obligations = None
    if len(parts) == 3:
        repair_path = resolve_existing_file(root, parts[2])
        if repair_path is None:
            return command_file_error(root, "verify-repair", "Repair JSON file was not found.")
        try:
            repair = json.loads(repair_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return command_file_error(root, "verify-repair", f"Invalid repair JSON: {exc}")
        if isinstance(repair, dict) and isinstance(repair.get("proof_obligations"), list):
            obligations = repair["proof_obligations"]

    verifier = load_script_module("chc_verify_repair")
    result = verifier.verify_repair(
        before.read_text(encoding="utf-8"),
        after.read_text(encoding="utf-8"),
        obligations,
    )
    return {
        "mode": "verify-repair",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Verified repair {before} -> {after}",
        "classification": result["verification"],
        "analysis_output": verifier.format_human(result),
        "analysis_json": result,
    }


def certificate(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "certificate", "Missing trace paths. Usage: /causal-halting certificate <before-jsonl> <after-jsonl> [repair-json]")
    verified = verify_repair(root, target)
    if "analysis_json" not in verified:
        return verified
    module = load_script_module("chc_certificate")
    cert = module.certificate_from_verification(verified["analysis_json"])
    return {
        "mode": "certificate",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": "Generated repair certificate.",
        "classification": cert["result"],
        "analysis_output": json.dumps(cert, indent=2, sort_keys=True),
        "analysis_json": cert,
    }


def report_file(root: Path, target: str | None) -> dict[str, Any]:
    if not target:
        return command_file_error(root, "report", "Missing analysis JSON file path. Usage: /causal-halting report <analysis-json>")

    path = resolve_existing_file(root, target)
    if path is None:
        return command_file_error(root, "report", f"File not found: {root / target}")
    reporter = load_script_module("chc_report")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return command_file_error(root, "report", f"Invalid JSON: {exc}")
    if not isinstance(data, dict):
        return command_file_error(root, "report", "Input must be a JSON object.")
    return {
        "mode": "report",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": f"Rendered CHC report for {path}",
        "classification": data.get("classification", data.get("verification", "unknown")),
        "analysis_output": reporter.render_markdown(data),
        "analysis_json": data,
    }


def command_file_error(root: Path, mode: str, message: str) -> dict[str, Any]:
    return {
        "mode": mode,
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": message,
    }


def resolve_existing_file(root: Path, target: str) -> Path | None:
    path = Path(target).expanduser()
    if not path.is_absolute():
        path = root / path
    if path.exists() and path.is_file():
        return path
    return None


def resolve_existing_dir(root: Path, target: str) -> Path | None:
    path = Path(target).expanduser()
    if not path.is_absolute():
        path = root / path
    if path.exists() and path.is_dir():
        return path
    return None


def read_target_or_literal(root: Path, target: str) -> str:
    path = resolve_existing_file(root, target)
    if path is not None:
        return path.read_text(encoding="utf-8")
    return target


def load_chc_check():
    return load_script_module("chc_check")


def load_script_module(name: str):
    script = Path(__file__).resolve().with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def command_result(root: Path, mode: str, target: str | None = None) -> dict[str, Any]:
    normalized = normalize_command(mode or "status")
    if normalized in {"on", "enable", "enabled"}:
        path = write_project_state(root, True)
        return {
            "mode": "on",
            "enabled": True,
            "scope": "project",
            "state_path": str(path),
            "message": "Causal Halting session mode is enabled for this workspace.",
        }
    if normalized in {"off", "disable", "disabled"}:
        path = write_project_state(root, False)
        return {
            "mode": "off",
            "enabled": False,
            "scope": "project",
            "state_path": str(path),
            "message": "Causal Halting session mode is disabled for this workspace.",
        }
    if normalized in {"status", ""}:
        enabled = read_project_enabled(root)
        return {
            "mode": "status",
            "enabled": enabled,
            "scope": "project",
            "state_path": str(project_state_path(root)),
            "message": (
                "Causal Halting session mode is enabled for this workspace."
                if enabled
                else "Causal Halting session mode is not enabled for this workspace."
            ),
        }
    if normalized == "explain":
        return explain_result(root)
    if normalized == "check":
        return check_file(root, target)
    if normalized == "analyze-design":
        return analyze_design(root, target)
    if normalized == "analyze-trace":
        return analyze_trace(root, target)
    if normalized == "analyze-process":
        return analyze_json_file(
            root,
            target,
            "chc_process_check",
            "analyze_process_ir",
            "analyze-process",
            "Missing ProcessIR JSON file path. Usage: /causal-halting analyze-process <process-ir-json>",
        )
    if normalized == "analyze-temporal":
        return analyze_temporal(root, target)
    if normalized == "analyze-prediction":
        return analyze_json_file(
            root,
            target,
            "chc_prediction_check",
            "analyze_prediction_ir",
            "analyze-prediction",
            "Missing PredictionIR JSON file path. Usage: /causal-halting analyze-prediction <prediction-ir-json>",
        )
    if normalized == "repair":
        return repair_file(root, target)
    if normalized == "adapt-workflow":
        return adapt_workflow(root, target)
    if normalized == "adapt-otel":
        return adapt_structured(
            root,
            target,
            "chc_otel_adapter",
            "adapt-otel",
            "Missing OpenTelemetry JSON file path. Usage: /causal-halting adapt-otel <otel-json>",
        )
    if normalized == "adapt-langgraph":
        return adapt_structured(
            root,
            target,
            "chc_langgraph_adapter",
            "adapt-langgraph",
            "Missing LangGraph-style JSON file path. Usage: /causal-halting adapt-langgraph <langgraph-json>",
        )
    if normalized == "adapt-temporal-airflow":
        return adapt_structured(
            root,
            target,
            "chc_temporal_airflow_adapter",
            "adapt-temporal-airflow",
            "Missing Temporal/Airflow-style JSON file path. Usage: /causal-halting adapt-temporal-airflow <temporal-airflow-json>",
        )
    if normalized == "eval-design-ir":
        return eval_design_ir(root, target)
    if normalized == "eval-suite":
        return eval_suite(root, target)
    if normalized == "verify-repair":
        return verify_repair(root, target)
    if normalized == "certificate":
        return certificate(root, target)
    if normalized == "report":
        return report_file(root, target)
    return {
        "mode": "invalid",
        "enabled": read_project_enabled(root),
        "scope": "project",
        "state_path": str(project_state_path(root)),
        "message": "Invalid mode. Use: on, off, status, explain, check <file>, analyze-design <design-ir-json>, analyze-trace <jsonl-file>, analyze-process <process-ir-json>, analyze-temporal <temporal-jsonl>, analyze-prediction <prediction-ir-json>, repair <analysis-json>, adapt-workflow <workflow-json>, adapt-otel <otel-json>, adapt-langgraph <langgraph-json>, adapt-temporal-airflow <temporal-airflow-json>, eval-design-ir <corpus-dir>, eval-suite <corpus-dir>, verify-repair <before> <after> [repair-json], certificate <before> <after> [repair-json], or report <analysis-json>.",
    }


def format_command_human(result: dict[str, Any]) -> str:
    if result["mode"] == "explain":
        return (
            f"{result['message']}\n"
            f"structural_trigger: {result['structural_trigger']}\n"
            f"default_guard: {result['default_guard']}\n"
            f"session_guard: {result['session_guard']}"
        )
    if result["mode"] == "check" and "checker_output" in result:
        return f"{result['message']}\n{result['checker_output']}"
    if result["mode"] in {
        "analyze-design",
        "analyze-trace",
        "analyze-process",
        "analyze-temporal",
        "analyze-prediction",
        "repair",
        "adapt-workflow",
        "adapt-otel",
        "adapt-langgraph",
        "adapt-temporal-airflow",
        "eval-design-ir",
        "eval-suite",
        "verify-repair",
        "certificate",
        "report",
    } and "analysis_output" in result:
        return f"{result['message']}\n{result['analysis_output']}"
    status = "enabled" if result.get("enabled") else "disabled"
    return (
        f"{result['message']}\n"
        f"status: {status}\n"
        f"scope: {result['scope']}\n"
        f"state_path: {result['state_path']}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Causal Halting hook/session guard.")
    parser.add_argument("mode_arg", nargs="?", help="Workspace session mode: on, off, or status.")
    parser.add_argument("target_args", nargs="*", help="File path or text for command mode.")
    parser.add_argument("--mode", help="Manage workspace session mode: on, off, or status.")
    parser.add_argument("--target", help="File path for check mode.")
    parser.add_argument("--cwd", help="Workspace directory for command mode. Defaults to current directory.")
    parser.add_argument(
        "--format",
        choices=("hook", "json", "human"),
        default="hook",
        help="Output format. Default reads hook stdin and returns hook JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    mode = args.mode if args.mode is not None else args.mode_arg
    target = args.target if args.target is not None else (" ".join(args.target_args) if args.target_args else None)
    if mode is not None or args.format != "hook":
        root = Path(args.cwd).expanduser() if args.cwd else Path.cwd()
        result = command_result(root, mode or "status", target)
        if args.format == "json":
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(format_command_human(result))
        return 0 if result["mode"] != "invalid" else 2

    result = handle_raw_input(sys.stdin.read())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
