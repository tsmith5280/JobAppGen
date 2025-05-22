import streamlit as st
from core.ui.tracker_view import tracker_section

CSV_FILE = "job_applications.csv"

st.set_page_config(page_title="Application Tracker", layout="wide")
st.title("🗂️ Application Tracker")

if "applications" not in st.session_state:
    st.session_state.applications = []

tracker_section(st.session_state.applications, CSV_FILE)
