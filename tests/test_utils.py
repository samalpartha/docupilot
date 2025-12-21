
import pytest
import sys
import os
import json

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import get_safe_text, parse_agent_json

def test_get_safe_text():
    # 1. Dict case
    assert get_safe_text({'description': 'Test'}, 'description') == 'Test'
    assert get_safe_text({'other': 'Test'}, 'description') == 'N/A'
    
    # 2. String case
    assert get_safe_text("Just a string") == "Just a string"
    assert get_safe_text(123) == "123"

def test_parse_agent_json():
    # 1. Valid JSON
    valid = '{"key": "value"}'
    assert parse_agent_json(valid) == {'key': 'value'}
    
    # 2. Markdown Wrapped
    markdown = '```json\n{"key": "value"}\n```'
    assert parse_agent_json(markdown) == {'key': 'value'}
    
    # 3. Dirty text
    dirty = 'Here is the json: {"key": "value"} thanks.'
    assert parse_agent_json(dirty) == {'key': 'value'}
    
    # 4. Invalid
    assert parse_agent_json("Not json") is None
    assert parse_agent_json(None) is None
