import datetime

import plotly.express as px
import psycopg2.extras
import streamlit as st

import config

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def app():
    # Main
    st.title("Trending Stocks on r/wallstreetbets")
    st.success("Reddit Comment Volume Analysis")

    # Siderbar
    d = st.sidebar.date_input("Select a date", datetime.date(2021, 1, 1), min_value=datetime.date(2021, 1, 1),
                              max_value=datetime.date(2021, 12, 31))
    num = st.sidebar.number_input("Most Mentioned Symbols amount", value=10, min_value=1, max_value=100)
    st.sidebar.markdown("---")
    text_input = st.sidebar.text_input("Search for a symbol", value="", max_chars=5)

    # Query
    try:
        cursor.execute("""
    SELECT "Symbol" , ("{0}") FROM reddit_comment_volume WHERE NOT "Symbol" = 'comment_volume' order by ("{0}") DESC LIMIT {1};
    """.format(
            d.strftime("%Y-%m-%d %H:%M:%S"), num))
        results = cursor.fetchall()
        symbol_list = [x[0] for x in results]
        volume_list = [x[1] for x in results]

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Most Mentioned Symbol", value=symbol_list[0])
        col2.metric(label="No. of Comments", value=volume_list[0])
        col3.metric("Stock Price", value=0)

        col1, col2 = st.columns(2)
        with col1:
            # TODO daily mention 'comment_volume' side
            fig = px.bar(x=symbol_list, y=volume_list, labels={'x': 'Symbol', 'y': 'Volume'},
                         title="Top {0} mentioned stocks of the day".format(num))
            st.plotly_chart(fig)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        st.warning("That date does not contain any comments after data processing, please select another date.")
        connection.rollback()
