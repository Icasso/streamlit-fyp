import datetime

import plotly.express as px
import psycopg2.extras
import streamlit as st

from database import connection, cursor


@st.cache
def query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def app():
    st.title("Sentiment Analysis - Part 2")
    st.success("Sentiment Analysis on Reddit Corpus based on top 10 mentioned stocks throughout the analysis period")

    symbol = st.sidebar.selectbox('Select a Stock Symbol',
                                  ('GME', 'AMC', 'BB', 'PLTR', 'TSLA', 'RH', 'NOK', 'RKT', 'AMD', 'TLRY'))

    date_range_from = st.sidebar.date_input('Date From', value=datetime.date(2021, 1, 1),
                                            min_value=datetime.date(2021, 1, 1),
                                            max_value=datetime.date(2021, 11, 28))
    date_range_to = st.sidebar.date_input('Date To', value=datetime.date(2021, 11, 28),
                                          min_value=datetime.date(2021, 1, 1),
                                          max_value=datetime.date(2021, 11, 28))

    container_1 = st.container()
    with container_1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("TextBlob - Polarity")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_textblob_polarity WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                tb_polarity_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=tb_polarity_list, labels={'x': 'Date', 'y': 'TextBlob Polarity'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
        with col2:
            st.subheader("TextBlob - Subjectivity")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_textblob_subjectivity WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                tb_subjectivity_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=tb_subjectivity_list, labels={'x': 'Date', 'y': 'TextBlob Subjectivity'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()

    container_2 = st.container()
    with container_2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("VADER - Positive")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_vader_positive WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                vader_positive_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=vader_positive_list, labels={'x': 'Date', 'y': 'VADER Positive'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
        with col2:
            st.subheader("VADER - Negative")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_vader_negative WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                vader_negative_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=vader_negative_list, labels={'x': 'Date', 'y': 'VADER Negative'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()

    container_3 = st.container()
    with container_3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("VADER - Neutral")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_vader_neutral WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                vader_neutral_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=vader_neutral_list, labels={'x': 'Date', 'y': 'VADER Neutral'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
        with col2:
            st.subheader("VADER - Compound")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_vader_compound WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                vader_compound_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=vader_compound_list, labels={'x': 'Date', 'y': 'VADER Compound'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()

    container_4 = st.container()
    with container_4:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Modified VADER - Positive")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_modified_vader_positive WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                modified_vader_positive_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=modified_vader_positive_list,
                              labels={'x': 'Date', 'y': 'Modified VADER Positive'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
        with col2:
            st.subheader("Modified VADER - Negative")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_modified_vader_negative WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                modified_vader_negative_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=modified_vader_negative_list,
                              labels={'x': 'Date', 'y': 'Modified VADER Negative'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()

    container_5 = st.container()
    with container_5:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Modified VADER - Neutral")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_modified_vader_neutral WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                modified_vader_neutral_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=modified_vader_neutral_list,
                              labels={'x': 'Date', 'y': 'Modified VADER Neutral'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
        with col2:
            st.subheader("Modified VADER - Compound")
            try:
                results = query("""
                SELECT created_utc, ("{0}") FROM sa_modified_vader_compound WHERE created_utc BETWEEN ('{1}') AND ('{2}')
                """.format(symbol, date_range_from, date_range_to))
                day_list = [x[0] for x in results]
                reddit_sentiment_index_list = [x[1] for x in results]
                fig = px.line(x=day_list, y=reddit_sentiment_index_list,
                              labels={'x': 'Date', 'y': 'Modified VADER Compound'})
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
