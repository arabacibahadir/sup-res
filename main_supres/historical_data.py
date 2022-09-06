import csv
import pandas as pd
from binance.client import Client
import frameselect

print("Ticker and Time Frame:")  # Example:"BTCUSDT 1H", "ETHBTC 3D", "BNBUSDT 15M"
ticker, frame_s = str(input().upper()).split()
time_frame = frameselect.frame_select(frame_s)[0]
# Creating a client object that is used to interact with the Binance API
client = Client("", "")
has_pair = any(ticker == i.get('symbol') for i in client.get_all_tickers())  # Check pair is in Binance API
if has_pair:
    print("Pair is in Binance API.")
else:
    print("Pair is not in Binance API.")
    exit()
start = frameselect.frame_select(frame_s)[1]
file_name = ticker + ".csv"
symbol_data = client.get_symbol_info(ticker)
header_list = ('unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
               'taker buy vol', 'taker buy quote vol', 'ignore')


def hist_data():
    """
    The function is used to get historical data from the Binance API and write it to a csv file
    """
    def historical_data_write(ticker_symbol):
        """
        Write the historical data to a csv file
        """
        def write_candlesticks():
            csv_file_w = open(file_name, "w", newline='')
            klines_writer = csv.writer(csv_file_w, delimiter=",")
            klines_writer.writerow(header_list)
            for candlestick in client.get_historical_klines(symbol=ticker_symbol, interval=time_frame, start_str=start,
                                                            limit=300):
                klines_writer.writerow(candlestick)
            csv_file_w.close()

        def final_csv():
            df = pd.read_csv(file_name)
            # Reversing the order of the dataframe
            df = df.iloc[::-1]
            df.to_csv(file_name, header=header_list, index=False)
            df = pd.read_csv(file_name)
            # Converting the unix time to a readable date format for today
            date = pd.to_datetime(df['unix'], unit='ms')
            df.insert(1, 'date', date)
            del df['volume'], df['close time'], df['taker buy vol'], df['taker buy quote vol'], df['ignore'], \
                df['tradecount']
            df.to_csv(file_name, index=False)

        write_candlesticks()
        final_csv()

    print("Data writing:", file_name)
    historical_data_write(ticker)
