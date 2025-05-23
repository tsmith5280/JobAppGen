import streamlit as st
from core.utils.auth import login_form, get_user_id

def auth_header():
    st.markdown("### 👤 Account")

    if "user" not in st.session_state:
        with st.expander("Login or Sign Up"):
            login_form()
        st.stop()
    else:
        user = st.session_state["user"]
        st.write(f"Logged in as: `{user.email}`")
        if st.button("Log Out"):
            st.session_state.pop("user")
            st.experimental_rerun()
