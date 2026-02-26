import streamlit as st 
from functions import *
# streamlit run My_app/logout_page.py to run the app

if st.button("Logout", type="primary"): #create a logout button, when clicked
    st.success("You have been logged out successfully.") #success message is displayed
    st.session_state["logged_in"]=False # set session state variable
    st.session_state['Username'] = None    #set session state variable
    st.session_state['stock_list'] = [] #set session state variable
    st.rerun() #rerun 



