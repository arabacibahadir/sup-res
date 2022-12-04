import csv
import pandas as pd
from binance.client import Client
import frameselect

print("Ticker and Time Frame: ")  # Example:"BTCUSDT 1H", "ETHBTC 3D", "BNBUSDT 15M"
ticker, frame_s = str(input().upper()).split()
time_frame, start = frameselect.frame_select(frame_s)
# Creating a client object that is used to interact with the Binance API
client = Client("", "")
if any(ticker == i.get('symbol') for i in client.get_all_tickers()):  # Check pair is in Binance API
    print("Pair is in Binance API.")
else:
    print("Pair is not in Binance API.")
    exit()
file_name = ticker + ".csv"
header_list = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
               'taker buy vol', 'taker buy quote vol', 'ignore']


def historical_data_write(ticker_symbol):
    """
    Write the historical data to a csv file
    """
    df = pd.DataFrame(reversed(
        client.get_historical_klines(symbol=ticker_symbol, interval=time_frame, start_str=start)), columns=header_list)
    # Converting the unix time to a readable date format for today
    date = pd.to_datetime(df['unix'], unit='ms')
    df.insert(1, 'date', date)
    df.drop(labels=["volume", "close time", "tradecount", "taker buy vol", "taker buy quote vol", "ignore"],
            inplace=True, axis=1)
    df.to_csv(file_name, index=False)
    print("Data writing:", file_name)
