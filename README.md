# DocuPilot

DocuPilot is a multi-agent document processing system that:
- Extracts text from PDFs using PaddleOCR (robust OCR; swap in PaddleOCR-VL if available)
- Normalizes extracted text into structured JSON using ERNIE (LLM)
- Analyzes risks using specialized agents coordinated in a CAMEL-style multi-agent loop
- Produces a comprehensive report with category scores and actionable findings

## Quick start

### 1) Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
```

### 2) Configure

Copy `.env.example` to `.env` and set:

* ERNIE_API_KEY
* ERNIE_BASE_URL (optional depending on your gateway/provider)
* ERNIE_MODEL (optional)

### 3) Run

```bash
python -m docupilot.main --pdf path/to/msa.pdf --out out/report.json
```

## Notes

* If your environment has PaddleOCR-VL specifically, update `models/ocr_paddle.py` to use it.
* ERNIE integration is implemented via a thin HTTP adapter (provider-agnostic).
