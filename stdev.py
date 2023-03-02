import config
import yfinance as yf
from datetime import datetime, timedelta

# connect to the database
conn = config.connection

# truncate the standard_deviation table
query = """
TRUNCATE TABLE standard_deviation;
"""
cur = conn.cursor()
cur.execute(query)

# query table for symbols
query = """
SELECT symbol
FROM watchlist_symbols;
"""

cur = conn.cursor()
cur.execute(query)
securities = cur.fetchall()

# query Yahoo Finance and calculate 
results = []
for symbol in securities:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3*365)
    df = yf.download(symbol, start=start_date, end=end_date)
    
    # Calculate the daily returns
    df['returns'] = df['Adj Close'].pct_change()
    
    # Calculate the standard deviation
    std_dev = df['Adj Close'].pct_change().std() * (252 ** 0.5) * 100

    # Append the result to the list of results
    results.append((symbol, std_dev, datetime.today().date()))

# query to insert the results into the standard deviation table
query = """
INSERT INTO standard_deviation (symbol, three_year_deviation, date)
VALUES (%s, %s, %s);
"""

# commit the changes to the database
cur = conn.cursor()
cur.executemany(query, results)
conn.commit()

# close the database connection
conn.close()


