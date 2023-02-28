import yfinance as yf

# Define the ticker symbol
tickerSymbol = input("Enter a symbol: ")

# Get data for the ticker
tickerData = yf.Ticker(tickerSymbol).history(period='2d')

# Get real-time data
latest_price = round(tickerData['Close'][-1],2)
previous_close = tickerData['Close'][-2]
change_pct = (latest_price - previous_close) / previous_close * 100
volume = tickerData['Volume'].iloc[-1]

# Format the volume value with a comma separator
formatted_volume = format(volume, ",d")

# Print the results
print(f"Current Price: ${latest_price}  Day Change: {change_pct:.2f}%  Volume: {formatted_volume}")
