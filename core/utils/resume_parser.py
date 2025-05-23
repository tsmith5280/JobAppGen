import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def basic_resume_parse(text):
    # SUPER basic placeholder logic – just to demo structure
    lines = text.splitlines()
    parsed = {
        "full_name": lines[0] if lines else "",
        "job_title": "Data Scientist",
        "skills": ["Python", "SQL", "Machine Learning"],
        "experience": "3+ years in analytics and modeling."
    }
    return parsed
