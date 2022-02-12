import streamlit as st


def app():
    st.title("Reddit Corpus")
    st.success("Reddit Corpus Analysis on Juypter Notebook")
    st.write("Data Collection, Data Preprocessing")
    code = '''
import pandas as pd
from pmaw import PushshiftAPI
api = PushshiftAPI()

import datetime as dt
after = int(dt.datetime(2021,1,1,0,1).timestamp())
before = int(dt.datetime(2021,12,31,23,59).timestamp())

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
