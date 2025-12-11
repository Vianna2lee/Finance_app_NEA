import re
from pathlib import Path
import requests
import streamlit as st 
import datetime as dt 
import pandas as pd
import yfinance as yf  # pip install yfinance
import json
from pathlib import Path

DB_FILE = Path("path/to/your/db.txt")

if "stock_list" not in st.session_state or st.session_state["stock_list"] is None:
    st.session_state["stock_list"] = []

if "Username" not in st.session_state:
    st.session_state["Username"] = None



def is_valid_email(email):

    """Check if the email is a valid format."""

    # Regular expression for validating an Email

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    # If the string matches the regex, it is a valid email

    if re.match(regex, email):

        return True
    else:
 
        return False

def create_account(username,password, email):
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    stock_list=[]
    # Write one JSON object per line so the DB file remains text-based
    entry = {"username": username, "password": password, "email": email, "stock_list": stock_list}
    with DB_FILE.open("a", encoding="utf-8") as db:
        db.write(json.dumps(entry, ensure_ascii=False) + "\n")

def username_exists(username_input):
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
                if data.get("username") == username_input:
                    return True
        return False
    except FileNotFoundError:
        return False        

def password_validation(password):
    try:
        if len(password) <8:
            return False
    except:
        return True
  


def password_checker(username, password):
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
                    if data.get("password") == password:
                        st.session_state["Username"] = username
                        st.session_state["stock_list"] = data.get("stock_list", [])
                        return True
        return False
    except FileNotFoundError:
        return False   


def read_all_users():
    users = []
    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    users.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return users


def write_all_users(users):
    tmp = DB_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for u in users:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")
    tmp.replace(DB_FILE)


def add_stock_to_user(username, symbol):
    """Add `symbol` to the user's stock_list if not present. Returns True if added."""
    users = read_all_users()
    modified = False
    for u in users:
        if u.get("username") == username:
            sl = u.get("stock_list")
            if not isinstance(sl, list):
                sl = []
                u["stock_list"] = sl
            if symbol not in sl:
                sl.append(symbol)
                modified = True
            break
    if modified:
        write_all_users(users)
    return modified


def remove_stock_from_user(username, symbol):
    """Remove `symbol` from the user's stock_list if present. Returns True if removed."""
    users = read_all_users()
    modified = False
    for u in users:
        if u.get("username") == username:
            sl = u.get("stock_list")
            if not isinstance(sl, list):
                sl = []
                u["stock_list"] = sl
            if symbol in sl:
                sl.remove(symbol)
                modified = True
            break
    if modified:
        write_all_users(users)
    return modified


def save_stock_list_for_current_user():
    """Persist `st.session_state['stock_list']` for the logged-in user. Returns True on success."""
    username = st.session_state.get("Username")
    if not username:
        return False
    users = read_all_users()
    for i, u in enumerate(users):
        if u.get("username") == username:
            users[i]["stock_list"] = st.session_state.get("stock_list", [])
            write_all_users(users)
            return True
    # user not found: append a new record (unlikely in normal flow)
    users.append({
        "username": username,
        "password": "",
        "email": "",
        "stock_list": st.session_state.get("stock_list", []),
    })
    write_all_users(users)
    return True

def search_stocks(search: str, count: int = 12):  #searh for stocks  yahoo finance , count=no.results   

    q = (search or "").strip()  #remove spave before and after the string 
    if not q:
        return [], None  # empty input = no results
    
    url = "https://query2.finance.yahoo.com/v1/finance/search" #URL that search for stocks

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

def stock_search_suggestions(query: str):
    results, err = search_stocks(query)
    if err or not results:
        return []
    return [f"{r['symbol']} — {r['name']} ({r['exchange']})" for r in results]


def stock_graph(stock_symbol):
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

def stock_box(name,stock_symbol):
    word,button = st.columns([3,2]) 
    with word:
        st.markdown(f"{name} ({stock_symbol})")
        price = yf.Ticker(stock_symbol).fast_info["last_price"]
        price=round(price,2)
        st.markdown(f"***Last stock price: ${price}***")
    with button:
        if st.button("Find out more", key=f"{stock_symbol}_btn"):
            st.session_state['stock_symbol'] = stock_symbol
            st.switch_page("stock_page.py")#
            st.rerun()

    stock_graph(stock_symbol)

def stock_page_graph(stock_symbol, time_period ,time_interval):
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