
from pathlib import Path
from .base import BaseAgent

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AnalystAgent", role="Senior Document Analyst")
        prompt_path = Path(__file__).parent / 'prompts' / 'analyst.txt'
        self.set_system_prompt(prompt_path.read_text())

    def analyze(self, evidence_text):
        return self.run(f"Analyze the following evidence and extract key information:\n\n{evidence_text}")
