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
    # truncated_text = full_text[:10000] # Use chunking instead 
    
    # Merge Helper removed in favor of LLM Aggregation

    # 2. Analyst Phase (Chunked)
    analyst = AnalystAgent()
    logger.info("🔍 Analyst Agent working (Chunked Mode)...")
    
    # Simple chunking by character count (approx 8000 chars ~ 2000 tokens)
    CHUNK_SIZE = 8000
    chunks = [full_text[i:i+CHUNK_SIZE] for i in range(0, len(full_text), CHUNK_SIZE)]
    
    partial_results = []
    total_chunks = len(chunks)
    
    for i, chunk in enumerate(chunks):
        update_status(f"🔍 Analyst Agent: Processing Part {i+1}/{total_chunks}...")
        try:
            # Add context header to chunk
            chunk_context = f"[PART {i+1} OF {total_chunks}]\n" + chunk
            res = analyst.analyze(chunk_context)
            if res:
                partial_results.append(res)
        except Exception as e:
            logger.error(f"Failed to analyze chunk {i}: {e}")
            
    # Aggregate Results using LLM (Map-Reduce)
    update_status("🔍 Analyst Agent: Aggregating partially extracted data into Master Record...")
    # Clean partial results to be just the JSONs
    valid_partials = [p for p in partial_results if isinstance(p, dict)]
    analysis_result = analyst.aggregate(valid_partials)
    analysis_text = str(analysis_result)
    
    # 3. Risk Phase (Multi-Agent)
    risk_agent = RiskAgent()
    logger.info("⚠️ Risk Agents working (Compliance, Financial, Legal)...")
    
    all_risks = []
    
    # Role 1: Compliance
    update_status("👮 Compliance Analyst: Checking regulatory... (Step 1/3)")
    r_comp = risk_agent.assess_risk(analysis_text, role="Compliance Analyst")
    if isinstance(r_comp, dict) and 'risks' in r_comp: all_risks.extend(r_comp['risks'])
    
    # Role 2: Financial
    update_status("💰 Financial Reviewer: Checking fiscal... (Step 2/3)")
    r_fin = risk_agent.assess_risk(analysis_text, role="Financial Reviewer")
    if isinstance(r_fin, dict) and 'risks' in r_fin: all_risks.extend(r_fin['risks'])

    # Role 3: Legal
    update_status("⚖️ Legal Expert: Checking contractual... (Step 3/3)")
    r_legal = risk_agent.assess_risk(analysis_text, role="Legal Expert")
    if isinstance(r_legal, dict) and 'risks' in r_legal: all_risks.extend(r_legal['risks'])
    
    risk_result = {"risks": all_risks}
    risk_text = str(risk_result)
    
    # 4. Summarizer Phase
    summarizer = SummarizerAgent()
    logger.info("📝 Summarizer Agent working...")
    update_status("📝 Summarizer Agent: Drafting executive report...")
    # Truncate inputs for summarizer to prevent token overflow
    summarizer_input = f"Create an executive summary based on the following Analysis and Risk Report:\n\nANALYSIS:\n{analysis_text[:10000]}\n\nRISKS:\n{str(risk_text)[:10000]}"
    summary_result = summarizer.run(summarizer_input)
    
    # 5. Verification Phase
    verifier = VerifierAgent()
    logger.info("✅ Verifier Agent working...")
    update_status("✅ Verifier Agent: Auditing citations...")
    # Verify the Summary against the Evidence
    # Use a safe slice of text for verification to avoid token limits
    # Use the structured analysis as evidence (since summary is derived from it)
    # This ensures consistency and avoids "missing evidence" issues from raw text truncation.
    verifier_evidence = analysis_text[:10000] 
    verification_report = verifier.verify(summary_result, verifier_evidence)
    
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
