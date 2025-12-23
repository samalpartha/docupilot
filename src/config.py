"""Configuration management for DocuPilot."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the application."""
    
    # ERNIE API Configuration
    ERNIE_API_KEY = os.getenv('ERNIE_API_KEY', '')
    ERNIE_SECRET_KEY = os.getenv('ERNIE_SECRET_KEY', '')
    ERNIE_MODEL = os.getenv('ERNIE_MODEL', 'ernie-bot-4')
    
    # PaddleOCR Configuration
    PADDLE_OCR_LANG = os.getenv('PADDLE_OCR_LANG', 'en')
    PADDLE_OCR_USE_GPU = os.getenv('PADDLE_OCR_USE_GPU', 'false').lower() == 'true'
    
    # Cloud OCR Configuration (Baidu)
    CLOUD_OCR_ENABLED = os.getenv('CLOUD_OCR_ENABLED', 'false').lower() == 'true'
    CLOUD_OCR_URL = os.getenv('CLOUD_OCR_URL', "https://g49fgd0070pda7k8.aistudio-app.com/layout-parsing")
    CLOUD_OCR_TOKEN = os.getenv('CLOUD_OCR_TOKEN', '')
    
    # CAMEL AI Configuration
    CAMEL_MODEL_TYPE = os.getenv('CAMEL_MODEL_TYPE', 'ernie')
    CAMEL_MAX_ITERATIONS = int(os.getenv('CAMEL_MAX_ITERATIONS', '5'))
    
    # Processing Configuration
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
    
    # Document Analysis Configuration
    RISK_CATEGORIES = [
        'compliance',
        'financial',
        'legal',
        'operational',
        'reputational'
    ]
    
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is set."""
        required_vars = ['ERNIE_API_KEY', 'ERNIE_SECRET_KEY']
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        
        return True
    
    @classmethod
    def get_output_paths(cls, base_name):
        """Generate output file paths."""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        
        return {
            'extracted_text': os.path.join(cls.OUTPUT_DIR, f"{base_name}_extracted.txt"),
            'normalized': os.path.join(cls.OUTPUT_DIR, f"{base_name}_normalized.json"),
            'analysis': os.path.join(cls.OUTPUT_DIR, f"{base_name}_analysis.json"),
            'summary': os.path.join(cls.OUTPUT_DIR, f"{base_name}_summary.json")
        }
