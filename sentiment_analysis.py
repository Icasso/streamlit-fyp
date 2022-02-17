import pandas as pd
import psycopg2.extras
import streamlit as st

from database import connection, cursor
from tables import textblob_distribution, vader_distribution


@st.cache
def query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def app():
    st.title("Sentiment Analysis")
    st.success("Sentiment Analysis on Reddit Corpus")

    container_1 = st.container()
    with container_1:
        st.header("TextBlob")
        col1, col2 = st.columns(2)
        with col1:
            st.write("TextBlob sentiment scores distribution")
            st.table(textblob_distribution)
            pass
        with col2:
            code = '''
Input: Reddit Corpus
Output: Polarity, Subjectivity

from textblob import TextBlob
TextBlob(Reddit Corpus).sentiment.polarity
TextBlob(Reddit Corpus).sentiment.subjectivity
'''
            st.code(code, language="python")

    container_2 = st.container()
    with container_2:
        st.header("VADER")
        col1, col2 = st.columns(2)
        with col1:
            st.write("VADER sentiment scores distribution")
            st.table(vader_distribution)
        with col2:
            code = '''
Input: Reddit Corpus
Output: Positive, Negative, Neutral, Compound

from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()
for corpus in Reddit Corpus:
    vader.polarity_scores(corpus)
            '''
            st.code(code, language="python")

    container_3 = st.container()
    with container_3:
        st.header("Modified VADER")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Modified VADER sentiment scores distribution")
            st.table(vader_distribution)
        with col2:
            code = '''
Input: Reddit Corpus
Output: Positive, Negative, Neutral, Compound

from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()
vader.lexicon.update(new_words)
for corpus in Reddit Corpus:
    vader.polarity_scores(corpus)
            '''
            st.code(code, language="python")

    st.write("---")
    container_4 = st.container()
    with container_4:
        st.subheader("Sampled Table - Sentiment analysed reddit corpus")
        try:
            results = query("""
            SELECT * FROM reddit_data WHERE "Symbol" != '' LIMIT 20""")
            body_list = [x[1] for x in results]
            symbol_list = [x[3] for x in results]
            tb_p_list = [x[4] for x in results]
            tb_s_list = [x[5] for x in results]
            d_v_neg_list = [x[6] for x in results]
            d_v_neu_list = [x[7] for x in results]
            d_v_pos_list = [x[8] for x in results]
            d_v_comp_list = [x[9] for x in results]
            m_v_neg_list = [x[10] for x in results]
            m_v_neu_list = [x[11] for x in results]
            m_v_pos_list = [x[12] for x in results]
            m_v_comp_list = [x[13] for x in results]
            sent_data = {
                "Body": body_list,
                "Symbol": symbol_list,
                "TextBlob Polarity": tb_p_list,
                "TextBlob Subjectivity": tb_s_list,
                "VADER Negative": d_v_neg_list,
                "VADER Neutral": d_v_neu_list,
                "VADER Positive": d_v_pos_list,
                "VADER Compound": d_v_comp_list,
                "Modified VADER Negative": m_v_neg_list,
                "Modified VADER Neutral": m_v_neu_list,
                "Modified VADER Positive": m_v_pos_list,
                "Modified VADER Compound": m_v_comp_list,
            }
            df = pd.DataFrame(sent_data)
            st.table(df)
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            st.warning("Error while fetching data from PostgreSQL.")
            connection.rollback()
