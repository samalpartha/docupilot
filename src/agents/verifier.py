
from pathlib import Path
from .base import BaseAgent

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="VerifierAgent", role="Quality Assurance Auditor")
        prompt_path = Path(__file__).parent / 'prompts' / 'verifier.txt'
        self.set_system_prompt(prompt_path.read_text())

    def verify(self, report_text, evidence_text):
        return self.run(f"Audit the following report against the provided evidence:\n\nEVIDENCE:\n{evidence_text}\n\nREPORT TO AUDIT:\n{report_text}")
