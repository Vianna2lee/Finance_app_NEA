import yfinance as yf

# Choose your ticker
ticker = "AAPL"   # example: Apple Inc.

# Create the Ticker object
stock = yf.Ticker(ticker)

# Fetch fast_info
info = stock.fast_info

# Display the results
print("Fast Info for", ticker)
for key, value in info.items():
    print(f"{key}: {value}")