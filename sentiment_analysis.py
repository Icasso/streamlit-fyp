import streamlit as st

from tables import textblob_distribution, vader_distribution


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
