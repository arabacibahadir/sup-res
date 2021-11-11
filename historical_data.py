from binance import Client
import csv
import binance_api
import pandas as pd

duration = 1000  # milliseconds
freq = 440  # Hz
client = Client(binance_api.api, binance_api.secret)  # Your Binance api and secret key
symbol_list = ["BTCUSDT"]  # Add which pairs do you want
symbol = symbol_list[0]
file_name = symbol_list[0] + ".csv"


def hist_data():
    headerList = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                  'taker buy vol', 'taker buy quote vol', 'ignore']

    def historical_Data_Write():
        csvFileW = open(symbol + ".csv", "w", newline='')
        klines_writer = csv.writer(csvFileW, delimiter=",")

        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)

        csvFileW.close()
        df = pd.read_csv(symbol + ".csv")
        df = df.iloc[::-1]
        df.to_csv(symbol + ".csv", header=headerList, index=False)
        df = pd.read_csv(symbol + ".csv")
        date = pd.to_datetime(df['unix'], unit='ms')
        df.insert(1, 'date', date)
        del df['volume'], df['close time'], df['taker buy vol'], df['taker buy quote vol'], df['ignore'], df[
            'tradecount']
        df.to_csv(symbol + ".csv", index=False)

    for s in symbol_list:
        print("Data writing: ", s)
        candlesticks = client.get_historical_klines(s, Client.KLINE_INTERVAL_1DAY,
                                                    "2 October, 2020")  # KLINE_INTERVAL_1DAY= '1d', Client.KLINE_INTERVAL_1HOUR
        historical_Data_Write()

# hist_data()
