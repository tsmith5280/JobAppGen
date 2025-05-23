import streamlit as st
from core.utils.auth import get_user_id
from core.utils.profile_api import get_user_profile, upsert_user_profile
from core.utils.resume_parser import extract_text_from_pdf, basic_resume_parse
from core.ui.auth_header import auth_header
auth_header()

st.set_page_config(page_title="Settings", layout="wide")
st.title("⚙️ Settings")

user_id = get_user_id()
if not user_id:
    st.warning("Please log in to access your settings.")
    st.stop()

profile = get_user_profile(user_id)
if profile:
    st.markdown("### Current Profile")
    st.json(profile)
else:
    st.info("No profile found. Upload your resume on the home page.")

st.markdown("### 🔁 Re-upload Resume")
uploaded_file = st.file_uploader("Upload a new resume (.pdf)", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    parsed = basic_resume_parse(raw_text)
    st.markdown("Parsed data:")
    st.json(parsed)

    if st.button("Overwrite My Profile"):
        upsert_user_profile(user_id, parsed)
        st.success("Profile updated successfully!")
