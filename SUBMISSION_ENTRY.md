## Inspiration

In today's business environment, legal errors cost billions. Lawyers spend 60% of their time manually reviewing complex layouts—tables, headers, and clauses—where standard OCR fails. We built **DocuPilot** to solve this "Last Mile" problem of Legal AI: bridging the gap between Visual Understanding (Layouts) and Logical Reasoning (Risks) using **ERNIE-4.0** and **Baidu AI Studio**.

## What it does

DocuPilot is a **Multimodal Agentic System** that:
- **👀 Sees Structure**: Uses **PaddleOCR** to extract not just text, but visual layout (headers, tables, signatures).
- **🧠 Reasons Verification**: Streams this visual context to **ERNIE-4.0 (via Baidu AI Studio)**.
- **🕵️ Check & Verify**: A multi-agent team (Ingestion, Analyst, Risk, Verifier) cross-checks every finding against the raw evidence.
- **📝 Delivers Reports**: Generates a verified Executive Summary and Risk Register via a polished **Streamlit Dashboard**.

## How we built it

**Technology Stack:**
- **AI/LLM**: **ERNIE-4.0** (via **Baidu AI Studio API**) for high-fidelity reasoning.
- **Computer Vision**: **PaddleOCR** for layout analysis and text extraction.
- **Frontend**: **Streamlit** for a premium, responsive User Interface.
- **Architecture**: Custom **Multi-Agent Orchestrator** (Python/LangChain) for verifiable workflows.

**Multimodal Pipeline:**
1.  **Visual Ingestion**: PDF is rendered and processed by PaddleOCR.
2.  **Structural Normalization**: ERNIE cleans OCR noise and reconstructs the document hierarchy.
3.  **Agentic Analysis**: Specialized agents (Risk, Analyst) query the structured data.
4.  **Evidence Verification**: A dedicated "Verifier Agent" checks every AI claim against the raw OCR blocks to prevent hallucinations.

## Challenges we ran into

- **Hallucinations**: Early models would invent risks. We solved this by adding a "Verifier Agent" that strictly audits every claim against raw evidence.
- **Complex Layouts**: Legal docs have weird formatting. PaddleOCR was crucial for preserving the "reading order" that standard text extractors miss.
- **Dependency Hell**: optimizing the build for the Cloud. We heavily optimized `requirements.txt` to run PaddleOCR on CPU-only instances.

## Accomplishments that we're proud of

- 🏆 **Built a "Verifiable" AI**: It doesn't just guess; it cites the evidence Block ID.
- 🚀 **Full End-to-End UI**: Deployed a production-ready Streamlit app, not just a script.
- 🔄 **Multimodal Integration**: Successfully linked Visual Perception (Paddle) with Semantic Reasoning (ERNIE).

## What we learned

- **Perception is Key**: You can't reason about a contract if you can't "see" the table structure. PaddleOCR + ERNIE is a killer combo.
- **Agents need Managers**: A single LLM fails. A team of specialized Agents (Analyst vs. Risk) succeeds.

## What's next for DocuPilot

- **Multi-Document Concurrency**: Analyzing entire data rooms at once.
- **Visual Q&A**: "Where do I sign?" (Pointing to the image coordinates).
- **Enterprise Integration**: Connecting directly to SharePoint/Clio.
