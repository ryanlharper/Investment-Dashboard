import pandas_datareader.data as web
import datetime
import config

# Set the start and end dates for the historical data
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=365 * 1)

# Set number of days back to retrieve data
when = -1

# Connect to the SQL database and retrieve the indicators
conn = config.connection
cur = conn.cursor()
cur.execute('SELECT symbol, description FROM indicators')
indicators = cur.fetchall()

# Get the data for all indicators in the list
data = {}
# WORKING - adding user input to limit query to relavant indicators
numeral = 0
for indicator in indicators:
    numeral += 1 
    print(f"{numeral}. {indicator[1]}")
    data[indicator[0]] = web.DataReader(indicator[0], 'fred', start_date, end_date, api_key='<your_API_key>')

# Print the last value for each indicator
for indicator in indicators:
    print(indicator[1] + ':', data[indicator[0]].iloc[-1][indicator[0]])


