import streamlit as st
import json
import os

PROFILE_FILE = "user_profile.json"

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

def save_profile():
    keys = ["name_input", "email_input", "skills_input", "experience_input",
            "job_title_input", "company_input", "job_description_input"]
    profile_data = {k: st.session_state.get(k, "") for k in keys}
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile_data, f)

def load_profile():
    if st.session_state.get("profile_loaded", False):
        return
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            profile_data = json.load(f)
            for k, v in profile_data.items():
                if k not in st.session_state or not st.session_state.get(k):
                    st.session_state[k] = v
    st.session_state["profile_loaded"] = True

