
from .base import BaseAgent

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SummarizerAgent", role="Executive Summarizer")
        self.set_system_prompt("""You are the Summarizer Agent for DocuPilot.
Create a high-level executive summary for a non-technical stakeholder.
Highlight the most critical findings (parties, value, risks).
Keep it under 12 bullet points.
Always include citations [block_id: ...] where possible.""")

    def summarize(self, analysis_text, risk_text):
        return self.run(f"Create an executive summary based on the following Analysis and Risk Report:\n\nANALYSIS:\n{analysis_text}\n\nRISKS:\n{risk_text}")
