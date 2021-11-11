from binance import Client
import csv
import binance_api

duration = 1000  # milliseconds
freq = 440  # Hz

client = Client(binance_api.api, binance_api.secret)  # Your Binance api and secret key
symbol_list = ["BTCUSDT"]


def historical_Data_Write():
    csvFileW = open(symbol + "btc.csv", "w", newline='')
    klines_writer = csv.writer(csvFileW, delimiter=",")

    for candlestick in candlesticks:
        klines_writer.writerow(candlestick)

    csvFileW.close()


for symbol in symbol_list:
    print("Data writing: ", symbol)
    candlesticks = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "20 October, 2021",
                                                "3 November, 2021")  # KLINE_INTERVAL_1DAY= '1d'
    historical_Data_Write()
