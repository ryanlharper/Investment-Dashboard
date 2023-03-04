import config
import login
import yfinance as yf

# get user id from login function
user_id = login.login()

# connect to db
conn = config.connection
cur = conn.cursor()

## get the ids of the symbols the user is already watching
cur.execute("SELECT watchlist_symbols_id FROM users_watchlist WHERE user_id = %s", (user_id,))
existing_user_symbols_ids = set(row[0] for row in cur.fetchall())

# get max id in watchlist_symbols
cur.execute("SELECT MAX(id) FROM watchlist_symbols")
max_id = cur.fetchone()[0]

if max_id is None:
    max_id = 0

# populate symbols with new user input
new_symbols = []
while True:
    symbol = input("Enter a symbol (or '*' to finish): ").upper()
    if symbol == '*':
        break
    cur.execute("SELECT id FROM watchlist_symbols WHERE symbol = %s", (symbol,))
    watchlist_symbols_id = cur.fetchone()
    if watchlist_symbols_id is not None and watchlist_symbols_id[0] in existing_user_symbols_ids:
        print(f"{symbol} is already in your watchlist. Please enter a new symbol.")
    elif watchlist_symbols_id is not None:
        watchlist_symbols_id = watchlist_symbols_id[0]
        cur.execute("INSERT INTO users_watchlist (user_id, watchlist_symbols_id) VALUES (%s, %s)", (user_id, watchlist_symbols_id))
        conn.commit()
        new_symbols.append(watchlist_symbols_id)
    else:
        try:
            stock_info = yf.Ticker(symbol).info
        except:
            print(f"{symbol} is not a valid symbol. Please enter a new symbol.")
            continue
        max_id += 1
        etf = input(f"Is {symbol} an ETF? Enter Yes or No: ")
        while etf.lower() not in ['yes', 'no']:
            etf = input(f"Invalid input. Is {symbol} an ETF? Enter Yes or No: ")
        cur.execute("INSERT INTO watchlist_symbols (id, symbol, etf) VALUES (%s, %s, %s) RETURNING id", (max_id, symbol, etf.capitalize()))
        watchlist_symbols_id = cur.fetchone()[0]
        cur.execute("INSERT INTO users_watchlist (user_id, watchlist_symbols_id) VALUES (%s, %s)", (user_id, watchlist_symbols_id))
        conn.commit()
        new_symbols.append(watchlist_symbols_id)

# insert new symbols into bridge table
if new_symbols:
    placeholders = ', '.join(['%s'] * len(new_symbols))
    cur.execute(f"INSERT INTO users_watchlist (user_id, watchlist_symbols_id) VALUES {placeholders}", [(user_id, watchlist_symbols_id) for watchlist_symbols_id in new_symbols])
    conn.commit()
    print(f"Added {len(new_symbols)} symbols to your watchlist.")
else:
    print("No new symbols added to your watchlist.")
