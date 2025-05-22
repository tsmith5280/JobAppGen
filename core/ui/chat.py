import streamlit as st
import streamlit.components.v1 as components

def render_chat_popup(html_path="static/chat_popup.html"):
    with open(html_path, "r", encoding="utf-8") as f:
        components.html(f.read(), height=450, width=350)
