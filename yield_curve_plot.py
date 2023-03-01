import pandas_datareader.data as web
import config
import matplotlib.pyplot as plt

# Set the API key
web.DataReader('GDP', 'fred', api_key=config.API_KEY)

# Set the dates
dates = ['2007-08-09', '2018-01-16' , '2023-02-27']
indicators = ['DGS3MO', 'DGS6MO', 'DGS2', 'DGS5', 'DGS10', 'DGS30']

# Get the data for all indicators in the list
data = {}
for date in dates:
    data[date] = {}
    for indicator in indicators:
        try:
            data[date][indicator] = web.DataReader(indicator, 'fred', date, date, api_key=config.API_KEY).iloc[0][0]
        except:
            print(f"No data found for indicator {indicator} on date {date}.")

# Plot the yield curve data
fig, ax = plt.subplots(figsize=(10, 6))
for i, date in enumerate(dates):
    x = [j for j in range(len(indicators))]
    y = [data[date][indicator] for indicator in indicators]
    linestyle = '--' if date != '2023-02-27' else '-'
    ax.plot(x, y, label=date, linestyle=linestyle)
    ax.annotate(f'{data[date]["DGS30"]:.2f}', xy=(5.5, data[date]["DGS30"]), xytext=(6.0, data[date]["DGS30"]),
                arrowprops=dict(facecolor='black', arrowstyle='-|>'))

ax.set_title('Historical U.S. Treasury Yield Curve')
ax.set_xlabel('Maturity')
ax.set_ylabel('Yield')
ax.set_xticks(x)
ax.set_xticklabels(indicators)
ax.legend()
plt.show()
