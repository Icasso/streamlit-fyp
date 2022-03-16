import streamlit as st

from tables import top_10_mentioned_stocks


def app():
    st.title("Exploratory Data Analysis")
    st.success("Exploratory Data Analysis on Reddit Corpus")

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

    container_3 = st.container()
    with container_3:
        st.header("Cosine Similarity between Top 10 Stocks")
        col1, col2 = st.columns(2)
        with col1:
            st.image("src/CosineSimilarity.png")
        with col2:
            code = '''
# Cosine Similarity between Documents
import math

# Cosine Similarity function
def cosine_similarity(a,b):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(a)):
        x = a[i]; y = b[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

# Save the similarity index between the documents
def pair(s):
    for i, v1 in enumerate(s):
        for j in range(i+1, len(s)):
            yield [v1, s[j]]

dic={}
for (a,b) in list(pair(['GME', 'AMC', 'BB', 'PLTR', 'TSLA', 'RH', 'NOK', 'RKT', 'AMD', 'TLRY'])):
    dic[(a,b)] = cosine_similarity(term_document_matrix[a].tolist(), term_document_matrix[b].tolist())

# Print the cosine similarity
dic
import numpy as np
documents= ['GME', 'AMC', 'BB', 'PLTR', 'TSLA', 'RH', 'NOK', 'RKT', 'AMD', 'TLRY']
final_df = pd.DataFrame(np.asarray([[(dic[(x,y)] if (x,y) in dic else 0) for y in documents] for x in documents]))
final_df.columns =  documents
final_df.index = documents

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_xticks(np.arange(len(documents)), labels=documents)
ax.set_yticks(np.arange(len(documents)), labels=documents)
ax.matshow(final_df, cmap='seismic')
for (i, j), z in np.ndenumerate(final_df):
    if z != 0 :
        ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    else:
        None
fig.suptitle('Cosine Similarity Index between the Documents')
fig.set_size_inches(10,10)
plt.xticks(np.arange(len(documents)))
plt.yticks(np.arange(len(documents)))
plt.show()
            '''
            st.code(code, language="python")
