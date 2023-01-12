import csv
import datetime
import os
import time
import pandas as pd
from binance.client import Client


frame_select_dict = {
    "1M": [Client.KLINE_INTERVAL_1MINUTE, -260],
    "3M": [Client.KLINE_INTERVAL_3MINUTE, -780],
    "5M": [Client.KLINE_INTERVAL_5MINUTE, -1300],
    "15M": [Client.KLINE_INTERVAL_15MINUTE, -3900],
    "30M": [Client.KLINE_INTERVAL_30MINUTE, -7800],
    "1H": [Client.KLINE_INTERVAL_1HOUR, -260],
    "2H": [Client.KLINE_INTERVAL_2HOUR, -520],
    "4H": [Client.KLINE_INTERVAL_4HOUR, -1040],
    "6H": [Client.KLINE_INTERVAL_6HOUR, -1560],
    "8H": [Client.KLINE_INTERVAL_8HOUR, -2080],
    "12H": [Client.KLINE_INTERVAL_12HOUR, -3120],
    "1D": [Client.KLINE_INTERVAL_1DAY, -260],
    "3D": [Client.KLINE_INTERVAL_3DAY, -780],
    "1W": [Client.KLINE_INTERVAL_1WEEK, -1040],
}


def frame_select(kline: str) -> tuple[str | int, str]:
    start_date = datetime.datetime.now()
    last_letter = frame_select_dict[kline][0][-1].upper()
    kline_interval = frame_select_dict[kline][1]
    times = {
        "M": datetime.timedelta(minutes=kline_interval),
        "H": datetime.timedelta(hours=kline_interval),
        "D": datetime.timedelta(days=kline_interval),
        "W": datetime.timedelta(weeks=kline_interval),
    }
    start_date += times[last_letter]
    return frame_select_dict[kline][0], start_date.strftime("%d %B, %Y")


def hist_data():
    header_list = [
        "unix",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close time",
        "Volume USDT",
        "tradecount",
        "taker buy vol",
        "taker buy quote vol",
        "ignore",
    ]

    def historical_data_write(self):
        """
        The function writes the data to a csv file
        """
        data = self + ".csv"
        csv_file_write = open(data, "w", newline="")
        klines_writer = csv.writer(csv_file_write, delimiter=",")
        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)
        csv_file_write.close()
        df = pd.read_csv(data)
        df = df.iloc[::-1]
        df.to_csv(data, header=header_list, index=False)

    candlesticks = client.get_historical_klines(ticker, time_frame, start, limit=300)
    historical_data_write(ticker)


