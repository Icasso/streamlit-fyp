import streamlit as st

import evaluation_measure
import exploratory_data_analysis
import reddit_community_distribution
import reddit_corpus
import sentiment_analysis
import sentiment_analysis_2
import trading_strategy
import trending_stocks_of_the_day

PAGES = {
    "Reddit Community Distribution": reddit_community_distribution,
    "Reddit Corpus": reddit_corpus,
    "Exploratory Data Analysis": exploratory_data_analysis,
    "Trending Stocks of the Day": trending_stocks_of_the_day,
    "Sentiment Analysis I": sentiment_analysis,
    "Sentiment Analysis II": sentiment_analysis_2,
    "Evaluation": evaluation_measure,
    "Trading Strategy": trading_strategy
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
# TODO UNHIDE
hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            tbody th {display:none}
            .blank {display:none}
            footer {visibility: hidden;}
            [class^='viewerBadge_container'] {visibility: hidden;}
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
