import streamlit as st
from utils.storage import load_profile
load_profile()

st.set_page_config(page_title="JobAppGen Launcher", layout="wide")

st.markdown("# 💼 JobAppGen Launcher")
st.markdown("""
Welcome to **JobAppGen**, your smart job application toolkit.  
Use the sidebar to access:

- 🗂️ **Application Tracker**
- 📄 **Resume & Cover Letter Generator**
- 💬 **Job Coach**

---

_This is just the home screen. Pick a page from the sidebar to get started._
""")
