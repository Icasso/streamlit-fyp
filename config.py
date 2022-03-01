# DB_HOST = 'localhost'
# DB_USER = 'postgres'
# DB_PASS = ''
# DB_NAME = 'Test'
import streamlit as st
DB_HOST = st.secrets["DB_HOST"]
DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]
DB_NAME = st.secrets["DB_NAME"]