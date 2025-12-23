from __future__ import annotations
from typing import Dict, Any, List
from .base import RiskAgent, RiskFinding

class LegalRiskAgent(RiskAgent):
    name = "legal-agent"
    category = "legal"

    def analyze(self, normalized_doc: Dict[str, Any]) -> List[RiskFinding]:
        findings: List[RiskFinding] = []

        # Heuristic examples (replace/extend with LLM-driven extraction if desired)
        text_blob = " ".join([s.get("text", "") for s in normalized_doc.get("sections", [])]).lower()

        if "limitation of liability" not in text_blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Missing limitation of liability",
                severity=75,
                rationale="No explicit limitation of liability clause detected in the extracted sections.",
                evidence=[],
                recommendation="Add or confirm a limitation of liability clause aligned to your risk posture."
            ))

        if "indemn" not in text_blob:
            findings.append(RiskFinding(
                category=self.category,
                title="Indemnification unclear or missing",
                severity=65,
                rationale="Indemnification language was not detected or may be incomplete due to OCR gaps.",
                evidence=[],
                recommendation="Confirm indemnity scope, trigger events, defense control, and caps."
            ))

        return findings
