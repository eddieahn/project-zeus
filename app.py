import streamlit as st

def page_2():
    st.title("Coming Soon")
pg=st.navigation([st.Page("NewClassification.py",title="Classification Assistant"),st.Page(page_2,title="Coming Soon...")])
pg.run()