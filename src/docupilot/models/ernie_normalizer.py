from __future__ import annotations
from typing import Dict, Any, List
import json
import os
from .llm_adapter import ChatLLM

NORMALIZE_SYSTEM = """You are a document normalization engine.
You convert OCR text into clean structured JSON.
Preserve clause numbering, headings, and defined terms when present.
Return ONLY valid JSON. No markdown. No commentary."""

def normalize_document(llm: ChatLLM, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    if os.getenv("MOCK_OCR_ENV"):
        # Match the keys requested in the prompt
        return {
            "document_type": "Court Order",
            "parties": [
                {"name": "Plaintiff", "role": "Plaintiff"},
                {"name": "Defendant", "role": "Defendant"}
            ],
            "effective_date": "2024-01-01",
            "term": None,
            "sections": [
                {"heading": "Order", "number": "1", "text": "Defendant to pay costs of $500."},
                {"heading": "Confidentiality", "number": "2", "text": "The parties shall maintain Confidentiality."},
                {"heading": "Indemnification", "number": "3", "text": "The vendor shall indemnify the client."},
                {"heading": "Liability", "number": "4", "text": "Limitation of liability cap at $1M."}
            ],
            "defined_terms": [],
            "obligations": [],
            "raw_extraction_notes": ["Mock extraction"]
        }
    ocr_text = "\n\n".join([f"--- PAGE {p['page_index']} ---\n{p['text']}" for p in pages])

    user = f"""Normalize this output output into JSON with these keys:
- document_type (string)
- parties (array of {{"name": string, "role": string}})
- effective_date (string|null)
- term (string|null)
- sections (array of {{"heading": string, "number": string|null, "text": string}})
- defined_terms (array of {{"term": string, "definition": string}})
- obligations (array of {{"party": string, "obligation": string, "section_ref": string|null}})
- raw_extraction_notes (array of string) for OCR uncertainties

OCR:
{ocr_text}
"""
    content = llm.chat(
        messages=[
            {"role": "system", "content": NORMALIZE_SYSTEM},
            {"role": "user", "content": user},
        ],
        temperature=0.1,
        max_tokens=4096,
    )

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Best-effort repair: ask model to fix JSON
        fix = llm.chat(
            messages=[
                {"role": "system", "content": "Fix invalid JSON. Return ONLY valid JSON."},
                {"role": "user", "content": content},
            ],
            temperature=0.0,
            max_tokens=4096,
        )
        return json.loads(fix)
