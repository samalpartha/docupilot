import pypdfium2 as pdfium
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
from typing import List, Dict, Any

from src.config import Config

class PaddleOCRExtractor:
    def __init__(self, lang: str = "en"):
        # Initialize PaddleOCR
        # Use GPU if valid in Config
        print(f"DEBUG: Initializing PaddleOCR (Config.PADDLE_OCR_USE_GPU={Config.PADDLE_OCR_USE_GPU})")
        
        # Explicitly check and print
        if Config.PADDLE_OCR_USE_GPU:
             print("\n" + "="*50)
             print("  🚀 OCR ENGINE: GPU ACCELERATION ENABLED! (FAST MODE)")
             print("="*50 + "\n")
             use_gpu = True
        else:
             print("\n" + "="*50)
             print("  🐢 OCR ENGINE: CPU MODE (SLOW MODE)")
             print("     Set PADDLE_OCR_USE_GPU=true to enable acceleration.")
             print("="*50 + "\n")
             use_gpu = False
        
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang=lang,
            use_gpu=use_gpu
        )

    def extract_pdf(self, pdf_path: str, dpi: int = 200) -> List[Dict[str, Any]]:
        """
        Extract text from a PDF file using PaddleOCR with pypdfium2 for rendering.
        Returns a list of dictionaries, one per page.
        """
        print(f"DEBUG: Opening PDF {pdf_path} with pypdfium2")
        try:
            pdf = pdfium.PdfDocument(pdf_path)
        except Exception as e:
            print(f"ERROR: Failed to open PDF with pypdfium2. Error: {e}")
            raise e

        pages_text = []
        scale = dpi / 72.0

        print(f"DEBUG: Processing {len(pdf)} pages...")
        for i, page in enumerate(pdf):
            print(f"DEBUG: Rendering page {i+1}")
            # Render page to PIL image
            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()
            
            # Convert to numpy array for PaddleOCR
            img_np = np.array(pil_image)

            print(f"DEBUG: Running OCR on page {i+1}")
            result = self.ocr.ocr(img_np)

            if result and result[0]:
                for item_idx, block in enumerate(result[0]):
                    # block structure: [ [x1,y1], [x2,y2], ... ], (text, confidence)
                    points = block[0]
                    text_res = block[1]
                    text, confidence = text_res
                    
                    # specific output format
                    # Convert points to [x0, y0, x1, y1] for compatibility if needed
                    # But points are usually [[x,y], [x,y], [x,y], [x,y]]
                    # We'll keep bbox as is or convert to [x0, y0, x1, y1]
                    xs = [p[0] for p in points]
                    ys = [p[1] for p in points]
                    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
                    
                    pages_text.append({
                        "block_id": f"p{i+1}_b{item_idx}",
                        "page": i + 1,
                        "type": "text",
                        "text": text,
                        "confidence": confidence,
                        "bbox": [x0, y0, x1, y1]
                    })
            
        return pages_text

# Standalone function for compatibility
def ocr_pdf(pdf_path: str):
    extractor = PaddleOCRExtractor()
    return extractor.extract_pdf(pdf_path)
