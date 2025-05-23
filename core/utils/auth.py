import streamlit as st
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_form():
    st.subheader("🔐 Log In or Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    login, signup = st.columns(2)
    login_success, signup_success = None, None

    with login:
        if st.button("Log In"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Logged in!")
            except Exception as e:
                st.error("Login failed.")

    with signup:
        if st.button("Create New Account"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Account created and logged in!")
            except Exception as e:
                st.error("Signup failed.")

def get_user_id():
    return getattr(st.session_state.get("user"), "id", None)
