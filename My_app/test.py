def search_stocks(search,count):  #searh for stocks  yahoo finance , count=no.results   

    url = "https://query2.finance.yahoo.com/v1/finance/search"

    results =[]
    error = None

    q = (search or "").strip()  #remove spave before and after the string 
    if not q:
        return [], None  # empty input = no results
    
    if q:
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

    def check_data(username, stock_symbol):
    result = False
    try: 
        with DB_FILE.open("r", encoding="utf-8") as db:
            for line in db:
                line = line.strip()
                if not line:
                    continue
                else:
                    data = json.loads(line)

                if data.get("username") == username:
                    for i in data.get("stock_list"):
                        if i == stock_symbol:
                            result = True
                            break
                        else:
                            result = False
    except Exception:
        st.error("An error occurred while checking the data.")
        result = False

    return result