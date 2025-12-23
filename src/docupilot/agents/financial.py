from __future__ import annotations
from typing import Dict, Any, List
from .base import RiskAgent, RiskFinding

class FinancialRiskAgent(RiskAgent):
    name = "financial-agent"
    category = "financial"

    def analyze(self, normalized_doc: Dict[str, Any]) -> List[RiskFinding]:
        findings: List[RiskFinding] = []
        blob = " ".join([s.get("text", "") for s in normalized_doc.get("sections", [])]).lower()

        if "late fee" in blob or "interest" in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Late fee / interest terms present",
                severity=35,
                rationale="Payment enforcement terms may create cost exposure.",
                evidence=[],
                recommendation="Confirm acceptable rates, grace periods, and dispute windows."
            ))

        if "invoice" not in blob and "payment" not in blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Payment terms unclear",
                severity=60,
                rationale="Payment schedule and invoicing mechanics were not detected.",
                evidence=[],
                recommendation="Add explicit payment schedule, invoice timing, and acceptance criteria."
            ))
        return findings
