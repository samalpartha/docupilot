
"""Normalize OCR output into structured evidence store"""

def create_evidence_store(blocks):
    """Create structured evidence store from OCR blocks.
    
    Args:
        blocks (list): List of block dictionaries from ocr.py
        
    Returns:
        dict: Evidence dictionary with 'blocks' and 'metadata'
    """
    
    cleaned_blocks = []
    
    for b in blocks:
        text = b.get('text', '').strip()
        # Clean up text - remove excessive newlines/spaces
        text = " ".join(text.split())
        
        # Simple heuristic to skip noise or empty blocks
        if text and len(text) > 2:
            cleaned_blocks.append({
                'id': b['block_id'],
                'page': b['page'],
                'text': text,
                'type': b.get('type', 'text')
                # We intentionally omit bbox/image data here to save context window size
                # The 'id' links back to the original OCR result if we need visual highlighting later
            })
            
    # Calculate metadata
    total_pages = 0
    if blocks:
        total_pages = max((b.get('page', 1) for b in blocks), default=1)
        
    return {
        'blocks': cleaned_blocks,
        'metadata': {
            'total_blocks': len(cleaned_blocks),
            'total_pages': total_pages,
            'source_validation': 'PaddleOCR-VL'
        }
    }
