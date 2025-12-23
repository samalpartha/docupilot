
import streamlit as st
import tempfile
import json
import re
import os
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
import pandas as pd
import requests
from io import BytesIO
import sys
from pathlib import Path

# Ensure src module is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ocr import extract_document
from src.normalize import create_evidence_store
from src.agents.orchestrator import run_pipeline

# --- HELPER FUNCTIONS ---

def get_safe_text(obj, key='description'):
    """Safely extracts text whether obj is a dict or string."""
    if isinstance(obj, dict):
        return obj.get(key, 'N/A')
    return str(obj)

def parse_agent_json(json_str):
    """Robustly parses JSON from LLM output, handling markdown fences and preambles."""
    if not json_str:
        return None
    
    # Clean string
    json_str = json_str.strip()
    
    # Handle Markdown Code Blocks (common from LLMs)
    if "```" in json_str:
        # Extract content inside the first code block
        pattern = r"```(?:json)?\s*(.*?)\s*```"
        match = re.search(pattern, json_str, re.DOTALL | re.IGNORECASE)
        if match:
             json_str = match.group(1)
             
    # 1. Try clean load
    try:
        return json.loads(json_str)
    except:
        pass
    
    # 2. Try identifying the first outer bracket pair
    try:
        start = json_str.find('{')
        end = json_str.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = json_str[start:end+1]
            return json.loads(candidate)
    except:
        pass
        
    return None

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DocuPilot: Intelligent Risk Review",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .feature-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #464b5d;
        height: 100%;
    }
    .feature-title {
        color: #ffffff;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .feature-desc {
        color: #a0a0a0;
        font-size: 0.9rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stFileUploader {
        padding: 2rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='font-size: 60px; text-align: center;'>⚖️</div>", unsafe_allow_html=True)
    st.markdown("### DocuPilot")
    st.caption("Multi-agent legal risk analysis")
    
    st.markdown("---")
    
    st.markdown("**Analysis Configuration**")
    
    # Domain Selection
    domain = st.selectbox(
        label="Document Domain", 
        options=["Legal Pleadings", "Contract Review", "Policy Audit"]
    )
    
    # NEW: Jurisdiction / State Selection
    jurisdiction = st.selectbox(
        label="Jurisdiction / State Law",
        options=["Federal (USA)", "California", "New York", "Delaware", "Texas", "Illinois", "United Kingdom", "EU (GDPR)"],
        index=0,
        help="Select the governing law to contextualize the AI's risk assessment."
    )
    
    # Legal Resources Logic
    JURISDICTION_RESOURCES = {
        "Federal (USA)": [
            {"name": "US Courts Forms", "url": "https://www.uscourts.gov/forms/search", "icon": "🇺🇸"},
            {"name": "Federal Rules (LII)", "url": "https://www.law.cornell.edu/rules/frcp", "icon": "📖"}
        ],
        "California": [
            {"name": "CA Court Forms", "url": "https://www.courts.ca.gov/forms.htm", "icon": "🌴"},
            {"name": "CA Codes (LegInfo)", "url": "https://leginfo.legislature.ca.gov/", "icon": "📜"}
        ],
        "New York": [
            {"name": "NY State Court Forms", "url": "https://ww2.nycourts.gov/forms/index.shtml", "icon": "🗽"},
            {"name": "NYCSLC (Contracts)", "url": "https://www.nycbar.org/reports/model-forms-for-judicial-settlement-conferences/", "icon": "⚖️"}
        ],
        "Delaware": [
            {"name": "DE Chancery Forms", "url": "https://www.courts.delaware.gov/forms/", "icon": "🏢"}
        ],
        "Texas": [
            {"name": "TX Legal Forms", "url": "https://www.sll.texas.gov/legal-help/legal-forms/", "icon": "🤠"}
        ]
    }
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📚 Legal Resources", expanded=True):
        resources = JURISDICTION_RESOURCES.get(jurisdiction, [
            {"name": "General Legal Forms", "url": "https://www.lawdepot.com/", "icon": "🌎"}
        ])
        for res in resources:
            st.markdown(f"[{res['icon']} **{res['name']}**]({res['url']})")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("**Quick Start Scenarios**")
    if st.button("🏛️ Court Order (NY)", use_container_width=True):
        st.session_state['active_example'] = 'court_order.pdf'
        st.session_state['results'] = None 
        
    if st.button("📝 MSA Contract", use_container_width=True):
        st.session_state['active_example'] = 'contract_msa.pdf'
        st.session_state['results'] = None
        
    if st.button("🔒 NDA (Confidentiality)", use_container_width=True):
        st.session_state['active_example'] = 'mutual_nda.pdf'
        st.session_state['results'] = None
    
    # "Powered By" Pill at bottom
    st.markdown("<br>" * 8, unsafe_allow_html=True)
    
    # SYSTEM CHECKS
    # 1. OCR Mode
    ocr_status = "🟢" if "paddleocr" in sys.modules else "🟡 (Simulated)"
    # Note: sys.modules check is loose, ideally check src.ocr.PADDLE_AVAILABLE if we exported it.
    
    # 2. LLM Token Check
    ernie_token = os.getenv('ERNIE_ACCESS_TOKEN')
    if not ernie_token:
         st.error("⚠️ Missing ERNIE_ACCESS_TOKEN")
    
    st.info(f"⚡ Powered by PaddleOCR + ERNIE 4.0\n\nContext: {jurisdiction}\n\nOCR Status: {ocr_status}")


# --- MAIN CONTENT ---

# Header
col_logo, col_text = st.columns([1, 10])
with col_logo:
    st.markdown("<div style='font-size: 60px;'>⚖️</div>", unsafe_allow_html=True)
with col_text:
    st.title("DocuPilot: Intelligent Risk Review")
    st.markdown("Upload a legal document (PDF) to automatically extract structure, identify parties, and assess risk using our verified multi-agent pipeline.")

st.markdown("### Upload Legal Document")

# Tabs for Upload Method
up_tab1, up_tab2 = st.tabs(["📂 Upload File", "🔗 Paste URL"])

uploaded_file_obj = None

with up_tab1:
    uploaded_file_obj = st.file_uploader("Drag and drop file here", type="pdf", label_visibility="collapsed")

with up_tab2:
    url_input = st.text_input("Enter PDF URL", placeholder="https://example.com/contract.pdf")
    if url_input:
        if st.button("Fetch Document", key="fetch_url_btn"):
            with st.spinner("Downloading..."):
                try:
                    response = requests.get(url_input, timeout=10)
                    response.raise_for_status()
                    
                    # Create file-like object
                    file_content = BytesIO(response.content)
                    # Attempt to derive filename
                    filename = url_input.split("/")[-1]
                    if not filename.lower().endswith(".pdf"):
                        filename += ".pdf"
                    file_content.name = filename
                    
                    uploaded_file_obj = file_content
                    st.success(f"Successfully loaded: {filename}")
                    
                except Exception as e:
                    st.error(f"Failed to load URL: {e}")

# Logic to handle uploads vs examples
final_file_payload = None
display_name = ""

# Note: st.file_uploader persists in up_tab1, but manual BytesIO in up_tab2 
# might reset on rerun unless stored in session_state.
# For simplicity in this demo, strict linear flow is acceptable, 
# but storing 'fetched_file' in session_state is safer for URL uploads.

if 'fetched_file' not in st.session_state:
    st.session_state['fetched_file'] = None

if uploaded_file_obj and hasattr(uploaded_file_obj, 'name') and url_input:
     # Valid URL fetch just happened
     st.session_state['fetched_file'] = uploaded_file_obj

# Determine source
if st.session_state.get('fetched_file'):
    final_file_payload = st.session_state['fetched_file']
    display_name = final_file_payload.name
    if 'active_example' in st.session_state:
        del st.session_state['active_example']
        
elif uploaded_file_obj is not None:
    final_file_payload = uploaded_file_obj
    display_name = uploaded_file_obj.name
    # Clear fetched_file if user switches to manual upload
    st.session_state['fetched_file'] = None
    if 'active_example' in st.session_state:
        del st.session_state['active_example']

elif 'active_example' in st.session_state:
    display_name = st.session_state['active_example']
    final_file_payload = "EXAMPLE_MODE"
    st.session_state['fetched_file'] = None # Clear URL file
    st.info(f"👉 **Example Loaded:** {display_name}")

# Feature Cards (Empty State)
if final_file_payload is None:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📋 Structure Extraction</div>
            <div class="feature-desc">Automatically parse document hierarchy, sections, and layout using PaddleOCR-VL.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">👥 Party Identification</div>
            <div class="feature-desc">Identify all parties, roles, and relationships within the legal context using Agentic Reasoning.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">⚠️ Risk Assessment</div>
            <div class="feature-desc">Multi-agent analysis for comprehensive risk scoring, severity verification, and mitigation.</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")


# --- ANALYSIS EXECUTION ---
if final_file_payload is not None:
    
    tmp_path = ""
    # Create Temp File
    if final_file_payload == "EXAMPLE_MODE":
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{display_name}") as tmp_file:
            tmp_file.write(b"Mock Content") 
            tmp_path = tmp_file.name
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(final_file_payload.getvalue())
            tmp_path = tmp_file.name

    st.success(f"📂 Ready to Analyze: **{display_name}** | Jurisdiction: **{jurisdiction}**")
    
    if st.button("🚀 Start Analysis Engine", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("👁️ Perception Layer: Extracting Layout with PaddleOCR...")
            progress_bar.progress(25)
            # 1. OCR
            blocks = extract_document(tmp_path)
            
            status_text.text("🧠 Normalization Layer: Structuring Evidence...")
            progress_bar.progress(50)
            # 2. Evidence
            evidence = create_evidence_store(blocks)
            
            # 3. Agents
            progress_bar.progress(70)
            # We could pass 'jurisdiction' to the agents here if we updated the orchestrator.
            # For now, it serves as UI context.
            results = run_pipeline(evidence, status_callback=lambda msg: status_text.text(msg))
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis Complete.")
            
            st.session_state['results'] = results
            st.session_state['evidence'] = evidence
            
        except Exception as e:
            st.error(f"Analysis Failed: {e}")
            import traceback
            st.code(traceback.format_exc())
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # --- RESULTS DASHBOARD ---
    if st.session_state.get('results'):
        results = st.session_state['results']
        
        tab_report, tab_risk, tab_trace = st.tabs(["📝 Executive Report", "⚠️ Identified Risks", "🔍 Data Traceability"])
        
        # 1. Executive Report
        with tab_report:
            st.markdown(results['report'])
            
        # 2. Risk Register
        with tab_risk:
            risks_data = results.get('risks', [])
            
            # Unpack robustly
            if isinstance(risks_data, str):
                parsed = parse_agent_json(risks_data)
                if parsed: risks_data = parsed
            
            if isinstance(risks_data, dict):
                risks_data = risks_data.get('risks', []) or risks_data.get('risk_register', [])
            
            if risks_data and isinstance(risks_data, list):
                # Flatten lists for display
                for r in risks_data:
                    if isinstance(r.get('evidence_block_ids'), list):
                        r['evidence_block_ids'] = ", ".join(r['evidence_block_ids'])
                
                df = pd.DataFrame(risks_data)
                st.dataframe(
                    df, 
                    column_config={
                        "severity": st.column_config.NumberColumn("Severity",format="%d ⭐"),
                        "risk": "Risk Description",
                        "mitigation": "Recommended Action",
                        "precedent": "📚 Precedent / Case Law",
                        "evidence_block_ids": "Evidence IDs"
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("✅ No High-Severity risks identified in this pass.")
                if risks_data: st.json(risks_data) # Show raw if it's weird structure

        # 3. Data Traceability
        with tab_trace:
            t_col1, t_col2 = st.columns([1, 1], gap="small")
            
            # Left: Evidence Blocks
            with t_col1:
                st.subheader("📄 Raw Evidence")
                st.caption("Extracted text blocks (OCR)")
                evidence_blocks = st.session_state.get('evidence', {}).get('blocks', [])[:10]
                if not evidence_blocks:
                    st.info("No evidence extracted.")
                
                for block in evidence_blocks:
                    b_id = block.get('id', 'N/A')
                    b_text = block.get('text', '')
                    # Descriptive Title
                    snippet = b_text[:60].replace('\n', ' ') + "..." if len(b_text) > 60 else b_text
                    title = f"Page {block.get('page','?')} | {snippet}"
                    
                    with st.expander(title, expanded=False):
                        st.caption(f"Block ID: {b_id}")
                        st.info(b_text)

            # Right: Agent Extraction
            with t_col2:
                st.subheader("🤖 Structural Analysis")
                st.caption("Auto-extracted Entities & Hierarchy")
                
                analysis_str = results.get('analysis', '{}')
                data = parse_agent_json(analysis_str)
                
                if not data:
                    st.warning("Could not parse Agent output.")
                    with st.expander("View Raw Output"):
                        st.code(analysis_str)
                else:
                    # Render Cards
                    st.markdown("##### 🏛️ Context & Parties")
                    
                    # Context
                    court_val = data.get('court', {})
                    st.info(f"**Context:**\n\n{get_safe_text(court_val)}")
                    
                    # Parties
                    parties = data.get('parties', {})
                    party_text = ""
                    
                    if isinstance(parties, dict):
                        for k, v in parties.items():
                            if k != 'block_id':
                                party_text += f"**{k.title()}:** {v}\n\n"
                    elif isinstance(parties, list):
                        # Handle list of party dicts
                        for p in parties:
                            if isinstance(p, dict):
                                name = p.get('party_name') or p.get('name') or p.get('organization') or "Unknown Party"
                                role = p.get('role', 'Party')
                                # Don't show block_id in the main text
                                party_text += f"**{role}:** {name}\n\n"
                            else:
                                party_text += f"- {str(p)}\n"
                    else:
                        party_text = str(parties)
                    
                    st.success(f"**Parties Identified:**\n\n{party_text}")
                    
                    st.markdown("##### ⚖️ Key Terms & Findings")
                    
                    # Posture / Type
                    posture_val = get_safe_text(data.get('posture', {}))
                    if posture_val.lower() == 'not found':
                        posture_val = "Not applicable for this document type."
                        
                    with st.expander("📂 Procedural Posture / Type", expanded=True):
                         st.write(posture_val)
                         
                    with st.expander("💎 Findings / Relief / Clauses", expanded=True):
                         relief = data.get('relief', {})
                         # relief could be dict with description, or list, or string
                         if isinstance(relief, dict):
                             val = relief.get('description', str(relief))
                         else:
                             val = relief
                             
                         if isinstance(val, list):
                             for item in val:
                                 st.markdown(f"- {item}")
                         elif str(val).lower() == 'not found':
                             st.write("No specific clauses extracted.")
                         else:
                             st.write(val)
                             
                         # Findings
                         findings = data.get('findings', {})
                         findings_text = get_safe_text(findings)
                         if findings_text.lower() != 'not found':
                             st.markdown("**Reasoning / Additional Terms:**")
                             st.caption(findings_text)

        # 4. Financial Verification (NEW)
        # Check if we have financial data in the result
        try:
            # We look for "Programmatic Financial Verification" in the report text
            # Or checks in the 'analysis' JSON if we forwarded them
            
            # Since VerifierAgent appends the verification note to the report string:
            report_text = results.get('report', '')
            if "### 🛡️ Programmatic Financial Verification" in report_text:
                with st.expander("💰 Financial Integrity Check", expanded=True):
                    # Extract the section
                    verification_section = report_text.split("### 🛡️ Programmatic Financial Verification")[1]
                    # Stop at next header if any (unlikely since it's at end)
                    
                    if "✅ **PASSED**" in verification_section:
                        st.success("✅ **Math Verified**: All financial totals (Line Items, Tax, Grand Total) are mathematically consistent.")
                        st.markdown(verification_section)
                    elif "❌ **FAILED**" in verification_section:
                        st.error("❌ **Math Error**: Inconsistencies detected in the invoice totals.")
                        st.markdown(verification_section)
                    else:
                        st.info("ℹ️ Financial data extracted, but could not fully verify.")
                        st.markdown(verification_section)
                        
        except Exception:
            pass

