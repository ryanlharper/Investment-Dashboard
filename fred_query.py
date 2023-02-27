import pandas_datareader.data as web
import datetime
import config

# Set the API key
web.DataReader('GDP', 'fred', api_key=config.API_KEY)

# Set the start and end dates for the historical data
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=365 * 1)

# Set number of days back to retrieve data
when = -1

# List of indicators
# GDP, CPI, UM C. Sentiment, Personal Income,  Personal Consumption Expenditures, Initial Claims, 
# Advance Retail Sales, Federal Funds Effective Rate, Existing Home Sales, Producer Price Index by Commodity: All Commodities 
# Unemployment Rate, Real GDP, Coinbase Bitcoin
indicators = ['GDP', 'CPALTT01USM657N', 'UMCSENT', 'PI', 'PCE', 'ICSA', 'RSXFS', 'DFF', 'EXHOSLUSM495S', 'PPIACO', 'UNRATE', 'GDPC1', 'CBBTCUSD']

# Get the data for all indicators in the list
data = {}
for indicator in indicators:
    data[indicator] = web.DataReader(indicator, 'fred', start_date, end_date, api_key='<your_API_key>')

# Print the last value for each indicator
for indicator in indicators:
    print(indicator + ':', data[indicator].iloc[-1][indicator])


