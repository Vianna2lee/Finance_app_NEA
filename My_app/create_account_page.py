import streamlit as st 
from functions import *
# streamlit run My_app/4_create_account_page.py to run the app


st.title("Create account")

with st.form("Create account", enter_to_submit=True):
    username = st.text_input("Create account name:", placeholder="Create an account name")
    password = st.text_input("Create password:", type="password", placeholder="Create password")
    password_again = st.text_input("Enter password again:", type="password", placeholder="Enter password again")
    email = st.text_input("Enter email address: ", placeholder="Enter email address")

    button = st.form_submit_button("Create account")

    if button:
        error=[]
        if password != password_again:
            error.append("Passwords do not match. Please try again.")
        if username =="" or  password =="" or email=="":
            error.append("All fields are required. Please fill in all details.")
        if is_valid_email(email) == False:
            error.append("Invalid email address. Please enter a valid email.")
        if username_exists(username):
            error.append("Username already exists. Please choose a different username.")
        if password_validation(password) == False:
            error.append("Password must be at least 8 characters long") 
            
        # input validaation for account name e.g num and str only, not symbol

        if error:
            for err in error:
                st.error(err)
        else:
            create_account(username, password, email)
            st.session_state["logged_in"]=True
            st.rerun()
            
      # log in rght after created an account        