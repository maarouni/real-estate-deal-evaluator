
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(property_data, metrics, summary_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Real Estate Evaluator Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # AI Verdict
    elements.append(Paragraph("<b><font color='green'> AI Verdict</font></b>", styles["Heading3"]))
    elements.append(Paragraph(summary_text, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Property & Loan Inputs
    elements.append(Paragraph("<b>🏠 Property & Loan Inputs</b>", styles["Heading3"]))
    inputs_data = [[k, str(v)] for k, v in property_data.items()]
    table_inputs = Table(inputs_data, colWidths=[200, 300])
    table_inputs.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    elements.append(table_inputs)
    elements.append(Spacer(1, 12))

    # Investment Metrics
    elements.append(Paragraph("<b>📊 Investment Metrics</b>", styles["Heading3"]))

    metrics_cleaned = []
    for k, v in metrics.items():
        if isinstance(v, list):
            grouped = [", ".join(str(round(val, 2)) for val in v[i:i+5]) for i in range(0, len(v), 5)]
            wrapped = "<br/>".join(grouped)
            metrics_cleaned.append([k, Paragraph(wrapped, styles["Normal"])])
        elif isinstance(v, float):
            metrics_cleaned.append([k, round(v, 2)])
        else:
            metrics_cleaned.append([k, v])

    table_metrics = Table(metrics_cleaned, colWidths=[200, 350])  # wider cell
    table_metrics.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))
    elements.append(table_metrics)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Alias for import compatibility
generate_pdf_report = generate_pdf
