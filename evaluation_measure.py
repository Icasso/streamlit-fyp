import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import streamlit as st

from database import cursor


@st.cache
def query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def app():
    st.title("Experimental Study & Evaluation Measure")
    st.success("Experimental Study & Evaluation Measure of Top 10 mentioned stock throughout the COVID-19 pandemic")

    symbol = st.sidebar.selectbox('Select a Stock Symbol',
                                  ('GME', 'AMC', 'BB', 'PLTR', 'TSLA', 'RH', 'NOK', 'RKT', 'AMD', 'TLRY'))

    date_range_from = st.sidebar.date_input('Date From', value=datetime.date(2021, 1, 1),
                                            min_value=datetime.date(2021, 1, 1),
                                            max_value=datetime.date(2021, 11, 28))
    date_range_to = st.sidebar.date_input('Date To', value=datetime.date(2021, 1, 31),
                                          min_value=datetime.date(2021, 1, 1),
                                          max_value=datetime.date(2021, 11, 28))

    container_1 = st.container()
    with container_1:
        col1, col2 = st.columns(2)
        df = pd.read_csv(f"stocks/{symbol}.csv")
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.date
        df = df[(df['Date'] >= date_range_from) & (df['Date'] <= date_range_to)]
        with col1:
            st.header(f"Historical Stock Price")
            fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                 open=df['Open'],
                                                 high=df['High'],
                                                 low=df['Low'],
                                                 close=df['Close'])])
            st.plotly_chart(fig)
        with col2:
            st.header(f"r/wallstreetbets {symbol} mentioned")
            fig = px.line(df, x="Date", y="count")
            st.plotly_chart(fig)

    container_2 = st.container()
    with container_2:
        st.subheader("Pearson Correlation Coefficient of Stock Price, Trading Volume against Comment Volume")
        col1, col2 = st.columns(2)
        with col1:
            st.write("The correlation coefficient is calculated as follows:")
            st.latex(r'''r = \frac{\sum\lparen x - m_x\rparen\lparen y - m_y\rparen}{\sqrt{\sum\lparen x - 
            m_x\rparen^2\lparen y - m_y\rparen^2}} ''')
        with col2:
            code = '''
            import scipy.stats as stats
scipy.stats.pearsonr(x, y)
            '''
            st.code(code, language="python")
        st.write("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        open_p_corr = stats.pearsonr(df['Open'], df['count'])
        high_p_corr = stats.pearsonr(df['High'], df['count'])
        low_p_corr = stats.pearsonr(df['Low'], df['count'])
        close_p_corr = stats.pearsonr(df['Close'], df['count'])
        vol_p_corr = stats.pearsonr(df['Volume'], df['count'])
        with col1:
            st.metric("Stock Price - Open & Comment Volume: r", "{:.3f}".format(open_p_corr[0]))
            st.metric("Stock Price - High & Comment Volume: r", "{:.3f}".format(high_p_corr[0]))
            st.metric("Stock Price - Low & Comment Volume: r", "{:.3f}".format(low_p_corr[0]))
            st.metric("Stock Price - Close & Comment Volume: r", "{:.3f}".format(close_p_corr[0]))
            st.metric("Trading Volume & Comment Volume: r", "{:.3f}".format(vol_p_corr[0]))
        with col2:
            st.metric("Stock Price - Open & Comment Volume: p", "{:.3f}".format(open_p_corr[1]))
            st.metric("Stock Price - High & Comment Volume: p", "{:.3f}".format(high_p_corr[1]))
            st.metric("Stock Price - Low & Comment Volume: p", "{:.3f}".format(low_p_corr[1]))
            st.metric("Stock Price - Close & Comment Volume: p", "{:.3f}".format(close_p_corr[1]))
            st.metric("Trading Volume & Comment Volume: p", "{:.3f}".format(vol_p_corr[1]))
        with col3:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name='Open'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['High'], name='High', yaxis='y2'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'], name='Low', yaxis='y3'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close', yaxis='y4'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Volume'], name='Trading Volume', yaxis='y5'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['count'], name='Comment Volume', yaxis='y6'))
            fig.update_layout(yaxis=dict(visible=False),
                              yaxis2=dict(visible=False, overlaying='y'),
                              yaxis3=dict(visible=False, overlaying='y'),
                              yaxis4=dict(visible=False, overlaying='y'),
                              yaxis5=dict(visible=False, overlaying='y'),
                              yaxis6=dict(visible=False, overlaying='y'))

            st.plotly_chart(fig)

    st.write("")
    container_3 = st.container()
    with container_3:
        st.subheader("Perason Correlation Coefficient of Stock Price and Different Sentiment Indicators")
        CHOICES = {"tb_polarity": "TextBlob Polarity", "tb_subjectivity": "TextBlob Subjectivity",
                   "v_pos": "Vader Positive",
                   "v_neg": "Vader Negative", "v_neu": "Vader Neutral", "v_com": "Vader Compound",
                   "mv_pos": "Modified Vader Positive",
                   "mv_neg": "Modified Vader Negative", "mv_neu": "Modified Vader Neutral",
                   "mv_com": "Modified Vader Compound", "rsi": "Reddit Sentiment Index"}
        sentiment_state = st.selectbox("Select Sentiment Type", CHOICES.keys(), format_func=lambda x: CHOICES[x])
        open_res = stats.pearsonr(df['Open'], df[sentiment_state])
        high_res = stats.pearsonr(df['High'], df[sentiment_state])
        low_res = stats.pearsonr(df['Low'], df[sentiment_state])
        close_res = stats.pearsonr(df['Close'], df[sentiment_state])
        movement_res = stats.pearsonr(df['Movement'], df[sentiment_state])
        mentioned_res = stats.pearsonr(df['count'], df[sentiment_state])
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric(f"Stock Price - Open & {sentiment_state}: r", "{:.3f}".format(open_res[0]))
            st.metric(f"Stock Price - High & {sentiment_state}: r", "{:.3f}".format(high_res[0]))
            st.metric(f"Stock Price - Low & {sentiment_state}: r", "{:.3f}".format(low_res[0]))
            st.metric(f"Stock Price - Close & {sentiment_state}: r", "{:.3f}".format(close_res[0]))
            st.metric(f"Stock Price - Movement & {sentiment_state}: r", "{:.3f}".format(movement_res[0]))
            st.metric(f"Comment Volume & {sentiment_state}: r", "{:.3f}".format(mentioned_res[0]))
        with col2:
            st.metric(f"Stock Price - Open & {sentiment_state}: p", "{:.3f}".format(open_res[1]))
            st.metric(f"Stock Price - High & {sentiment_state}: p", "{:.3f}".format(high_res[1]))
            st.metric(f"Stock Price - Low & {sentiment_state}: p", "{:.3f}".format(low_res[1]))
            st.metric(f"Stock Price - Close & {sentiment_state}: p", "{:.3f}".format(close_res[1]))
            st.metric(f"Stock Price - Movement & {sentiment_state}: p", "{:.3f}".format(movement_res[1]))
            st.metric(f"Comment Volume & {sentiment_state}: p", "{:.3f}".format(mentioned_res[1]))
        with col3:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Movement'], name='Movement'))
            fig.add_trace(go.Scatter(x=df['Date'], y=df[sentiment_state], name=sentiment_state, yaxis='y2'))
            fig.update_layout(yaxis=dict(visible=False),
                              yaxis2=dict(visible=False, overlaying='y'))
            st.plotly_chart(fig)

    st.write("")
    container_4 = st.container()
    with container_4:
        st.subheader(f"Accumulated Predictability of Reddit Sentiment Index")
        col1, col2, col3 = st.columns([1, 1, 2])
        prediction = df['Prediction']
        tbprediction = df['tbPrediction']
        dvprediction = df['dvPrediction']
        positive_count, tb_positive_count, dv_positive_count = 0, 0, 0
        negative_count, tb_negative_count, dv_negative_count = 0, 0, 0
        for item in prediction:
            if item == "correct":
                positive_count += 1
            else:
                negative_count += 1
        for item in tbprediction:
            if item == "correct":
                tb_positive_count += 1
            else:
                tb_negative_count += 1
        for item in dvprediction:
            if item == "correct":
                dv_positive_count += 1
            else:
                dv_negative_count += 1
        positive_res = positive_count / (positive_count + negative_count) * 100
        negative_res = negative_count / (positive_count + negative_count) * 100
        tb_positive_res = tb_positive_count / (tb_positive_count + tb_negative_count) * 100
        tb_negative_res = tb_negative_count / (tb_positive_count + tb_negative_count) * 100
        dv_positive_res = dv_positive_count / (dv_positive_count + dv_negative_count) * 100
        dv_negative_res = dv_negative_count / (dv_positive_count + dv_negative_count) * 100
        with col1:
            st.info(f"From: {date_range_from}")
            st.metric(f"Correct Predictions for RSI: {positive_count} out of {positive_count + negative_count} days",
                      "{:.2f}%".format(positive_res))
            st.metric(
                f"Correct Predictions for TextBlob: {tb_positive_count} out of {tb_positive_count + tb_negative_count} days",
                "{:.2f}%".format(tb_positive_res))
            st.metric(
                f"Correct Predictions for VADER: {dv_positive_count} out of {dv_positive_count + dv_negative_count} days",
                "{:.2f}%".format(dv_positive_res))
        with col2:
            st.info(f"To: {date_range_to}")
            st.metric(f"Incorrect Predictions: {negative_count} out of {positive_count + negative_count} days",
                      "{:.2f}%".format(negative_res))
            st.metric(
                f"Incorrect Predictions for TextBlob: {tb_negative_count} out of {tb_positive_count + tb_negative_count} days",
                "{:.2f}%".format(tb_negative_res))
            st.metric(
                f"Incorrect Predictions for VADER: {dv_negative_count} out of {dv_positive_count + dv_negative_count} days",
                "{:.2f}%".format(dv_negative_res))
        with col3:
            fig = px.pie(labels=['Correct', 'Incorrect'], values=[positive_res, negative_res])
            st.plotly_chart(fig)
