import streamlit as st
from datetime import date
from core.utils.applications_api import insert_application, get_user_applications
from core.utils.auth import login_form, get_user_id
from core.ui.auth_header import auth_header
auth_header()

st.set_page_config(page_title="Application Tracker", layout="wide")
st.title("🗂️ Application Tracker")
# TOGGLE AUTH
USE_AUTH = True  # set to False to bypass login during dev

if USE_AUTH:
    if "user" not in st.session_state:
        login_form()
        st.stop()

    user_id = get_user_id()
    if not user_id:
        st.error("User ID not found. Please log in.")
        st.stop()
else:
    user_id = None  # Optional: fallback mode or skip insert

# 🔽 New Application Form
st.markdown("## ✏️ Add New Job Application")

with st.form("new_application_form"):
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    status = st.selectbox("Status", ["Saved", "Applied", "Interviewing", "Rejected", "Offer"])
    date_applied = st.date_input("Date Applied", value=date.today())
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add to Tracker")

    if submitted:
        response = insert_application(
            user_id=user_id,
            job_title=job_title,
            company=company,
            status=status,
            date=str(date_applied),
            notes=notes
        )
        if response.get("data"):
            st.success("Application added successfully!")
            st.experimental_rerun()
        else:
            st.error("Failed to add application.")

# 🔍 Display User Applications
st.markdown("## 📋 Your Job Applications")

user_apps = get_user_applications(user_id)

if user_apps:
    st.dataframe(user_apps, use_container_width=True)
else:
    st.info("No applications found.")
