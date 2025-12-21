from loguru import logger
from .ingestion import IngestionAgent
from .analyst import AnalystAgent
from .risk import RiskAgent
from .summarizer import SummarizerAgent
from .verifier import VerifierAgent

def run_pipeline(evidence, status_callback=None):
    """
    Run the DocuPilot Multi-Agent Pipeline.
    
    Flow:
    1. Ingestion Agent -> Cleans and Structures OCR
    2. Analyst Agent -> Extracts structured facts
    3. Risk Agent -> Evaluates facts for risks
    4. Summarizer Agent -> Creates executive summary
    5. Verifier Agent -> Checks validity
    """
    
    logger.info("🚀 Starting Multi-Agent Pipeline...")

    # helper to update status safely
    def update_status(msg):
        if status_callback:
            status_callback(msg)

    # 1. Ingestion Phase
    ingestion = IngestionAgent()
    logger.info("🧹 Ingestion Agent working...")
    update_status("🧹 Ingestion Agent: Cleaning OCR data...")
    # Process blocks (taking a subset if too large, or all)
    # We'll rely on the agent to handle the json dump
    cleaned_evidence = ingestion.process(evidence['blocks'])
    
    # Prepare text for context from CLEANED evidence
    # Format: [block_id] text
    full_text = "\n".join([f"[{b.get('id', 'N/A')}] {b.get('text', '')}" for b in cleaned_evidence])
    
    # Truncate for context window if needed (keeping reasonable size)
    truncated_text = full_text[:15000] 
    
    # 2. Analyst Phase
    analyst = AnalystAgent()
    logger.info("🔍 Analyst Agent working...")
    update_status("🔍 Analyst Agent: Extracting structured facts...")
    analysis_result = analyst.analyze(truncated_text)
    
    # 3. Risk Phase
    risk_agent = RiskAgent()
    logger.info("⚠️ Risk Agent working...")
    update_status("⚠️ Risk Agent: Assessing vulnerabilities...")
    risk_result = risk_agent.assess_risk(analysis_result)
    
    # 4. Summarizer Phase
    summarizer = SummarizerAgent()
    logger.info("📝 Summarizer Agent working...")
    update_status("📝 Summarizer Agent: Drafting executive report...")
    summary_result = summarizer.summarize(analysis_result, risk_result)
    
    # 5. Verification Phase
    verifier = VerifierAgent()
    logger.info("✅ Verifier Agent working...")
    update_status("✅ Verifier Agent: Auditing citations...")
    # Verify the Summary against the Evidence
    verification_report = verifier.verify(summary_result, truncated_text)
    
    # Combine into Report
    # Note: verification_report from Verifier Agent is supposed to be "Corrected Content" according to prompt.
    # So we might want to use that as the final summary if it rewrites it.
    # The prompt says: "Output corrected content only."
    # So let's assume verification_report IS the verified summary.
    
    final_report = f"""# DocuPilot Analysis Report

## Executive Summary (Verified)
{verification_report}

## Risk Assessment
See `Identified Risks` tab for the verified Risk Register.
"""

    return {
        'report': final_report,
        'risks': risk_result,
        'analysis': analysis_result,
        'verification': verification_report,
        'cleaned_evidence': cleaned_evidence
    }
