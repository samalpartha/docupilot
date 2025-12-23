
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
            f"REQUIRED JSON STRUCTURE (Strict): \n"
            f"{{\n"
            f"  'document_type': 'string',\n"
            f"  'court': 'string (context/jurisdiction)',\n"
            f"  'posture': 'string (procedural status)',\n"
            f"  'parties': [ 'list of strings or objects' ],\n"
            f"  'relief': [ 'list of clauses or remedies' ],\n"
            f"  'findings': 'string (summary of key terms)',\n"
            f"  'dates': {{ 'key': 'value' }},\n"
            f"  'obligations': [ 'list of strings' ],\n"
            f"  'financials': [ 'list of strings' ]\n"
            f"}}\n\n"
            f"{hint_str}\n\n"
            f"Text:\n{text}"
        )
        response = self.run(prompt)
        
        # Robust Parsing
        try:
            # Clean string
            json_str = response.strip()
            
            # Handle Markdown Code Blocks
            if "```" in json_str:
                import re
                pattern = r"```(?:json)?\s*(.*?)\s*```"
                match = re.search(pattern, json_str, re.DOTALL | re.IGNORECASE)
                if match:
                     json_str = match.group(1)
            
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse Analyst JSON: {e}")
            return {} 

    def aggregate(self, partial_results):
        """
        Aggregates partial JSON extractions using deterministic Python logic 
        (safer and cheaper than LLM).
        """
        master_record = {
            "document_type": "Unknown",
            "court": "N/A",
            "posture": "N/A",
            "parties": [],
            "relief": [],
            "findings": "N/A",
            "dates": {},
            "obligations": [],
            "financials": []
        }
        
        doc_types = []
        courts = []
        postures = []
        findings_list = []
        
        for p in partial_results:
            # 1. Document Type (Voting)
            dt = p.get('document_type')
            if dt and dt not in ["N/A", "Unknown", "string"]:
                doc_types.append(dt)
            
            # 1b. Court / Context (Voting)
            c = p.get('court')
            if c and c not in ["N/A", "Unknown", "string"]:
                courts.append(c)

            # 1c. Posture (Voting)
            pos = p.get('posture')
            if pos and pos not in ["N/A", "Unknown", "string"]:
                postures.append(pos)
                
            # 1d. Findings (Concatenate)
            find = p.get('findings')
            if find and find not in ["N/A", "Unknown", "string"]:
                findings_list.append(find)

            # 2. Parties / Entities (Merge & Dedup)
            # Handle both keys for robustness
            p_list = p.get('parties') or p.get('entities') or []
            if isinstance(p_list, list):
                for item in p_list:
                    if item and item not in master_record['parties']:
                        master_record['parties'].append(item)
                        
            # 3. Obligations
            o_list = p.get('obligations') or []
            if isinstance(o_list, list):
                 for item in o_list:
                    if item and item not in master_record['obligations']:
                        master_record['obligations'].append(item)
            
            # 3b. Relief / Clauses
            r_list = p.get('relief') or []
            if isinstance(r_list, list):
                 for item in r_list:
                    if item and item not in master_record['relief']:
                        master_record['relief'].append(item)
                        
            # 4. Financials
            f_list = p.get('financials') or []
            if isinstance(f_list, list):
                 for item in f_list:
                    if item and item not in master_record['financials']:
                        master_record['financials'].append(item)
                        
            # 5. Dates (Merge Dicts)
            d_dict = p.get('dates') or {}
            if isinstance(d_dict, dict):
                master_record['dates'].update(d_dict)
                
        # Finalize Single Value Fields (Most Frequent)
        from collections import Counter
        if doc_types:
            master_record['document_type'] = Counter(doc_types).most_common(1)[0][0]
        if courts:
            master_record['court'] = Counter(courts).most_common(1)[0][0]
        if postures:
            master_record['posture'] = Counter(postures).most_common(1)[0][0]
        if findings_list:
            # Join findings into a summary blob
            master_record['findings'] = "; ".join(findings_list[:3]) # Limit to top 3 chunks to avoid spam
            
        logger.info(f"✅ Aggregated {len(partial_results)} chunks into Master Record.")
        return master_record
