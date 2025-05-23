import streamlit as st
from core.ui.auth_header import auth_header
auth_header()
import os
from dotenv import load_dotenv
import openai
import re
from core.utils.state import init_session_state
from core.coach import show_tip
from core.match import compare_resume_to_job
from core.utils.storage import persistent_input, persistent_textarea, load_profile, save_profile
load_profile()
from core.ui.resume_cover import (
    resume_section,
    render_resume_output,
    cover_letter_section,
    render_cover_letter_output
)

# --- Persistent Input Functions ---
def persistent_input(label, key, default=""):
    value = st.text_input(label, key=key, value=st.session_state.get(key, default))
    if st.session_state.get(key) != value:
        st.session_state[key] = value
        save_profile()
    return value

def persistent_textarea(label, key, default=""):
    value = st.text_area(label, key=key, value=st.session_state.get(key, default))
    if st.session_state.get(key) != value:
        st.session_state[key] = value
        save_profile()
    return value



# --- Config & Setup ---
st.set_page_config(page_title="JobAppGen – Resume & Cover", layout="wide")
load_dotenv()
init_session_state()
if "applications" not in st.session_state:
    st.session_state.applications = []

# --- API & Model Setup ---
openai_api_key = os.getenv("OPENAI_API_KEY")
premium_model = os.getenv("PREMIUM_MODEL", "gpt-4")
free_model = os.getenv("FREE_MODEL", "gpt-3.5-turbo")
use_placeholder = os.getenv("USE_PLACEHOLDER", "false").lower() == "true"
client = openai.OpenAI(api_key=openai_api_key) if not use_placeholder else None

if use_placeholder:
    st.warning("⚠️ Placeholder Mode is ACTIVE — no real API calls are being made.")

# --- Sidebar ---
def sidebar_inputs():
    with st.sidebar:
        st.header("User Information")
        name = persistent_input("Your Name", "name_input")
        email = persistent_input("Your Email", "email_input")
        skills = persistent_textarea("Top Skills (comma-separated)", "skills_input")
        experience = persistent_textarea("Your Work Experience", "experience_input")

        st.header("Job Details")
        job_title = persistent_input("Job Title", "job_title_input")
        company = persistent_input("Company Name", "company_input")
        job_description = persistent_textarea("Job Description", "job_description_input")

        user_type = st.radio("Select User Type", ["Free (GPT-3.5)", "Premium (GPT-4)"], key="user_type")

        if st.button("🧹 Clear Resume & Cover Letter"):
            st.session_state.pop("resume", None)
            st.session_state.pop("cover_letter", None)
            st.toast("Cleared!")
            
    return name, email, skills, experience, job_title, company, job_description, user_type

# 🧠 Get inputs once
name, email, skills, experience, job_title, company, job_description, user_type = sidebar_inputs()
model = premium_model if user_type == "Premium (GPT-4)" else free_model

# --- Resume ---
st.header("📄 Resume Generator")
resume_section(name, email, skills, experience, job_title, company, model, client, openai_api_key, use_placeholder)

if "resume" in st.session_state:
    render_resume_output()

# --- Cover Letter ---
st.header("✉️ Cover Letter Generator")
cover_letter_section(name, job_title, company, job_description, model, client, openai_api_key, use_placeholder)

if "cover_letter" in st.session_state:
    render_cover_letter_output()

# --- Resume Match ---
st.header("🧠 Resume Match Scorer")
show_tip("job_description")
jd_input = st.text_area("Paste Job Description")

if st.button("🔍 Score My Resume"):
    if "resume" not in st.session_state:
        st.warning("⚠️ Generate your resume first.")
    elif not jd_input:
        st.warning("⚠️ Please paste a job description.")
    else:
        with st.spinner("Comparing your resume to the job..."):
            try:
                comparison = compare_resume_to_job(openai_api_key, st.session_state.resume, jd_input, model, use_placeholder, client)
                st.markdown(comparison)
                match = re.search(r"(\d{1,3})/100", comparison)
                if match:
                    st.progress(int(match.group(1)))
            except Exception as e:
                st.error(f"❌ An error occurred during comparison: {e}")
