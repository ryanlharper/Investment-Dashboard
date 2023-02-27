import yfinance as yf
import config
import time

def update_indexes():
    conn = config.connection
    cur = conn.cursor()
    cur.execute("""
        SELECT i.symbol
        FROM indexes i  
    """)
    symbols = [r[0] for r in cur.fetchall()]
    
    while True:
        try:
            for symbol in symbols:
                data = yf.Ticker(symbol).history(period='4d')
                latest_price = data['Close'][-1]
                previous_close = data['Close'][-2]
                change_pct = (latest_price - previous_close) / previous_close * 100
                
                cur.execute("""
                    INSERT INTO index_prices (symbol, level, change_pct)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (symbol) DO UPDATE
                    SET level = excluded.level, change_pct = excluded.change_pct;
                """, (symbol, latest_price, change_pct))
                
                conn.commit()
                print(f"{symbol}: {latest_price:.2f} ({change_pct:.2f}%)")
            
            time.sleep(60)
        except KeyboardInterrupt:
            break
            
    cur.close()
    conn.close()

update_indexes()