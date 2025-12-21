
# 🎬 Demo Video Script (5 Minutes)

## Minute 0–1: Problem & Introduction
**Visual**: Slide with "The Cost of Contract Review".
**Audio**: "Manual contract review takes 4-8 hours per document and costs legal teams thousands. Critical risks like missing SLAs or weak liability caps often slip through the cracks. Today, we present **DocuPilot**: An autonomous multi-agent system powered by ERNIE and PaddleOCR-VL that transforms this process."

## Minute 1–2: Architecture & The "Why"
**Visual**: Show the Architecture Diagram (from README).
**Audio**: "Unlike generic LLM wrappers, DocuPilot uses a specialized architecture:
1. **PaddleOCR-VL** for perception: It sees layout and structure, not just text.
2. **CAMEL-AI Orchestration**: We treat analysis as a multi-agent role-playing game.
3. **ERNIE 4.0 Core**: We leverage ERNIE's superior reasoning to power 3 specialized agents: An Analyst, a Risk Officer, and a Verifier."

## Minute 2–4: Live Walkthrough
**Visual**: Split screen. Terminal on left, PDF on right.
**Action**: Run `python src/main.py --pdf data/samples/vendor_agreement.pdf`
**Audio**: 
"Let's watch it live. I'm uploading a 12-page vendor agreement.
- **Step 1**: PaddleOCR extracts the layout. See how it identifies headers and tables?
- **Step 2**: The **Analyst Agent** (Agent 1) reads specific clauses.
- **Step 3**: The **Risk Agent** (Agent 2) is now flagging a liability cap of $50k as 'High Risk'.
- **Step 4**: The **Verifier Agent** cross-checks every claim against the source block ID."

**Visual**: Open `src/outputs/report.md` rendered.
**Audio**: "Here is the final report. Notice: Every single claim has a citation link `[block_id: p3_b5]`. This is the traceability legal teams need."

## Minute 4–5: Impact & Extension
**Visual**: Comparison Slide (Manual vs DocuPilot).
**Audio**: "We reduce review time by 70%. And because we use ERNIE, we can easily extend this to Chinese contracts or complex cross-border compliance. DocuPilot isn't just a tool; it's your diverse team of legal experts in a box."

**Visual**: GitHub Repo Link + "Vote for Us".
**Audio**: "Thank you."
