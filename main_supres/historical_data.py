import csv
import pandas as pd
from binance.client import Client
import frameselect

print("Ticker:")  # Pair
ticker = input().upper()
print("Time frame:")  # 15M, 1H, 1D etc
frame_s = str(input().upper())
time_frame = frameselect.frame_select(frame_s)[0]
# Creating a client object that is used to interact with the Binance API
client = Client("", "")
has_pair = any(ticker == i.get('symbol') for i in client.get_all_tickers())  # Check pair is in Binance API
print('Pair found in Binance API.' if has_pair else 'Pair not found in Binance API.')
start = frameselect.frame_select(frame_s)[1]
file_name = ticker + ".csv"
symbol_info = client.get_symbol_info(ticker)


def hist_data():
    """
    The function is used to get historical data from the Binance API and write it to a csv file
    """
    header_list = ('unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                   'taker buy vol', 'taker buy quote vol', 'ignore')

    def historical_data_write(self):
        """
        Write the historical data to a csv file
        """
        data = self + ".csv"
        csv_file_w = open(data, "w", newline='')
        klines_writer = csv.writer(csv_file_w, delimiter=",")
        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)
        csv_file_w.close()
        df = pd.read_csv(data)
        # Reversing the order of the dataframe
        df = df.iloc[::-1]
        df.to_csv(data, header=header_list, index=False)
        df = pd.read_csv(data)
        # Converting the unix time to a readable date format for today
        date = pd.to_datetime(df['unix'], unit='ms')
        df.insert(1, 'date', date)
        del df['volume'], df['close time'], df['taker buy vol'], df['taker buy quote vol'], df['ignore'], \
            df['tradecount']
        df.to_csv(data, index=False)

    print("Data writing:", file_name)
    candlesticks = client.get_historical_klines(ticker, time_frame, start, limit=300)
    historical_data_write(ticker)
