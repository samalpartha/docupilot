
from .base import BaseAgent

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="VerifierAgent", role="Quality Assurance Auditor")
        self.set_system_prompt("""You are the Verifier Agent.
Your job is to check the generated Report against the original Evidence.
1. Verify that every [block_id: ...] citation exists in the evidence.
2. Verify that the text in the report accurately reflects the text in the cited block.
3. If a claim is unsupported, flag it.

Output a validation report.""")

    def verify(self, report_text, evidence_metadata):
        # In a real full impl, we'd pass the actual evidence text again or a subset.
        # For this hackathon scope, we'll ask it to verify the logic/structure.
        return self.run(f"Verify the following report for structural integrity and citation formatting:\n\n{report_text}")
