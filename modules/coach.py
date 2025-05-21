import streamlit as st

def is_coach_enabled() -> bool:
    """Check if the AI Coach is toggled on by the user."""
    return st.session_state.get("ai_coach_enabled", False)

def show_tip(context: str):
    """Display a context-sensitive coaching tip if enabled."""
    if not is_coach_enabled():
        return

    tips = {
        "resume": "💡 Tip: Use bullet points and quantify your impact (e.g., 'Increased sales by 20%').",
        "cover_letter": "📄 Tip: Address the letter to a person, not just 'Hiring Manager' if possible.",
        "job_description": "🧠 Tip: Use keywords from the job posting in your resume and cover letter.",
        "tracker": "📋 Tip: Regularly update your status and follow up after 7–10 days.",
        "first_time": "👋 Hey there! Want help as you go? Enable AI Coach in the sidebar.",
    }

    tip = tips.get(context)
    if tip:
        st.info(tip)
