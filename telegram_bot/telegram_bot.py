import csv
import os
import sys
import time
from datetime import datetime
import pandas as pd
import pandas_ta.momentum as ta
import plotly.graph_objects as go
from binance.client import Client
import telegram_frameselect

os.chdir("../telegram_bot")  # Changing the directory to the `telegram_bot` folder
client = Client("", "")
current = datetime.now()
current_time = current.strftime("%b-%d-%y %H:%M")
# Taking the arguments from the command line and assigning them to variables.
ticker = sys.argv[1]  # Pair
frame_s = sys.argv[2]  # Timeframe


def historical_data_write():
    """
    This function writes the historical data to a csv file
    """
    data = ticker + ".csv"
    candlesticks = client.get_historical_klines(ticker, time_frame, start, limit=270)
    headerList = ['unix', 'open', 'high', 'low', 'close', 'volume', 'close time', 'Volume USDT', 'tradecount',
                  'taker buy vol', 'taker buy quote vol', 'ignore']
    csvFileW = open(f"../telegram_bot/{data}", "w", newline='')
    klines_writer = csv.writer(csvFileW, delimiter=",")
    # Writing the data to a CSV file.
    for c in candlesticks:
        klines_writer.writerow(c)
    csvFileW.close()
    df = pd.read_csv(data)
    df = df.iloc[::-1]
    df.to_csv(data, header=headerList, index=False)
    df = pd.read_csv(data)
    date = pd.to_datetime(df['unix'], unit='ms')
    df.insert(1, 'date', date)
    del df['Volume USDT'], df['volume'], df['close time'], df['taker buy vol'], df['taker buy quote vol'], \
        df['ignore'], df['tradecount']

    def drop_null():
        """
        Drop all rows with NULL values in the dataframe
        """
        for col in df.columns:
            index_null = df[df[col] == "NULL"].index
            df.drop(index_null, inplace=True)
            df.isna().sum()

    drop_null()
    df.to_csv(data, index=False)


