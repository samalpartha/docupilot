
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

def create_court_order_pdf(filename):
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    
    # 1. Header / Caption
    c.setFont("Times-Bold", 12)
    c.drawCentredString(width/2, height - 50, "UNITED STATES DISTRICT COURT")
    c.drawCentredString(width/2, height - 65, "SOUTHERN DISTRICT OF NEW YORK")
    
    # Box for parties
    c.rect(50, height - 200, 250, 120)
    c.setFont("Times-Roman", 11)
    c.drawString(60, height - 100, "ACME CORP.,")
    c.drawString(150, height - 115, "Plaintiff,")
    c.drawString(60, height - 140, "v.")
    c.drawString(60, height - 160, "TECHVENDOR INC.,")
    c.drawString(150, height - 175, "Defendant.")
    
    # Case Number
    c.drawString(320, height - 100, "Civil Action No. 24-CV-12345 (JSD)")
    
    # Title
    c.setFont("Times-Bold", 14)
    c.drawCentredString(width/2, height - 240, "ORDER GRANTING MOTION FOR SUMMARY JUDGMENT")
    
    # Body Text
    text_start_y = height - 280
    line_height = 16
    c.setFont("Times-Roman", 12)
    
    paragraphs = [
        "J. DOE, District Judge:",
        "",
        "This matter comes before the Court on Plaintiff Acme Corp.'s Motion for Summary Judgment.",
        "The Court having reviewed the pleadings, affidavits, and exhibits, finds as follows:",
        "",
        "1. FINDINGS OF FACT",
        "The Court finds that on January 1, 2024, Defendant failed to deliver the software",
        "modules as required by the Master Services Agreement (MSA), Section 4.2.",
        "Defendant's argument that the delay was due to 'Force Majeure' is rejected as the",
        "server outage cited does not meet the contractual definition in Clause 12.",
        "",
        "2. CONCLUSIONS OF LAW",
        "Under New York Law, a material breach of a time-is-of-the-essence clause entitles",
        "the non-breaching party to immediate termination. The liability cap of $50,000",
        "asserted by Defendant is found to be unenforceable due to gross negligence found",
        "in the handling of customer data.",
        "",
        "3. ORDER",
        "It is hereby ORDERED AND ADJUDGED that:",
        "   A. Plaintiff's Motion for Summary Judgment is GRANTED.",
        "   B. Defendant shall pay damages in the amount of $450,000 within 30 days.",
        "   C. Failure to comply may result in further sanctions.",
        "   D. This case is DISMISSED WITH PREJUDICE.",
        "",
        "SO ORDERED.",
        "Dated: December 21, 2025",
        "New York, New York"
    ]
    
    y = text_start_y
    for line in paragraphs:
        c.drawString(72, y, line)
        y -= line_height
        
    c.save()
    print("Created " + filename)

if __name__ == "__main__":
    os.makedirs("data/samples", exist_ok=True)
    create_court_order_pdf("data/samples/court_order.pdf")
