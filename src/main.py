#!/usr/bin/env python3
"""DocuPilot - Multi-agent document analysis system"""

import os
import json
from pathlib import Path
import click
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

@click.command()
@click.option('--pdf', required=True, type=click.Path(exists=True), help='Path to PDF file')
@click.option('--output', default='outputs', help='Output directory')
def main(pdf, output):
    """Process PDF through DocuPilot multi-agent system."""
    
    logger.info(f"🚀 DocuPilot starting: {pdf}")
    
    try:
        # Step 1: OCR extraction
        logger.info("📄 Step 1: Extracting with PaddleOCR...")
        from ocr import extract_document
        blocks = extract_document(pdf)
        logger.success(f"Extracted {len(blocks)} text blocks")
        
        # Step 2: Normalize
        logger.info("🔄 Step 2: Normalizing evidence...")
        from normalize import create_evidence_store
        evidence = create_evidence_store(blocks)
        
        # Step 3: Run multi-agent pipeline
        logger.info("🤖 Step 3: Running ERNIE agents...")
        from agents.orchestrator import run_pipeline
        results = run_pipeline(evidence)
        
        # Step 4: Save outputs
        output_dir = Path(output) / Path(pdf).stem
        output_dir.mkdir(parents=True, exist_ok=True)
        
        (output_dir / 'evidence.json').write_text(json.dumps(evidence, indent=2))
        (output_dir / 'report.md').write_text(results['report'])
        (output_dir / 'risk_register.csv').write_text(results['risks'])
        
        logger.success(f"✅ Complete! Outputs in: {output_dir}")
        logger.info(f"📁 Files: evidence.json, report.md, risk_register.csv")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    main()
