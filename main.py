import streamlit as st

import reddit_community_distribution
import reddit_corpus

PAGES = {
    "Reddit Community Distribution": reddit_community_distribution,
    "Reddit Corpus": reddit_corpus,
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

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Dashboard", list(PAGES.keys()))
page = PAGES[selection]
try:
    page.app()
except Exception as e:
    st.error("Oops, something went wrong! Stay calm and do not panic.\n")
    st.error(e)
