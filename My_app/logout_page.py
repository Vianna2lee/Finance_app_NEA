import streamlit as st 
from functions import *
# streamlit run My_app/logout_page.py to run the app

if st.button("Logout", type="primary"):
    st.success("You have been logged out successfully.")
    st.session_state["logged_in"]=False
    st.session_state['Username'] = None
    st.session_state['stock_list'] = []
    st.rerun()

# button aappear in all page so i can remove this page
