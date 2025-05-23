import streamlit as st

def init_session_state():
    if "applications" not in st.session_state:
        st.session_state.applications = []
    if "resume" not in st.session_state:
        st.session_state.resume = ""
    if "cover_letter" not in st.session_state:
        st.session_state.cover_letter = ""
    if "coach_prompted" not in st.session_state:
        st.session_state.coach_prompted = False
    if "ai_coach_enabled" not in st.session_state:
        st.session_state.ai_coach_enabled = False
    if "coach_history" not in st.session_state:
        st.session_state.coach_history = [{
            "role": "system",
        "content": "You are an expert job coach named Virel. Keep replies job-focused and brief."
    }]
