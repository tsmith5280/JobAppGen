import streamlit as st
import pandas as pd
import uuid
from collections import defaultdict
from utils.data import save_applications
STATUS_OPTIONS = ["Applied", "Interview", "Rejected", "Offer", "Generated"]
import re

def clean_resume_output(text):
    """Remove assistant commentary from resume output."""
    pattern = r"\n?In this resume,? I .*?$"
    return re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL).strip()
def extract_resume_commentary(text):
    """Pull out the AI commentary from the resume, if it exists."""
    match = re.search(r"(In this resume,? I .*)", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else None


def tracker_section(applications, csv_file):
    st.header("📋 Job Application Tracker")

        # --- Add New Application Form ---
    with st.form("application_form"):
        col1, col2 = st.columns(2)
        with col1:
            job = st.text_input("Job Title")
            company = st.text_input("Company")
        with col2:
            date = st.date_input("Date Applied")
            status = st.selectbox("Status", STATUS_OPTIONS)
        notes = st.text_area("Notes or Contact Info")

        if st.form_submit_button("➕ Add Application") and job and company:
            new_app = {
                "ID": str(uuid.uuid4()),
                "Job Title": job,
                "Company": company,
                "Date Applied": str(date),
                "Status": status,
                "Notes": notes
            }
            applications.append(new_app)
            save_applications(csv_file, applications)
            st.success("✅ Application added.")
            st.rerun()


    # --- Group & Display Applications ---
    grouped = defaultdict(list)
    for app in applications:
        try:
            month_year = pd.to_datetime(app["Date Applied"]).strftime('%B %Y')
        except Exception:
            month_year = "Unknown"
        grouped[month_year].append(app)

    if not applications:
        st.info("No job applications yet. Add one above to get started.")
    else:
        st.caption(f"📦 Loaded {len(applications)} applications.")

    for date in sorted(grouped, reverse=True):
        st.subheader(f"📅 Applications for {date} ({len(grouped[date])})")
        for app in grouped[date]:
            with st.expander(f"📝 {app['Job Title']} at {app['Company']} — {app['Status']}", expanded=False):
                title = st.text_input("Edit Job Title", value=app["Job Title"], key=f"title_{app['ID']}")
                status = st.selectbox(
                    "Edit Status",
                    STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(app["Status"]),
                    key=f"status_{app['ID']}"
)

                notes = st.text_area("Edit Notes", value=app["Notes"], key=f"notes_{app['ID']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save", key=f"save_{app['ID']}"):
                        app["Job Title"] = title
                        app["Status"] = status
                        app["Notes"] = notes
                        save_applications(csv_file, applications)
                        st.success("✅ Saved.")
                        st.rerun()
                with col2:
                    if st.button("❌ Delete", key=f"delete_{app['ID']}"):
                        st.session_state.applications = [
                            a for a in applications if a["ID"] != app["ID"]
                        ]
                        save_applications(csv_file, st.session_state.applications)
                        st.warning("🗑️ Deleted.")
                        st.rerun()

    # --- Download Tracker ---
    if applications:
        full_df = pd.DataFrame(applications)
        st.download_button(
            "📥 Download Tracker CSV",
            full_df.to_csv(index=False).encode("utf-8"),
            file_name="job_applications.csv",
            mime="text/csv"
        )
