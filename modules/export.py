from fpdf import FPDF
from docx import Document
import io

def export_as_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer

def export_as_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def export_as_txt(text):
    return io.BytesIO(text.encode("utf-8"))
