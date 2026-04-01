from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf(data):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("TrustCheck AI Compliance Report", styles["Title"]))
    content.append(Spacer(1, 10))

    # ✅ Summary
    total = len(data)
    mismatches = sum(1 for d in data if d["status"] == "mismatch")
    verified = sum(1 for d in data if d["status"] == "verified")

    summary_text = f"""
    <b>Total Questions:</b> {total}<br/>
    <b>Verified:</b> {verified}<br/>
    <b>Mismatches:</b> {mismatches}<br/><br/>
    """
    content.append(Paragraph(summary_text, styles["Normal"]))
    content.append(Spacer(1, 10))

    # ✅ Each Question
    for item in data:
        # Color based on status
        if item["status"] == "mismatch":
            color = "red"
        else:
            color = "green"

        text = f"""
        <b>Question:</b> {item['question']}<br/>
        <b>Answer:</b> {item['answer']}<br/>
        <b>Status:</b> <font color="{color}">{item['status']}</font><br/>
        <b>Explanation:</b> {item['explanation']}<br/><br/>
        """

        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    return "report.pdf"