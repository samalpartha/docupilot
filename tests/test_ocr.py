
import pytest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ocr import extract_document, _mock_extraction

def test_mock_extraction_scenarios():
    """Verify that different filenames trigger specific mock scenarios."""
    
    # 1. Court Order
    res_court = _mock_extraction("debug_court_order.pdf")
    texts_court = [b['text'] for b in res_court]
    assert any("UNITED STATES DISTRICT COURT" in t for t in texts_court)
    
    # 2. MSA / Contract
    res_msa = _mock_extraction("my_contract_msa.pdf")
    texts_msa = [b['text'] for b in res_msa]
    assert any("MASTER SERVICES AGREEMENT" in t for t in texts_msa)
    
    # 3. NDA
    res_nda = _mock_extraction("mutual_nda_final.pdf")
    texts_nda = [b['text'] for b in res_nda]
    assert any("MUTUAL NON-DISCLOSURE AGREEMENT" in t for t in texts_nda)
    
    # 4. Fallback Generic
    res_generic = _mock_extraction("random_file.pdf")
    assert res_generic[0]['text'].startswith("Generic Document")

def test_extract_document_fallback():
    """Verify that extract_document calls mock if Paddle fails."""
    
    # Since PPStructure is imported inside the try/except block or at top level
    # We must patch where it is *looked up* in src.ocr
    
    # If PADDLE_AVAILABLE is True (which it is now), PPStructure exists in src.ocr namespace.
    # However, to be robust if the import fails in test env, we use create=True
    with patch('src.ocr.PPStructure', side_effect=Exception("Simulated OCR Crash"), create=True):
        # This simulates the initialization failing
        result = extract_document("test_court.pdf")
        
        # Should have fallen back to mock data
        assert len(result) > 0
        assert any("UNITED STATES DISTRICT COURT" in b['text'] for b in result)
