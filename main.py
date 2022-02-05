import streamlit as st

import app1
import app2

PAGES = {
    "Reddit Community Distribution": app1,
    "2": app2,
}
st.set_page_config(
    page_title="Reddit Sentiment Index: Stock Price Movement Prediction with Valence Aware Dictionary Sentiment Reasoner",
    page_icon="🚀",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a bug': 'https://github.com/Icasso',
        'Get Help': 'https://www.google.com.hk/',
        'About': "# Made with ❤️. *Tsui Hoi Ming*"
    }
)

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Dashboard", list(PAGES.keys()))
page = PAGES[selection]
try:
    page.app()
except Exception as e:
    st.error("Oops, something went wrong! Stay calm and do not panic.\n")
    st.error(e)
