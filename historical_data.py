from binance import Client
import csv
import api_binance
import pandas as pd
from datetime import datetime
import frameselect

print("Ticker:")  # Pair
ticker = input().upper()
print("Time frame:")  # 1H,1D etc.
frame_s = str(input().upper())
time_frame = frameselect.frame_select(frame_s)[0]
client = Client(api_binance.api, api_binance.secret)  # Your Binance api and secret key
current = datetime.now()
current_time = current.strftime("%b-%d-%y %H:%M")
start = frameselect.frame_select(frame_s)[1]
file_name = ticker + ".csv"


def hist_data():
    headerList = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                  'taker buy vol', 'taker buy quote vol', 'ignore']

    def historical_Data_Write(self):
        data = self + ".csv"
        csvFileW = open(data, "w", newline='')
        klines_writer = csv.writer(csvFileW, delimiter=",")
        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)
        csvFileW.close()
        df = pd.read_csv(data)
        df = df.iloc[::-1]
        df.to_csv(data, header=headerList, index=False)
        df = pd.read_csv(data)
        date = pd.to_datetime(df['unix'], unit='ms')
        df.insert(1, 'date', date)
        del df['volume'], df['close time'], df['taker buy vol'], df['taker buy quote vol'], df['ignore'], df[
            'tradecount']
        df.to_csv(data, index=False)

    print("Data writing:", file_name)
    candlesticks = client.get_historical_klines(ticker, time_frame, start)
    historical_Data_Write(ticker)
