import docx
import PyPDF2

async def extract_text(file):
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        return " ".join([page.extract_text() for page in reader.pages])

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""