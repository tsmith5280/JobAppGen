import streamlit as st

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
