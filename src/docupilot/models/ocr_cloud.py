import base64
import requests
import json
from typing import List, Dict, Any
from loguru import logger
from src.config import Config

class CloudOCRExtractor:
    def __init__(self):
        self.api_url = Config.CLOUD_OCR_URL
        self.token = Config.CLOUD_OCR_TOKEN
        
        if not self.token:
            logger.warning("Cloud OCR Token not found. Please set CLOUD_OCR_TOKEN in .env")

    def extract_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text and layout from PDF using Baidu Cloud Layout Parsing API.
        """
        logger.info(f"Uploading {pdf_path} to Baidu Cloud OCR...")
        
        with open(pdf_path, "rb") as file:
            file_bytes = file.read()
            file_data = base64.b64encode(file_bytes).decode("ascii")

        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json"
        }

        # fileType 0 for PDF
        payload = {
            "file": file_data,
            "fileType": 0, 
            "useDocOrientationClassify": False,
            "useDocUnwarping": False,
            "useChartRecognition": False,
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=120)
            
            if response.status_code != 200:
                logger.error(f"Cloud OCR Failed: {response.text}")
                raise Exception(f"Cloud OCR Error: {response.status_code}")
                
            result = response.json()
            if result.get("errorCode") != 0:
                 logger.error(f"Cloud OCR API Error: {result.get('errorMsg')}")
                 raise Exception(f"API Error: {result.get('errorMsg')}")
                 
            return self._parse_response(result)
            
        except Exception as e:
            logger.error(f"Cloud OCR Request Failed: {e}")
            raise e

    def _parse_response(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        blocks = []
        
        layout_results = result.get("result", {}).get("layoutParsingResults", [])
        
        for page_idx, page_res in enumerate(layout_results):
            pruned = page_res.get("prunedResult", {})
            parsing_list = pruned.get("parsing_res_list", [])
            
            for item in parsing_list:
                # API returns [x1, y1, x2, y2] style or similar.
                # Example JSON check shown: "block_bbox": [344, 71, 876, 106] which is x1, y1, x2, y2
                bbox = item.get("block_bbox", [])
                text = item.get("block_content", "")
                label = item.get("block_label", "text")
                
                # Standardize Block ID
                block_id = f"p{page_idx+1}_b{item.get('block_id', 0)}"
                
                blocks.append({
                    "block_id": block_id,
                    "page": page_idx + 1,
                    "type": label,
                    "text": text,
                    "confidence": 0.99, # Cloud API doesn't give per-block confidence easily in this list, assume high
                    "bbox": bbox
                })
                
        return blocks
