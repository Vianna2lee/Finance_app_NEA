import streamlit as st 
from functions import *
# streamlit run My_app/4_create_account_page.py to run the app


st.title("Create account") #title for page 

with st.form("Create account", enter_to_submit=True): #form to creae account
    username = st.text_input("Create account name:", placeholder="Create an account name") #input box for username
    password = st.text_input("Create password:", type="password", placeholder="Create password") #input box for password
    password_again = st.text_input("Enter password again:", type="password", placeholder="Enter password again") #input bax for password again to confirm 
    email = st.text_input("Enter email address: ", placeholder="Enter email address") #input box for email address

    button = st.form_submit_button("Create account") # button the submit (create account)

    if button: #when the button is clicked
        error=[] #list to store error messages
        if password != password_again: #error when password and password again don't match
            error.append("Passwords do not match. Please try again.") 
        if username =="" or  password =="" or email=="": #erroe when any field is blank
            error.append("All fields are required. Please fill in all details.")
        if is_valid_email(email) == False: # error when the email address is not valid
            error.append("Invalid email address. Please enter a valid email.")
        if username_exists(username): #error when the same username exists in database
            error.append("Username already exists. Please choose a different username.") 
        if password_validation(password) == False: #error when the password is not 8 chars long
            error.append("Password must be at least 8 characters long") 
            
        

        if error:
            for err in error:
                st.error(err) #output the error messages 
        else:
            create_account(username, password, email) # if all the inputs are valid, the account will be created and stored in database
            st.session_state["logged_in"]=True #set this variable to true for the naviagtion page to change 
            st.rerun()# app is rerun 
            
      # log in rght after created an account        