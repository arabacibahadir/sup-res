import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# def coinbase_historical_data():
#     # Get the current time in seconds
#     current_time = int(time.time())
#     # Get the time 24 hours ago in seconds
#     past_time = current_time - 86400
#     # Get the data from coinbase
#     data = requests.get(
#         "https://api.pro.coinbase.com/products/BTC-USD/candles?start="
#         + str(past_time)
#         + "&end="
#         + str(current_time)
#         + "&granularity=3600"
#     )
#     # Convert the data to a pandas dataframe
#     df = pd.DataFrame(data.json(), columns=["unix", "low", "high", "open", "close", "volume"])
#     # Convert the unix time to a readable date format
#     date = pd.to_datetime(df["unix"], unit="s")
#     df.insert(1, "date", date)
#     df.drop(labels=["unix"], axis=1, inplace=True)
#     # Convert the dataframe to a csv file
#     df.to_csv("coinbase_historical_data.csv", index=False)
#     print("Coinbase historical data written to csv file.")
apiUrl = "https://api.pro.coinbase.com"
sym = "BTC-USD"
barSize = "300"
timeEnd = datetime.now()
delta = timedelta(minutes=5)
timeStart = timeEnd - (300 * delta)
timeStart = timeStart.isoformat()
timeEnd = timeEnd.isoformat()
print(timeStart)
print(timeEnd)

parameters = {"start": timeStart, "end": timeEnd, "granularity": barSize}
data = requests.get(
    apiUrl + "/products/" + sym + "/candles",
    params=parameters,
    headers={"content-type": "application/json"},
)
data = data.json()
df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
df["time"] = pd.to_datetime(df["time"], unit="s")
df.set_index("time", inplace=True)
df.to_csv("test.csv")
print(df.head(10))
