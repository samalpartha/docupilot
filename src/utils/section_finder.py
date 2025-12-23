
from typing import Dict, List, Optional
    
try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False

def is_section_heading(line: str, required_sections: List[str], threshold: int = 80) -> Optional[str]:
    """
    Detect if a line is a section heading.
    Uses fuzzy partial matching to handle cases like 'Submission Date: 15 Oct'.
    """
    line_lower = line.lower()
    
    if RAPIDFUZZ_AVAILABLE:
        for sec in required_sections:
            # Partial ratio is good for "Section 1: Payment Terms" matching "Payment Terms"
            if fuzz.partial_ratio(line_lower, sec.lower()) >= threshold:
                return sec
    else:
        # Fallback: simple substring
        for sec in required_sections:
            if sec.lower() in line_lower:
                return sec
    return None

def extract_sections(text: str, target_sections: List[str]) -> Dict[str, str]:
    """
    Extract specific sections from a document text.
    Returns a dict { 'Section Name': 'Content...' }
    """
    found_sections = {}
    text_lines = text.splitlines()

    current_section = None
    buffer = []

    for line in text_lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        matched_section = is_section_heading(line_stripped, target_sections)

        if matched_section:
            # Save previous section if any
            if current_section:
                found_sections[current_section] = "\n".join(buffer).strip()
            
            # Start new section
            current_section = matched_section
            
            # If heading has inline content (e.g. "Submission Date: 15 Oct"), capture it
            # We try to remove the header part from the line
            if RAPIDFUZZ_AVAILABLE:
                # Naively just keep the whole line if it's short, or split?
                # The external repo did: line_stripped.replace(matched_section, "") which is case sensitive and partial...
                # Let's keep the whole line in buffer as context usually helps
                buffer = [line_stripped]
            else:
                buffer = [line_stripped]
                
        else:
            if current_section:
                buffer.append(line_stripped)

    # Save last section
    if current_section:
        found_sections[current_section] = "\n".join(buffer).strip()

    return found_sections
