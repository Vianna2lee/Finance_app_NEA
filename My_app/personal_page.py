from functions import *
import streamlit as st 
from streamlit_searchbox import st_searchbox # pip install streamlit-searchbox
# streamlit run My_app/navigation_page.py to run the app



if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None:
        st.session_state["stock_searchbox"] = 0

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"])
 
if selected is not None: # new selection made
    st.session_state['stock_symbol'] =  str(selected.split(' - ')[0] )
    st.session_state['stock_searchbox'] += 1 
    st.switch_page("stock_page.py")
    st.rerun()



st.title("Personal Page")


st.write(f"Welcome, {st.session_state['Username']}!")

st.header("Followed stock list:")
if len(st.session_state["stock_list"]) > 0:
      for i in st.session_state["stock_list"]:
        col1, col2,col3  = st.columns([20,15,70])

        with col1:
            st.subheader(f"{i}")
            get_last_price(i)

            if st.button("Unfollow", key=f"unfollow_{i}", type="primary"):
                unfollow_stock(st.session_state["Username"], i)
                st.success(f"You have unfollowed {i}.")
                st.session_state["stock_list"].remove(i)
                st.rerun()
                
        with col2:
            if st.button("More info", key=f"moreinfo_{i}", type="secondary"):
                st.session_state['stock_symbol'] = i
                st.switch_page("stock_page.py")
        with col3:
            stock_page_graph(i, "5d" ,"1m")
else:
    st.write(''':red[**No followed stock, follow stocks to see them here!**]''')

