import streamlit as st

from tables import top_10_mentioned_stocks


def app():
    st.title("Exploratory Data Analysis")
    st.success("Exploratory Data Analysis on Reddit Corpus")
    # st.write("WordCloud, Construction of lexicon for VADER")

    container_1 = st.container()
    with container_1:
        st.header("Top 10 mentioned stock symbols from 2021-01-01 to 2021-11-28")
        col1, col2 = st.columns(2)
        with col1:
            st.table(top_10_mentioned_stocks)
        with col2:
            code = '''
            symbol_list = comment_df.Symbol.tolist()
symbol_list
from collections import Counter
c = Counter(symbol_list)
top_symbol = [key for key, value in c.most_common(10)]
top_symbol
            '''
            st.code(code, language="python")

    container_2 = st.container()
    with container_2:
        st.header("Most Common Words / Significant words that have an impact on sentiment")
        col1, col2 = st.columns(2)
        with col1:
            st.image("src/WordCloud.png")
        with col2:
            code = '''
            stop_words = stopwords.words('english')
comments_df['body'] = comments_df['body'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
body_list = comments_df.body.tolist()
lst = []
for item in body_list:
    for word in item.split():
        lst.append(word)
c = Counter()
for word in lst:
    c[word] += 1
c.most_common()
            '''
            st.code(code, language="python")
