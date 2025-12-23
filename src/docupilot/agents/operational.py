from __future__ import annotations
from typing import Dict, Any, List
from .base import RiskAgent, RiskFinding

class OperationalRiskAgent(RiskAgent):
    name = "operational-agent"
    category = "operational"

    def analyze(self, normalized_doc: Dict[str, Any]) -> List[RiskFinding]:
        findings: List[RiskFinding] = []
        blob = " ".join([s.get("text", "") for s in normalized_doc.get("sections", [])]).lower()

        if "sla" not in blob and "service level" not in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Service levels not defined",
                severity=50,
                rationale="No SLA or service level terms detected; operational expectations may be ambiguous.",
                evidence=[],
                recommendation="Define uptime targets, incident response times, and remedies."
            ))

        if "termination" in blob and "transition" not in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Termination without transition support",
                severity=45,
                rationale="Termination language exists but transition assistance is not obvious.",
                evidence=[],
                recommendation="Add exit support terms: data return, run-off, and knowledge transfer."
            ))

        return findings
