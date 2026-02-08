import streamlit as st
from functions import *
from login_page import *
# streamlit run My_app/navigation_page.py to run the app


if "logged_in" not in st.session_state: #if the session state variable- logged_in does not exist
    st.session_state["logged_in"] = False #it is created and set to false


public_pages = [ #this is the navigation bar for users who are not logged in 
        st.Page("home_page.py", title="Home page"), #home page
        st.Page("stock_page.py", title="Stock page"), #stock page
        st.Page("login_page.py", title="Login page"), #login page   
        st.Page("create_account_page.py", title="Sign up page"), #sign up page
        st.Page("option_price_calculator_page.py", title="Option price calculator page"), #option price calculator page
    ]

private_pages = [ #this is the navigation bar for users who are logged in
        st.Page("home_page.py", title="Home page"), #home page 
        st.Page("stock_page.py", title="Stock page"), #stock page
        st.Page("option_price_calculator_page.py", title="Option price calculator page"), #option price calculator page 
        st.Page("personal_page.py", title="Personal page"), #personal page  
        st.Page("logout_page.py", title="Logout"), #logout page 
    ]

if st.session_state["logged_in"]==True: #if user is logged in
    pages = private_pages #set to private pages
else: #if user is not logged in
    pages = public_pages #set to public pages


nav = st.navigation(pages) #create the navigation bar
nav.run() #run the navigation bar


