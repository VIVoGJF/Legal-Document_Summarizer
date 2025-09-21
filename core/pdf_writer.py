# core/pdf_writer.py
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def save_json_to_pdf(json_str: str, filename: str = "legal_analysis.pdf"):
    
    try:
        data = json.loads(json_str)
    except Exception:
        data = {"raw_output": json_str}

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    flow = [Paragraph("AI Legal Document Analysis", styles["Title"]), Spacer(1, 20)]

    for key, value in data.items():
        flow.append(Paragraph(f"<b>{key.title()}:</b>", styles["Heading3"]))
        flow.append(Spacer(1, 6))
        flow.append(Paragraph(str(value), styles["Normal"]))
        flow.append(Spacer(1, 12))

    doc.build(flow)
    print(f"[PDF Saved] {filename}")
