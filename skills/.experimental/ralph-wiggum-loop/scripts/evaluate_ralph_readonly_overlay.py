#!/usr/bin/env python3
"""Run a bounded comparison pilot between Ralph control and read-only audit overlay runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
AUTO_MEMORY_DIR = Path(os.environ.get("AUTO_MEMORY_DIR", CODEX_HOME / "skills" / "auto-memory"))
RALPH_DIR = Path(os.environ.get("RALPH_DIR", CODEX_HOME / "skills" / "ralph-wiggum-loop"))
RALPH_LOOP = RALPH_DIR / "scripts" / "ralph_loop.py"
AUTO_MEMORY_SAVE = AUTO_MEMORY_DIR / "scripts" / "save_memory.py"
DEMO_REPO_GENERATOR = RALPH_DIR / "scripts" / "demo_repo_generator.py"
COMPACTION_HANDOFF = AUTO_MEMORY_DIR / "scripts" / "compaction_handoff.py"


@dataclass
class RunSpec:
    trigger_index: int
    pattern: str
    mode: str
    readonly: bool
    max_iterations: int
    allow_search: bool = True
    search_disabled_simulated: bool = False
    induce_verification_failure: bool = False
    induce_compaction_cycle: bool = False


@dataclass
class LoopEvalRunRecord:
    run_id: str
    pattern: str
    trigger_index: int
    goal: str
    repo_path: str
    mode: str
    max_iterations: int
    status: str
    acceptance_met: bool
    acceptance_criteria: list[str]
    verification_summary: str
    failure_domain: str
    changed_files: list[str]
    compaction_checkpoint_id: str | None
    changed_file_count: int
    changed_in_readonly: bool
    run_seconds: float
    test_command: str
    output_last_message_path: str | None
    artifact_schema_version: str
    decision: str
    readonly: bool
    search_enabled: bool
    search_disabled_simulated: bool
    verification_failure_injected: bool
    compaction_cycle_injected: bool
    baseline_mutation_injected: bool
    timestamp_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AggregateState:
    project: str
    target_triggers: int
    trigger_count: int
    control_runs: int
    control_pass: int
    audit_runs: int
    audit_pass: int
    read_only_mutations: int
    search_disabled_simulated_runs: int
    verification_failure_injected_runs: int
    compaction_cycle_injected_runs: int
    run_seconds_total: float
    failure_domains: Counter
    confidence_notes: list[str]

    def overall_pass_rate(self) -> float:
        if self.trigger_count == 0:
            return 0.0
        return (self.control_pass + self.audit_pass) / self.trigger_count

    def control_pass_rate(self) -> float:
        if self.control_runs == 0:
            return 0.0
        return self.control_pass / self.control_runs

    def audit_pass_rate(self) -> float:
        if self.audit_runs == 0:
            return 0.0
        return self.audit_pass / self.audit_runs

    def avg_duration_seconds(self) -> float:
        if self.trigger_count == 0:
            return 0.0
        return self.run_seconds_total / self.trigger_count

    def record(self, run: LoopEvalRunRecord) -> None:
        self.trigger_count += 1
        self.run_seconds_total += run.run_seconds
        self.failure_domains[run.failure_domain or "none"] += 1
        self.confidence_notes.append(
            f"run={run.run_id} pattern={run.pattern} status={run.status} acceptance={str(run.acceptance_met).lower()}"
        )

        if run.pattern == "ralph_control":
            self.control_runs += 1
            if run.acceptance_met:
                self.control_pass += 1
        elif run.pattern == "readonly_audit":
            self.audit_runs += 1
            if run.acceptance_met and not run.changed_in_readonly:
                self.audit_pass += 1

        if run.pattern == "readonly_audit" and run.changed_in_readonly:
            self.read_only_mutations += 1
        if run.search_disabled_simulated:
            self.search_disabled_simulated_runs += 1
        if run.verification_failure_injected:
            self.verification_failure_injected_runs += 1
        if run.compaction_cycle_injected:
            self.compaction_cycle_injected_runs += 1


def _run_cmd(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd is not None else None,
        text=True,
        capture_output=True,
        check=False,
    )


def _now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _parse_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _latest_iteration_file(iterations_dir: Path) -> Path | None:
    files = sorted(iterations_dir.glob("iter_*.json"))
    return files[-1] if files else None


def _latest_state_file(work_root: Path) -> Path | None:
    state = work_root / ".ralph" / "state.json"
    return state if state.exists() else None


def _ensure_demo_repo(repo_path: Path, regenerate: bool) -> None:
    if regenerate and repo_path.exists():
        shutil.rmtree(repo_path)
    if repo_path.exists() and any(repo_path.iterdir()):
        return

    if repo_path.exists() and not repo_path.is_dir():
        raise ValueError(f"--repo-path is not a directory: {repo_path}")

    _run_cmd([
        sys.executable,
        str(DEMO_REPO_GENERATOR),
        "--output",
        str(repo_path),
        "--force",
    ])


def _find_test_file(repo_path: Path) -> Path | None:
    test_candidates = sorted(repo_path.rglob("test_*.py"))
    if not test_candidates:
        test_candidates = sorted(repo_path.rglob("*_test.py"))
    return test_candidates[0] if test_candidates else None


def _inject_failing_test(repo_path: Path) -> tuple[Path | None, str]:
    test_file = _find_test_file(repo_path)
    if test_file is None:
        return None, ""

    marker = "\n# Ralph Loop evaluation injected failure marker\n"
    injection = (
        "\n\ndef test_ralph_loop_eval_injected_failure() -> None:\n"
        "    assert False, 'Ralph loop evaluation injected failure condition.\n\n'")

    original = test_file.read_text(encoding="utf-8")
    if marker in original:
        return test_file, original

    test_file.write_text(f"{original}{marker}{injection}", encoding="utf-8")
    return test_file, original


def _restore_file(path: Path | None, before: str | None) -> None:
    if path is None or before is None:
        return
    path.write_text(before, encoding="utf-8")


def _snapshot_repo_state(repo_path: Path) -> dict[str, str]:
    state: dict[str, str] = {}
    for file_path in sorted(repo_path.rglob("*")):
        if not file_path.is_file():
            continue
        rel_path = file_path.relative_to(repo_path)
        if rel_path.parts and rel_path.parts[0] == ".git":
            continue
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        state[rel_path.as_posix()] = digest
    return state


def _diff_repo_state(before: dict[str, str], after: dict[str, str]) -> list[str]:
    changed: list[str] = []
    for rel_path in sorted(set(before) | set(after)):
        if before.get(rel_path) != after.get(rel_path):
            changed.append(rel_path)
    return changed


def _decision_for_status(status: str, pattern: str, changed_in_readonly: bool) -> str:
    if status == "pass" and (pattern != "readonly_audit" or not changed_in_readonly):
        return "accept"
    return "reject"


def _run_ralph_once(
    *,
    repo_path: Path,
    run_id: str,
    goal: str,
    test_command: str,
    acceptance_criteria: list[str],
    mode: str,
    readonly: bool,
    max_iterations: int,
    work_root: Path,
) -> subprocess.CompletedProcess[str]:
    cfg: dict[str, Any] = {
        "goal": goal,
        "repo_path": str(repo_path),
        "test_command": test_command,
        "acceptance_criteria": acceptance_criteria,
        "mode": mode,
        "max_iterations": max_iterations,
        "sleep_seconds": 0,
        "dry_run": False,
        "readonly": readonly,
        "work_dir": str(work_root),
        "llm": {
            "adapter": "stub",
            "model": "gpt-4.1-mini",
            "context_max_files": 8,
            "context_max_chars_per_file": 1800,
            "context_max_total_chars": 12000,
        },
    }

    with tempfile.TemporaryDirectory(prefix=f"ralph-eval-{run_id}-") as tmp_dir:
        cfg_path = Path(tmp_dir) / "run_config.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        cmd = [sys.executable, str(RALPH_LOOP), "--config", str(cfg_path)]
        return _run_cmd(cmd, cwd=repo_path)


def _parse_ralph_run(
    *,
    work_root: Path,
    run_id: str,
    goal: str,
    repo_path: Path,
    pattern: str,
    mode: str,
    max_iterations: int,
    test_command: str,
    proc: subprocess.CompletedProcess[str],
    trigger_index: int,
    acceptance_criteria: list[str],
    readonly: bool,
    allow_search: bool,
    search_disabled_simulated: bool,
    verification_failure_injected: bool,
    compaction_cycle_injected: bool,
    compaction_checkpoint_id: str | None,
    run_seconds: float,
    baseline_mutation_injected: bool,
    pre_repo_state: dict[str, str] | None,
    post_repo_state: dict[str, str] | None,
) -> LoopEvalRunRecord:
    acceptance_met = False
    failure_domain = "none"
    changed_files: list[str] = []
    verification_summary = "tests=n/a, lint=n/a, returncode=n/a"
    changed_in_readonly = False

    state_path = _latest_state_file(work_root)
    iterations_dir = work_root / ".ralph" / "iterations"
    if iterations_dir.exists():
        latest = _latest_iteration_file(iterations_dir)
        if latest is not None:
            latest_record = _parse_json(latest)
            acceptance = latest_record.get("acceptance", {}) or {}
            verification = latest_record.get("verification", {}) or {}
            apply_result = latest_record.get("apply_result", {}) or {}
            acceptance_met = bool(acceptance.get("met", False))
            failure_domain = str(latest_record.get("failure_domain", "none"))
            changed_files = list(apply_result.get("changed_files") or [])
            tests = verification.get("tests") or {}
            lint = verification.get("lint") or {}
            verification_summary = (
                f"tests={tests.get('command', 'n/a')}({str(tests.get('ok', 'n/a'))}, rc={tests.get('returncode', 'n/a')}); "
                f"lint={lint.get('command', 'n/a')}({str(lint.get('ok', 'n/a'))}, rc={lint.get('returncode', 'n/a')}); "
                f"proc_returncode={proc.returncode}"
            )

    if state_path is not None:
        _ = _parse_json(state_path)

    # Read-only guard invariant: flag mutation only on real repository state deltas.
    changed_repo_delta = (
        _diff_repo_state(pre_repo_state or {}, post_repo_state or {})
        if pre_repo_state is not None and post_repo_state is not None
        else []
    )
    if changed_repo_delta:
        changed_in_readonly = True
        changed_files = sorted(set(changed_files) | set(changed_repo_delta))

    status = "pass"
    if proc.returncode != 0:
        status = "error"
    elif not acceptance_met:
        status = "fail"

    if pattern == "readonly_audit" and changed_in_readonly:
        status = "error"

    decision = _decision_for_status(status, pattern, bool(changed_in_readonly))

    return LoopEvalRunRecord(
        run_id=run_id,
        pattern=pattern,
        trigger_index=trigger_index,
        goal=goal,
        repo_path=str(repo_path),
        mode=mode,
        max_iterations=max_iterations,
        status=status,
        acceptance_met=acceptance_met,
        acceptance_criteria=acceptance_criteria,
        verification_summary=verification_summary,
        failure_domain=failure_domain,
        changed_files=changed_files,
        compaction_checkpoint_id=compaction_checkpoint_id,
        changed_file_count=len(changed_files),
        changed_in_readonly=bool(changed_in_readonly),
        run_seconds=run_seconds,
        test_command=test_command,
        output_last_message_path=str(work_root / "output-last-message.txt") if work_root else None,
        artifact_schema_version="1.1",
        decision=decision,
        readonly=readonly,
        search_enabled=allow_search,
        search_disabled_simulated=search_disabled_simulated,
        verification_failure_injected=verification_failure_injected,
        compaction_cycle_injected=compaction_cycle_injected,
        baseline_mutation_injected=baseline_mutation_injected,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )


def _note_title(kind: str, value: str) -> str:
    return f"Ralph Loop Evaluation {kind} / {value}"


def _emit_output_last_message(path: Path, record: LoopEvalRunRecord) -> None:
    payload = {
        "schema_version": record.artifact_schema_version,
        "timestamp_utc": record.timestamp_utc,
        "run_id": record.run_id,
        "pattern": record.pattern,
        "trigger_index": record.trigger_index,
        "status": record.status,
        "decision": record.decision,
        "acceptance_met": record.acceptance_met,
        "acceptance_criteria": record.acceptance_criteria,
        "run_seconds": round(record.run_seconds, 3),
        "failure_domain": record.failure_domain,
        "readonly": record.readonly,
        "changed_in_readonly": record.changed_in_readonly,
        "search_enabled": record.search_enabled,
        "search_disabled_simulated": record.search_disabled_simulated,
        "verification_failure_injected": record.verification_failure_injected,
        "compaction_cycle_injected": record.compaction_cycle_injected,
        "compaction_checkpoint_id": record.compaction_checkpoint_id,
        "test_command": record.test_command,
        "changed_file_count": record.changed_file_count,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def _run_compaction_cycle(project: str, objective: str) -> str:
    pre_proc = _run_cmd(
        [
            sys.executable,
            str(COMPACTION_HANDOFF),
            "--project",
            project,
            "--mode",
            "pre",
            "--objective",
            objective,
            "--summary",
            "pilot context-loss stress event",
        ]
    )
    if pre_proc.returncode != 0:
        raise RuntimeError(f"compaction pre failed: {pre_proc.stdout or pre_proc.stderr}")
    payload = json.loads(pre_proc.stdout)

    _run_cmd(
        [
            sys.executable,
            str(COMPACTION_HANDOFF),
            "--project",
            project,
            "--mode",
            "post",
            "--objective",
            objective,
        ]
    )
    return payload.get("checkpoint_file", "")


def _save_memory(project: str, title: str, body: str, tags: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        note_path = Path(tmp_dir) / "note.md"
        note_path.write_text(body, encoding="utf-8")
        proc = _run_cmd(
            [
                sys.executable,
                str(AUTO_MEMORY_SAVE),
                "--project",
                project,
                "--title",
                title,
                "--body-file",
                str(note_path),
                "--tags",
                ",".join(tags),
            ]
        )
    if proc.returncode != 0:
        raise RuntimeError(f"save_memory failed: {proc.stdout or proc.stderr}")


def _note_body_run(record: LoopEvalRunRecord) -> str:
    started = datetime.now(timezone.utc).isoformat()
    changed = ", ".join(record.changed_files) if record.changed_files else "(none)"
    decision = record.decision
    rationale = "Read-only mutation guard passed" if not record.changed_in_readonly else "Read-only mutation guard failed"
    verification_line = f"- verification_summary: {record.verification_summary}\n"

    return (
        "## Summary\n"
        f"- run_id: {record.run_id}\n"
        f"- trigger_index: {record.trigger_index}\n"
        f"- pattern: {record.pattern}\n"
        f"- status: {record.status}\n"
        f"- acceptance_met: {str(record.acceptance_met).lower()}\n"
        f"- Decision: {decision}\n"
        "\n## Context\n"
        f"- repo_path: {record.repo_path}\n"
        f"- mode: {record.mode}\n"
        f"- max_iterations: {record.max_iterations}\n"
        f"- goal: {record.goal}\n"
        f"- run duration: {record.run_seconds:.2f}s\n"
        f"- search_enabled: {str(record.search_enabled).lower()}\n"
        f"- search_disabled_simulated: {str(record.search_disabled_simulated).lower()}\n"
        f"- acceptance_criteria: {';'.join(record.acceptance_criteria)}\n"
        f"- artifact_schema_version: {record.artifact_schema_version}\n"
        f"- compaction_checkpoint_id: {record.compaction_checkpoint_id or 'none'}\n"
        f"- output_last_message: {record.output_last_message_path or 'n/a'}\n"
        "\n## Decision\n"
        f"- self-improve decision: {decision}\n"
        f"- changed_files: {changed}\n"
        f"- baseline mutation injected: {str(record.baseline_mutation_injected).lower()}\n"
        f"- verification_failure_injected: {str(record.verification_failure_injected).lower()}\n"
        f"- compaction_cycle_injected: {str(record.compaction_cycle_injected).lower()}\n"
        f"- changed_in_readonly: {str(record.changed_in_readonly).lower()}\n"
        "\n## Rationale\n"
        f"- {rationale}\n"
        f"{verification_line}"
        "- This run uses read-only overlay semantics only for non-mutating audit validation when pattern is `readonly_audit`.\n"
        "\n## Implementation\n"
        "- Ran one bounded trigger on the requested repo with a fresh temporary loop work root.\n"
        f"- Test command: {record.test_command}\n"
        f"- Verification summary: {record.verification_summary}\n"
        f"- Failure domain: {record.failure_domain}\n"
        "\n## Verification\n"
        f"- Completed at: {started}\n"
        f"- status={record.status}; acceptance_met={record.acceptance_met}; failure_domain={record.failure_domain}\n"
        "\n## Follow-ups\n"
        "- If status != pass and acceptance was expected, route to failure-domain recovery checks.\n"
        "- For readonly-audit runs, immediately audit any changed files; any mutation is a hard fail.\n"
        "\n## Changelog\n"
        f"- {started}: updated run record and emitted single-line output artifact.\n\n"
        "## LoopEvalRunRecord\n"
        f"```json\n{json.dumps(record.to_dict(), sort_keys=True, indent=2)}\n```\n"
    )


def _note_body_aggregate(state: AggregateState) -> str:
    started = datetime.now(timezone.utc).isoformat()
    failure_lines = "\n".join(
        f"- {domain}: {count}" for domain, count in sorted(state.failure_domains.items())
    ) or "- none"
    confidence = "\n".join(state.confidence_notes[-8:]) or "- none"

    return (
        "## Summary\n"
        f"- trigger_count: {state.trigger_count}\n"
        f"- trigger_target: {state.target_triggers}\n"
        f"- control_runs: {state.control_runs} (pass={state.control_pass}, rate={state.control_pass_rate() * 100:.1f}%)\n"
        f"- readonly_audit_runs: {state.audit_runs} (pass={state.audit_pass}, rate={state.audit_pass_rate() * 100:.1f}%)\n"
        f"- overall_acceptance_rate: {state.overall_pass_rate() * 100:.1f}%\n"
        f"- acceptance_rate_target: control>=80%, audit_mutations=0\n"
        f"- read_only_mutations: {state.read_only_mutations}\n"
        f"- search_disabled_simulated_runs: {state.search_disabled_simulated_runs}\n"
        f"- verification_failure_injected_runs: {state.verification_failure_injected_runs}\n"
        f"- compaction_cycle_injected_runs: {state.compaction_cycle_injected_runs}\n"
        f"- avg_run_duration_seconds: {state.avg_duration_seconds():.2f}\n"
        "\n## Context\n"
        f"- project: {state.project}\n"
        f"- updated_at_utc: {started}\n"
        f"- trigger target: {state.target_triggers}\n"
        "\n## Decision\n"
        "- Keep `ralph-wiggum-loop` as primary execution path while read-only overlay remains companion for now.\n"
        f"- Current pilot status: {'pass' if state.trigger_count >= 12 else 'incomplete'}\n"
        "\n## Rationale\n"
        "- Control runs preserve bounded-write behavior and existing dual-gate contracts.\n"
        "- Read-only audit runs enforce mutation guard and collect evidence-only artifacts.\n"
        "\n## Implementation\n"
        "- One run record note per trigger created under title format `Ralph Loop Evaluation Run / <run_id>`.\n"
        "- Aggregate note updated with `Ralph Loop Evaluation Aggregate / <YYYY-MM-DD>`.\n"
        "- No standalone stats file is written.\n"
        "\n## Verification\n"
        f"- failure_domain_breakdown:\n{failure_lines}\n"
        f"- confidence_notes(last 8):\n{confidence}\n"
        "\n## Follow-ups\n"
        "- Promote only components that satisfy detachment criteria in final decision.\n"
        "- Keep searching for external mode impact when readonly wrappers call external tools.\n"
        "\n## Changelog\n"
        f"- {started}: aggregate counters refreshed for trigger_count={state.trigger_count}.\n"
    )


def run_batch(
    *,
    repo_path: Path,
    goal: str,
    project: str,
    test_command: str,
    control_runs: int,
    readonly_runs: int,
    max_iterations: int,
    acceptance_criteria: list[str],
    artifacts_dir: Path,
    resume_from: int,
    no_search_run: int,
    fail_injection_run: int,
    compaction_run: int,
) -> None:
    aggregate = AggregateState(
        project=project,
        target_triggers=control_runs + readonly_runs,
        trigger_count=0,
        control_runs=0,
        control_pass=0,
        audit_runs=0,
        audit_pass=0,
        read_only_mutations=0,
        search_disabled_simulated_runs=0,
        verification_failure_injected_runs=0,
        compaction_cycle_injected_runs=0,
        run_seconds_total=0.0,
        failure_domains=Counter(),
        confidence_notes=[],
    )

    total_runs = control_runs + readonly_runs
    run_specs: list[RunSpec] = []
    # RunSpec sequencing invariant: triggers 1..N are deterministic and ordered.
    for trigger in range(1, total_runs + 1):
        is_control = trigger <= control_runs
        run_specs.append(
            RunSpec(
                trigger_index=trigger,
                pattern="ralph_control" if is_control else "readonly_audit",
                mode="auto",
                readonly=not is_control,
                max_iterations=max_iterations,
                allow_search=(trigger != no_search_run),
                search_disabled_simulated=(trigger == no_search_run),
                induce_verification_failure=(trigger == fail_injection_run),
                induce_compaction_cycle=(trigger == compaction_run),
            )
        )
    expected_patterns = (["ralph_control"] * control_runs) + (["readonly_audit"] * readonly_runs)
    actual_patterns = [spec.pattern for spec in run_specs]
    if actual_patterns != expected_patterns:
        raise RuntimeError("RunSpec sequencing invariant violated.")

    aggregate_title = _note_title("Aggregate", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    _save_memory(
        project=project,
        title=aggregate_title,
        body=_note_body_aggregate(aggregate),
        tags=["ralph-eval", "aggregate"],
    )

    for run_spec in run_specs:
        if run_spec.trigger_index < resume_from:
            continue

        run_id = f"{_now_ts()}-{run_spec.trigger_index:03d}"
        work_root = artifacts_dir / f"run-{run_id}"
        work_root.mkdir(parents=True, exist_ok=True)

        pre_repo_state: dict[str, str] | None = None
        post_repo_state: dict[str, str] | None = None
        injected_file: Path | None = None
        injected_before: str | None = None
        checkpoint_id: str | None = None

        if run_spec.readonly:
            pre_repo_state = _snapshot_repo_state(repo_path)

        if run_spec.induce_verification_failure:
            injected_file, injected_before = _inject_failing_test(repo_path)

        if run_spec.induce_compaction_cycle:
            checkpoint_id = _run_compaction_cycle(
                project=project,
                objective=f"run_{run_spec.trigger_index}: pilot stress test",
            )

        started = time.perf_counter()
        proc = _run_ralph_once(
            repo_path=repo_path,
            run_id=run_id,
            goal=goal,
            test_command=test_command,
            acceptance_criteria=acceptance_criteria,
            mode=run_spec.mode,
            readonly=run_spec.readonly,
            max_iterations=run_spec.max_iterations,
            work_root=work_root,
        )
        run_seconds = time.perf_counter() - started

        if run_spec.readonly:
            post_repo_state = _snapshot_repo_state(repo_path)

        record = _parse_ralph_run(
            work_root=work_root,
            run_id=run_id,
            goal=goal,
            repo_path=repo_path,
            pattern=run_spec.pattern,
            mode=run_spec.mode,
            max_iterations=run_spec.max_iterations,
            test_command=test_command,
            proc=proc,
            trigger_index=run_spec.trigger_index,
            acceptance_criteria=acceptance_criteria,
            readonly=run_spec.readonly,
            allow_search=run_spec.allow_search,
            search_disabled_simulated=run_spec.search_disabled_simulated,
            verification_failure_injected=run_spec.induce_verification_failure,
            compaction_cycle_injected=run_spec.induce_compaction_cycle,
            compaction_checkpoint_id=checkpoint_id,
            run_seconds=run_seconds,
            baseline_mutation_injected=bool(injected_file),
            pre_repo_state=pre_repo_state,
            post_repo_state=post_repo_state,
        )

        _restore_file(injected_file, injected_before)

        output_path = work_root / "output-last-message.txt"
        _emit_output_last_message(output_path, record)
        record.output_last_message_path = str(output_path)

        aggregate.record(record)
        # save_memory enforces required note sections for run + aggregate notes.
        _save_memory(
            project=project,
            title=_note_title("Run", run_id),
            body=_note_body_run(record),
            tags=["ralph-eval", run_spec.pattern],
        )
        _save_memory(
            project=project,
            title=aggregate_title,
            body=_note_body_aggregate(aggregate),
            tags=["ralph-eval", "aggregate"],
        )

        print(
            f"{record.trigger_index:03d}/{total_runs} {record.pattern} status={record.status} "
            f"acceptance={record.acceptance_met} changed={record.changed_file_count}"
        )

    if aggregate.trigger_count < total_runs:
        print(
            "pilot_incomplete=1 trigger_count={} target={}".format(
                aggregate.trigger_count,
                total_runs,
            )
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a bounded Ralph vs read-only overlay comparison pilot and persist notes in auto-memory.",
    )
    parser.add_argument("--project", default="ralph-loop-eval", help="Auto-memory project name.")
    parser.add_argument("--repo-path", required=True, help="Target repository path.")
    parser.add_argument("--goal", default="Repair repository until tests pass.", help="Loop objective.")
    parser.add_argument("--test-command", default="python3 -m unittest -q", help="Verification command.")
    parser.add_argument(
        "--acceptance-criteria",
        action="append",
        default=["tests_pass"],
        help="Acceptance criteria (repeatable). Allowed: tests_pass, lint_pass.",
    )
    parser.add_argument("--control-runs", type=int, default=6, help="Number of control runs.")
    parser.add_argument("--readonly-runs", type=int, default=6, help="Number of read-only runs.")
    parser.add_argument("--max-iterations", type=int, default=5, help="Ralph max_iterations.")
    parser.add_argument(
        "--resume-from",
        type=int,
        default=1,
        help="Resume run trigger index from this value.",
    )
    parser.add_argument(
        "--no-search-run",
        type=int,
        default=7,
        help="Trigger index that simulates search-disabled audit. 0 to disable simulation.",
    )
    parser.add_argument(
        "--fail-injection-run",
        type=int,
        default=3,
        help="Trigger index where a verification failure is injected.",
    )
    parser.add_argument(
        "--compaction-run",
        type=int,
        default=9,
        help="Trigger index that runs pre/post compaction stress cycle.",
    )
    parser.add_argument("--demo", action="store_true", help="Generate the Ralph demo repo when needed.")
    parser.add_argument(
        "--artifacts-dir",
        default=str(Path.home() / ".codex" / "tmp" / "ralph-readonly-audit-pilot"),
        help="Directory for run artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_path = Path(args.repo_path).expanduser().resolve()
    artifacts_dir = Path(args.artifacts_dir).expanduser().resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    if args.demo:
        _ensure_demo_repo(repo_path, regenerate=True)

    if not repo_path.exists():
        raise SystemExit(f"repo_path does not exist: {repo_path}")
    if not repo_path.is_dir():
        raise SystemExit(f"repo_path is not a directory: {repo_path}")
    if args.control_runs < 0 or args.readonly_runs < 0:
        raise SystemExit("control-runs and readonly-runs must be >= 0")
    if args.control_runs + args.readonly_runs <= 0:
        raise SystemExit("Total trigger count must be > 0")
    if args.resume_from < 1:
        raise SystemExit("--resume-from must be >= 1")
    if any(item not in {"tests_pass", "lint_pass"} for item in args.acceptance_criteria):
        raise SystemExit("acceptance-criteria must be tests_pass and/or lint_pass")

    run_batch(
        repo_path=repo_path,
        goal=args.goal,
        project=args.project,
        test_command=args.test_command,
        control_runs=args.control_runs,
        readonly_runs=args.readonly_runs,
        max_iterations=args.max_iterations,
        acceptance_criteria=args.acceptance_criteria,
        artifacts_dir=artifacts_dir,
        resume_from=args.resume_from,
        no_search_run=args.no_search_run,
        fail_injection_run=args.fail_injection_run,
        compaction_run=args.compaction_run,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
