# 🏆 Winning Demo Script: DocuPilot

**Goal:** Show Judges this is a "Product", not a "Script".
**Focus:** Visuals (UI), Reliability (Green Tests), and Real Tech (PaddleOCR).

---

## 0:00 - 0:30 🎣 The Problem (Camera)
"Lawyers spend 60% of their time just checking if a contract has the right clauses. It's boring, expensive, and if they miss one thing, it's a malpractice suit."

"Generative AI should help, but lawyers don't trust it. It hallucinates. It makes things up."

"That's why we built **DocuPilot**. It's not a chatbot. It's a **Verified Risk Engine**."

---

## 0:30 - 1:15 🚀 The Dashboard (Screen Share)
**Visual:** Show `localhost:8501`.
*Point out the polished Sidebar, the Jurisdiction Selector.*

**Action:**
1.  Select **"California"** in the Jurisdiction Dropdown.
    *   *Say:* "Notice we set the context. DocuPilot adapts its risk scoring based on the governing law."
2.  Click **"🏛️ Court Order (NY)"** button.
    *   *Say:* "Let's ingest a complex Court Order. In the background, **PaddleOCR** extracts the physical layout, feeding our **ERNIE 4.0** agents."

**Action:**
3.  Show the **"Data Traceability"** Tab.
    *   *Say:* "This is what wins trust. We don't just give you text; we give you the **Evidence**. On the right, clean structured data. On the left, the raw perceived text."
    *   *Point out:* The standard formatting (e.g. "**Context:** United States District Court").

---

## 1:15 - 2:00 🕵️‍♀️ The "No-Hallucinations" Logic
**Visual:** Switch to **"Executive Report"** tab.

**Action:**
1.  Scroll to the **"Risk Register"**.
2.  *Say:* "Here is the magic. The **Analyst Agent** found the risk. But the **Verifier Agent** audited it. If the evidence didn't exist, this row wouldn't be here."

**Visual:** Switch to **"Identified Risks"** tab.
1.  Show the table.
2.  *Say:* "High severity items are flagged instantly. This turns 4 hours of reading into 30 seconds of review."

---

## 2:00 - 2:45 ⚡ Real-Time Factors (The "Wow" Moment)
**Visual:** Go to **"Paste URL"** tab.

**Action:**
1.  Paste a link to a PDF (sample provided below, or use your own).
    *   *Sample:* `https://www.uscourts.gov/sites/default/files/ao088.pdf` (or any public PDF).
2.  Click **"Fetch Document"**.
3.  *Say:* "It works on the fly. We're fetching the binary stream, running OCR locally, and piping it to the agents in real-time."

---

## 2:45 - 3:00 🛡️ Reliability (The Closer)
**Visual:** Show VS Code terminal with green test results (`pytest tests/`).

**Action:**
1.  Flash the terminal log showing **100% Passing**.
2.  *Say:* "And we didn't just hack this together. We built a production-grade test suite covering OCR fallback and Agent Logic. It's robust, it's verified, and it's ready for the firm."

**"Thank You."**
