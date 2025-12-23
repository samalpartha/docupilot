from __future__ import annotations
import argparse
from typing import Dict, Any
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from .config import settings
from .models.ocr_paddle import PaddleOCRExtractor
from .models.llm_adapter import ChatLLM
from .models.ernie_normalizer import normalize_document
from .pipeline.risk_orchestrator import CAMELStyleOrchestrator
from .pipeline.report import build_report, write_report

def run(pdf_path: str, out_path: str) -> None:
    # 1) OCR
    ocr = PaddleOCRExtractor(lang="en")
    pages = ocr.extract_pdf(pdf_path)
    pages_payload = [{"page_index": p.page_index, "text": p.text, "blocks": p.blocks} for p in pages]

    # 2) Normalize with ERNIE
    llm = ChatLLM(
        api_key=settings.ernie_api_key,
        base_url=settings.ernie_base_url,
        model=settings.ernie_model,
    )
    normalized = normalize_document(llm, pages_payload)

    # 3) Risk analysis via agents
    orchestrator = CAMELStyleOrchestrator()
    risk_bundle = orchestrator.run(normalized)

    # 4) Report
    report = build_report(normalized, risk_bundle)
    write_report(report, out_path)

def cli() -> None:
    ap = argparse.ArgumentParser(description="DocuPilot: OCR -> Normalize -> Multi-agent Risk Report")
    ap.add_argument("--pdf", required=True, help="Path to PDF")
    ap.add_argument("--out", required=True, help="Output report JSON path")
    args = ap.parse_args()
    run(args.pdf, args.out)

if __name__ == "__main__":
    cli()
