from functions import *
import streamlit as st 
from streamlit_searchbox import st_searchbox # pip install streamlit-searchbox
# streamlit run My_app/navigation_page.py to run the app



if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None:
        st.session_state["stock_searchbox"] = 0

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"])
 


def update_stock_variable(username):
    try:
        with DB_FILE.open("r", encoding="utf-8") as db:
            for line in db:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if data.get("username") == username:
                        st.session_state["Username"] = username
                        st.session_state["stock_list"] = data.get("stock_list", [])
                        break 
    except FileNotFoundError:
        pass 

update_stock_variable(st.session_state['Username'])

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
        col1, col2  = st.columns([30,70])
        with col1:
            st.subheader(f"- {i}")
            get_last_price(i)
        with col2:
            stock_page_graph(i, "5d" ,"1m")
else:
    st.write(''':red[**No followed stock, save stocks to see them here!**]''')

def unfollow_stock(username, stock_symbol):
    try:
        data = []
        with DB_FILE.open("r", encoding="utf-8") as db:
            for i in db:
                i = i.strip()
                data.append(json.loads(i))
    except FileNotFoundError:
        data = []

    for i in data:
        if i["username"] == username:
            stocklist = i.get("stock_list") or []
            if stock_symbol in stocklist:
                stocklist.remove(stock_symbol)
            i["stock_list"] = stocklist
    
    
    temp = DB_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as db:
        for i in data:
            db.write(json.dumps(i, ensure_ascii=False) + "\n")
    temp.replace(DB_FILE)