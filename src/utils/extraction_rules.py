
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime

# =============================================================================
# INVOICE EXTRACTION RULES
# =============================================================================

def extract_invoice_line_items(text: str) -> List[Dict[str, Union[float, int]]]:
    """
    Extracts line items from invoice text using common regex patterns.
    Returns a list of dicts: {'qty': int, 'unit_price': float, 'line_total': float}
    """
    line_items = []
    # Patterns from external repo (best practices)
    line_patterns = [
        # Qty | Unit Price | Line Total
        r"(\d+)\s*(?:/\s*\w+)?\s+([\d,]+\.\d{2,3})\s+([\d,]+\.\d{2,3})",
        # Qty | Unit Price | Line Total (Flexible spacing)
        r"(\d+)[\s\S]{1,20}?([\d,]+\.\d{2})[\s\S]{1,20}?([\d,]+\.\d{2})",
    ]

    for pattern in line_patterns:
        matches = re.findall(pattern, text)
        if matches:
            potential_items = []
            for match in matches:
                try:
                    qty = int(match[0])
                    unit = float(match[1].replace(",", ""))
                    total = float(match[2].replace(",", ""))
                    potential_items.append({"qty": qty, "unit_price": unit, "line_total": total})
                except (ValueError, IndexError):
                    continue
            
            # If we found items that look mathematically valid, assume this pattern is the right one
            if potential_items:
                # Basic validation: check if at least one item makes sense (Qty * Unit ~= Total)
                valid_count = sum(1 for item in potential_items if abs(item['qty'] * item['unit_price'] - item['line_total']) < 0.05)
                if valid_count > 0:
                    line_items = potential_items
                    break
    
    return line_items

def extract_invoice_totals(text: str) -> Dict[str, Optional[float]]:
    """
    Extracts Total, Discount, Tax using regex hierarchies.
    """
    def _extract_first_match(patterns: List[str]) -> Optional[float]:
        for p in patterns:
            # Case insensitive search
            m = re.search(p, text, re.IGNORECASE)
            if m:
                try:
                    clean_str = m.group(1).replace(",", "").replace("$", "").strip()
                    return float(clean_str)
                except ValueError:
                    continue
        return None

    # Patterns derived from external repo
    data = {}
    
    data['total_sales'] = _extract_first_match([
        r"Total Sales[^\d]*([\d,]+\.\d+)",
        r"Subtotal[^\d]*([\d,]+\.\d+)",
        r"Net Amount[^\d]*([\d,]+\.\d+)"
    ])
    
    data['discount'] = _extract_first_match([
        r"Total discount[^\d]*([\d,]+\.\d+)",
        r"Discount[^\d]*([\d,]+\.\d+)",
        r"Less Discount[^\d]*([\d,]+\.\d+)"
    ])
    
    data['tax'] = _extract_first_match([
        r"Value added tax[^\d]*([\d,]+\.\d+)",
        r"VAT[^\d]*([\d,]+\.\d+)",
        r"Tax[^\d]*([\d,]+\.\d+)"
    ])
    
    data['grand_total'] = _extract_first_match([
        r"Total Amount[^\d]*([\d,]+\.\d+)",
        r"Grand Total[^\d]*([\d,]+\.\d+)",
        r"Amount Due[^\d]*([\d,]+\.\d+)",
        r"TOTAL[^\d]*([\d,]+\.\d+)"
    ])
    
    return data

# =============================================================================
# CONTRACT EXTRACTION RULES
# =============================================================================

def extract_contract_dates(text: str) -> Dict[str, Optional[str]]:
    """
    Heuristically finds Effective Date and Expiry Date.
    """
    dates = {}
    
    # Expiry Date patterns
    expiry_match = re.search(
        r"(?:expiry|expire|termination|end)[\s\S]{0,20}?date[\s\S]{0,10}?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", 
        text, re.IGNORECASE
    )
    if not expiry_match:
        # Try context like "expires on 12/12/2024"
        expiry_match = re.search(r"expires\s*on\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text, re.IGNORECASE)

    dates['expiry_date'] = expiry_match.group(1) if expiry_match else None
    
    # Effective Date patterns
    eff_match = re.search(
        r"(?:effective|start|commencement)[\s\S]{0,20}?date[\s\S]{0,10}?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        text, re.IGNORECASE
    )
    dates['effective_date'] = eff_match.group(1) if eff_match else None
    
    return dates

def extract_contract_value(text: str) -> Optional[str]:
    """
    Extracts contract value with currency.
    """
    # Look for large numbers associated with currency symbols/codes
    # e.g. $1,000,000 or 50,000 USD
    pattern = r"((?:\$|USD|EUR|GBP|SAR)[\s]*[\d,]+\.?\d*|[\d,]+\.?\d*[\s]*(?:USD|EUR|GBP|SAR))"
    
    matches = re.findall(pattern, text)
    if matches:
        # Return the 'largest' number found that looks like a contract value (heuristic)
        # Not perfect, but a good hint
        return matches[0] # Naive first match for now
        
    return None
