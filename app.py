# Streamlit app script
import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Pokemon", page_icon="", layout="wide"
)

# ---- Page Setup ----
main_page = st.Page(
    page="pages/1_general.py",
    title="General",
    icon=":material/search:",
    default=True
)
contact_page = st.Page(
    page="pages/2_contact.py",
    title="General",
    icon=":material/mail:"
)
# ---- Sidebar ----
with st.sidebar:
    st.write("Test")
# add logo

# ---- Navigation Setup ----
pg = st.navigation(
    pages={"Pagina's": [main_page, contact_page]}
)
# --- Run navigation
pg.run()