# 🎥 DocuPilot Demo Video Script

**Duration**: ~3 Minutes
**Goal**: Demonstrate "Agentic Document Intelligence" (Multi-Agent, Verified, Traceable).

---

## 0:00 - 0:20: The "Hook" (Face to Camera)
> "Legal teams waste 40% of their time manually reviewing agreements for basic risks. Generative AI helps, but lawyers don't trust it because it hallucinates."
> "That's why we built **DocuPilot**. It's not a chatbot. It's a **Verified Multi-Agent Risk Engine** that links every finding back to the raw evidence."

## 0:20 - 0:40: The Dashboard (Screen Share)
*   **Action**: Show `localhost:8501` (or your Cloud URL).
*   **Visual**: Point to the Sidebar.
> "Here is the DocuPilot Command Center. We verify against specific jurisdictions—like California or New York—because a risk in NY might be fine in CA."
*   **Action**: Select **"California"** in the sidebar.

## 0:40 - 1:30: Real-Time Ingestion (The "Magic")
*   **Action**: Click **"🔒 NDA (Confidentiality)"** under Quick Start (or Upload a PDF).
*   **Visual**: Watch the Progress Bar & Status Text.
> "Watch what happens. We don't just dump text into GPT. We run a multi-stage pipeline:"
> 1.  "First, **PaddleOCR** (our Perception Layer) extracts the physical layout."
> 2.  "Then, the **Ingestion Agent** cleans the OCR noise."
> 3.  "Next, the **Analyst Agent** extracts structured facts—Parties, Dates, Obligations."
> 4.  "Finally, the **Risk Agent** audits the contract."

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
