from __future__ import annotations
from typing import Dict, Any, List
from .base import RiskAgent, RiskFinding

class ComplianceRiskAgent(RiskAgent):
    name = "compliance-agent"
    category = "compliance"

    def analyze(self, normalized_doc: Dict[str, Any]) -> List[RiskFinding]:
        findings: List[RiskFinding] = []
        blob = " ".join([s.get("text", "") for s in normalized_doc.get("sections", [])]).lower()

        if "gdpr" in blob or "ccpa" in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Privacy regulation triggers present",
                severity=55,
                rationale="Document references privacy laws; ensure required notices, DPA terms, and subprocessors are covered.",
                evidence=[],
                recommendation="Validate DPA obligations, breach notification timelines, and data transfer mechanisms."
            ))

        if "audit" not in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Audit rights not explicit",
                severity=40,
                rationale="No clear audit clause detected; may be missing or not captured by OCR.",
                evidence=[],
                recommendation="Confirm audit rights, frequency, scope, and cost allocation."
            ))

        return findings
