import streamlit as st
from modules.Generator import generate_resume, generate_cover_letter
import os
from dotenv import load_dotenv
from fpdf import FPDF
from docx import Document
import io

# --- Export Functions ---
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

# --- Load .env and OpenAI Settings ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
premium_model = os.getenv("PREMIUM_MODEL", "gpt-4")
free_model = os.getenv("FREE_MODEL", "gpt-3.5-turbo")
use_placeholder = os.getenv("USE_PLACEHOLDER", "false").lower() == "true"

# --- UI ---
st.title("Job Application Generator")
if use_placeholder:
    st.warning("⚠️ Placeholder Mode is ACTIVE — no real API calls are being made.")

user_type = st.radio("Select User Type", ["Free (GPT-3.5)", "Premium (GPT-4)"])
model = premium_model if user_type == "Premium (GPT-4)" else free_model

# --- Sidebar Inputs ---
st.sidebar.header("User Information")
name = st.sidebar.text_input("Your Name")
email = st.sidebar.text_input("Your Email")
skills = st.sidebar.text_area("Your Skills (comma-separated)")
experience = st.sidebar.text_area("Your Work Experience")

st.sidebar.header("Job Details")
job_title = st.sidebar.text_input("Job Title")
company = st.sidebar.text_input("Company Name")
job_description = st.sidebar.text_area("Job Description")

st.header("Resume and Cover Letter Generator")

# --- Resume ---
if name and email and skills and experience:
    if st.button("Generate Resume"):
        if not openai_api_key and not use_placeholder:
            st.error("OpenAI API Key is missing. Set it as an environment variable.")
        else:
            with st.spinner("Generating your resume..."):
                resume_text = generate_resume(openai_api_key, name, email, skills, experience, model)
                st.session_state.resume = resume_text

# --- Resume Output ---
if "resume" in st.session_state:
    if st.checkbox("Show Resume as plain text"):
        st.text_area("Generated Resume", st.session_state.resume, height=300)
    else:
        st.markdown(f"```markdown\n{st.session_state.resume}\n```")

    st.download_button("Download Resume (TXT)", st.session_state.resume, file_name="Resume.txt")
    st.download_button("Download Resume (PDF)", export_as_pdf(st.session_state.resume), file_name="Resume.pdf")
    st.download_button("Download Resume (Word)", export_as_docx(st.session_state.resume), file_name="Resume.docx")

# --- Cover Letter ---
if name and job_title and company and job_description:
    if st.button("Generate Cover Letter"):
        if not openai_api_key and not use_placeholder:
            st.error("OpenAI API Key is missing. Set it as an environment variable.")
        else:
            with st.spinner("Generating your cover letter..."):
                cover_letter_text = generate_cover_letter(openai_api_key, name, job_title, company, job_description, model)
                st.session_state.cover_letter = cover_letter_text

# --- Cover Letter Output ---
if "cover_letter" in st.session_state:
    st.text_area("Generated Cover Letter", st.session_state.cover_letter, height=300)
    st.download_button("Download Cover Letter (TXT)", st.session_state.cover_letter, file_name="Cover_Letter.txt")
    st.download_button("Download Cover Letter (PDF)", export_as_pdf(st.session_state.cover_letter), file_name="Cover_Letter.pdf")
    st.download_button("Download Cover Letter (Word)", export_as_docx(st.session_state.cover_letter), file_name="Cover_Letter.docx")
