
from .base import BaseAgent

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RiskAgent", role="Compliance Risk Officer")
        self.set_system_prompt("""You are the Risk Agent for DocuPilot.
Your goal is to identify risks in the document analysis provided.
Focus on: Liability caps, indeterminate terms, missing SLAs, auto-renewals without notice, and unbalanced indemnification.

Output Format (CSV):
Risk ID,Risk Description,Severity (1-5),Evidence Block IDs,Mitigation
R001,Description,5,"id1, id2",Suggestion

Strictly follow CSV format.""")

    def assess_risk(self, analysis_text):
        return self.run(f"Based on this analysis, generate a risk register:\n\n{analysis_text}")
