
from loguru import logger
from .analyst import AnalystAgent
from .risk import RiskAgent
from .summarizer import SummarizerAgent
from .verifier import VerifierAgent

def run_pipeline(evidence):
    """
    Run the DocuPilot Multi-Agent Pipeline.
    
    Flow:
    1. Analyst Agent -> Extracts structured facts
    2. Risk Agent -> Evaluates facts for risks
    3. Summarizer Agent -> Creates executive summary
    4. Verifier Agent -> Checks validity (optional/parallel)
    """
    
    # Prepare text for context (taking first 10k chars to avoid token limits if simple)
    # In a real app we would chunk.
    full_text = "\n".join([f"[{b['id']}] {b['text']}" for b in evidence['blocks']])
    truncated_text = full_text[:12000] 
    
    logger.info("🚀 Starting Multi-Agent Pipeline...")

    # 1. Analyst Phase
    analyst = AnalystAgent()
    logger.info("🔍 Analyst Agent working...")
    analysis_result = analyst.analyze(truncated_text)
    
    # 2. Risk Phase
    risk_agent = RiskAgent()
    logger.info("⚠️ Risk Agent working...")
    risk_result = risk_agent.assess_risk(analysis_result)
    
    # 3. Summarizer Phase
    summarizer = SummarizerAgent()
    logger.info("📝 Summarizer Agent working...")
    summary_result = summarizer.summarize(analysis_result, risk_result)
    
    # 4. Verification Phase (Optional but adds value)
    verifier = VerifierAgent()
    logger.info("✅ Verifier Agent working...")
    verification_report = verifier.verify(summary_result, evidence)
    
    # Combine into Report
    final_report = f"""# DocuPilot Analysis Report

## Executive Summary
{summary_result}

## Risk Assessment
See `risk_register.csv` for details.

## Document Analysis
{analysis_result}

## Verification Report
{verification_report}
"""

    return {
        'report': final_report,
        'risks': risk_result,
        'analysis': analysis_result,
        'verification': verification_report
    }
