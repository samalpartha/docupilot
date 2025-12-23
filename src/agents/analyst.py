
from pathlib import Path
from .base import BaseAgent
import json
from loguru import logger

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AnalystAgent", role="Senior Document Analyst")
        prompt_path = Path(__file__).parent / 'prompts' / 'analyst.txt'
        self.set_system_prompt(prompt_path.read_text())

    def analyze(self, text):
        # Hybrid Approach: Run deterministic rules first
        from ..utils.extraction_rules import extract_invoice_totals, extract_invoice_line_items, extract_contract_dates, extract_contract_value
        
        # We try running all rules; they return empty if not applicable
        rule_hints = {}
        
        # Invoice Rules
        inv_totals = extract_invoice_totals(text)
        if inv_totals.get('grand_total'):
            rule_hints['deterministic_financials'] = inv_totals
            
        inv_lines = extract_invoice_line_items(text)
        if inv_lines:
            rule_hints['deterministic_line_items_count'] = len(inv_lines)
            rule_hints['deterministic_line_items_sample'] = inv_lines[:2] # Pass first 2 as hints
            
        # Contract Rules
        dates = extract_contract_dates(text)
        if any(dates.values()):
            rule_hints['deterministic_dates'] = dates
            
        val = extract_contract_value(text)
        if val:
            rule_hints['deterministic_contract_value'] = val
            
        # Construct Prompt
        hint_str = ""
        if rule_hints:
            hint_str = f"\n\n[SYSTEM HINT: Deterministic rules found the following potential data. Use this to double-check your extraction but verify context: {json.dumps(rule_hints, indent=2)}]"
        
        prompt = (
            f"Extract structured data from the text below.\n"
            f"You are a strict data extraction engine. You MUST output VALID JSON only.\n"
            f"Do not include any conversational text, preamble, or markdown formatting (like ```json).\n"
            f"Just return the raw JSON object.\n\n"
            f"REQUIRED JSON STRUCTURE:\n"
            f"{{\n"
            f"  'document_type': 'string',\n"
            f"  'entities': [ 'list of strings or objects' ],\n"
            f"  'dates': {{ 'key': 'value' }},\n"
            f"  'obligations': [ 'list of strings' ],\n"
            f"  'financials': [ 'list of strings' ]\n"
            f"}}\n\n"
            f"{hint_str}\n\n"
            f"Text:\n{text}"
        )
        return self.run(prompt)

    def aggregate(self, partial_results):
        """
        Uses the LLM to merge multiple partial JSON extractions into a single master record.
        """
        # Serialize the partial results into a string for the prompt
        context = json.dumps(partial_results, indent=2)
        prompt = (
            "You are an expert Data Consolidator.\n"
            "I have multiple partial extractions from a single document.\n"
            "Your task is to MERGE them into a single, deduplicated Master Record.\n\n"
            "Rules:\n"
            "1. Combine 'entities' list (deduplicate).\n"
            "2. Merge 'obligations' and 'financials'.\n"
            "3. Determine the single best 'document_type'.\n"
            "4. OUTPUT ONLY JSON with keys: 'document_type', 'entities', 'dates', 'obligations', 'financials'.\n\n"
            f"Partial Results:\n{context}"
        )
        
        response = self.run(prompt)
        try:
            # Clean potential markdown
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return json.loads(cleaned.strip())
        except Exception as e:
            logger.error(f"Failed to aggregate JSON: {e}")
            # Fallback: validation failed, return the first one or empty
            return partial_results[0] if partial_results else {}
