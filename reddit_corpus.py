import pandas as pd
import plotly.express as px
import psycopg2.extras
import streamlit as st

import config

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


@st.cache
def query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def app():
    st.title("Reddit Corpus")
    st.success("Reddit Corpus Analysis on Juypter Notebook")

    # Data Collection
    container_1 = st.container()
    with container_1:
        st.header("Data Collection")
        col1, col2 = st.columns(2)
        with col1:
            try:
                results = query("""
                SELECT * FROM reddit_corpus_pre
                """)
                month_list = [result[1] for result in results]
                count_list = [result[2] for result in results]
                # st.write(month_list, count_list)
                fig = px.bar(x=month_list, y=count_list, labels={'x': 'Month', 'y': 'Reddit Corpus Volume'},
                             title="Sub-reddit r/wallstreetbets comment volume across 2021 collected via PushshiftAPI")
                st.plotly_chart(fig)
            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
        # column 2
        with col2:
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

    st.write("---")

    # Data Preprocessing
    container_2 = st.container()
    with container_2:
        st.header("Data Pre-Processing")
        st.info(
            "Minimum Viable Product approach. Tokenization, Stopword Removal, Regular Expression (RegEx) Matching "
            "techniques")
        st.subheader("Sample un-processed data")
        # Table
        try:
            results = query("""
            SELECT * FROM reddit_corpus_sample
            """)
            id_list = [result[0] for result in results]
            body_list = [result[1] for result in results]
            created_utc_list = [result[2] for result in results]
            # st.write(body_list, created_utc_list)
            sample_unprocessed_data = {
                'id': id_list,
                'body': body_list,
                'created_utc': created_utc_list
            }
            df = pd.DataFrame(sample_unprocessed_data)
            # CSS to inject contained in a string
            hide_table_row_index = """
                                <style>
                                tbody th {display:none}
                                .blank {display:none}
                                </style>
                                """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.table(df)

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            st.warning("Error while fetching data from PostgreSQL")
            connection.rollback()

        st.subheader("Concatenate into two stages of processing")
        col1, col2 = st.columns(2)
        with col1:
            try:
                results = query("""
                SELECT * FROM reddit_corpus_pre_stats
                """)
                created_utc_list = [result[1] for result in results]
                raw_list = [result[2] for result in results]
                empty_list = [result[3] for result in results]
                regex_list = [result[4] for result in results]

                pre_stats = {
                    'created_utc': created_utc_list,
                    'Corpus': raw_list,
                    'First Stage Cleaning': empty_list,
                    'Second Stage Cleaning': regex_list
                }
                df = pd.DataFrame.from_dict(pre_stats)
                hide_table_row_index = """
                                    <style>
                                    tbody th {display:none}
                                    .blank {display:none}
                                    </style>
                                    """

                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st.table(df)
                fig = px.bar(df, x='created_utc', y='Second Stage Cleaning',
                             labels={'created_utc': 'Month', 'Second Stage Cleaning': 'Number of comments'},
                             title="Volume of Reddit Corpus after two stages of cleaning")
                st.plotly_chart(fig)

            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                st.warning("Error while fetching data from PostgreSQL")
                connection.rollback()
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
