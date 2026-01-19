import streamlit as st
import sqlite3
import pandas as pd

# --- Read data ---
conn = sqlite3.connect("sqlite/pokemon_names_urls.db")
df = pd.read_sql('select * from pokemon_names_urls', conn)

# --- Session state ---



# --- Body ---
st.header("VGC explorer")

cols = st.columns(1)
with cols[0].container(border=True, height="content"):
    choices = st.multiselect(
    "What are your favorite colors?",
    ["Green", "Yellow", "Red", "Blue"],
    default=["Yellow", "Red"],
)


st.data_editor(data=df.head(),
               column_config={
                   "url" : st.column_config.ImageColumn("Pokemon")
               },
               hide_index=True)