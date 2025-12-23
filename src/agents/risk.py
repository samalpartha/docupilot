
from pathlib import Path
from .base import BaseAgent

import json
from loguru import logger

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RiskAgent", role="Compliance Risk Officer")
        prompt_path = Path(__file__).parent / 'prompts' / 'risk.txt'
        self.set_system_prompt(prompt_path.read_text())

    def assess_risk(self, analysis_text, role=None):
        if role:
            # specialized role injection
            prompt = f"As a {role}, review this analysis and identify risks strictly within your domain:\n\n{analysis_text}"
        else:
            prompt = (
                f"Based on this analysis, generate a strict JSON risk register.\n"
                f"Output MUST be a JSON object with key 'risks' containing a list of objects.\n"
                f"Each object must have keys: 'risk', 'severity' (1-10), 'mitigation', 'evidence_block_ids' (list of strings).\n"
                f"No markdown, no conversation. JUST JSON.\n\n"
                f"Analysis:\n{analysis_text}"
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
            logger.error(f"Failed to parse Risk JSON: {e}")
            return []
