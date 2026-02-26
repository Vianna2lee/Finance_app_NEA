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

if "stock_list" not in st.session_state or st.session_state["stock_list"] is None: #if variabel is empty or none set to blank list 
    st.session_state["stock_list"] = []

if "Username" not in st.session_state: #if variabel is empty set to none
    st.session_state["Username"] = None



def is_valid_email(email): #check if the email is in valid format 

    pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    return (re.match(pattern, email) is not None)#retun true if the email is valid, false if not valid


def create_account(username,password, email): #create account function 
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    stock_list=[]
    # Write one JSON object per line so the DB file remains text-based
    entry = {"username": username, 
             "password": password,  
             "email": email, 
             "stock_list": stock_list} #creata a dict to store data 
    with DB_FILE.open("a", encoding="utf-8") as db: #open file 
        db.write(json.dumps(entry, ensure_ascii=False) + "\n") #write data

    st.session_state["Username"] = username #store username in variable
    st.session_state["stock_list"]= stock_list #store stock list in variabel 


def username_exists(username_input): #functaion to check if username exist 
    found = False #set found as false
    with DB_FILE.open("r", encoding="utf-8") as db: #oprn file to read
        for line in db: #reaqd every line 
            line = line.strip() #remove empty space 
            if line:
                data = json.loads(line) #convert line to dict 
                if data.get("username") == username_input: #check if username matches
                    found = True #set to true of found 
                    break      
    return found

  

def password_validation(password): #function to check if password is valid
    match = False #set match to false
    if len(password) <8: #if length is less tahn 8 
        match = False #false
    else: 
        match = True #set to true if greate 
    return match
  


def password_checker(username, password): #function for login, check if the username and password match
    checked = False
    with DB_FILE.open("r", encoding="utf-8") as db: #open file to read
        for line in db:
            line = line.strip() #remove empthy space
            if not line:
                continue  
            data = json.loads(line)  #convert line to dict 
            if data.get("username") == username: #if username matches
                if data.get("password") == password: #if password matches
                    st.session_state["Username"] = username #set variable to username
                    st.session_state["stock_list"] = data.get("stock_list", []) #set variabel to stock list if exist if not then assign []
                    checked = True #return true 
                    break

        return checked  



def search_stocks(search: str, count: int = 12):  #function for teh search bar 

    url = "https://query2.finance.yahoo.com/v1/finance/search" # search api endpoint

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
    return results, None #return the result and no error


def stock_search_suggestions(query: str):  # function for the suggestion in search bar 
    lst =[]
    results, err = search_stocks(query) #call search stock function 
    if err or not results:#if non then return empty list 
        lst = []
    else:
        for r in results:
            lst.append(f"{r['symbol']} - {r['name']} ({r['exchange']})") #output format for suggestion 
    return lst


def stock_graph(stock_symbol): # function for stock graph 
    market_open  = pd.Timestamp.now(tz="America/New_York").replace(hour=9,  minute=30, second=0) # market open
    market_close = pd.Timestamp.now(tz="America/New_York").replace(hour=16, minute=0, second=0) #market close
    current_time = pd.Timestamp.now(tz="America/New_York") #current time
    current_date = dt.date.today() #current date
    if market_open<=current_time<=market_close and 1<=int(current_date.strftime("%w"))<=5: #if market is open, show graph for today 
        stock_data = yf.download(stock_symbol, period="1d", interval="2m") 
    else:
        st.markdown(''':red[Market is closed. Graph for this month]''') #tell user marcket is closed and shw graph for this month 
        stock_data = yf.download(stock_symbol, period="1mo", interval="1d")
    st.line_chart(stock_data['Close'], height="content",use_container_width=True) #draw graph 

def stock_box(name,stock_symbol):# function for the stock box on home page 
    word,button = st.columns([3,2])  #format 
    with word:
        st.markdown(f"{name} ({stock_symbol})") #name and symbol 
        price = yf.Ticker(stock_symbol).fast_info["last_price"] #get stock price 
        price=round(price,2) #round it up 
        st.markdown(f"***Last stock price: ${price}***")#show info
    with button:
        if st.button("Find out more", key=f"{stock_symbol}_button"): #button for more info 
            st.session_state['stock_symbol'] = stock_symbol #store in variable 
            st.switch_page("stock_page.py") #switch page 
            st.rerun() #rerun 
    stock_graph(stock_symbol) #show graph 

