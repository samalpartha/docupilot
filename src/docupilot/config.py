from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    ernie_api_key: str = os.getenv("ERNIE_API_KEY") or os.getenv("ERNIE_ACCESS_TOKEN") or ""
    # Try to deduce base_url if missing but assume user might provide it later
    ernie_base_url: str = os.getenv("ERNIE_BASE_URL", "")
    ernie_model: str = os.getenv("ERNIE_MODEL", "ernie-4.0")

    # Risk scoring defaults (tunable)
    score_min: int = 0
    score_max: int = 100

settings = Settings()

if not settings.ernie_base_url and settings.ernie_api_key:
    # Fallback to standard Ernie public API if not specified (best effort)
    # This might need adjustment based on specific model
    print("WARNING: ERNIE_BASE_URL not set. Defaulting to standard public endpoint for ERNIE-4.0-8K.")
    settings.ernie_base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro" 

