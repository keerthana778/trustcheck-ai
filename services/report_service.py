from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("TrustCheck AI Compliance Report", styles["Title"]))
    content.append(Spacer(1, 12))

    for item in data:
        color = "red" if item["status"] == "mismatch" else "green"
        text = f"<b>Q:</b> {item['question']}<br/><b>Status:</b> <font color='{color}'>{item['status']}</font><br/><b>Note:</b> {item['explanation']}<br/><br/>"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)
    return "report.pdf"