
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.base import BaseAgent
from src.agents.orchestrator import run_pipeline

@pytest.fixture
def mock_ernie_response():
    """Mock ERNIE response object."""
    mock_resp = MagicMock()
    mock_resp.get_result.return_value = '{"risks": [{"risk": "Test Risk", "severity": 5}]}'
    return mock_resp

def test_base_agent_run(mock_ernie_response):
    """Test BaseAgent.run with valid ERNIE response."""
    
    with patch('erniebot.ChatCompletion.create') as mock_create:
        mock_create.return_value = mock_ernie_response
        
        agent = BaseAgent(name="TestAgent", role="Tester")
        result = agent.run("Hello")
        
        assert "Test Risk" in result
        mock_create.assert_called_once()

def test_base_agent_failure():
    """Test BaseAgent handling API failure."""
    
    with patch('erniebot.ChatCompletion.create') as mock_create:
        mock_create.side_effect = Exception("API Down")
        
        agent = BaseAgent("FaultyAgent", "Tester")
        result = agent.run("Do work")
        
        assert "Error executing task" in result

def test_orchestrator_pipeline():
    """Test full pipeline orchestration with mocked agents."""
    
    # Create fake evidence
    evidence = {'blocks': [{'id': 'b1', 'text': 'Test evidence'}]}
    
    # We mock BaseAgent.run to return canned JSON responses
    # This avoids mocking the deep internal ERNIE calls for every step
    with patch('src.agents.base.BaseAgent.run') as mock_run:
        
        def side_effect(message):
            if "Analyst" in message or "Expert" in message: 
                return '{"analysis": "Valid"}'
            if "Risk" in message:
                return '{"risks": [{"risk": "Mock Risk", "severity": 5, "evidence_block_ids": ["b1"]}]}'
            return "{}"

        mock_run.side_effect = side_effect
        
        # Run pipeline
        # Status callback is a lambda that does nothing
        results = run_pipeline(evidence, status_callback=lambda x: None)
        
        assert isinstance(results, dict)
        assert 'report' in results
        assert 'risks' in results
