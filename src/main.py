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
@click.option('--output', default='src/outputs', help='Output directory')
def main(pdf, output):
    """DocuPilot: Multi-Agent Contract Review System"""
    
    print(r"""
    ____                  ____  _ __      __ 
   /           _  __     / __ \(_) /___  / /_
  / /   / __ \/ / / /____/ /_/ / / / __ \/ __/
 / /___/ /_/ / /_/ /____/ ____/ / / /_/ / /_  
/_____/\____/\__,_/    /_/   /_/_/\____/\__/  
                                              
    """)
    logger.info(f"Stats: Processing {pdf}")
    
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
    output_path = Path(output) / Path(pdf).stem
    output_path.mkdir(parents=True, exist_ok=True)
    
    (output_path / 'evidence.json').write_text(json.dumps(evidence, indent=2))
    (output_path / 'report.md').write_text(results['report'])
    (output_path / 'risk_register.csv').write_text(results['risks'])
    (output_path / 'run.log').write_text(f"Processed {pdf}\nStats: {evidence['metadata']}")
    
    logger.success(f"✨ Analysis Complete! Results in: {output_path}")

if __name__ == '__main__':
    main()
