from __future__ import annotations
from typing import Dict, Any, List
from .base import RiskAgent, RiskFinding

class ReputationalRiskAgent(RiskAgent):
    name = "reputational-agent"
    category = "reputational"

    def analyze(self, normalized_doc: Dict[str, Any]) -> List[RiskFinding]:
        findings: List[RiskFinding] = []
        blob = " ".join([s.get("text", "") for s in normalized_doc.get("sections", [])]).lower()

        if "publicity" in blob or "press release" in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Publicity / press terms present",
                severity=35,
                rationale="Public communications may be permitted; brand exposure risk depends on approval controls.",
                evidence=[],
                recommendation="Require prior written approval for name/logo use and press releases."
            ))

        if "confidential" not in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Confidentiality language not detected",
                severity=80,
                rationale="Confidentiality clause is missing or not captured; could be a major reputational and legal risk.",
                evidence=[],
                recommendation="Confirm confidentiality scope, exclusions, duration, and remedies."
            ))

        return findings
