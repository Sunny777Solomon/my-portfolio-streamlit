# utils.py

import streamlit as st

def link_button(url: str, label: str):
    """Render an HTML-styled link that looks like a button (opens in new tab)."""
    st.markdown(
        f"<a href=\"{url}\" target=\"_blank\"><button style=\"background-color:#0b5cff;color:white;padding:8px 16px;border-radius:8px;border:none;cursor:pointer;margin:4px;\">{label}</button></a>",
        unsafe_allow_html=True,
    )

def github_link_button(user: str, repo: str, label: str = "View on GitHub"):
    url = f"https://github.com/{user}/{repo}"
    link_button(url, label)