def main():
    print(f"Start main function in {time.perf_counter() - perf} seconds")
    print(f"{file_name} data analysis in progress.")
    candle_count = 254  # Number of candlesticks
    df = pd.read_csv(file_name, delimiter=',', encoding="utf-8-sig", index_col=False, nrows=candle_count,
                     keep_default_na=False)
    df = df.iloc[::-1]
    for_macd = df['close'][:-1]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, df.tail(1)], axis=0, ignore_index=True)
    dfsma = df[:-1]
    sma10 = tuple((dfsma.ta.sma(10)))
    sma50 = tuple((dfsma.ta.sma(50)))
    sma100 = tuple((dfsma.ta.sma(100)))
    rsi = tuple((ta.rsi(df['close'][:-1])))
    macd = ta.macd(close=for_macd, fast=12, slow=26, signal=9)
    fib_up, fib_down, pattern_list = [], [], []
    fib_multipliers = (0.236, 0.382, 0.500, 0.618, 0.705, 0.786, 0.886, 1.13)
    new_sup, new_res, sup_below, res_above = [], [], [], []
    support_list, resistance_list = [], []  # support_list : Support list, resistance_list : Resistance list
    # Chart settings
    fig, x_date = [], ''  # Chart
    legend_color = "#D8D8D8"
    plot_color = "#E7E7E7"
    bg_color = "#E7E7E7"
    support_color = "LightSeaGreen"
    res_color = "MediumPurple"
    # Adding a watermark to the plot.
    watermark_layout = (dict(name="draft watermark", text="twitter.com/sup_res", textangle=-30, opacity=0.15,
                             font=dict(color="black", size=100), xref="paper", yref="paper", x=0.5, y=0.5,
                             showarrow=False))

    def support(price1, l, n1, n2):
        """
        If the price of the asset is increasing for the last n1 days and decreasing for the last n2
        days, then return 1. Otherwise return 0
        
        :param price1: The price data for the asset
        :param l: The index of the first bar in the support
        :param n1: The number of bars back you want to look
        :param n2: The number of bars in the second trend
        :return: 1 if the price of the asset is supported by the previous low price, and 0 if it is not.
        """
        try:
            for last_s in range(l - n1 + 1, l + 1):
                if price1.low[last_s] > price1.low[last_s - 1]:
                    return 0
            for last_s in range(l + 1, l + n2 + 1):
                if price1.low[last_s] < price1.low[last_s - 1]:
                    return 0
            return 1
        except KeyError:
            pass

    def resistance(price1, l, n1, n2):
        """
        If the price of the stock is increasing for the last n1 days and decreasing for the last n2
        days, then return 1. Otherwise return 0

        :param price1: The price data for the asset
        :param l: The index of the first bar in the resistance
        :param n1: The number of bars back you want to look
        :param n2: The number of days after the first resistance line where the price will be considered
        to be broken
        :return: 1 if the price has been increasing for the last n1 periods and decreasing for the last
        n2 periods.
        """
        try:
            for last_r in range(l - n1 + 1, l + 1):
                if price1.high[last_r] < price1.high[last_r - 1]:
                    return 0
            for last_r in range(l + 1, l + n2 + 1):
                if price1.high[last_r] > price1.high[last_r - 1]:
                    return 0
            return 1
        except KeyError:
            pass

    def fib_pl(high_price, low_price):
        """
        The function `fib_pl` takes two arguments, `high_price` and `low_price`, and returns a list of
        retracement levels
        Uptrend Fibonacci Retracement Formula =>
        Fibonacci Price Level = High Price - (High Price - Low Price)*Fibonacci Level
        :param high_price: The high price for the current price level
        :param low_price: Low price for the period
        """
        for multi in fib_multipliers:
            retracement_levels_uptrend = low_price + (high_price - low_price) * multi
            fib_up.append(retracement_levels_uptrend)
            retracement_levels_downtrend = high_price - (high_price - low_price) * multi
            fib_down.append(retracement_levels_downtrend)

    def candlestick_patterns():
        """
        The function takes in a dataframe and returns a list of candlestick patterns found in the
        dataframe
        """
        from candlestick import candlestick
        nonlocal df
        df = candlestick.inverted_hammer(df, target='inverted_hammer')
        df = candlestick.hammer(df, target='hammer')
        df = candlestick.doji(df, target='doji')
        df = candlestick.bearish_harami(df, target='bearish_harami')
        df = candlestick.bearish_engulfing(df, target='bearish_engulfing')
        df = candlestick.bullish_harami(df, target='bullish_harami')
        df = candlestick.bullish_engulfing(df, target='bullish_engulfing')
        df = candlestick.dark_cloud_cover(df, target='dark_cloud_cover')
        df = candlestick.dragonfly_doji(df, target='dragonfly_doji')
        df = candlestick.hanging_man(df, target='hanging_man')
        df = candlestick.gravestone_doji(df, target='gravestone_doji')
        df = candlestick.morning_star(df, target='morning_star')
        df = candlestick.morning_star_doji(df, target='morning_star_doji')
        df = candlestick.piercing_pattern(df, target='piercing_pattern')
        df = candlestick.star(df, target='star')
        df = candlestick.shooting_star(df, target='shooting_star')
        pattern_find = []

        def pattern_find_func(self):
            """
            The function takes in a dataframe and a list of column names. It then iterates through the
            list of column names and checks if the column name is in the dataframe. If it is, it adds
            the column name to a list and adds the date of the match to another list
            """
            for col in df.columns:
                pattern_find.append(col)
            t = 0
            for pattern in self:
                if pattern == True:
                    pattern_list.append(pattern_find[t])
                    pattern_list.append(self['date'].strftime('%b-%d-%y'))
                t += 1

        # Looping through the dataframe and finding the pattern in the dataframe.
        for item in range(-3, -30, -1):
            last_row = df.iloc[item]
            pattern_find_func(last_row)

    hist_ltf = (Client.KLINE_INTERVAL_1MINUTE,
                Client.KLINE_INTERVAL_3MINUTE,
                Client.KLINE_INTERVAL_5MINUTE,
                Client.KLINE_INTERVAL_15MINUTE,
                Client.KLINE_INTERVAL_30MINUTE,
                Client.KLINE_INTERVAL_1HOUR,
                Client.KLINE_INTERVAL_2HOUR,
                Client.KLINE_INTERVAL_4HOUR,
                Client.KLINE_INTERVAL_6HOUR,
                Client.KLINE_INTERVAL_8HOUR,
                Client.KLINE_INTERVAL_12HOUR)
    hist_htf = (Client.KLINE_INTERVAL_1DAY,
                Client.KLINE_INTERVAL_3DAY)

    if time_frame in hist_htf:
        candlestick_patterns()
        x_date = '%b-%d-%y'
    elif time_frame in hist_ltf:  # For LTF chart
        x_date = '%b-%d-%y %H:%M'
    # The below code is creating a candlestick chart.
    fig = go.Figure([go.Candlestick(x=df['date'][:-1].dt.strftime(x_date),
                                    name="Candlestick",
                                    text=df['date'].dt.strftime(x_date),
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close'])])
    fig.update_layout(annotations=[watermark_layout])

    def sensitivity(sens):
        """
        Find the support and resistance levels for a given asset
        sensitivity:1 is recommended for daily charts or high frequency trade scalping 
        :param sens: sensitivity parameter default:2, level of detail 1-2-3 can be given to function
        """
        for row in range(3, len(df) - 1):
            if support(df, row, 3, sens):
                support_list.append((row, df.low[row]))
            if resistance(df, row, 3, sens):
                resistance_list.append((row, df.high[row]))

    sensitivity(2)

    sup = tuple(map(lambda sup1: sup1[1], support_list))
    res = tuple(map(lambda res1: res1[1], resistance_list))
    latest_close = tuple(df['close'])[-1]

    def supres():
        # Checking if the support is below the latest close. If it is, it is appending it to the list
        # sup_below. If it isn't, it is appending it to the list new_res.
        for s in sup:
            if s < latest_close:
                sup_below.append(s)
            else:
                new_res.append(s)
        # Checking if the price is above the latest close price. If it is, it is appending it to the
        # res_above list. If it is not, it is appending it to the new_sup list.
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
    # Checking if the support level is empty. If it is, it appends the minimum value of the low
    # column to the list.
    if len(sup_below) == 0:
        sup_below.append(min(df['low']))
    # Checking if the resistance level is empty. If it is, it appends the minimum value of the high
    # column to the list.
    if len(res_above) == 0:
        res_above.append(max(df['high']))

    # Computing the Fibonacci sequence for the numbers in the range of the last element of the
    # res_above list and the last element of the sup_below list.
    fib_pl(res_above[-1], sup_below[-1])
    res_above = [float(a) for a in res_above]
    sup_below = [float(a) for a in sup_below]

    c = 0
    # Adding the support lines and annotations to the chart.
    while 1:
        if c > len(support_list) - 1:
            break
        # Support Lines
        fig.add_shape(type='line', x0=support_list[c][0] - 1, y0=support_list[c][1],
                      x1=len(df) + 25,
                      y1=support_list[c][1], line=dict(color=support_color, width=2))
        # Support annotations
        fig.add_annotation(x=len(df) + 7, y=support_list[c][1], text=str(support_list[c][1]),
                           font=dict(size=15, color=support_color))
        c += 1

    c = 0
    # Adding the resistance lines and annotations to the chart.
    while 1:
        if c > len(resistance_list) - 1:
            break
        # Resistance Lines
        fig.add_shape(type='line', x0=resistance_list[c][0] - 1, y0=resistance_list[c][1],
                      x1=len(df) + 25,
                      y1=resistance_list[c][1], line=dict(color=res_color, width=1))
        # Resistance annotations
        fig.add_annotation(x=len(df) + 20, y=resistance_list[c][1], text=str(resistance_list[c][1]),
                           font=dict(size=15, color=res_color))
        c += 1

    # Legend texts
    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"Resistances    ||   Supports", mode="markers+lines",
        marker=dict(color=res_color, size=10)))

    str_price_len = 3
    sample_price = df['close'][0]
    if sample_price < 1:
        str_price_len = len(str(sample_price))
    blank = " " * (len(str(sample_price)) + 1)
    differ = len(res_above) - len(sup_below)
    try:
        if differ < 0:
            for i in range(abs(differ)):
                res_above.extend([0])
        if differ > 0:
            for i in range(abs(differ)):
                sup_below.extend([0])
        temp = 0
        for _ in range(max(len(res_above), len(sup_below))):
            if res_above[temp] == 0:  # This is for legend allignment
                legend_supres = f"{float(res_above[temp]):.{str_price_len - 1}f}{blank}     " \
                                f"||   {float(sup_below[temp]):.{str_price_len - 1}f}"
            else:
                legend_supres = f"{float(res_above[temp]):.{str_price_len - 1}f}       " \
                                f"||   {float(sup_below[temp]):.{str_price_len - 1}f}"
            fig.add_trace(go.Scatter(y=[support_list[0]],
                name=legend_supres,
                mode="lines",
                marker=dict(color=legend_color, size=10)))
            temp += 1
            if temp == 14:
                break
    except IndexError:
        pass
    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"github.com/arabacibahadir/sup-res", mode="markers",
        marker=dict(color=legend_color, size=0)))
    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"-------  twitter.com/sup_res  --------", mode="markers",
        marker=dict(color=legend_color, size=0)))
    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"Indicators", mode="markers", marker=dict(color=legend_color, size=14)))
    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"RSI         "
                                  f": {int(rsi[-1])}", mode="lines", marker=dict(color=legend_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"MACD      : {int(macd['MACDh_12_26_9'][1]):.{str_price_len}f}", mode="lines",
        marker=dict(color=legend_color, size=10)))

    # The below code is adding the SMA10, SMA50, and SMA100 to the chart and legend.
    if time_frame in hist_htf:
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma10,
                       name=f"SMA10     : {float(sma10[-1]):.{str_price_len}f}",
                       line=dict(color='#5c6cff', width=3)))
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma50,
                       name=f"SMA50     : {float(sma50[-1]):.{str_price_len}f}",
                       line=dict(color='#950fba', width=3)))
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma100,
                       name=f"SMA100   : {float(sma100[-1]):.{str_price_len}f}",
                       line=dict(color='#a69b05', width=3)))
    elif time_frame in hist_ltf:
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y %H:%M'), y=sma10,
                       name=f"SMA10     : {float(sma10[-1]):.{str_price_len}f}",
                       line=dict(color='#5c6cff', width=3)))
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y %H:%M'), y=sma50,
                       name=f"SMA50     : {float(sma50[-1]):.{str_price_len}f}",
                       line=dict(color='#950fba', width=3)))
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y %H:%M'), y=sma100,
                       name=f"SMA100   : {float(sma100[-1]):.{str_price_len}f}",
                       line=dict(color='#a69b05', width=3)))
    else:
        print("Time frame error.")

    fig.add_trace(go.Scatter(
        y=[support_list[0]], name=f"-- Fibonacci Uptrend | Downtrend --", mode="markers",
        marker=dict(color=legend_color, size=0)))
    mtp = 7
    # Adding a line to the plot for each Fibonacci level.
    for _ in fib_up:
        fig.add_trace(go.Scatter(
            y=[support_list[0]], name=f"Fib {fib_multipliers[mtp]:.3f} : {float(fib_up[mtp]):.{str_price_len}f} "
                                      f"| {float(fib_down[mtp]):.{str_price_len}f} ", mode="lines",
            marker=dict(color=legend_color, size=10)))
        mtp -= 1

    def candle_patterns():
        fig.add_trace(go.Scatter(
            y=[support_list[0]], name="----------------------------------------", mode="markers",
            marker=dict(color=legend_color, size=0)))
        fig.add_trace(go.Scatter(
            y=[support_list[0]], name="Latest Candlestick Patterns",
            mode="markers", marker=dict(color=legend_color, size=14)))
        for pat1 in range(1, len(pattern_list), 2):  # candlestick patterns
            fig.add_trace(go.Scatter(
                y=[support_list[0]], name=f"{pattern_list[pat1]} -> {pattern_list[pat1 - 1]}", mode="lines",
                marker=dict(color=legend_color, size=10)))

    if time_frame in hist_htf:
        candle_patterns()

    # Chart updates
    fig.update_layout(
        title=str(f"{ticker} {time_frame.upper()} Chart"),
        hovermode='x', dragmode="zoom",
        paper_bgcolor=bg_color, plot_bgcolor=plot_color, xaxis_rangeslider_visible=False,
        legend=dict(bgcolor=legend_color, font=dict(size=12)), margin=dict(t=30, l=0, b=0, r=0))
    fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)
    text_image = f"{ticker} {df['date'].dt.strftime('%b-%d-%Y')[candle_count]} " \
                 f"{time_frame.upper()}\n Support and resistance levels:\n" \
                 f"Res={res_above[:7]} \nSup={sup_below[:7]}"

    def save():
        """
        Saves the image and text file.
        """
        if not os.path.exists("../telegram_bot"):
            os.mkdir("../telegram_bot")
        image = f"../telegram_bot/{ticker}.jpeg"
        fig.write_image(image, width=1920, height=1080)
        with open('output.txt', 'w') as f:
            f.write(f"{image}\n{text_image}")

    save()

    def pinescript_code():
        templines = []
        lines_sma = f"//@version=5\nindicator('Sup-Res {ticker} {frame_s}', overlay=true)\n" \
                    "plot(ta.sma(close, 50), title='50 SMA', color=color.new(color.blue, 0), linewidth=1)\n" \
                    "plot(ta.sma(close, 100), title='100 SMA', color=color.new(color.purple, 0), linewidth=1)\n" \
                    "plot(ta.sma(close, 200), title='200 SMA', color=color.new(color.red, 0), linewidth=1)\n"

        for line_res in res_above[:10]:
            lr = f"hline({line_res}, title=\"Lines\", color=color.red, linestyle=hline.style_solid, linewidth=1)"
            templines.append(lr)

        for line_sup in sup_below[:10]:
            ls = f"hline({line_sup}, title=\"Lines\", color=color.green, linestyle=hline.style_solid, linewidth=1)"
            templines.append(ls)
        lines = '\n'.join(map(str, templines))
        f = open("../telegram_bot/pinescript.txt", "w")
        f.write(lines_sma + lines)
        f.close()

    pinescript_code()
    print(f"\nCompleted execution in {time.perf_counter() - perf} seconds")


if __name__ == "__main__":

    # Selecting the time frame for the data to be retrieved.
    time_frame = telegram_frameselect.frame_select(frame_s)[0]
    # Selecting the frame that the user wants to start from.
    start = telegram_frameselect.frame_select(frame_s)[1]
    perf = time.perf_counter()
    historical_data_write()
    file_name = ticker + ".csv"
    # Getting the information about the asset from the Binance API.
    symbol_info = client.get_symbol_info(ticker)
    print("Data writing:", file_name)
    if os.path.isfile(file_name):
        print(f"{file_name} downloaded and created.")
    else:
        print(
            "One or more issues caused the download to fail. "
            "Make sure you typed the filename correctly in the settings.")
    main()
