
from pathlib import Path
from .base import BaseAgent

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SummarizerAgent", role="Executive Summarizer")
        prompt_path = Path(__file__).parent / 'prompts' / 'summarizer.txt'
        self.set_system_prompt(prompt_path.read_text())

    def summarize(self, analysis_text, risk_text):
        return self.run(f"Create an executive summary based on the following Analysis and Risk Report:\n\nANALYSIS:\n{analysis_text}\n\nRISKS:\n{risk_text}")
