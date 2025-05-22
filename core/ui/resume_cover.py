import streamlit as st
from core.generator import generate_resume, generate_cover_letter
from core.export import export_as_pdf, export_as_docx
import pandas as pd
import uuid
from core.ui.tracker_view import STATUS_OPTIONS
from utils.cleaning import clean_resume_output, extract_resume_commentary

RESUME_KEY = "resume"
COVER_LETTER_KEY = "cover_letter"

def auto_track_generated_resume(job_title, company):
    return {
        "ID": str(uuid.uuid4()),
        "Job Title": job_title,
        "Company": company,
        "Date Applied": str(pd.Timestamp.now().date()),
        "Status": "Generated",
        "Notes": "Auto-added via resume builder"
    }

def resume_section(name, email, skills, experience, job_title, company, model, client, api_key, use_placeholder):
    format_choice = st.selectbox("Choose Resume Format", ["Standard", "Creative", "Compact"])

    if st.button("Generate Resume"):
        with st.spinner("Generating your resume..."):
            resume_text = generate_resume(
                api_key, name, email, skills, experience, model, use_placeholder, client
                # When ready, add format_choice as an arg to generator
            )
            comment = extract_resume_commentary(resume_text)
            resume_text = clean_resume_output(resume_text)

        if "Error" in resume_text:
            st.error(resume_text)
        else:
            st.session_state[RESUME_KEY] = resume_text
            st.success("✅ Resume generated successfully!")
            if comment:
                st.info(f"🧠 AI Tip: {comment}")
                st.toast("Tip added from AI assistant.")

            if not any(
                a for a in st.session_state.applications
                if a["Job Title"] == job_title and a["Company"] == company and a["Status"] == "Generated"
            ):
                st.session_state.applications.append(auto_track_generated_resume(job_title, company))

def render_resume_output():
    if RESUME_KEY in st.session_state:
        st.markdown(f"```markdown\n{st.session_state[RESUME_KEY]}\n```")
        for fmt, func, ext in [
            ("PDF", lambda: export_as_pdf(st.session_state[RESUME_KEY]), "pdf"),
            ("Word", lambda: export_as_docx(st.session_state[RESUME_KEY]), "docx")
        ]:
            st.download_button(
                f"Download Resume ({fmt})",
                func(),
                file_name=f"Resume.{ext}"
            )

def cover_letter_section(name, job_title, company, job_description, model, client, api_key, use_placeholder):
    if st.button("Generate Cover Letter"):
        with st.spinner("Generating your cover letter..."):
            text = generate_cover_letter(api_key, name, job_title, company, job_description, model, use_placeholder, client)

        if "Error" in text:
            st.error(text)
        else:
            st.session_state[COVER_LETTER_KEY] = text
            st.success("✅ Cover letter generated successfully!")
            st.markdown("---")

def render_cover_letter_output():
    if COVER_LETTER_KEY in st.session_state:
        st.text_area("Generated Cover Letter", st.session_state[COVER_LETTER_KEY], height=300)
        st.download_button("Download Cover Letter (PDF)", export_as_pdf(st.session_state[COVER_LETTER_KEY]), file_name="Cover_Letter.pdf")
        st.download_button("Download Cover Letter (Word)", export_as_docx(st.session_state[COVER_LETTER_KEY]), file_name="Cover_Letter.docx")
