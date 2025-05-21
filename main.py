import streamlit as st
st.set_page_config(page_title="JobAppGen", layout="wide")
ai_enabled = st.sidebar.checkbox("💬 Enable AI Coach", key="ai_coach_enabled")
from modules.generator import generate_resume, generate_cover_letter
from modules.match import compare_resume_to_job
from modules.export import export_as_pdf, export_as_docx
from modules.tracker import load_applications
import os
from dotenv import load_dotenv
import openai
import pandas as pd
import re
import uuid
from collections import defaultdict  
from modules.coach import is_coach_enabled, show_tip
from modules.coach_chat import run_ai_coach_chat
CSV_FILE = "job_applications.csv"
import streamlit.components.v1 as components

# --- Load .env and OpenAI Settings ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
premium_model = os.getenv("PREMIUM_MODEL", "gpt-4")
free_model = os.getenv("FREE_MODEL", "gpt-3.5-turbo")
use_placeholder = os.getenv("USE_PLACEHOLDER", "false").lower() == "true"
client = openai.OpenAI(api_key=openai_api_key) if not use_placeholder else None
if not st.session_state.get("coach_prompted"):
    show_tip("first_time")
    st.session_state.coach_prompted = True
if use_placeholder:
    st.warning("⚠️ Placeholder Mode is ACTIVE — no real API calls are being made.")

# Move user_type/model selection here so 'model' is defined before use
user_type = st.radio("Select User Type", ["Free (GPT-3.5)", "Premium (GPT-4)"])
model = premium_model if user_type == "Premium (GPT-4)" else free_model
if ai_enabled:
    if "ai_coach_ran_once" not in st.session_state:
        st.session_state.ai_coach_ran_once = True
        st.rerun()


if st.session_state.get("ai_coach_enabled"):
    components.html(
        open("chat_popup.html", "r").read(),
        height=500,
        width=350
    )
    
    components.html(
        open("chat_popup.html", "r").read(),
        height=450,
        width=350
    )

# --- Application Tracker ---
with st.expander("📋 Job Application Tracker", expanded=True):
    # Ensure applications list exists in session
    if "applications" not in st.session_state:
        st.session_state.applications = load_applications()

    # 🩹 PATCH: Ensure each application has a UUID
    for app in st.session_state.applications:
        if "ID" not in app:
            app["ID"] = str(uuid.uuid4())

    def save_applications(applications):
        columns = ["ID", "Job Title", "Company", "Date Applied", "Status", "Notes"]
        df = pd.DataFrame(applications, columns=columns)
        df.to_csv(CSV_FILE, index=False)

    # --- Form to Add New Application ---
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
        if submitted and applied_job_title and company_applied:
            new_app = {
                "ID": str(uuid.uuid4()),
                "Job Title": applied_job_title,
                "Company": company_applied,
                "Date Applied": str(date_applied),
                "Status": status,
                "Notes": notes
            }
            st.session_state.applications.append(new_app)
            save_applications(st.session_state.applications)
            st.success("✅ Application added!")
        elif submitted:
            st.warning("⚠️ Please enter both a job title and company.")

    # --- Group Applications by Month-Year ---
    grouped_apps = defaultdict(list)
    for app in st.session_state.applications:
        try:
            month_year = pd.to_datetime(app["Date Applied"]).strftime('%B %Y')
        except Exception:
            month_year = "Unknown Date"
        grouped_apps[month_year].append(app)

    # --- Display Grouped Applications ---
    for date in sorted(grouped_apps.keys(), reverse=True):
        st.subheader(f"📅 Applications for {date} ({len(grouped_apps[date])})")
        for app in grouped_apps[date]:
            with st.expander(f"📝 {app['Job Title']} at {app['Company']} — {app['Status']}", expanded=False):
                edited_title = st.text_input("Edit Job Title", value=app["Job Title"], key=f"title_{app['ID']}")
                edited_status = st.selectbox(
                    "Edit Status", ["Applied", "Interview", "Rejected", "Offer"],
                    index=["Applied", "Interview", "Rejected", "Offer"].index(app["Status"]),
                    key=f"status_{app['ID']}"
                )
                edited_notes = st.text_area("Edit Notes", value=app["Notes"], key=f"notes_{app['ID']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Changes", key=f"save_{app['ID']}"):
                        for real_app in st.session_state.applications:
                            if real_app["ID"] == app["ID"]:
                                real_app["Job Title"] = edited_title
                                real_app["Status"] = edited_status
                                real_app["Notes"] = edited_notes
                                break
                        save_applications(st.session_state.applications)
                        st.success("✅ Changes saved.")
                        st.rerun()

                with col2:
                    if st.button("❌ Delete", key=f"delete_{app['ID']}"):
                        st.session_state.applications = [
                            a for a in st.session_state.applications if a["ID"] != app["ID"]
                        ]
                        save_applications(st.session_state.applications)
                        st.warning("🗑️ Application deleted.")
                        st.rerun()


    # --- Download Full Tracker ---
    if st.session_state.applications:
        full_df = pd.DataFrame(st.session_state.applications)
        st.download_button(
            "📥 Download Full Tracker as CSV",
            full_df.to_csv(index=False).encode("utf-8"),
            file_name="job_applications.csv",
            mime="text/csv"
        )
