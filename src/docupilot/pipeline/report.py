from __future__ import annotations
from typing import Dict, Any
import json
from datetime import datetime

def build_report(normalized_doc: Dict[str, Any], risk_bundle: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "document_type": normalized_doc.get("document_type"),
        "parties": normalized_doc.get("parties", []),
        "effective_date": normalized_doc.get("effective_date"),
        "term": normalized_doc.get("term"),
        "risk": risk_bundle,
        "actionable_summary": _actionable_summary(risk_bundle),
    }

def _actionable_summary(risk_bundle: Dict[str, Any]) -> Dict[str, Any]:
    findings = risk_bundle.get("findings", [])
    findings_sorted = sorted(findings, key=lambda x: x.get("severity", 0), reverse=True)

    top = findings_sorted[:8]
    return {
        "top_findings": top,
        "next_steps": [
            "Validate missing or weak clauses flagged by Legal and Compliance agents.",
            "Confirm data protection and confidentiality coverage if any gaps were detected.",
            "Align operational terms (SLA, termination, transition) to delivery needs.",
            "Re-run after redaction/clean OCR if confidence is low."
        ]
    }

def write_report(report: Dict[str, Any], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