def main():
    df = pd.read_csv(
        file_name,
        delimiter=",",
        encoding="utf-8-sig",
        index_col=False,
        nrows=254,
        keep_default_na=False,
    )
    df = df.iloc[::-1]
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, df.tail(1)], axis=0, ignore_index=True)
    ss, rr, new_res, new_sup = [], [], [], []

    def support(candle_value, candle_index, before_candle_count, after_candle_count):
        """
        If the price of the asset is increasing for the last before_candle_count and decreasing for
        the last after_candle_count, then return 1. Otherwise, return 0
        :param candle_value: The price data for the asset
        :param candle_index: The index of the first bar in the support
        :param before_candle_count: The number of bars back you want to look
        :param after_candle_count: The number of bars in the second trend
        :return: 1 if the price of the asset is supported by the previous low price, and 0 if it is not.
        """
        try:
            for current_value in range(
                candle_index - before_candle_count + 1, candle_index + 1
            ):
                if (
                    candle_value.low[current_value]
                    > candle_value.low[current_value - 1]
                ):
                    return 0
            for current_value in range(
                candle_index + 1, candle_index + after_candle_count + 1
            ):
                if (
                    candle_value.low[current_value]
                    < candle_value.low[current_value - 1]
                ):
                    return 0
            return 1
        except KeyError:
            pass

    def resistance(candle_value, candle_index, before_candle_count, after_candle_count):
        """
        If the price of the stock is increasing for the last before_candle_count and decreasing for
        the last after_candle_count, then return 1. Otherwise, return 0
        :param candle_value: The price data for the asset
        :param candle_index: The index of the first bar in the resistance
        :param before_candle_count: The number of bars back you want to look
        :param after_candle_count: The number of days after the first resistance line where the price will be considered
        to be broken
        :return: 1 if the price has been increasing for the last n1 periods and decreasing for the last
        n2 periods.
        """
        try:
            for current_value in range(
                candle_index - before_candle_count + 1, candle_index + 1
            ):
                if (
                    candle_value.high[current_value]
                    < candle_value.high[current_value - 1]
                ):
                    return 0
            for current_value in range(
                candle_index + 1, candle_index + after_candle_count + 1
            ):
                if (
                    candle_value.high[current_value]
                    > candle_value.high[current_value - 1]
                ):
                    return 0
            return 1
        except KeyError:
            pass

    def drop_null():
        """
        Drop all rows with NULL values in the dataframe
        """
        for col in df.columns:
            index_null = df[df[col] == "NULL"].index
            df.drop(index_null, inplace=True)
            df.isna().sum()

    drop_null()
    df = df[: len(df)]

    def sensitivity(sens):
        for row in range(3, len(df) - 1):
            if support(df, row, 3, sens):
                ss.append((row, df.low[row]))
            if resistance(df, row, 3, sens):
                rr.append((row, df.high[row]))

    sensitivity(2)

    sup_below = []
    res_above = []
    sup = tuple(map(lambda sup1: sup1[1], ss))
    res = tuple(map(lambda res1: res1[1], rr))
    latest_close = tuple(df["close"])[-1]

    def supres():
        for s in sup:
            if s < latest_close:
                sup_below.append(s)
            else:
                new_res.append(s)

        for r in res:
            if r > latest_close:
                res_above.append(r)
            else:
                new_sup.append(r)

    supres()

    sup_below.extend(new_sup)
    res_above.extend(new_res)
    sup_below = sorted(sup_below, reverse=True)
    res_above = sorted(res_above)
    if not sup_below:
        sup_below.append(min(df["low"]))

    if not res_above:
        res_above.append(min(df["high"]))

    res_above = [float(a) for a in res_above]
    sup_below = [float(a) for a in sup_below]

    print("res:", res_above)
    print("sup:", sup_below)
    with open("../miniscripts/all_timeframes.txt", "a") as f:
        f.writelines(
            [
                ticker,
                " ",
                i,
                "\nResistance:",
                str(res_above),
                "\nSupport:",
                str(sup_below),
                "\n\n",
            ]
        )


if __name__ == "__main__":
    perf = time.perf_counter()
    client = Client("", "")
    ticker_list = [
        "BTCUSDT",
        "ETHUSDT",
    ]  # Add coin pairs here, it will generate all_timeframes.txt file
    frame_s = (
        "3M",
        "5M",
        "15M",
        "30M",
        "1H",
        "2H",
        "4H",
        "6H",
        "8H",
        "12H",
        "1D",
        "3D",
    )
    timestamp = client.get_server_time().get("serverTime") / 1000
    server_time = datetime.datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    with open("../miniscripts/all_timeframes.txt", "w") as file:
        file.writelines(["Server time: ", server_time, "\n"])
    print(f"Server time: {server_time}")
    for ticker in ticker_list:
        print("----", ticker, "----")
        file_name = "../miniscripts/" + str(ticker).upper() + ".csv"
        for i in frame_s:
            time_frame = frame_select(i)[0]
            start = frame_select(i)[1]
            print(i)
            try:
                hist_data()
                main()
                if os.path.exists(file_name):
                    os.remove(file_name)
                else:
                    print("The file does not exist.")
                print(f"Completed execution in {time.perf_counter() - perf} seconds")
            except KeyError:
                print("ERROR")
                os.remove(file_name)
                pass
    print(f"Completed execution in {time.perf_counter() - perf} seconds")
