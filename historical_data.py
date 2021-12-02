from binance import Client
import csv
import binance_api
import pandas as pd
from datetime import datetime, timedelta
import timeframes

current = datetime.now()
current_time = current.strftime("%b-%d-%y %H:%M")
time_frame = Client.KLINE_INTERVAL_1HOUR  # Client.KLINE_INTERVAL_1DAY, Client.KLINE_INTERVAL_1HOUR etc.
start = timeframes.timeframe(time_frame)
client = Client(binance_api.api, binance_api.secret)  # Your Binance api and secret key
symbol_list = ["BTCUSDT"]  # Pairs
file_name = symbol_list[0] + ".csv"
file_name_wo = symbol_list[0]


def hist_data():
    headerList = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                  'taker buy vol', 'taker buy quote vol', 'ignore']

    def historical_Data_Write(self):
        csvFileW = open(self + ".csv", "w", newline='')
        klines_writer = csv.writer(csvFileW, delimiter=",")

        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)

        csvFileW.close()
        df = pd.read_csv(self + ".csv")
        df = df.iloc[::-1]
        df.to_csv(self + ".csv", header=headerList, index=False)
        df = pd.read_csv(self + ".csv")
        date = pd.to_datetime(df['unix'], unit='ms')
        df.insert(1, 'date', date)
        del df['volume'], df['close time'], df['taker buy vol'], df['taker buy quote vol'], df['ignore'], df[
            'tradecount']
        df.to_csv(self + ".csv", index=False)

    for s in symbol_list:
        print("Data writing:", s)
        candlesticks = client.get_historical_klines(s, time_frame, start)
        historical_Data_Write(s)

