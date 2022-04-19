import csv
import datetime
import os
import time
import pandas as pd
from binance.client import Client
import frameselect



def hist_data():
    headerList = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                  'taker buy vol', 'taker buy quote vol', 'ignore']

    def historical_Data_Write(self):
        """
        The function writes the data to a csv file
        """
        data = self + ".csv"
        csvFileW = open(data, "w", newline='')
        klines_writer = csv.writer(csvFileW, delimiter=",")
        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)
        csvFileW.close()
        df = pd.read_csv(data)
        df = df.iloc[::-1]
        df.to_csv(data, header=headerList, index=False)

    candlesticks = client.get_historical_klines(ticker, time_frame, start, limit=300)
    historical_Data_Write(ticker)


def main():
    df = pd.read_csv(file_name, delimiter=',', encoding="utf-8-sig", index_col=False, nrows=254, keep_default_na=False)
    df = df.iloc[::-1]
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, df.tail(1)], axis=0, ignore_index=True)
    ss, rr, new_res, new_sup = [], [], [], []

    def support(price1, l, n1, n2):
        for s in range(l - n1 + 1, l + 1):
            if price1.low[s] > price1.low[s - 1]:
                return 0
        for s in range(l + 1, l + n2 + 1):
            if price1.low[s] < price1.low[s - 1]:
                return 0
        return 1

    def resistance(price1, l, n1, n2):
        for r in range(l - n1 + 1, l + 1):
            if price1.high[r] < price1.high[r - 1]:
                return 0
        for r in range(l + 1, l + n2 + 1):
            if price1.high[r] > price1.high[r - 1]:
                return 0
        return 1

    def drop_null():
        for col in df.columns:
            index_null = df[df[col] == "NULL"].index
            df.drop(index_null, inplace=True)
            df.isna().sum()

    drop_null()
    df = df[:len(df)]

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
    latest_close = tuple(df['close'])[-1]

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
        sup_below.append(min(df['low']))

    if not res_above:
        res_above.append(min(df['high']))

    res_above = [float(a) for a in res_above]
    sup_below = [float(a) for a in sup_below]

    print('res:', res_above)
    print('sup:', sup_below)
    with open('../main_supres/all_timeframes.txt', 'a') as f:
        f.writelines([ticker, " ", i, "\nResistance:", str(res_above), "\nSupport:", str(sup_below), "\n\n"])


if __name__ == "__main__":
    perf = time.perf_counter()
    client = Client("", "")
    ticker_list = ['BTCUSDT', 'ETHUSDT']  # Add coin pairs here, it will generate all_timeframes.txt file
    frame_s = ('3M', '5M', '15M', '30M', '1H', '2H', '4H', '6H', '8H', '12H', '1D', '3D')
    timestamp = client.get_server_time().get('serverTime') / 1000
    server_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    with open('../main_supres/all_timeframes.txt', 'w') as file:
        file.writelines(["Server time: ", server_time, "\n"])
    print(f"Server time: {server_time}")
    for ticker in ticker_list:
        print("----", ticker, "----")
        file_name = "../main_supres/" + str(ticker).upper() + ".csv"
        for i in frame_s:
            time_frame = frameselect.frame_select(i)[0]
            start = frameselect.frame_select(i)[1]
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
