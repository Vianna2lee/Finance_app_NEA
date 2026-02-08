import streamlit as st 
from functions import *
# streamlit run My_app/logout_page.py to run the app

if st.button("Logout", type="primary"): #create a logout button, when clicked
    st.success("You have been logged out successfully.") #success message is displayed
    st.session_state["logged_in"]=False #session state variable- logged_in is set to false
    st.session_state['Username'] = None    #session state variable- Username is set to none
    st.session_state['stock_list'] = [] #session state variable- stock_list is set to an empty list
    st.rerun() #the app is rerun to reflect the changes in the session state and navigation bar is updated


