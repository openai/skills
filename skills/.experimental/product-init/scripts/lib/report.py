"""Finding/Report primitives shared by every audit script."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def rank(self) -> int:
        return ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"].index(self.value)


@dataclass
class Finding:
    severity: Severity
    gate: str
    check: str
    evidence: str
    fix: str

    def to_dict(self) -> dict:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d


@dataclass
class Report:
    name: str = "audit"
    findings: List[Finding] = field(default_factory=list)

    def add_finding(
        self,
        severity: Severity,
        gate: str,
        check: str,
        evidence: str,
        fix: str,
    ) -> None:
        self.findings.append(Finding(severity, gate, check, evidence, fix))

    def merge(self, other: "Report") -> None:
        self.findings.extend(other.findings)

    @property
    def exit_code(self) -> int:
        for f in self.findings:
            if f.severity in (Severity.HIGH, Severity.CRITICAL):
                return 1
        return 0

    def counts(self) -> dict:
        out = {s.value: 0 for s in Severity}
        for f in self.findings:
            out[f.severity.value] += 1
        return out

    def to_markdown(self) -> str:
        lines = [f"# Audit Report: {self.name}", ""]
        c = self.counts()
        lines.append(
            f"**Counts**: CRITICAL={c['CRITICAL']} HIGH={c['HIGH']} MEDIUM={c['MEDIUM']} "
            f"LOW={c['LOW']} INFO={c['INFO']}"
        )
        lines.append(f"**Exit code**: {self.exit_code}")
        lines.append("")
        if not self.findings:
            lines.append("_No findings._")
            return "\n".join(lines)
        lines.append("| Severity | Gate | Check | Evidence | Fix |")
        lines.append("| --- | --- | --- | --- | --- |")
        for f in self.findings:
            ev = f.evidence.replace("|", "\\|").replace("\n", " ")
            fx = f.fix.replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| {f.severity.value} | {f.gate} | {f.check} | {ev} | {fx} |"
            )
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "exit_code": self.exit_code,
                "counts": self.counts(),
                "findings": [f.to_dict() for f in self.findings],
            },
            indent=2,
        )
