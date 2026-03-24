from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(content: str):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    for line in content.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)

    buffer.seek(0)
    return buffer
from docx import Document

def generate_docx(content: str):
    buffer = BytesIO()

    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)

    doc.save(buffer)
    buffer.seek(0)

    return buffer