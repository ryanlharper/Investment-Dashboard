import config
import yfinance as yf

def new_values():
    # get positions from table
    conn = config.connection
    cur = conn.cursor()
    cur.execute("""
        SELECT p.symbol, p.number_shares, p.price
        FROM positions p
        ORDER BY p.symbol
    """)
    rows = cur.fetchall()
    # query & calculate
    for row in rows:
        symbol, number_shares, price = row
        # get the real-time price
        data = yf.Ticker(symbol).history(period='2d')
        latest_price = data['Close'][-1]
        # calc mkt_val
        market_value = float(number_shares) * latest_price
        # update the data in the table
        cur.execute("""
            UPDATE positions
            SET price = %s, market_value = %s
            WHERE symbol = %s
        """, (latest_price, market_value, symbol))
        conn.commit()
        print(price)
        cur.close()
        conn.close()

    
