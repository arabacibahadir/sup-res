import numpy as np
import pandas as pd
import yfinance as yf
import plotly

# from datetime import datetime, timedelta
# now = datetime.now().strftime('%Y-%m-%d')
# eurusd = yf.Ticker("EURUSD=X")
# forex_data = eurusd.history(period="5d",interval="15m")
forex_data = yf.download("EURUSD=X", period="10d", interval="15m")
# forex_data = yf.download(['EURUSD=X', 'GBPUSD=X'],
# start='2019-01-02', end='2021-12-31', group_by='ticker')
# forex_data = yf.download('EURUSD=X', start='2019-01-02')

# Set the index to a datetime object
forex_data.index = pd.to_datetime(forex_data.index)
# drop volume column
# forex_data.drop('Volume', axis=1, inplace=True)

# Display the last five rows
print(forex_data.tail())
print(len(forex_data))
# save to csv
# forex_data.to_csv('forex_wo_drop.csv')
# drop if two rows are the same "open", "high", "low", "close", "adj close"
# forex_data.drop_duplicates(keep='first', inplace=True)

# forex_data.to_csv('forex_data.csv')
# forex_data.drop_duplicates(keep='first', inplace=True)
print(len(forex_data))
# plot
# save to csv
# forex_data.to_csv('eurusd.csv')
fig = plotly.graph_objects.Figure(
    data=[
        plotly.graph_objects.Candlestick(
            x=forex_data.index,
            open=forex_data["Open"],
            high=forex_data["High"],
            low=forex_data["Low"],
            close=forex_data["Close"],
        )
    ]
)
fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
fig.update_layout(title="EURUSD=X", xaxis_title="Date", yaxis_title="Price")
fig.show()