st.markdown("---")

# --- Sidebar Inputs ---
st.sidebar.header("User Information")
name = st.sidebar.text_input("Your Name")
email = st.sidebar.text_input("Your Email")
skills = st.sidebar.text_area("Top Skills (comma-separated, e.g., Python, Excel, Data Analysis)")
experience = st.sidebar.text_area("Your Work Experience")

st.sidebar.header("Job Details")
job_title = st.sidebar.text_input("Job Title")
company = st.sidebar.text_input("Company Name")
job_description = st.sidebar.text_area("Job Description")
st.header("Resume and Cover Letter Generator")
st.sidebar.markdown("---")
show_tip("resume")

# --- Resume ---
if name and email and skills and experience:
    if st.button("Generate Resume"):
        if not openai_api_key and not use_placeholder:
            st.error("OpenAI API Key is missing. Set it as an environment variable.")
        else:
            with st.spinner("Generating your resume..."):
                resume_text = generate_resume(
                    openai_api_key, name, email, skills, experience, model, use_placeholder, client
                )

            if "Error" in resume_text:
                st.error(resume_text)
            else:
                st.session_state.resume = resume_text
                st.success("✅ Resume generated successfully!")
                st.markdown("---")

                # Auto-save to tracker, avoiding duplicates
                auto_app = {
                    "ID": str(uuid.uuid4()),
                    "Job Title": job_title,
                    "Company": company,
                    "Date Applied": str(pd.Timestamp.now().date()),
                    "Status": "Generated",
                    "Notes": "Auto-added via resume builder"
                }

                if not any(
                    app.get("Job Title") == job_title and
                    app.get("Company") == company and
                    app.get("Status") == "Generated"
                    for app in st.session_state.applications
                ):
                    st.session_state.applications.append(auto_app)
                    save_applications(st.session_state.applications)

# --- Resume Output ---
if "resume" in st.session_state:
    if st.checkbox("Show Resume as plain text"):
        st.text_area("Generated Resume", st.session_state.resume, height=300)
    else:
        st.markdown(f"```markdown\n{st.session_state.resume}\n```")

    st.download_button("Download Resume (TXT)", st.session_state.resume, file_name="Resume.txt")
    st.download_button("Download Resume (PDF)", export_as_pdf(st.session_state.resume), file_name="Resume.pdf")
    st.download_button("Download Resume (Word)", export_as_docx(st.session_state.resume), file_name="Resume.docx")

# --- Resume Match Scorer ---
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
            comparison = compare_resume_to_job(openai_api_key, st.session_state.resume, jd_input, model, use_placeholder, client)
            st.markdown(comparison)
            match = re.search(r"(\d{1,3})/100", comparison)
            if match:
                score = int(match.group(1))
                st.progress(score)

st.markdown("---")

# --- Cover Letter ---
if name and job_title and company and job_description:
    show_tip("cover_letter")
    if st.button("Generate Cover Letter"):
        if not openai_api_key and not use_placeholder:
            st.error("OpenAI API Key is missing. Set it as an environment variable.")
        else:
            with st.spinner("Generating your cover letter..."):
                cover_letter_text = generate_cover_letter(openai_api_key, name, job_title, company, job_description, model, use_placeholder, client)
            if "Error" in cover_letter_text:
                st.error(cover_letter_text)
            else:
                st.session_state.cover_letter = cover_letter_text
                st.success("✅ Cover letter generated successfully!")
                st.markdown("---")

# --- Cover Letter Output ---
if "cover_letter" in st.session_state:
    st.text_area("Generated Cover Letter", st.session_state.cover_letter, height=300)
    st.download_button("Download Cover Letter (TXT)", st.session_state.cover_letter, file_name="Cover_Letter.txt")
    st.download_button("Download Cover Letter (PDF)", export_as_pdf(st.session_state.cover_letter), file_name="Cover_Letter.pdf")
    st.download_button("Download Cover Letter (Word)", export_as_docx(st.session_state.cover_letter), file_name="Cover_Letter.docx")

