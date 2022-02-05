import streamlit as st

import app1
import app2

PAGES = {
    "Reddit Community Distribution": app1,
    "2": app2,
}

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Dashboard", list(PAGES.keys()))
page = PAGES[selection]
page.app()
