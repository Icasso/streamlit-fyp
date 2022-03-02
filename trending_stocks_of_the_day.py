import datetime
from datetime import timedelta
import pandas as pd
import plotly.express as px
import psycopg2.extras
import streamlit as st
import yfinance as yf

from database import connection, cursor


@st.cache
def query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def app():
    # Main
    st.title("Trending Stocks on r/wallstreetbets")
    st.success("Reddit Comment Volume Analysis")

    # Siderbar
    d = st.sidebar.date_input("Select a date", datetime.date(2021, 1, 29), min_value=datetime.date(2021, 1, 1),
                              max_value=datetime.date(2021, 11, 28))
    num = st.sidebar.number_input("Most Mentioned Symbols amount", value=10, min_value=1, max_value=100)
    st.sidebar.markdown("---")

    # Query
    try:
        results = query("""
    SELECT "Symbol" , ("{0}") FROM reddit_comment_volume WHERE NOT "Symbol" = 'comment_volume' order by ("{0}") DESC LIMIT {1};
    """.format(
            d.strftime("%Y-%m-%d %H:%M:%S"), num))
        symbol_list = [x[0] for x in results]
        volume_list = [x[1] for x in results]

        # Metrics
        container_1 = st.container()
        with container_1:
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Most Mentioned Symbol", value=symbol_list[0])
            col2.metric(label="No. of Comments", value=volume_list[0])
            print(d)
            try:
                his_stock_price = yf.download(symbol_list[0], start=d, end=d + timedelta(days=1))
            except Exception as e:
                st.error(e)

            print(his_stock_price)
            if len(his_stock_price) > 0:
                his_stock_price = "{0:.2f}".format(his_stock_price['Close'][0])
                col3.metric("Previous Day Stock Closing Price", value=his_stock_price)

        container_2 = st.container()
        with container_2:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(x=symbol_list, y=volume_list, labels={'x': 'Symbol', 'y': 'Volume'},
                             title="Top {0} mentioned stocks on {1}".format(int(num), d.strftime("%Y-%m-%d")))
                st.plotly_chart(fig)

        results = query("""
        SELECT body, "Symbol" FROM reddit_data WHERE created_utc = '{0}' and "Symbol" != '' LIMIT 20;
        """.format(d.strftime("%Y-%m-%d %H:%M:%S"), ))
        comment_list = [x[0] for x in results]
        comment_symbol_list = [x[1] for x in results]
        comments = {
            "20 Sample Comments of the Day": comment_list,
            "Stock": comment_symbol_list
        }
        df = pd.DataFrame(comments)
        st.table(df)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        st.warning("That date does not contain any comments after data processing, please select another date.")
        connection.rollback()
