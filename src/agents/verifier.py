
from pathlib import Path
from .base import BaseAgent
import json
from loguru import logger
from ..utils.financial_validator import validate_invoice_financials

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="VerifierAgent", role="Quality Assurance Auditor")
        prompt_path = Path(__file__).parent / 'prompts' / 'verifier.txt'
        self.set_system_prompt(prompt_path.read_text())

    def verify(self, report_text, evidence_text):
        # 1. Standard LLM Semantic Audit
        llm_audit = self.run(f"Audit the following report against the provided evidence:\n\nEVIDENCE:\n{evidence_text}\n\nREPORT TO AUDIT:\n{report_text}")
        
        # 2. Programmatic Financial Validation (if applicable)
        validation_note = ""
        try:
            # Try to extract JSON from report_text to check for financials
            clean_json = report_text.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()
                
            data = json.loads(clean_json)
            
            # Use financial validator
            # We assume if the JSON has keys like 'line_items' or 'total', it's worth checking
            if isinstance(data, dict) and any(k in data for k in ["line_items", "total_sales", "grand_total", "financials"]):
                # If specific 'financials' key exists (from Analyst output structure), use that
                obj_to_check = data.get("financials", data)
                
                checks = validate_invoice_financials(obj_to_check)
                
                if checks:
                    validation_note = f"\n\n### 🛡️ Programmatic Financial Verification\n"
                    if checks.get("is_consistent"):
                        validation_note += "✅ **PASSED**: All financial totals are mathematically consistent.\n"
                    else:
                        validation_note += "❌ **FAILED**: internal inconsistencies detected in the report.\n"
                    
                    # Add details
                    for k, v in checks.items():
                        if k != "is_consistent":
                            icon = "✅" if (v is True or (isinstance(v, str) and "valid" in v)) else ("❌" if v is False else "ℹ️")
                            validation_note += f"- {k}: {icon} {v}\n"
                            
        except json.JSONDecodeError:
            pass # Not a JSON report, skip programmatic check
        except Exception as e:
            logger.warning(f"Programmatic verification skipped due to error: {e}")

        return llm_audit + validation_note
