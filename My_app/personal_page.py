from functions import *
import streamlit as st 
from streamlit_searchbox import st_searchbox # pip install streamlit-searchbox
# streamlit run My_app/navigation_page.py to run the app



if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None:
        st.session_state["stock_searchbox"] = 0

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"])
 


if selected is not None: # new selection made
    st.session_state['stock_symbol'] =  str(selected.split(' — ')[0] )
    st.session_state['stock_searchbox'] += 1 
    st.switch_page("stock_page.py")
    st.rerun()


def get_last_price(symbol):
    price = yf.Ticker(symbol).fast_info["last_price"]
    price=round(price,2)
    st.markdown(f"***Last stock price: ${price}***")








st.title("Personal Page")


st.write(f"Welcome, {st.session_state['Username']}!")

st.header("Followed stock list:")
if len(st.session_state["stock_list"]) > 0:
      for i in st.session_state["stock_list"]:
        col1, col2  = st.columns([70,30])
        with col1:
            st.subheader(f"- {i}")
            st.write(get_last_price(i))
        with col2:
            stock_page_graph(i, "5d" ,"1m")
else:
    st.write(''':red[**No followed stock, save stocks to see them here!**]''')


