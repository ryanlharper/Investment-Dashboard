import config, login
import requests, time
from datetime import datetime, timedelta

"""user_id = login.login()"""

# Connect to database and query symbols
conn = config.connection
cur = conn.cursor()
cur.execute("""
    SELECT DISTINCT ws.symbol
    FROM watchlist_symbols ws
    JOIN users_watchlist uw ON
    uw.watchlist_symbols_id = ws.id
    WHERE ws.etf = 'No' 
    ORDER BY ws.symbol
""")
symbols = [r[0] for r in cur.fetchall()]

# Query Alpha Vantage for headlines
for symbol in symbols:
    response = requests.get(f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={config.ALPHA_KEY}")
    data = response.json()
    if 'feed' not in data:
        continue  # skip to the next symbol if feed is empty
    articles = data['feed']
    print(f"Recent headlines for {symbol}:")
    for article in articles:
        # check if article is within the last 24 hours
        article_time = datetime.strptime(article['time_published'], '%Y%m%dT%H%M%S')
        if datetime.now() - article_time > timedelta(hours=24):
            continue  # skip article if it's older than 24 hours
        if 'title' not in article:
            continue  # skip article if it doesn't have a title
        print(article['title'])
    print("\n")
    time.sleep(12)  # add a delay of 12 seconds between API requests to stay within the rate limits


cur.close()
conn.close()
