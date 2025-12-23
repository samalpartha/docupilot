from __future__ import annotations
from typing import Dict, Any, List, Optional
import requests

class ChatLLM:
    """
    Thin HTTP adapter to an ERNIE-compatible chat endpoint.
    Adjust payload keys to match your provider's schema.
    """
    def __init__(self, api_key: str, base_url: str, model: str):
        if not api_key:
            raise ValueError("ERNIE_API_KEY is required")
        if not base_url:
            raise ValueError("ERNIE_BASE_URL is required")
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 2048) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        r = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()

        # Common chat completion shape:
        # data["choices"][0]["message"]["content"]
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            # Fallback
            return str(data)
