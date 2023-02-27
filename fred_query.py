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

# Dictionary of indicators with their names
indicators = {'GDP': 'Gross Domestic Product', 
            'CPALTT01USM657N': 'Consumer Price Index', 
            'UMCSENT': 'University of Michigan Consumer Sentiment Index', 
            'PI': 'Personal Income', 
            'PCE': 'Personal Consumption Expenditures', 
            'ICSA': 'Initial Claims', 
            'RSXFS': 'Advance Retail Sales', 
            'DFF': 'Federal Funds Effective Rate', 
            'EXHOSLUSM495S': 'Existing Home Sales', 
            'PPIACO': 'Producer Price Index by Commodity: All Commodities', 
            'UNRATE': 'Unemployment Rate', 
            'GDPC1': 'Real Gross Domestic Product', 
            'CBBTCUSD': 'Coinbase Bitcoin', 
            'MICH': 'Inflation Expectation', 
            'STICKCPIM157SFRBATL': 'Sticky Price Consumer Price Index', 
            'M2SL': 'M2 Money Stock', 
            'M2V': 'Velocity of M2'}

# Get the data for all indicators in the list
data = {}
for indicator in indicators.keys():
    data[indicator] = web.DataReader(indicator, 'fred', start_date, end_date, api_key='<your_API_key>')

# Print the value for each indicator
for indicator in indicators.keys():
    print(indicators[indicator] + ':', data[indicator].iloc[when][indicator])



