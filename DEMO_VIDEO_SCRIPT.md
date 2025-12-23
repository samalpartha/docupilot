# 🎥 DocuPilot Demo Video Script

**Duration**: ~3 Minutes
**Goal**: Demonstrate "Agentic Document Intelligence" (Multi-Agent, Verified, Traceable).

---

## 0:00 - 0:20: The "Hook" (Face to Camera)
> "Legal teams waste 40% of their time manually reviewing agreements. But traditional OCR fails on complex layouts, and standard LLMs hallucinate."
> "That's why we built **DocuPilot**. It's a **Multimodal Agentic System** powered by **Baidu AI Studio** that bridges Computer Vision and Reasoning."

## 0:20 - 0:40: The Dashboard (Screen Share)
*   **Action**: Show `https://docu-pilot.streamlit.app/` (Live Demo).
*   **Visual**: Point to the Sidebar.
> "Here is the DocuPilot Command Center. We verify against specific jurisdictions—like California or New York—because a risk in NY might be fine in CA."
*   **Action**: Select **"California"** in the sidebar.

## 0:40 - 1:30: Multimodal Ingestion (The "Magic")
*   **Action**: Click **"🔒 NDA (Confidentiality)"** under Quick Start (or Upload a PDF).
*   **Visual**: Watch the Progress Bar & Status Text.
> "Watch what happens. This is a true **Multimodal Pipeline**:"
> 1.  "First, **PaddleOCR** serves as our 'Eyes', extracting the physical layout and visual structure."
> 2.  "Then, we stream this visual context to **ERNIE-4.0** (via **Baidu AI Studio**), our reasoning engine."
> 3.  "The **Analyst Agent** extracts structured facts, while the **Risk Agent** audits the contract."

## 1:30 - 2:10: Trust & Traceability
*   **Action**: Click the **"🔍 Data Traceability"** Tab.
*   **Visual**: Show "Raw Evidence" (Left) vs "Structural Analysis" (Right).
> "This is the Trust Layer. On the left, you see the Raw OCR blocks. On the right, the Structured Data extracted by our Agents."
> "Notice how it correctly identified the **Parties** and the **Clauses**. If the Agent hallucinated, you'd see the mismatch right here."

## 2:10 - 2:40: The Risk Register (Value Prop)
*   **Action**: Click **"⚠️ Identified Risks"** Tab.
*   **Visual**: Show the Risk Table with "High" Severity rows.
> "And here is the money shot. The Risk Register. The Agent found a **'Unilateral Termination Clause'** and flagged it as **High Severity**."
> "It cites the **Precise Evidence ID**, so a lawyer can click and verify instantly."

## 2:40 - 3:00: The Executive Summary (Closing)
*   **Action**: Click **"📝 Executive Report"** Tab.
> "Finally, the **Summarizer Agent** writes a clean executive brief for the partner."
> "DocuPilot transforms hours of reading into seconds of Verified Review. Thank you."
