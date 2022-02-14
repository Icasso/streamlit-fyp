import pandas as pd
import plotly.express as px
import streamlit as st

from tables import reddit_corpus_pre, sample_unprocessed_data, pre_stats, stock_symbol_stats, stock_data_set


def app():
    st.title("Reddit Corpus")
    st.success("Reddit Corpus Analysis on Juypter Notebook")

    # Data Collection
    container_1 = st.container()
    with container_1:
        st.header("Data Collection")
        col1, col2 = st.columns(2)
        with col1:
            results = reddit_corpus_pre
            fig = px.bar(x=results['month_list'], y=results['count_list'],
                         labels={'x': 'Month', 'y': 'Reddit Corpus Volume'},
                         title="Sub-reddit r/wallstreetbets comment volume across 2021 collected via PushshiftAPI")
            st.plotly_chart(fig)

        with col2:
            code = '''
        import pandas as pd
        from pmaw import PushshiftAPI
        api = PushshiftAPI()
        
        import datetime as dt
        after = int(dt.datetime(2021,1,1,0,1).timestamp())
        before = int(dt.datetime(2021,11,28,23,59).timestamp())
        
        subreddit = 'wallstreetbets'
        comments = api.search_comments(subreddit=subreddit, after=after, filter=['body', 'created_utc'])
        print(f'Retrieved {len(comments)} comments from Pushshift')
        comments_df = pd.DataFrame(comments)
        comments_df['created_utc'] = pd.to_datetime(comments_df['created_utc'], unit='s')
        comments_df.head(5)
        comments_df.shape
        comments_df.to_pickle('comments_df.pkl')
            '''
            st.code(code, language="python")

    st.write("---")

    # Data Preprocessing
    container_2 = st.container()
    with container_2:
        st.header("Data Pre-Processing")
        st.info(
            "Minimum Viable Product approach. Tokenization, Stopword Removal, Regular Expression (RegEx) Matching "
            "techniques")
        st.subheader("Sample un-processed data")
        df = pd.DataFrame(sample_unprocessed_data)
        st.table(df)
        st.subheader("Concatenate into two stages of processing")
        col1, col2 = st.columns(2)
        with col1:
            df = pd.DataFrame.from_dict(pre_stats)
            st.table(df)
            fig = px.bar(df, x='Month', y='Second Stage Cleaning',
                         title="Volume of Reddit Corpus after two stages of cleaning")
            st.plotly_chart(fig)

        with col2:
            st.write("Body - Comment processing")
            code = '''
row_to_be_deleted_1 = comments_df[comments_df['body'] == '[removed]'].index
row_to_be_deleted_2 = comments_df[comments_df['body'] == '[deleted]'].index
comments_df.drop(row_to_be_deleted_1, inplace=True)
comments_df.drop(row_to_be_deleted_2, inplace=True)

raw_comments_df3 = raw_comments_df3.replace(r'\n', ' ', regex=True)
raw_comments_df3 = raw_comments_df3.replace(r'http\S+', '', regex=True)
raw_comments_df3 = raw_comments_df3.replace({' +':' '},regex=True)
row_to_be_deleted_3 = raw_comments_df3[raw_comments_df3['body'] == ''].index
raw_comments_df3.drop(row_to_be_deleted_3, inplace=True)'''
            st.code(code, language="python")
            st.write("Date related cleaning")
            code2 = '''
comments_df['created_utc'] = comments_df['created_utc'].dt.date
comments_df = comments_df.sort_values(by="created_utc", ascending=True)
comments_df
'''
            st.code(code2, language="python")

        st.subheader("Stock Symbol Extraction")
        col1, col2 = st.columns(2)
        with col1:
            df = pd.DataFrame(stock_symbol_stats)
            st.table(df)
            fig = px.pie(df, values='Number of comments', names='Comment contains stock symbol',
                         title="Number of comments containing stock symbols from 01/01/21 - 28/11/21")
            st.plotly_chart(fig)

        with col2:
            code = '''
            body_list = comment_df.body.tolist()
symbol_list = []
for i in body_list:
    inserted = False
    split = i.split(" ")
    for word in split:
        word = word.replace("$", "")
        if word.isupper() and len(word) <= 5 and word in us:
            symbol_list.append(word)
            inserted = True
            break
    if not inserted:
        symbol_list.append("")
symbol_list'''
            st.code(code, language="python")
            st.info("Statistics overview of 3 Exchanges in US, and the selected stock symbols")
            df = pd.DataFrame(stock_data_set)
            st.table(df)
