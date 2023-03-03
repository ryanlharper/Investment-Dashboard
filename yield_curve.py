import pandas_datareader.data as web
import config

# Set the API key
web.DataReader('GDP', 'fred', api_key=config.API_KEY)

# Set the parameters
dates = []
indicators = ['DGS3MO', 'DGS6MO', 'DGS2', 'DGS5', 'DGS10', 'DGS30']
number_of_dates = int(input("How many dates will be used? "))
for number in range(0,number_of_dates,1):
    dates.append(input("Enter a date: "))    

# Get the data for all indicators in the list
data = {}
for date in dates:
    data[date] = {}
    for indicator in indicators:
        try:
            data[date][indicator] = web.DataReader(indicator, 'fred', date, date, api_key=config.API_KEY).iloc[0][0]
        except:
            print(f"No data found for indicator {indicator} on date {date}.")

# Print the yields for each date
for date in dates:
    print('Yields for date:', date)
    for indicator in indicators:
        if indicator in data[date]:
            print(indicator + ':', data[date][indicator])

