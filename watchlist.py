import yfinance as yf
import config, login
import time

#user_id = login.login()

# connect to db and query user symbols
conn = config.connection
cur = conn.cursor()
cur.execute("""
    SELECT DISTINCT ws.symbol
    FROM watchlist_symbols ws
    JOIN users_watchlist uw ON 
    uw.watchlist_symbols_id = ws.id
    WHERE etf = 'No' 
    ORDER BY ws.symbol
""")
symbols = [r[0] for r in cur.fetchall()]

# query yfinance and stream real-time rrices
while True:
    try:
        for symbol in symbols:
            data = yf.Ticker(symbol).history(period='4d')
            latest_price = data['Close'][-1]
            previous_close = data['Close'][-2]
            change_pct = (latest_price - previous_close) / previous_close * 100
            
            cur.execute("""
                INSERT INTO watchlist (symbol, price, change_pct)
                VALUES (%s, %s, %s)
                ON CONFLICT (symbol) DO UPDATE
                SET price = excluded.price, change_pct = excluded.change_pct;
            """, (symbol, latest_price, change_pct))
            
            conn.commit()
            
            print(f"{symbol}: ${latest_price:.2f} ({change_pct:.2f}%)")
        
        time.sleep(60)
    except KeyboardInterrupt:
        break
        
cur.close()
conn.close()


