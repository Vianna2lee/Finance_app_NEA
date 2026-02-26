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


if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None: # if the variable is non then set it to 0
    st.session_state["stock_searchbox"] = 0

if "stock_symbol" not in st.session_state or st.session_state["stock_symbol"] is None: #if variable is none or empty then set to none 
    st.session_state["stock_symbol"] = None
    st.info("Please search a stock to view") 
    st.stop()

selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"]) #search bar 

col_left, col_mid, col_right = st.columns([80,10,10])
if col_right.button("refresh"): #refresh button
    st.cache_data.clear()
    st.rerun() #rerun page

if selected is not None: #when stock is selected 
    st.session_state['stock_symbol'] = selected.split(' - ')[0] #stock symbol is saved in this variable
    st.session_state['stock_searchbox'] += 1 #change this variable so it know it is changed
    st.switch_page("stock_page.py")# switch tostock page
    st.rerun() #rerun page



stock_symbol =st.session_state['stock_symbol'] 
stock_name = yf.Ticker(stock_symbol).info.get('longName') #get stock long name


left, right = st.columns([80,20]) #formatting of page 

with left:
    st.title(f"{st.session_state['stock_symbol']} - {stock_name}" ) #stock symbol and name is on the top of page
    #add stock logo later on
with right:
    star = st.button( "Follow stock") #follow stock button 
    


if star==True:
    if st.session_state["logged_in"]==True: #if the user is logged in
        if check_data(st.session_state["Username"], stock_symbol) == False: #check if the user is already following the stock
            follow_stock(st.session_state["Username"], stock_symbol) #add stock to stock list 
            st.success(f"You are now following {stock_symbol}!") #to show that the user is now following the stock
        elif check_data(st.session_state["Username"], stock_symbol) == True: #check if the user is already following the stock
            st.error("You are already following this stock.") #tell user thay are already following it 
    else:
        st.switch_page("login_page.py") # switch page to login page
        st.error("You need to be logged in to follow stocks.") #tell them the reason 




def get_stock_price(stock_symbol):  #function to get stock price
    fi = yf.Ticker(stock_symbol).fast_info #get info for stock
    price = fi.get("last_price",None) #if get last_price, set to none if not found
    if price is None: # if none
        price= fi.get("lastPrice",None) #try to use this key instead
    return round(price,4) #round the price to 4 decimal places


st.subheader(get_stock_price(stock_symbol)) #show stock price in subheading

current_time = pd.Timestamp.now(tz="America/New_York") # get current US time 
st.markdown(f"As of {current_time}") #show user when was it last updated 






col1, col2 = st.columns(2)
with col1:
    time_period = st.selectbox(
        "Time period",
        ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),
        index=4
    )

with col2:
    if time_period == "1d": #options for users to select time period and time interval
        time_interval = st.selectbox( #time interval is based on the time period user selected 
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


graph=stock_page_graph(st.session_state['stock_symbol'], time_period ,time_interval)  #show stock graph 

# later use plotly_chart() for it to be interactive

stock_symbol = yf.Ticker(stock_symbol)

def format_output(value):  #formate the output
    if value == None: #if value is none 
        return "N/A" #show N/A
    elif isinstance(value, float) and not math.isnan(value): #if value is a float and is not not a number 
        return round(value, 2) #it is rounded to 2dp
    else:
        return value #else return orginal value



with st.container(border=True):
    st.subheader('Statistics: ') #show the statistics
    col3, col4=st.columns(2) #formatting 
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



st.subheader("Performance chart & data:") #title for performance chart and data


price = stock_symbol.history(period="2y") # a graph for a 2 year period 

close = price["Close"] #get closing price 
ma50=price['Close'].rolling(50).mean() #50 days moving average 
ma150=price['Close'].rolling(150).mean() #150 days moving average
ma200=price['Close'].rolling(200).mean() #200 days moving average 


graph= pd.DataFrame({ #the data for the graph 
    "Price":close #must include the price line, other lines are optional 
})

col5,col6,col7 = st.columns(3)

with col5:
    ma_50 = st.checkbox("show 50 days moving average") #checkbox for 50 days average 
with col6:
    ma_150 = st.checkbox("show 150 days moving average")#checkbox for 150 days average 
with col7:
    ma_200 = st.checkbox("show 200 days moving average")#checkbox for 200 days average 

if ma_50:
    graph["ma50"] = ma50 #if checkbox is selected, add line for 50 moving average 
if ma_150:
    graph["ma150"] = ma150#if checkbox is selected, add line for 150 moving average 
    
if ma_200:
    graph["ma200"] = ma200#if checkbox is selected, add line for 200 moving average 

st.line_chart(graph) #show graph
st.markdown(f"As of {current_time}") # time for when teh graph was last updated  
 
# can add more data e.g company insights and financial highlights later on 


with st.container(border=True): #form to show earning info
    st.subheader("Earnings trend and info:") #subheading 
    earning_info = stock_symbol.get_earnings_dates() #get data
    st.write(earning_info) #show them
   






#formate the num better, use T or , between nums
#formate the informaation buton to circle, add button (dialog)