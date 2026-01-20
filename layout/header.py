import streamlit as st
from config import APP_TITLE, APP_SUBTITLE

def render_header():
    st.markdown(
        f"""
        <div class="card">
            <h1>{APP_TITLE}</h1>
            <p class="sub-text">{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
