
from pathlib import Path
from .base import BaseAgent
import json
from loguru import logger

class IngestionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="IngestionAgent", role="OCR Data Cleaner")
        prompt_path = Path(__file__).parent / 'prompts' / 'ingestion.txt'
        self.set_system_prompt(prompt_path.read_text())

    def process(self, blocks):
        # Convert blocks to a JSON string for the agent to process
        # We might need to chunk this if it's too large, but for now we pass it all.
        blocks_str = json.dumps(blocks, indent=2)
        
        response = self.run(f"Process these OCR blocks and return cleaned structure:\n\n{blocks_str}")
        
        try:
            # Attempt to parse the response as JSON
            # The agent might return markdown code blocks, so we strip them
            cleaned_text = response.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            return json.loads(cleaned_text.strip())
        except Exception as e:
            logger.warning(f"Ingestion Agent returned invalid JSON: {e}. Returning original blocks.")
            return blocks
