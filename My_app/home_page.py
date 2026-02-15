from streamlit_searchbox import st_searchbox
from functions import *
import pandas as pd
import yfinance as yf # pip install yfinance
import streamlit as st
import datetime as dt 
st.set_page_config(layout="wide")

# need to install streamlit-searchbox by trying: pip install streamlit-searchbox
# run with: streamlit run My_app/home_page.py
# streamlit run My_app/navigation_page.py to run the app


# initialise session state variables
if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None: 
    st.session_state["stock_searchbox"] = 0


selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...", key=st.session_state["stock_searchbox"])
 


if selected is not None: 
    st.session_state['stock_symbol'] =  str(selected.split(' - ')[0] )
    st.session_state['stock_searchbox'] += 1 # key changes so searchbox resets after a stock is picked
    st.switch_page("stock_page.py")
    st.rerun()





col_left, col_mid, col_right = st.columns([80,10,10]) #the layout of the page with three columns

if col_right.button("refresh"): #create a refresh button on the right side of the page
    st.cache_data.clear() #if clicked, clear the cache
    st.rerun() #rerun app


st.header("Overview of the stock market today") #header of the page

# Indices 
st.subheader("Indices:") #subheader for indices section
col1, col2, col3 = st.columns(3) #three columns for three major indices
with col1:
    stock_box("S&P 500", "SPY")
with col2:
    stock_box("Dow Jones", "DIA")
with col3:
    stock_box("NASDAQ-100", "QQQ")

st.subheader("Performance of each sector:") #subheader for sector performance section

# technology sector 
st.subheader("Technology Sector") #subheader for technology sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("Apple Inc.", "AAPL")
with col2:
    stock_box("Microsoft Corp.", "MSFT")
with col3:
    stock_box("NVIDIA Corp.", "NVDA")

# health care sector
st.subheader("Health Care Sector") #subheader for health care sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("UnitedHealth Group Inc.", "UNH")
with col2:
    stock_box("Johnson & Johnson", "JNJ")
with col3:
    stock_box("Pfizer Inc.", "PFE")

#financials sector
st.subheader("Financials Sector") #subheader for financials sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("JPMorgan Chase & Co.", "JPM")
with col2:
    stock_box("Bank of America Corp.", "BAC")
with col3:
    stock_box("Wells Fargo & Co.", "WFC")

#consumer discretionary sector 
st.subheader("Consumer Discretionary Sector") #subheader for consumer discretionary sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("Amazon.com Inc.", "AMZN")
with col2:
    stock_box("Tesla Inc.", "TSLA")
with col3:
    stock_box("The Home Depot Inc.", "HD")

#communication services sector 
st.subheader("Communication Services Sector") #subheader for communication services sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("Alphabet Inc.", "GOOGL")
with col2:
    stock_box("Meta Platforms Inc.", "META")
with col3:
    stock_box("Netflix Inc.", "NFLX")

# industrials sector 
st.subheader("Industrials Sector") #subheader for industrials sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("The Boeing Company", "BA")
with col2:
    stock_box("Caterpillar Inc.", "CAT")
with col3:
    stock_box("Honeywell International Inc.", "HON")

#consumer staples sector 
st.subheader("Consumer Staples Sector") #subheader for consumer staples sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("Procter & Gamble Co.", "PG")
with col2:
    stock_box("The Coca-Cola Company", "KO")
with col3:
    stock_box("Costco Wholesale Corp.", "COST")

#energy sector 
st.subheader("Energy Sector") #subheader for energy sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("Exxon Mobil Corp.", "XOM")
with col2:
    stock_box("Chevron Corp.", "CVX")
with col3:
    stock_box("ConocoPhillips", "COP")

# utilities sector
st.subheader("Utilities Sector") #subheader for utilities sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("NextEra Energy Inc.", "NEE")
with col2:
    stock_box("Duke Energy Corp.", "DUK")
with col3:
    stock_box("The Southern Company", "SO")

#  real estate sector
st.subheader("Real Estate Sector") #subheader for real estate sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("American Tower Corp.", "AMT")
with col2:
    stock_box("Prologis Inc.", "PLD")
with col3:
    stock_box("Realty Income Corp.", "O")

# materials sector
st.subheader("Materials Sector") #subheader for materials sector
col1, col2, col3 = st.columns(3)
with col1:
    stock_box("Linde plc", "LIN")
with col2:
    stock_box("Nucor Corp.", "NUE")
with col3:
    stock_box("The Sherwin-Williams Company", "SHW")





# use middle baseline , and change color based on positive or negative change
#make teh y axis smaller to zoom in graph use Altair
# create auto refresh every minute during market hours






