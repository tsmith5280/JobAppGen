import streamlit as st
import pandas as pd
import uuid
from collections import defaultdict
from core.utils.storage import save_applications
from core.utils.data import save_applications

def tracker_section(CSV_FILE):
    if "applications" not in st.session_state:
        st.session_state.applications = []

    with st.expander("📋 Job Application Tracker", expanded=True):
        for app in st.session_state.applications:
            if "ID" not in app:
                app["ID"] = str(uuid.uuid4())

        with st.form("application_form"):
            col1, col2 = st.columns(2)
            with col1:
                job = st.text_input("Job Title")
                company = st.text_input("Company")
            with col2:
                date = st.date_input("Date Applied")
                status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
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
                st.session_state.applications.append(new_app)
                save_applications(CSV_FILE, st.session_state.applications)
                st.success("✅ Application added!")

        grouped = defaultdict(list)
        for app in st.session_state.applications:
            try:
                month_year = pd.to_datetime(app["Date Applied"]).strftime('%B %Y')
            except Exception:
                month_year = "Unknown Date"
            grouped[month_year].append(app)

        for date in sorted(grouped, reverse=True):
            st.subheader(f"📅 Applications for {date} ({len(grouped[date])})")
            for app in grouped[date]:
                with st.expander(f"📝 {app['Job Title']} at {app['Company']} — {app['Status']}", expanded=False):
                    title = st.text_input("Edit Job Title", value=app["Job Title"], key=f"title_{app['ID']}")
                    status = st.selectbox("Edit Status", ["Applied", "Interview", "Rejected", "Offer"],
                                          index=["Applied", "Interview", "Rejected", "Offer"].index(app["Status"]),
                                          key=f"status_{app['ID']}")
                    notes = st.text_area("Edit Notes", value=app["Notes"], key=f"notes_{app['ID']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save Changes", key=f"save_{app['ID']}"):
                            for real in st.session_state.applications:
                                if real["ID"] == app["ID"]:
                                    real["Job Title"] = title
                                    real["Status"] = status
                                    real["Notes"] = notes
                                    break
                            save_applications(CSV_FILE, st.session_state.applications)
                            st.success("✅ Changes saved.")
                            st.rerun()
                    with col2:
                        if st.button("❌ Delete", key=f"delete_{app['ID']}"):
                            st.session_state.applications = [
                                a for a in st.session_state.applications if a["ID"] != app["ID"]
                            ]
                            save_applications(CSV_FILE, st.session_state.applications)
                            st.warning("🗑️ Application deleted.")
                            st.rerun()

        if st.session_state.applications:
            full_df = pd.DataFrame(st.session_state.applications)
            st.download_button(
                "📥 Download Full Tracker as CSV",
                full_df.to_csv(index=False).encode("utf-8"),
                file_name="job_applications.csv",
                mime="text/csv"
            )
