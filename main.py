import streamlit as st
from modules.generator import generate_resume, generate_cover_letter
from modules.match import compare_resume_to_job
from modules.export import export_as_pdf, export_as_docx
# from modules.tracker import load_applications, save_applications_to_csv (if used)
import os
from dotenv import load_dotenv
import openai
import pandas as pd

st.header("📋 Job Application Tracker")
st.set_page_config(page_title="JobAppGen", layout="wide")


if "applications" not in st.session_state:
    st.session_state.applications = []

with st.form("application_form"):
    col1, col2 = st.columns(2)
    with col1:
        applied_job_title = st.text_input("Job Title")
        company_applied = st.text_input("Company")
    with col2:
        date_applied = st.date_input("Date Applied")
        status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])

    notes = st.text_area("Notes or Contact Info")

    submitted = st.form_submit_button("➕ Add Application")
    if submitted:
        new_app = {
            "Job Title": applied_job_title,
            "Company": company_applied,
            "Date Applied": str(date_applied),
            "Status": status,
            "Notes": notes
        }
        st.session_state.applications.append(new_app)
        st.success("✅ Application added!")

if st.session_state.applications:
    df = pd.DataFrame(st.session_state.applications)
    st.dataframe(df, use_container_width=True)

# --- Load .env and OpenAI Settings ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
premium_model = os.getenv("PREMIUM_MODEL", "gpt-4")
free_model = os.getenv("FREE_MODEL", "gpt-3.5-turbo")
use_placeholder = os.getenv("USE_PLACEHOLDER", "false").lower() == "true"
client = openai.OpenAI(api_key=openai_api_key) if not use_placeholder else None
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
                resume_text = generate_resume(openai_api_key, name, email, skills, experience, model, use_placeholder, client)
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
st.header("🧠 Resume Match Scorer")

jd_input = st.text_area("Paste Job Description")
if st.button("🔍 Score My Resume"):
    if "resume" not in st.session_state:
        st.warning("⚠️ Generate your resume first.")
    elif not jd_input:
        st.warning("⚠️ Please paste a job description.")
    else:
        with st.spinner("Comparing your resume to the job..."):
            comparison = compare_resume_to_job(openai_api_key, st.session_state.resume, jd_input, model, use_placeholder, client)
            st.markdown(comparison)

# --- Cover Letter ---
if name and job_title and company and job_description:
    if st.button("Generate Cover Letter"):
        if not openai_api_key and not use_placeholder:
            st.error("OpenAI API Key is missing. Set it as an environment variable.")
        else:
            with st.spinner("Generating your cover letter..."):
                cover_letter_text = generate_cover_letter(openai_api_key, name, job_title, company, job_description, model, use_placeholder, client)
                st.session_state.cover_letter = cover_letter_text

# --- Cover Letter Output ---
if "cover_letter" in st.session_state:
    st.text_area("Generated Cover Letter", st.session_state.cover_letter, height=300)
    st.download_button("Download Cover Letter (TXT)", st.session_state.cover_letter, file_name="Cover_Letter.txt")
    st.download_button("Download Cover Letter (PDF)", export_as_pdf(st.session_state.cover_letter), file_name="Cover_Letter.pdf")
    st.download_button("Download Cover Letter (Word)", export_as_docx(st.session_state.cover_letter), file_name="Cover_Letter.docx")
