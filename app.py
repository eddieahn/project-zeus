import streamlit as st

def page_2():
    st.title("Coming Soon")
pg=st.navigation([st.Page("Classification.py",title="Classification Assistant"),st.Page(page_2,title="Resource Assistant")])
pg.run()