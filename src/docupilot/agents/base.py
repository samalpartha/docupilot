from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class RiskFinding:
    category: str
    title: str
    severity: int  # 0-100
    rationale: str
    evidence: List[Dict[str, Any]]  # e.g. {"section": "12.3", "quote": "..."}
    recommendation: str

class RiskAgent:
    name: str = "base"
    category: str = "general"

    def analyze(self, normalized_doc: Dict[str, Any]) -> List[RiskFinding]:
        raise NotImplementedError
