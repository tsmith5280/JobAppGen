import streamlit as st
from core.utils.storage import load_profile
from dotenv import load_dotenv
load_dotenv()
from core.utils.auth import get_user_id
from core.utils.profile_api import get_user_profile, upsert_user_profile
from core.utils.resume_parser import extract_text_from_pdf, basic_resume_parse
from core.ui.auth_header import auth_header
auth_header()

st.set_page_config(page_title="JobAppGen Launcher", layout="wide")
load_profile()

st.markdown("# 💼 JobAppGen Launcher")
st.markdown("""
Welcome to **JobAppGen**, your smart job application toolkit.  
Use the sidebar to access:

-  **Application Tracker**
-  **Resume & Cover Letter Generator**
-  **Job Coach**
""")

user_id = get_user_id()

if user_id:
    profile = get_user_profile(user_id)
    
    if not profile:
        st.markdown("## 📎 Upload Your Resume")
        uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])

        if uploaded_file:
            raw_text = extract_text_from_pdf(uploaded_file)
            parsed = basic_resume_parse(raw_text)

            st.markdown("### ✏️ Parsed Resume Data")
            st.json(parsed)

            if st.button("Save My Profile"):
                upsert_user_profile(user_id, parsed)
                st.success("Profile saved! Reloading...")
                st.experimental_rerun()
    else:
        st.success(f"Welcome back, {profile['full_name']} — {profile['job_title']}!")

else:
    st.warning("Please log in to personalize your experience.")
