from functions import *
import streamlit as st 
from streamlit_searchbox import st_searchbox # pip install streamlit-searchbox
# streamlit run My_app/navigation_page.py to run the app


st.title("Personal Page") #title of page

if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None: #if variabel is not in variable or none, set to 0
        st.session_state["stock_searchbox"] = 0

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"]) #for search bar
 
if selected is not None: # stock is selected from search bar
    st.session_state['stock_symbol'] =  str(selected.split(' - ')[0] ) #store symbol in variable
    st.session_state['stock_searchbox'] += 1  #change this variable so it know there is a change
    st.switch_page("stock_page.py") #switch page
    st.rerun()#rerun




st.write(f"Welcome, {st.session_state['Username']}!") #greeting

st.header("Followed stock list:") #header
if len(st.session_state["stock_list"]) > 0: #if the length of stock is greater than 0, show stock list 
      for i in st.session_state["stock_list"]:
        col1, col2,col3  = st.columns([20,15,70]) #formatting of page

        with col1:
            st.subheader(f"{i}") #subheading 
            get_last_price(i) #get last price of stock and show it

            if st.button("Unfollow", key=f"unfollow_{i}", type="primary"): #button to unfolow stock
                unfollow_stock(st.session_state["Username"], i) #call the unfollow stock funcation 
                st.success(f"You have unfollowed {i}.") #show user that they have unfollowed the stock
                st.rerun() #rerun 
        with col2:
            if st.button("More info", key=f"moreinfo_{i}", type="secondary"): #button for more info about stock
                st.session_state['stock_symbol'] = i #store symbol iin variable
                st.switch_page("stock_page.py") #switch page
        with col3:
            stock_page_graph(i, "5d" ,"1m") #show stock graph
else:
    st.write(''':red[**No followed stock, follow stocks to see them here!**]''') #tell user they need to follow stock to see them here 

