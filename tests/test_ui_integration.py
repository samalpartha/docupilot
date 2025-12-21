
import pytest
from streamlit.testing.v1 import AppTest
import os
from unittest.mock import patch, MagicMock

# We need to set the dummy token so the app doesn't show "Missing Token" error
os.environ['ERNIE_ACCESS_TOKEN'] = 'TEST_TOKEN'
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

def test_app_startup():
    """Smoke test: Verify the app starts and loads title."""
    at = AppTest.from_file("src/app.py", default_timeout=10).run()
    assert not at.exception
    assert "DocuPilot" in at.title[0].value

def test_app_scenario_court_order():
    """Integration Test: Load Court Order Scenario & Run Analysis."""
    
    # We must patch the 'run_pipeline' to avoid real Agent/OCR calls during UI testing
    # We want to test that the UI *calls* it and renders the *result*
    
    mock_results = {
        'report': '# Executive Summary\n\nMock Report Content.',
        'risks': [{'risk': 'UI Test Risk', 'severity': 5, 'evidence_block_ids': ['p1_b1']}],
        'analysis': '{"court": "Mock Court", "parties": {"plaintiff": "Mock P"}}'
    }
    
    mock_evidence = {
        'blocks': [{'id': 'p1_b1', 'text': 'Mock Evidence Text'}]
    }

    # Patch deeply to ensure AppTest picks it up regardless of import reference
    with patch('src.agents.orchestrator.run_pipeline', return_value=mock_results) as mock_run:
        with patch('src.normalize.create_evidence_store', return_value=mock_evidence):
            with patch('src.ocr.extract_document', return_value=[]):
        
                at = AppTest.from_file("src/app.py", default_timeout=15).run()
                
                # 1. Click "Court Order (NY)" button
                at.sidebar.button[0].click().run()
                
                # Verify "Ready to Analyze" message appeared
                # The message says: "Ready to Analyze: **court_order.pdf**"
                assert len(at.success) > 0
                assert "court_order.pdf" in at.success[0].value
                
                # 2. Click "Start Analysis Engine"
                try:
                    at.button[0].click().run()
                except Exception:
                    pass # Sometimes timeout happens on click even if logic is fast if Streamlit decides to rerender all
                
                # 3. Verify Results Rendered
                md_values = [m.value for m in at.markdown]
                assert any("Executive Summary" in m for m in md_values)
                
                assert len(at.dataframe) > 0
                
                info_values = [i.value for i in at.info]
                # The 'Context' is rendered in an info box
                assert any("Mock Court" in i for i in info_values)

def test_app_url_upload_tab():
    """Verify URL Tab exists and interacts."""
    at = AppTest.from_file("src/app.py").run()
    
    # Check Tabs exist
    assert len(at.tabs) == 2
    assert at.tabs[1].label == "🔗 Paste URL"
