from __future__ import annotations
from typing import Dict, Any, List
from dataclasses import asdict
from ..agents.base import RiskAgent, RiskFinding
from ..agents.compliance import ComplianceRiskAgent
from ..agents.financial import FinancialRiskAgent
from ..agents.legal import LegalRiskAgent
from ..agents.operational import OperationalRiskAgent
from ..agents.reputational import ReputationalRiskAgent

class CAMELStyleOrchestrator:
    """
    Lightweight CAMEL-style orchestrator:
    - Run agents independently
    - Merge findings
    - Produce category scores and overall score
    - Optionally run a second pass where agents see each other's top findings
    """
    def __init__(self):
        self.agents: List[RiskAgent] = [
            ComplianceRiskAgent(),
            FinancialRiskAgent(),
            LegalRiskAgent(),
            OperationalRiskAgent(),
            ReputationalRiskAgent(),
        ]

    def run(self, normalized_doc: Dict[str, Any]) -> Dict[str, Any]:
        all_findings: List[RiskFinding] = []
        for agent in self.agents:
            all_findings.extend(agent.analyze(normalized_doc))

        # Score aggregation: max severity per category + overall weighted mean
        by_cat: Dict[str, List[RiskFinding]] = {}
        for f in all_findings:
            by_cat.setdefault(f.category, []).append(f)

        category_scores: Dict[str, int] = {
            cat: int(max(x.severity for x in items)) for cat, items in by_cat.items()
        }
        overall = int(sum(category_scores.values()) / max(len(category_scores), 1)) if category_scores else 0

        return {
            "category_scores": category_scores,
            "overall_risk_score": overall,
            "findings": [asdict(f) for f in all_findings],
        }
