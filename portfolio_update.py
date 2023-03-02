import config, time
import yfinance as yf

# get positions from table
conn = config.connection
cur = conn.cursor()
cur.execute("""
    SELECT p.symbol, p.number_shares, p.cost, p.price, p.return, p.dollar_return, p.market_value
    FROM positions p
    ORDER BY p.symbol
""")
rows = cur.fetchall()

while True:
    # print headers
    print("\n")
    print(f"{'Symbol':<8}{'Shares':<8}{'Cost':<12}{'Price':<8}{'% Return':<12}{'$ Return':<12}{'Market Value':<12}")
    try:
    # query & calculate
        for row in rows:
            symbol, number_shares, cost, _, _, _, _ = row
            
            # get the real-time price
            data = yf.Ticker(symbol).history(period='2d')
            price = data['Close'][-1]
            
            # calc % return , $ return & mkt_val
            cost, number_shares = float(cost), float(number_shares)
            r = (price - cost) / cost
            dollar_return = r * number_shares * price
            market_value = number_shares * price
            
            # update the data in the table
            cur.execute("""
                UPDATE positions
                SET price = %s, return = %s, dollar_return = %s, market_value = %s
                WHERE symbol = %s
            """, (price, r, dollar_return, market_value, symbol))
            conn.commit()

            # print data
            print(f"{symbol:<8}{int(number_shares):<8}{cost:>8.2f}{price:>8.2f}{r*100:>12.2f}%{dollar_return:>12.2f}{market_value:>12.2f} ")
    
        time.sleep(60)
    except KeyboardInterrupt:
        break

# close the cursor and connection
cur.close()
conn.close()