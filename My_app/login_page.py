import streamlit as st 
from functions import *
# streamlit run My_app/login_page.py to run the app

st.title("Login Page") #title of the page 

if "Username" not in st.session_state: #if the session state variable-Username does not exist
    st.session_state["Username"] = None # it is created and set to None



if "stock_list" not in st.session_state or st.session_state["stock_list"] is None: #if the session state variable- stock_list, does not exist or is None 
    st.session_state["stock_list"] = [] #it is created and set to an empty list 



with st.form("Login", enter_to_submit=True): #create a form for login 
    username = st.text_input("Enter username:", placeholder="Enter username") #text input box for username
    password = st.text_input("Enter password:", type="password", placeholder="Enter password") #text input box for password
    

    button = st.form_submit_button("Login") #button to submit the form


    if button: #if the button is clicked
        error=[] #error list is created to store error messages, it is initially empty
        if username == "" or password == "": #if the username or password is empty
            error.append("All fields are required. Please fill in all details.") #add error message to the error list
        if password_checker(username, password) == False: #if password doesn't meet the reuirements
            error.append("Incorrect username or password")    #add error message to the error list
        
        if error: #if there is any error message in the error list
            for err in error:
                st.error(err) #each one is displayed using st.error()
        else: #if there are no errors 
            st.success("You have been logged in successfully.") #display success message
            st.session_state["logged_in"]=True #set the session state variable- logged_in to true
            st.rerun() #the app is rerun to reflect the changes in the session state and navigation bar is updated



            
            
            
