import streamlit as st
from functions import *
from streamlit_searchbox import st_searchbox # pip install streamlit-searchbox
from datetime import datetime
import time
import pytz
#pip install lxml
 # pip install yahoo_fin pip install yahoo_fin --upgrade   
# import plotly.graph_objects as go #pip install plotly use for later 

# streamlit run My_app/navigation_page.py to run the app


if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None:
    st.session_state["stock_searchbox"] = 0

if "stock_symbol" not in st.session_state or st.session_state["stock_symbol"] is None:
    st.session_state["stock_symbol"] = None
    st.info("Please search a stock to view")
    st.stop()

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"])

col_left, col_mid, col_right = st.columns([80,10,10])
if col_right.button("refresh"):
    st.cache_data.clear()
    st.rerun()

if selected is not None: 
    st.session_state['stock_symbol'] = selected.split(' - ')[0] 
    st.session_state['stock_searchbox'] += 1 
    st.switch_page("stock_page.py")
    st.rerun()



stock_symbol =st.session_state['stock_symbol'] 
stock_name = yf.Ticker(stock_symbol).info.get('longName')


left, right = st.columns([80,20])

with left:
    st.title(f"{st.session_state['stock_symbol']} - {stock_name}" )
    #add stock logo later on
with right:
    star = st.button( "Follow stock")
    


if star==True:
    if st.session_state["logged_in"]==True:
        if check_data(st.session_state["Username"], stock_symbol) == False:
            follow_stock(st.session_state["Username"], stock_symbol)
            st.success(f"You are now following {stock_symbol}!")
        elif check_data(st.session_state["Username"], stock_symbol) == True:
            st.error("You are already following this stock.")
    else:
        st.error("You need to be logged in to follow stocks.")
        st.switch_page("login_page.py")




def get_stock_price(stock_symbol):
    fi = yf.Ticker(stock_symbol).fast_info
    price = fi.get("last_price",None)
    if price is None:
        price= fi.get("lastPrice",None)
    return round(price,4)


st.subheader(get_stock_price(stock_symbol))

current_time = pd.Timestamp.now(tz="America/New_York")
st.markdown(f"As of {current_time}")






col1, col2 = st.columns(2)
with col1:
    time_period = st.selectbox(
        "Time period",
        ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),
        index=4
    )

with col2:
    if time_period == "1d":
        time_interval = st.selectbox(
        "Time interval:",
        ("1m", "2m", "5m", "15m", "30m", "60m", "1h"),
        index=4
    )
    elif time_period == "5d":
            time_interval = st.selectbox(
            "Time interval:",
            ("1m", "2m", "5m", "15m", "30m", "60m", "1h", "1d"),
            index=4
            )
    elif time_period == "1mo":
            time_interval = st.selectbox(
            "Time interval:",
            ("1m", "2m", "5m", "15m", "30m", "1h", "1d","5d"),
            index=4
            )
    elif time_period == "3mo":
            time_interval = st.selectbox(
            "Time interval:",
            ("1h", "1d","5d" ,"1wk", "1mo"),
            index=4
            )
    else:
            time_interval = st.selectbox(
                "Time interval:",
                ("1d", "5d", "1wk", "1mo","3mo"),
                index=1
            )


graph=stock_page_graph(st.session_state['stock_symbol'], time_period ,time_interval)
# use plotly_chart() for it to be interactive

stock_symbol = yf.Ticker(stock_symbol)

def format_output(value):  ##
    if value == None:
        return "N/A"
    elif isinstance(value, float) and math.isnan(value):
        return round(value, 2)
    else:
        return value



with st.container(border=True):
    st.subheader('Statistics: ')
    col3, col4=st.columns(2)
    with col3:
        st.markdown(f"**Previous close** : {format_output(stock_symbol.info.get('previousClose'))}")
        st.markdown(f"**Opening price of the day** : {format_output(stock_symbol.info.get('open'))}")
        st.markdown(f"**Lowest price today** : {format_output(stock_symbol.info.get('dayLow'))}")
        st.markdown(f"**Highest price today** : {format_output(stock_symbol.info.get('dayHigh'))}")
        st.markdown(f"**Day's Range** : {format_output(stock_symbol.info.get('dayHigh'))}-{format_output(stock_symbol.info.get('dayLow'))}")
        st.markdown(f"**52 Week Range** : {format_output(stock_symbol.info.get('fiftyTwoWeekLow'))} - {format_output(stock_symbol.info.get('fiftyTwoWeekHigh'))}")
        st.markdown(f"**Volume** : {format_output(stock_symbol.info.get('volume'))}")
        st.markdown(f"**Avg. Volume** : {format_output(stock_symbol.info.get('averageDailyVolume3Month'))}")
    with col4:
        st.markdown(f"**Market Cap (intraday)** : {format_output(stock_symbol.info.get('marketCap'))}")
        st.markdown(f"**Beta** : {format_output(stock_symbol.info.get('beta'))}")
        st.markdown(f"**PE Ratio (TTM)** : {format_output(stock_symbol.info.get('trailingPE'))}")
        st.markdown(f"**EPS (TTM)** : {format_output(stock_symbol.info.get('trailingEps'))}")
        st.markdown(f"**Forward Dividend & Yield** : {format_output(stock_symbol.info.get('dividendYield'))}")
        st.markdown(f"**Ex-Dividend Date** : {format_output(stock_symbol.info.get('exDividendDate'))}")
        st.markdown(f"**1 year Target Est** : {format_output(stock_symbol.info.get('targetMeanPrice'))}")



st.subheader("Performance chart & data:")


price = stock_symbol.history(period="2y")

close = price["Close"]
ma50=price['Close'].rolling(50).mean()
ma150=price['Close'].rolling(150).mean()
ma200=price['Close'].rolling(200).mean()


graph= pd.DataFrame({
    "Price":close
})

col5,col6,col7 = st.columns(3)

with col5:
    ma_50 = st.checkbox("show 50 days moving average")
with col6:
    ma_150 = st.checkbox("show 150 days moving average")
with col7:
    ma_200 = st.checkbox("show 200 days moving average")

if ma_50:
    graph["ma50"] = ma50

if ma_150:
    graph["ma150"] = ma150
    
if ma_200:
    graph["ma200"] = ma200

st.line_chart(graph)
st.markdown(f"As of {current_time}")
 
# can add more data e.g company insights and financial highlights later on 


with st.container(border=True):
    st.subheader("Earnings trend and info:")
    earning_info = stock_symbol.get_earnings_dates()
    st.write(earning_info)
   






#formate the num better, use T or , between nums
#formate the informaation buton to circle, add button (dialog)