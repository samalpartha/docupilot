
from .base import BaseAgent

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AnalystAgent", role="Senior Document Analyst")
        self.set_system_prompt("""You are the Analyst Agent for DocuPilot.
Your goal is to extract structured facts from legal and technical documents.
You MUST cite the 'block_id' for every fact you extract.

Output Format:
- Document Type: [Type] [block_id: ...]
- Key Parties: [Party1, Party2] [block_id: ...]
- Effective Dates: [Date] [block_id: ...]
- Obligations:
  - [Obligation 1] [block_id: ...]
  - [Obligation 2] [block_id: ...]

If you cannot find specific information, state "Not found".""")

    def analyze(self, evidence_text):
        return self.run(f"Analyze the following evidence and extract key information:\n\n{evidence_text}")
