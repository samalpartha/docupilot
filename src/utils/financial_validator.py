
from typing import Dict, List, Any, Optional

def safe_float(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    try:
        # Handle string like "1,234.56"
        clean = str(value).replace(",", "").replace("$", "").strip()
        return float(clean)
    except (ValueError, TypeError):
        return 0.0

def validate_invoice_financials(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates financial consistency of an invoice data structure.
    Expected keys in data:
    - line_items: list of dicts with keys like 'qty'/'quantity', 'unit_price'/'price', 'line_total'/'total'
    - subtotal or total_sales
    - tax
    - discount
    - grand_total or total
    
    Returns:
        Dict with keys like 'line_items_valid', 'subtotal_valid', 'grand_total_valid'
    """
    checks = {}
    
    # Normalize keys
    line_items = data.get("line_items", [])
    subtotal = data.get("subtotal") if data.get("subtotal") is not None else data.get("total_sales")
    tax = data.get("tax", 0.0)
    discount = data.get("discount", 0.0)
    grand_total = data.get("grand_total") if data.get("grand_total") is not None else data.get("total")

    # 1. Check Line Items (Qty * Unit Price = Total)
    # We support multiple key variations
    if line_items and isinstance(line_items, list):
        valid_items_count = 0
        total_items_count = 0
        calculated_lines_sum = 0.0
        
        for item in line_items:
            if not isinstance(item, dict): continue
            
            # extract q, u, l
            q = safe_float(item.get("quantity") or item.get("qty"))
            u = safe_float(item.get("unit_price") or item.get("price"))
            l = safe_float(item.get("line_total") or item.get("total") or item.get("amount"))
            
            # If we have all three, valid check
            if q and u and l:
                total_items_count += 1
                expected = round(q * u, 2)
                # Allow small rounding diff
                if abs(expected - l) < 0.05:
                    valid_items_count += 1
            
            calculated_lines_sum += l

        if total_items_count > 0:
            checks["line_items_valid"] = (valid_items_count == total_items_count)
            checks["line_items_details"] = f"{valid_items_count}/{total_items_count} valid"
        else:
             checks["line_items_valid"] = True # No detailed items to fail on
             
        # 2. Check Subtotal (Sum of line totals = Subtotal)
        # Only check if we actually summed some lines and have a subtotal
        if subtotal is not None and calculated_lines_sum > 0:
            s_val = safe_float(subtotal)
            checks["subtotal_valid"] = abs(round(calculated_lines_sum, 2) - round(s_val, 2)) < 0.05
            checks["calculated_subtotal"] = round(calculated_lines_sum, 2)
        else:
             checks["subtotal_valid"] = None

    else:
        checks["line_items_valid"] = None
        checks["subtotal_valid"] = None

    # 3. Check Grand Total (Subtotal - Discount + Tax = Grand Total)
    if grand_total is not None and subtotal is not None:
        s = safe_float(subtotal)
        d = safe_float(discount)
        t = safe_float(tax)
        g = safe_float(grand_total)
        
        expected_total = s - d + t
        checks["grand_total_valid"] = abs(round(expected_total, 2) - round(g, 2)) < 0.05
        checks["expected_total"] = round(expected_total, 2)
        checks["found_total"] = round(g, 2)
    else:
        checks["grand_total_valid"] = None
        
    # Summarize pass/fail
    # If any specific check returned False, the whole validation fails
    all_checks = [v for k, v in checks.items() if k.endswith("_valid") and v is not None]
    checks["is_consistent"] = all(all_checks) if all_checks else True
    
    return checks
