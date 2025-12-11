import streamlit as st
from functions import *
from streamlit_searchbox import st_searchbox # pip install streamlit-searchbox
#pip install lxml
 # pip install yahoo_fin pip install yahoo_fin --upgrade   
# import plotly.graph_objects as go #pip install plotly use for later 

# streamlit run My_app/navigation_page.py to run the app


if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None:
    st.session_state["stock_searchbox"] = 0

if "stock_symbol" not in st.session_state or st.session_state["stock_symbol"] is None:
    st.session_state["stock_symbol"] = "blank"

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"])
 
col_left, col_mid, col_right = st.columns([80,10,10])
if col_right.button("refresh"):
    st.cache_data.clear()
    st.rerun()

if selected is not None: 
    st.session_state['stock_symbol'] = selected.split(' — ')[0] 
    st.session_state['stock_searchbox'] += 1 
    st.switch_page("stock_page.py")
    st.rerun()



stock_symbol =st.session_state['stock_symbol']
stock_name = yf.Ticker(stock_symbol).info.get('longName')

current_time = pd.Timestamp.now(tz="America/New_York")


#def follow_stock(username, stock_symbol):



left, right = st.columns([80,20])

with left:
    st.title(f"{st.session_state['stock_symbol']} - {stock_name}" )
    #add stock logo later on
with right:
    star = st.checkbox("Follow this stock")
    


def create_account(username,password, email):
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    stock_list=[]
    # Write one JSON object per line so the DB file remains text-based
    entry = {"username": username, "password": password, "email": email, "stock_list": stock_list}
    with DB_FILE.open("a", encoding="utf-8") as db:
        db.write(json.dumps(entry, ensure_ascii=False) + "\n")

if star:
    if st.session_state["logged_in"]==True:
        
        st.success(f"You are now following {stock_symbol}!")
    else:
        st.error("Please log in to follow stocks.")
        st.switch_page("login_page.py")




price= yf.Ticker(stock_symbol).fast_info["last_price"]
price= round(price,4)
st.subheader(price)

st.markdown(f"As of {current_time}")






col1, col2 = st.columns(2)
with col1:
    time_period = st.selectbox(
        "time period",
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

with st.container(border=True):
    st.subheader('Statistics: ')
    col3, col4=st.columns(2)
    with col3:
        st.markdown(f"**Previous close** : {stock_symbol.info['previousClose']}")
        st.markdown(f"**Opening price of the day** : {stock_symbol.info['open']}")
        st.markdown(f"**Lowest price today** : {stock_symbol.info['dayLow']}")
        st.markdown(f"**Highest price today** : {stock_symbol.info['dayHigh']}")
        st.markdown(f"**Day's Range** : {stock_symbol.info['dayHigh']}-{stock_symbol.info['dayLow']}")
        st.markdown(f"**52 Week Range** : {stock_symbol.info['fiftyTwoWeekLow']} - {stock_symbol.info['fiftyTwoWeekHigh']}")
        st.markdown(f"**Volume** : {stock_symbol.info['volume']}")
        st.markdown(f"**Avg. Volume** : {stock_symbol.info['averageDailyVolume3Month']}")
    with col4:
        st.markdown(f"**Market Cap (intraday)** : {stock_symbol.info['marketCap']}")
        st.markdown(f"**Beta** : {stock_symbol.info['beta']}")
        st.markdown(f"**PE Ratio (TTM)** : {stock_symbol.info['trailingPE']}")
        st.markdown(f"**EPS (TTM)** : {stock_symbol.info['trailingEps']}")
        st.markdown(f"**Forward Dividend & Yield** : {stock_symbol.info['dividendYield']}")
        st.markdown(f"**Ex-Dividend Date** : {stock_symbol.info['exDividendDate']}")
        st.markdown(f"**1 year Target Est** : {stock_symbol.info['targetMeanPrice']}")



st.subheader("Performance charts & data:")


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