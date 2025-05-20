import streamlit as st
from modules.Generator import generate_resume, generate_cover_letter
import os

# Load OpenAI API Key securely
openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("Job Application Generator")

# User Type Selection (Free or Premium)
user_type = st.radio("Select User Type", ["Free (GPT-3.5)", "Premium (GPT-4)"])
is_premium = user_type == "Premium (GPT-4)"

# User Inputs
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

# Generate Resume
if st.button("Generate Resume"):
    if not openai_api_key:
        st.error("OpenAI API Key is missing. Set it as an environment variable.")
    else:
        resume_text = generate_resume(openai_api_key, name, email, skills, experience, is_premium=is_premium)
        st.text_area("Generated Resume", resume_text, height=300)
        st.download_button("Download Resume", resume_text, file_name="Resume.txt")

# Generate Cover Letter
if st.button("Generate Cover Letter"):
    if not openai_api_key:
        st.error("OpenAI API Key is missing. Set it as an environment variable.")
    else:
        cover_letter_text = generate_cover_letter(openai_api_key, name, job_title, company, job_description, is_premium=is_premium)
        st.text_area("Generated Cover Letter", cover_letter_text, height=300)
        st.download_button("Download Cover Letter", cover_letter_text, file_name="Cover_Letter.txt")
