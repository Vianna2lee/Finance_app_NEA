import re
from pathlib import Path
import requests
import streamlit as st 
import datetime as dt 
import pandas as pd
import yfinance as yf  # pip install yfinance
import json
from pathlib import Path
import math


#modified - changed to more human like
# no need to modify - don't need to change, but can be made more efficient
# done - already done, don't change 



DB_FILE = Path("path/to/your/db.txt")

if "stock_list" not in st.session_state or st.session_state["stock_list"] is None:
    st.session_state["stock_list"] = []

if "Username" not in st.session_state:
    st.session_state["Username"] = None



def is_valid_email(email): #check if the email is in valid format #modified

    pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    return (re.match(pattern, email) is not None)#retun true if the email is valid, false if not valid


def create_account(username,password, email): #modified
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    stock_list=[]
    # Write one JSON object per line so the DB file remains text-based
    entry = {"username": username, 
             "password": password, 
             "email": email, 
             "stock_list": stock_list}
    with DB_FILE.open("a", encoding="utf-8") as db:
        db.write(json.dumps(entry, ensure_ascii=False) + "\n")

    st.session_state["Username"] = username
    st.session_state["stock_list"]= stock_list


def username_exists(username_input): #modified
    found = False
    with DB_FILE.open("r", encoding="utf-8") as db:
        for line in db:
            line = line.strip()
            if line:
                data = json.loads(line)
                if data.get("username") == username_input:
                    found = True
                    break      
    return found

  

def password_validation(password): #modified
    match = False
    if len(password) <8:
        match = False
    else:
        match = True
    return match
  


def password_checker(username, password): #modified
    checked = False
    with DB_FILE.open("r", encoding="utf-8") as db:
        for line in db:
            line = line.strip()
            if not line:
                continue  
            data = json.loads(line)  
            if data.get("username") == username:
                if data.get("password") == password:
                    st.session_state["Username"] = username
                    st.session_state["stock_list"] = data.get("stock_list", [])
                    checked = True
                    break

        return checked  



def search_stocks(search: str, count: int = 12):  #searh for stocks  yahoo finance , count=no.results   ** change it later

    url = "https://query2.finance.yahoo.com/v1/finance/search"

    q = (search or "").strip()  #remove spave before and after the string 
    if not q:
        return [], None  # empty input = no results
    
    
    params = {
        "q": q, # the string user want to search
        "quotesCount": count,  #no. of results to return
        "newsCount": 10,  #no. of news required
        "enableFuzzyQuery": True, #it will guess the closest match
        "quotesQueryID": "tss_match_phrase_query", #tell yahoo I am searching for stock tickers not data 
        "lang": "en-US",  #english 
        "region": "US"  #on US market
    }

    headers = {"User-Agent": "Mozilla/5.0"} # tell yahoo we are a browser

    try: #send request and handle errors
        r= requests.get(url, params=params, headers=headers, timeout=8) #send the request to yahoo, url is the link, parms is all the requirement, timeout ask it to stop after 8 sec
        r.raise_for_status() #if there is an error e.g 404 500, stop the program
        data = r.json() #convert the response to json format  so it iis like a python dictionary
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"  #return empty results and the error message, so it won't crash
    
    results = []
    for item in data.get("quotes", []):  #go through each result in the dict
        sym = item.get("symbol")  #get the stock ticker symbol
        if not sym:
            continue  #skip if no symbol 
        results.append({
            "symbol": sym,
            "name": item.get("shortname") or item.get("longname") or "",  #company name
            "exchange": item.get("exchDisp") or "",  #exchange name
            "security_type": item.get("typeDisp") or "",  #type of security e.g equity etf
        })
    return results, None


def stock_search_suggestions(query: str):  # Modified 
    lst =[]
    results, err = search_stocks(query)
    if err or not results:
        lst = []
    else:
        for r in results:
            lst.append(f"{r['symbol']} - {r['name']} ({r['exchange']})")
    return lst


