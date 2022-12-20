import pandas as pd
from binance.client import Client
import frameselect


class BinanceTicker:
    def __init__(self, ticker_binance, time_frame_binance):
        self.ticker = ticker_binance
        self.time_frame = time_frame_binance
        self.client = Client("", "")  # Replace with your own API keys
        self.file_name = ticker + ".csv"
        self.header_list = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                            'taker buy vol', 'taker buy quote vol', 'ignore']

    def check_pair(self, ticker_symbol):
        """
        Checks if the given ticker symbol is a valid pair.
        :param ticker_symbol: The ticker symbol to check.
        :return: True if the ticker symbol is a valid pair, False otherwise.
        """
        if self.client.get_symbol_info(ticker_symbol):
            print("Pair found in Binance API.")
            return self.client.get_symbol_info(ticker_symbol)
        else:
            print("Pair is not found in Binance API.")
            exit()
            return

    def historical_data_write(self):
        """
        Writes the historical data for a given ticker symbol to a csv file.
        """
        df = pd.DataFrame(reversed(
            user_ticker.client.get_historical_klines(symbol=self.ticker, interval=self.time_frame, start_str=start)),
            columns=self.header_list)
        # Converting the unix time to a readable date format for today
        date = pd.to_datetime(df['unix'], unit='ms')
        df.insert(1, 'date', date)
        df.drop(labels=["volume", "close time", "tradecount", "taker buy vol", "taker buy quote vol", "ignore"],
                inplace=True, axis=1)
        df.to_csv(self.file_name, index=False)
        print("Data writing:", self.file_name)


print("Ticker and Time Frame: ")  # Example:"BTCUSDT 1H", "ETHBTC 3D", "BNBUSDT 15M"
ticker, frame_s = str(input().upper()).split()
time_frame, start = frameselect.frame_select(frame_s)
user_ticker = BinanceTicker(ticker, time_frame)
user_ticker.check_pair(ticker)
