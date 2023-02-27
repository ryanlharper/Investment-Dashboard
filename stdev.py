import config
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Connect to the database
conn = config.connection

# Truncate the standard_deviation table
query = """
TRUNCATE TABLE standard_deviation;
"""
cur = conn.cursor()
cur.execute(query)

# Define the SQL query to get the latest date and all security symbols, excluding '*USD'
query = """
SELECT symbol
FROM watchlist_symbols;
"""


# Execute the query and fetch the results
cur = conn.cursor()
cur.execute(query)
securities = cur.fetchall()

# Loop through each security, query Yahoo Finance, and calculate the standard deviation
results = []
for symbol in securities:
    # Query Yahoo Finance to get historical price data for the past 3 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3*365)
    df = yf.download(symbol, start=start_date, end=end_date)
    
    # Calculate the daily returns
    df['returns'] = df['Adj Close'].pct_change()
    
    # Calculate the standard deviation
    std_dev = df['Adj Close'].pct_change().std() * (252 ** 0.5) * 100

    # Append the result to the list of results
    results.append((symbol, std_dev, datetime.today().date()))

# Define the SQL query to insert the results into the standard deviation table
query = """
INSERT INTO standard_deviation (symbol, three_year_deviation, date)
VALUES (%s, %s, %s);
"""

# Execute the query and commit the changes to the database
cur = conn.cursor()
cur.executemany(query, results)
conn.commit()

# Close the database connection
conn.close()


