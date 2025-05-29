from docx import Document
import fitz  # PyMuPDF
import re

def extract_text_from_docx(file):
    try:
        document = Document(file)
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e:
        print("DOCX Parse Error:", e)
        return ""

def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        print("EXTRACTED TEXT PREVIEW:", text[:500])  # Debug
        return text
    except Exception as e:
        print("PDF Parse Error:", e)
        return ""

def extract_job_title(text):
    titles = ["Data Scientist", "Software Engineer", "Teacher", "Surveyor", "Analyst", "Developer", "Engineer"]
    for title in titles:
        if re.search(rf"\b{re.escape(title)}\b", text, re.IGNORECASE):
            return title
    return "Unknown"

def basic_resume_parse(text):
    lines = text.splitlines()

    # Expand the skill pool later as needed
    skills_pool = [
        "python", "sql", "javascript", "typescript", "excel", "pandas", "numpy", 
        "machine learning", "data analysis", "data cleaning", "deep learning", "aws", "power bi"
    ]
    detected_skills = [s for s in skills_pool if s.lower() in text.lower()]

    return {
        "full_name": lines[0] if lines else "",
        "job_title": extract_job_title(text),
        "skills": detected_skills,
        "experience": "\n".join([line for line in lines if "experience" in line.lower()])
    }

def parse_resume_file(file):
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file.file)
    else:
        return {"error": "Unsupported file type"}

    return basic_resume_parse(text)
