import yfinance as yf
import time

# set  ticker symbols
symbols = []
while True:
    try:
        number_of_stocks = int(input("How many stocks? "))
        break
    except ValueError:
        print("Please enter a valid integer.")    

for stock in range(0,number_of_stocks,1):
    while True: 
        symbol = input("Enter a symbol: ").upper()
        if symbol == "":
             print("Symbol cannot be empty.")
             continue
        elif isinstance(symbol, str) and symbol.isalpha():
            symbols.append(symbol)  
            break
        else: 
             print(symbol, "is an invalid symbol.")
             continue 

# set delay time
while True:
    try:
        delay_time = int(input("How many seconds between updates? "))
        break
    except ValueError:
        print("Please enter a valid integer.")

#get real-time data
while True:
    try:
        for symbol in symbols:
            tickerData = yf.Ticker(symbol).history(period='365d')
            latest_price = round(tickerData['Close'][-1],2)
            previous_close = tickerData['Close'][-2]
            change_pct = (latest_price - previous_close) / previous_close * 100
            volume = tickerData['Volume'].iloc[-1]
            average_volume = int(tickerData['Volume'].mean())

            # Format the volume value with a comma separator
            formatted_volume = format(volume, ",d")
            formatted_average_volume = format(average_volume, ",d")
            
            # Print the results
            print(f"{symbol}: Current Price: ${latest_price}  Day Change: {change_pct:.2f}%  Volume: {formatted_volume}   1-Yr Avg Volume: {formatted_average_volume}")
        
        time.sleep(delay_time)
    
    except KeyboardInterrupt:
            break