def stock_page_graph(stock_symbol, time_period ,time_interval): #function for stock graph 
    market_open  = pd.Timestamp.now(tz="America/New_York").replace(hour=9,  minute=30, second=0) # market open
    market_close = pd.Timestamp.now(tz="America/New_York").replace(hour=16, minute=0, second=0) #market close
    current_time = pd.Timestamp.now(tz="America/New_York")#current time
    current_date = dt.date.today()#current time
    if market_open<=current_time<=market_close and 1<=int(current_date.strftime("%w"))<=5: #if market is open
        stock_data = yf.download(stock_symbol, period=time_period, interval=time_interval) 
    else:
        st.markdown(''':red[Market is closed]''') #tell user market is closed
        stock_data = yf.download(stock_symbol, period=time_period, interval=time_interval)

    st.line_chart(stock_data["Close"], height="content",use_container_width=True) #show graph


def check_data(username, stock_symbol): #function to check if user is alreading folowing stock 
    with DB_FILE.open("r", encoding="utf-8") as db:
        for line in db: #read each lin
            line = line.strip() #remove empty space 
            if not line:
                continue
            try:
                data = json.loads(line) #convert line to dict 
            except Exception:
                continue
            if data.get("username") == username: #if username matches
                for i in data.get("stock_list"): #get stock list 
                    if i == stock_symbol: #reaf each stock in stock list until it matches
                        return True #true when found 
                return False #flase if nont foun d 

def update_stock_variable(username):  #funcation to update stocklist after follow and unfollow stock 
    with DB_FILE.open("r", encoding="utf-8") as db: #open read stock 
        for line in db: #read every line 
            line = line.strip() #remove empty space 
            if not line:
                continue
            data = json.loads(line)
            if data.get("username") == username: #if username matches
                    st.session_state["stock_list"] = data.get("stock_list", []) # set stocklist to the stock list in file, if not found, set to none 
                    break 
                

    
def follow_stock(username, stock_symbol): #function when follow stock is clicked
    try:
        data = []
        with DB_FILE.open("r", encoding="utf-8") as db: #open file to read
            for i in db: #read every line
                i = i.strip()# remove empty space
                if i != "": #if line is not empty, convert to dict 
                    data.append(json.loads(i)) #add to list
    except FileNotFoundError: #if error 
        data = [] #set to empty list 

    for i in data: # for eveer item in list 
        if i["username"] == username: #if username matches
            stocklist = i.get("stock_list") or [] #get ~~ change to noraml if statement 
            if stock_symbol not in stocklist: #if stock is not in list, add to list 
                stocklist.append(stock_symbol) # add stock to list
            i["stock_list"] = stocklist #update stock list in dict


    temp = DB_FILE.with_suffix(".tmp") #create a temporary file 
    with temp.open("w", encoding="utf-8") as db: #open file
        for i in data: #for each data 
            db.write(json.dumps(i, ensure_ascii=False) + "\n") #wite file 
    temp.replace(DB_FILE) #replace old file 
    update_stock_variable(st.session_state['Username']) #update stock variable to update stock list 







def get_last_price(symbol): #funcation to get last stock price 
    price = yf.Ticker(symbol).fast_info["last_price"] #get price
    price=round(price,2) #rounding 
    st.markdown(f"***Last stock price: ${price}***") #show price 



def unfollow_stock(username, stock_symbol): #function to unfollow stock 
    try:
        data = [] #create list 
        with DB_FILE.open("r", encoding="utf-8") as db: #open file
            for i in db: #every item
                i = i.strip() #remove empty space
                if i != "": #if not empty, convert to dict  and add to list 
                    data.append(json.loads(i)) #add to list 
    except FileNotFoundError: #except error
        data = [] #return empty list 

    for i in data: #for ever item every item 
        if i["username"] == username: #if username matches
            stocklist = i.get("stock_list") or [] ## chang to normal if statement 
            if stock_symbol in stocklist: #if stock is in list 
                stocklist.remove(stock_symbol) #remove stock 
            i["stock_list"] = stocklist #update stock list 
    
    
    temp = DB_FILE.with_suffix(".tmp") #create a temporary file 
    with temp.open("w", encoding="utf-8") as db: #open file 
        for i in data: #in every item 
            db.write(json.dumps(i, ensure_ascii=False) + "\n") #wite file 
    temp.replace(DB_FILE) #replace old file
    update_stock_variable(st.session_state['Username']) #update stock variable 

