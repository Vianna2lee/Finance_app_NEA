import streamlit as st
from functions import *
import numpy as np

if not hasattr(np, "float"): 
    np.float = float

from optionprice import Option #pip install option-price
from streamlit_searchbox import st_searchbox
import datetime
import numpy as np #pip install --upgrade numpy

# streamlit run My_app/navigation_page.py to run the app


#https://pypi.org/project/option-price/ website 

st.title("Option Price Calculator") #title of page

if "stock_searchbox" not in st.session_state or st.session_state["stock_searchbox"] is None: #set if stock_searchbox is not in session state variable 
        st.session_state["stock_searchbox"] = 0 #set to 0



option_type,option_kind,approach,s0,strike_price,volatility_of_stock,risk_free_interest_rate,start_date,end_date= (None,)*9 #set all variables to none 

option_type = st.pills("Option type", ["European option", "American option"],default="European option", selection_mode="single") #pills for option type 

if option_type == "European option":
    option_type = True #set to true for European option
else:
    option_type = False #set to false for American option




option_kind = st.pills("Option kind",["Call option", "Put option"],default="Call option",selection_mode="single")  #pills for option kind

if option_kind == "Call option":
    option_kind = "call" #set to call if call option
else:
    option_kind = "put" #set to put if put option



approach = st.pills("Approach to calculate",["Black-Scholes-Merton (BSM) model", "Monte Carlo simulation","Binomial Tree"],
                default="Black-Scholes-Merton (BSM) model", selection_mode="single") #pills for how to calculate option price





s0_input_type = st.pills("How do you want to enter the spot price (current stock price)",["Manual", "Auto"],
                         default="Manual", selection_mode ="single") #pills for how to enter spot price


if s0_input_type == "Manual": 
    s0 = st.number_input("spot price (current stock price): ", placeholder="Type current stock price...") #a text box is shown if want to enter the value manually
else:
    selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...",
                             key=st.session_state["stock_searchbox"]) #search box is shown if user typed in auto 
    if selected: #let the user to selete the stock they want 
        stock_symbol = str(selected.split(' — ')[0] ) 
        s0 = yf.Ticker(stock_symbol).fast_info["last_price"] #the last price of that stock is fetched and set to variable 



strike_price = st.number_input("Strike price: ", placeholder="Type current stock price...") #enter strike price



volatility_of_stock_input_type =  st.pills("How do you want to enter the volatility of stock",["Manual", "Auto"],default="Manual",selection_mode="single") # pill for input volatility
if volatility_of_stock_input_type == "Manual":  #provide textbox
    volatility_of_stock = st.number_input("Volatility of stock(%): ", placeholder="Type volatility of stock...", min_value= 0.0,
                                           max_value = 100.0, step= 0.01)
    volatility_of_stock = volatility_of_stock/100 #divide by 100 for cos the input is in % 
else:
    selected = st_searchbox(stock_search_suggestions, placeholder="Type to search for stocks ...",key="volatility_stock_searchbox") #search for search and their voilatility 
    if selected:
        stock_symbol = str(selected.split(' — ')[0] )
        price_history = yf.download(stock_symbol, period="1y")["Close"]
        volatility_of_stock = np.log(price_history).diff().std()*np.sqrt(252)
        volatility_of_stock = volatility_of_stock/100



risk_free_interest_rate_input_type = st.pills("Risk free interest rate per annum",["Self input", "0%"], default="0%",selection_mode="single") #pill for risk free interest rate
if risk_free_interest_rate_input_type== "Self input": #textbox for manal input
    risk_free_interest_rate = st.number_input("Risk free interest rate per annum: ", placeholder="Type risk free interest rate per annum...", 
                                              min_value= 0.0, max_value = 100.0, step= 0.01)
    risk_free_interest_rate = risk_free_interest_rate/100 #turn % into decimal 
else:
    risk_free_interest_rate = 0.0    #set to 0




today = datetime.datetime.now()


date = st.date_input( #date input
    "Select how long you are going to hold your option",
    value=(today, today + dt.timedelta(days=10)),
    min_value=today,
    max_value=today + dt.timedelta(days=365 * 10),
    format="MM.DD.YYYY"
)

start_date = date[0]
end_date = date[1]

if not isinstance(date, tuple) or len(date) != 2: #check if the date is valid
    st.info("Pick an end date to complete the range.")
    st.stop()



calculate = st.button("Calculate option price") #buttton to calculate price


if calculate:
    error_important = []
    if (
        option_type is None or option_kind is None or s0 is None or strike_price is None or volatility_of_stock is None
        or start_date is None or end_date is None or risk_free_interest_rate is None ):

        error_important.append("Please fill in all the required fields.")
    if error_important:
        for err in error_important:
                st.error(err)
    else:
        error = []
        if end_date <= start_date:
            error.append("End date must be after start date")
        if s0 == 0:
                error.append("Spot price must be greater than 0")
        if strike_price ==0:
                error.append("Strike price must be greater than 0")
        if strike_price > s0 and option_kind == "call":
            error.append("For a call option, the strike price should not be greater than the spot price.")
        if strike_price < s0 and option_kind == "put":
            error.append("For a put option, the strike price should not be less than the spot price.")  
        
        if error:
            for err in error:
                st.error(err)
        else:
            risk_free_interest_rate= round(risk_free_interest_rate, 2)
            strike_price = round(strike_price, 2)
            s0 = round(s0, 2)
            volatility_of_stock= round(volatility_of_stock, 2)

            option_input = Option(european=option_type ,
                kind=option_kind,
                s0=s0,
                k=strike_price,
                sigma=volatility_of_stock,
                r=risk_free_interest_rate,
                start=start_date,
                end=end_date
                )
            
            if approach == "Black-Scholes-Merton (BSM) model":
                price = option_input.getPrice()
            elif approach == "Monte Carlo simulation":
                price = option_input.getPrice(method="MC")
            else:
                price = option_input.getPrice(method="BT")



            st.write(option_input)
            st.subheader(f"Option price: {round(price,4)}")
        