def stock_graph(stock_symbol): # no need to modify
    market_open  = pd.Timestamp.now(tz="America/New_York").replace(hour=9,  minute=30, second=0) # market open
    market_close = pd.Timestamp.now(tz="America/New_York").replace(hour=16, minute=0, second=0) #market close
    current_time = pd.Timestamp.now(tz="America/New_York")
    current_date = dt.date.today()
    if market_open<=current_time<=market_close and 1<=int(current_date.strftime("%w"))<=5:
        stock_data = yf.download(stock_symbol, period="1d", interval="2m") 
    else:
        st.markdown(''':red[Market is closed. Graph for this month]''')
        stock_data = yf.download(stock_symbol, period="1mo", interval="1d")
    st.line_chart(stock_data['Close'], height="content",use_container_width=True)

def stock_box(name,stock_symbol):# no need to modify
    word,button = st.columns([3,2]) 
    with word:
        st.markdown(f"{name} ({stock_symbol})")
        price = yf.Ticker(stock_symbol).fast_info["last_price"]
        price=round(price,2)
        st.markdown(f"***Last stock price: ${price}***")
    with button:
        if st.button("Find out more", key=f"{stock_symbol}_btn"):
            st.session_state['stock_symbol'] = stock_symbol
            st.switch_page("stock_page.py")
            st.rerun()
    stock_graph(stock_symbol)

def stock_page_graph(stock_symbol, time_period ,time_interval): #no need to modify
    market_open  = pd.Timestamp.now(tz="America/New_York").replace(hour=9,  minute=30, second=0) # market open
    market_close = pd.Timestamp.now(tz="America/New_York").replace(hour=16, minute=0, second=0) #market close
    current_time = pd.Timestamp.now(tz="America/New_York")
    current_date = dt.date.today()
    if market_open<=current_time<=market_close and 1<=int(current_date.strftime("%w"))<=5:
        stock_data = yf.download(stock_symbol, period=time_period, interval=time_interval)
    else:
        st.markdown(''':red[Market is closed]''')
        stock_data = yf.download(stock_symbol, period=time_period, interval=time_interval)

    st.line_chart(stock_data["Close"], height="content",use_container_width=True)


def check_data(username, stock_symbol): ##!!! need to fix, personal page not working 
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
                for i in data.get("stock_list"):
                    if i == stock_symbol:
                        return True
                return False

def update_stock_variable(username):  ##!!! need to fix, personal page not working 
    with DB_FILE.open("r", encoding="utf-8") as db:
        for line in db:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if data.get("username") == username:
                    st.session_state["stock_list"] = data.get("stock_list", [])
                    break 
                

    
def follow_stock(username, stock_symbol): ##!!! need to fix, personal page not working 
    try:
        data = []
        with DB_FILE.open("r", encoding="utf-8") as db:
            for i in db:
                i = i.strip()
                if i != "":
                    data.append(json.loads(i))
    except FileNotFoundError:
        data = []

    for i in data:
        if i["username"] == username:
            stocklist = i.get("stock_list") or []
            if stock_symbol not in stocklist:
                stocklist.append(stock_symbol)
            i["stock_list"] = stocklist
  
    temp = DB_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as db:
        for i in data:
            db.write(json.dumps(i, ensure_ascii=False) + "\n")
    temp.replace(DB_FILE)
    update_stock_variable(st.session_state['Username'])







def get_last_price(symbol): #done
    price = yf.Ticker(symbol).fast_info["last_price"]
    price=round(price,2)
    st.markdown(f"***Last stock price: ${price}***")



def unfollow_stock(username, stock_symbol): ##!!! need to fix, personal page not working 
    try:
        data = []
        with DB_FILE.open("r", encoding="utf-8") as db:
            for i in db:
                i = i.strip()
                if i != "":
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
    update_stock_variable(st.session_state['Username'])