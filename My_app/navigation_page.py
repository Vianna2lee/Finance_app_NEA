import streamlit as st
from functions import *
from login_page import *
# streamlit run My_app/navigation_page.py to run the app


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


public_pages = [
        st.Page("home_page.py", title="Home page"),
        st.Page("stock_page.py", title="Stock page"),
        st.Page("login_page.py", title="Login page"),
        st.Page("create_account_page.py", title="Sign up page"),
        st.Page("option_price_calculator_page.py", title="Option price calculator page"),
    ]

private_pages = [
        st.Page("home_page.py", title="Home page"),
        st.Page("stock_page.py", title="Stock page"),
        st.Page("option_price_calculator_page.py", title="Option price calculator page"),
        st.Page("personal_page.py", title="Personal page"),
        st.Page("logout_page.py", title="Logout"),
    ]

if st.session_state["logged_in"]==True:
    pages = private_pages 
else:
    pages = public_pages

# direct user to personal page after login 

nav = st.navigation(pages)
nav.run()

