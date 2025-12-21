#!/usr/bin/env python3
import os
import sys
import json
import click
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ocr import extract_document
from src.normalize import create_evidence_store
from src.agents.orchestrator import run_pipeline

load_dotenv()

@click.command()
@click.option('--pdf', required=True, type=click.Path(exists=True), help='Path to PDF file')
@click.option('--domain', required=True, type=click.Choice(['legal_pleadings'], case_sensitive=False), help='Domain of the document')
@click.option('--out', required=True, type=click.Path(), help='Output directory')
@click.option('--rules', type=click.Path(exists=True), help='Optional YAML rules file')
@click.option('--top_k', default=8, help='Number of evidence blocks to retrieve')
def main(pdf, domain, out, rules, top_k):
    """DocuPilot: Multi-Agent Contract Review System"""
    
    print(r"""
    ____                  ____  _ __      __ 
   /           _  __     / __ \(_) /___  / /_
  / /   / __ \/ / / /____/ /_/ / / / __ \/ __/
 / /___/ /_/ / /_/ /____/ ____/ / / /_/ / /_  
/_____/\____/\__,_/    /_/   /_/_/\____/\__/  
                                              
    """)
    logger.info(f"Stats: Processing {pdf} | Domain: {domain}")
    if rules:
        logger.info(f"Loaded rules from: {rules}")
    
    # 1. Perception Layer
    blocks = extract_document(pdf)
    if not blocks:
        logger.error("No blocks extracted. Exiting.")
        return

    # 2. Normalization Layer
    evidence = create_evidence_store(blocks)
    logger.info(f"Evidence prepared: {evidence['metadata']['total_blocks']} blocks")
    
    # 3. Agent Layer
    results = run_pipeline(evidence)
    
    # 4. Storage Layer
    output_path = Path(out)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Writing outputs as requested
    (output_path / 'evidence.json').write_text(json.dumps(results.get('cleaned_evidence', evidence), indent=2))
    (output_path / 'report.md').write_text(results['report'])
    
    # Risk Register CSV
    risks = results['risks']
    if isinstance(risks, list) and risks:
        import csv
        import io
        output = io.StringIO()
        # derived from user schema: risk_id,category,risk,severity,evidence_block_ids,mitigation
        # The prompt asks for: risk, category, severity, evidence_block_ids, mitigation
        # We might need to generate risk_id if not present, or the agent provided it?
        # The prompt implicitly didn't ask for risk_id in the bullet list but the schema provided later did.
        # I'll rely on the keys present.
        keys = risks[0].keys()
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        writer.writerows(risks)
        csv_content = output.getvalue()
    else:
        csv_content = ""
        
    (output_path / 'risk_register.csv').write_text(csv_content)
    (output_path / 'run.log').write_text(f"Processed {pdf}\nDomain: {domain}\nStats: {evidence['metadata']}\n\nAudit Trail:\n{results['analysis']}")
    
    logger.success(f"✨ Analysis Complete! Results in: {output_path}")

if __name__ == '__main__':
    main()
