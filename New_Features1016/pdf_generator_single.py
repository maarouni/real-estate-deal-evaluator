
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_pdf(metrics, address="", zip_code=""):
    doc = SimpleDocTemplate("real_estate_single_report.pdf")
    styles = getSampleStyleSheet()
    flowables = []

    flowables.append(Paragraph("🏡 Real Estate Deal Summary", styles['Title']))
    if address:
        flowables.append(Paragraph(f"<b>Address:</b> {address}", styles["Normal"]))
    if zip_code:
        flowables.append(Paragraph(f"<b>ZIP Code:</b> {zip_code}", styles["Normal"]))
    flowables.append(Spacer(1, 12))

    for key, value in metrics.items():
        flowables.append(Paragraph(f"<b>{key}:</b> {value}", styles["Normal"]))
        flowables.append(Spacer(1, 6))

    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Italic"]))

    doc.build(flowables)
