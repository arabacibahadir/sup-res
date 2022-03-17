import os
import time
import pandas as pd
import pandas_ta.momentum as ta
import plotly.graph_objects as go
import historical_data
import delete_file


def main():
    print(f"Start main function in {time.perf_counter() - perf} seconds")
    csv = historical_data.file_name
    print(f"{csv} data analysis in progress.")
    candle_count = 254  # Number of candlesticks
    df = pd.read_csv(csv, delimiter=',', encoding="utf-8-sig", index_col=False, nrows=candle_count,
                     keep_default_na=False)
    df = df.iloc[::-1]
    for_macd = df['close'][:-1]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)
    df = df.append(df.tail(1), ignore_index=True)
    dfsma = df[:-1]
    sma10 = tuple((dfsma.ta.sma(10)))
    sma50 = tuple((dfsma.ta.sma(50)))
    sma100 = tuple((dfsma.ta.sma(100)))
    rsi = tuple((ta.rsi(df['close'][:-1])))
    macd = ta.macd(close=for_macd, fast=12, slow=26, signal=9)
    fib = []
    fib_multipliers = (0.236, 0.382, 0.500, 0.618, 0.786, 1.382, 1.618)
    new_sup = []
    new_res = []
    pattern_list = []
    legend_color = "#D8D8D8"
    plot_color = "#E7E7E7"
    bg_color = "#E7E7E7"
    support_color = "LightSeaGreen"
    res_color = "MediumPurple"

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
        for i in range(l - n1 + 1, l + 1):
            if price1.low[i] > price1.low[i - 1]:
                return 0
        for i in range(l + 1, l + n2 + 1):
            if price1.low[i] < price1.low[i - 1]:
                return 0
        return 1

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
        for i in range(l - n1 + 1, l + 1):
            if price1.high[i] < price1.high[i - 1]:
                return 0
        for i in range(l + 1, l + n2 + 1):
            if price1.high[i] > price1.high[i - 1]:
                return 0
        return 1

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
            retracement_levels = low_price + (high_price - low_price) * multi
            fib.append(retracement_levels)

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
            for i in self:
                if i == True:
                    # even pattern, odd date
                    pattern_list.append(pattern_find[t])
                    pattern_list.append(self['date'].strftime('%b-%d-%y'))
                t += 1

        # Looping through the dataframe and finding the pattern in the dataframe.
        for item in range(-3, -30, -1):
            last_row = df.iloc[item]
            pattern_find_func(last_row)

    hist_htf = (historical_data.Client.KLINE_INTERVAL_1DAY,
                historical_data.Client.KLINE_INTERVAL_3DAY)
    hist_ltf = (historical_data.Client.KLINE_INTERVAL_1MINUTE,
                historical_data.Client.KLINE_INTERVAL_3MINUTE,
                historical_data.Client.KLINE_INTERVAL_5MINUTE,
                historical_data.Client.KLINE_INTERVAL_15MINUTE,
                historical_data.Client.KLINE_INTERVAL_30MINUTE,
                historical_data.Client.KLINE_INTERVAL_1HOUR,
                historical_data.Client.KLINE_INTERVAL_2HOUR,
                historical_data.Client.KLINE_INTERVAL_4HOUR,
                historical_data.Client.KLINE_INTERVAL_6HOUR,
                historical_data.Client.KLINE_INTERVAL_8HOUR,
                historical_data.Client.KLINE_INTERVAL_12HOUR)

    if historical_data.time_frame in hist_htf:
        candlestick_patterns()

    def drop_null():
        """
        Drop all rows with NULL values in the dataframe
        """
        for col in df.columns:
            index_null = df[df[col] == "NULL"].index
            df.drop(index_null, inplace=True)
            df.isna().sum()

    drop_null()
    df = df[:len(df)]  # Candle range

    # The below code is creating a candlestick chart.
    if historical_data.time_frame in hist_htf:
        fig = go.Figure([go.Candlestick(x=df['date'][:-1].dt.strftime('%b-%d-%y'),
                                        name="Candlestick",
                                        text=df['date'].dt.strftime('%b-%d-%y'),
                                        open=df['open'],
                                        high=df['high'],
                                        low=df['low'],
                                        close=df['close'])])

    elif historical_data.time_frame in hist_ltf:
        fig = go.Figure([go.Candlestick(x=df['date'][:-1].dt.strftime('%b-%d-%y %H:%M'),
                                        name="Candlestick",
                                        text=df['date'].dt.strftime('%b-%d-%y %H:%M'),
                                        open=df['open'],
                                        high=df['high'],
                                        low=df['low'],
                                        close=df['close'])])

    ss = []  # ss : Support list
    rr = []  # rr : Resistance list
    # Adding a watermark to the plot.
    fig.layout.annotations = [
        dict(
            name="draft watermark",
            text="twitter.com/sup_res",
            textangle=-30,
            opacity=0.2,
            font=dict(color="black", size=100),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    ]

    def sensitivity(sens):
        """
        Find the support and resistance levels for a given asset
        sensitivity:1 is recommended for daily charts or high frequency trade scalping 
        :param sens: sensitivity parameter default:2, level of detail 1-2-3 can be given to function
        """
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
        # Checking if the support is below the latest close. If it is, it is appending it to the list
        # sup_below. If it isn't, it is appending it to the list new_res.
        for s in sup:  # Find closes
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
        res_above.append(min(df['high']))

    # Computing the Fibonacci sequence for the numbers in the range of the last element of the
    # res_above list and the last element of the sup_below list.
    fib_pl(res_above[-1], sup_below[-1])  # Fibonacci func
    res_above = [float(a) for a in res_above]
    sup_below = [float(a) for a in sup_below]

    c = 0
    # Adding the support lines and annotations to the chart.
    while 1:
        if c > len(ss) - 1:
            break
        # Support Lines
        fig.add_shape(type='line', x0=ss[c][0] - 1, y0=ss[c][1],
                      x1=len(df) + 25,
                      y1=ss[c][1], line=dict(color=support_color, width=2))
        # Support annotations
        fig.add_annotation(x=len(df) + 7, y=ss[c][1], text=str(ss[c][1]),
                           font=dict(size=15, color=support_color))
        c += 1

    c = 0
    # Adding the resistance lines and annotations to the chart.
    while 1:
        if c > len(rr) - 1:
            break
        # Resistance Lines
        fig.add_shape(type='line', x0=rr[c][0] - 1, y0=rr[c][1],
                      x1=len(df) + 25,
                      y1=rr[c][1], line=dict(color=res_color, width=1))
        # Resistance annotations
        fig.add_annotation(x=len(df) + 20, y=rr[c][1], text=str(rr[c][1]),
                           font=dict(size=15, color=res_color))
        c += 1

    # Legend
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Current Resistance : {float(res_above[0])}", mode="markers+lines",
        marker=dict(color=res_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Next Resistances: {', '.join(map(str, res_above[1:4]))}", mode="lines",
        marker=dict(color=res_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"|-> : {', '.join(map(str, res_above[4:8]))}", mode="lines",
        marker=dict(color=legend_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Current Support : {float(sup_below[0])}", mode="markers+lines",
        marker=dict(color=support_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Next Supports: {', '.join(map(str, sup_below[1:4]))}", mode="lines",
        marker=dict(color=support_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"|-> : {', '.join(map(str, sup_below[4:8]))}", mode="lines",
        marker=dict(color=legend_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f" ----------  twitter.com/sup_res  ----------- ", mode="markers",
        marker=dict(color=legend_color, size=0)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Indicators", mode="markers", marker=dict(color=legend_color, size=14)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"RSI         : {int(rsi[-1])}", mode="lines", marker=dict(color=legend_color, size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"MACD      : {int(macd['MACDh_12_26_9'][1])}", mode="lines",
        marker=dict(color=legend_color, size=10)))

    # The below code is adding the SMA10, SMA50, and SMA100 to the chart and legend.
    if historical_data.time_frame in hist_htf:
        fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma10, name=f"SMA10     : {int(sma10[-1])}",
                                 line=dict(color='#5c6cff', width=3)))
        fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma50, name=f"SMA50     : {int(sma50[-1])}",
                                 line=dict(color='#950fba', width=3)))
        fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma100, name=f"SMA100   : {int(sma100[-1])}",
                                 line=dict(color='#a69b05', width=3)))
    elif historical_data.time_frame in hist_ltf:
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y %H:%M'), y=sma10, name=f"SMA10     : {int(sma10[-1])}",
                       line=dict(color='#5c6cff', width=3)))
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y %H:%M'), y=sma50, name=f"SMA50     : {int(sma50[-1])}",
                       line=dict(color='#950fba', width=3)))
        fig.add_trace(
            go.Scatter(x=df['date'].dt.strftime('%b-%d-%y %H:%M'), y=sma100, name=f"SMA100   : {int(sma100[-1])}",
                       line=dict(color='#a69b05', width=3)))
    else:
        print("Time frame error.")

    mtp = 6
    # Adding a line to the plot for each Fibonacci level.
    for _ in fib:
        fig.add_trace(go.Scatter(
            y=[ss[0]], name=f"Fib {fib_multipliers[mtp]:.3f} : {float(fib[mtp]):.2f}", mode="lines",
            marker=dict(color=legend_color, size=10)))
        mtp -= 1

    def candle_patterns():
        fig.add_trace(go.Scatter(
            y=[ss[0]], name=f" --------------------------------- ", mode="markers",
            marker=dict(color=legend_color, size=0)))
        fig.add_trace(go.Scatter(
            y=[ss[0]], name=f"Latest Candlestick Patterns", mode="markers", marker=dict(color=legend_color, size=14)))
        for pat1 in range(1, 24, 2):  # candlestick patterns
            fig.add_trace(go.Scatter(
                y=[ss[0]], name=f"{pattern_list[pat1]} -> {pattern_list[pat1 - 1]}", mode="lines",
                marker=dict(color=legend_color, size=10)))

    if historical_data.time_frame in hist_htf:
        candle_patterns()

    # Chart updates
    fig.update_layout(title=str(f"{historical_data.ticker} {historical_data.time_frame.upper()} Chart"),
                      hovermode='x', dragmode="zoom",
                      paper_bgcolor=bg_color, plot_bgcolor=plot_color, xaxis_rangeslider_visible=False,
                      legend=dict(bgcolor=legend_color, font=dict(size=11)), margin=dict(t=30, l=0, b=0, r=0))
    fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)

    def save():
        if not os.path.exists("images"):
            os.mkdir("images")
        image = f"images/{df['date'].dt.strftime('%b-%d-%y')[candle_count]}{historical_data.ticker}.jpeg"
        fig.write_image(image, width=1920, height=1080)  # Save image for tweet
        fig.write_html(f"images/{df['date'].dt.strftime('%b-%d-%y')[candle_count]}{historical_data.ticker}.html",
                       full_html=False, include_plotlyjs='cdn')
        text_image = f"#{historical_data.ticker} #{historical_data.symbol_info.get('baseAsset')} " \
                     f"{historical_data.time_frame.upper()} Support and resistance levels \n " \
                     f"{df['date'].dt.strftime('%b-%d-%Y')[candle_count]} #crypto #btc"

        def for_tweet():
            import tweet
            tweet.send_tweet(image, text_image)
            while tweet.is_image_tweet().text != text_image:
                time.sleep(1)
                if tweet.is_image_tweet().text != text_image:
                    tweet.api.update_status(status=
                                            f"#{historical_data.ticker}  "
                                            f"{df['date'].dt.strftime('%b-%d-%Y')[candle_count]} "
                                            f"{historical_data.time_frame.upper()} Support and resistance levels"
                                            f"\nRes={res_above[:7]} \nSup={sup_below[:7]}",
                                            in_reply_to_status_id=tweet.is_image_tweet().id)
                break
        # for_tweet()

    # save()
    def pinescript_code():
        temp = []
        lines_sma = "//@version=5\nindicator('Sup-Res', overlay=true)\n" \
                    "plot(ta.sma(close, 50), title='50 SMA', color=color.new(color.blue, 0), linewidth=1)\n" \
                    "plot(ta.sma(close, 100), title='100 SMA', color=color.new(color.purple, 0), linewidth=1)\n" \
                    "plot(ta.sma(close, 200), title='200 SMA', color=color.new(color.red, 0), linewidth=1)\n"

        for line_res in res_above[:10]:
            lr = f"hline({line_res}, title=\"Lines\", color=color.red, linestyle=hline.style_solid, linewidth=1)"
            temp.append(lr)

        for line_sup in sup_below[:10]:
            ls = f"hline({line_sup}, title=\"Lines\", color=color.green, linestyle=hline.style_solid, linewidth=1)"
            temp.append(ls)
        lines = '\n'.join(map(str, temp))
        f = open("pinescript.txt", "w")
        f.write(lines_sma + lines)
        f.close()

    pinescript_code()
    fig.show(id='the_graph', config={'displaylogo': False})
    print(f"Completed execution in {time.perf_counter() - perf} seconds")


if __name__ == "__main__":
    try:
        perf = time.perf_counter()
        historical_data.hist_data()
        if os.path.isfile(historical_data.file_name):  # <- Check .csv file is there or not
            print(f"{historical_data.file_name} downloaded and created.")
        else:
            print(
                "One or more issues caused the download to fail. "
                "Make sure you typed the filename correctly in the settings.")
        main()
        delete_file.remove()
    except KeyError:
        delete_file.remove()
        raise KeyError("Key error, algorithm issue")
