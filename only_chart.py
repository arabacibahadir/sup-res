import os
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta
import delete_file
import get_data
import settings
import tweet
import time


def main():
    csv = settings.full_filename
    print(f"{csv} data analysis in progress.")
    candle_count = 254  # Number of candlesticks
    df = pd.read_csv(csv, delimiter=',', encoding="utf-8-sig", index_col=False, skiprows=[0], nrows=candle_count,
                     keep_default_na=False)
    df = df.iloc[::-1]
    for_macd = df['close']
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)
    df = df.append(df.tail(1), ignore_index=True)  # Dodging algorithm issue
    volume = list(reversed((df['Volume USDT'])))
    rsi = list((ta.rsi(df['close'])))
    macd = ta.macd(close=for_macd, fast=12, slow=26, signal=9)
    fib = []
    fib_multipliers = [0.236, 0.382, 0.500, 0.618, 0.786, 1.382, 1.618]
    new_sup = []
    new_res = []

    def support(price1, l, n1, n2):
        for i in range(l - n1 + 1, l + 1):
            if price1.low[i] > price1.low[i - 1]:
                return 0
        for i in range(l + 1, l + n2 + 1):
            if price1.low[i] < price1.low[i - 1]:
                return 0
        return 1

    def resistance(price1, l, n1, n2):
        for i in range(l - n1 + 1, l + 1):
            if price1.high[i] < price1.high[i - 1]:
                return 0
        for i in range(l + 1, l + n2 + 1):
            if price1.high[i] > price1.high[i - 1]:
                return 0
        return 1

    # -> Fibonacci Price Level between highest resistance line and lowest support line

    def fib_pl(high_price, low_price):
        """ Uptrend Fibonacci Retracement Formula => Fibonacci Price Level = High Price - (High Price - Low Price)*Fibonacci Level
         In this code section we will use only lines, not the highest and lowest prices on chart.
         Be careful on that, this fib levels can be wrong and irrelevant.
        """
        for multi in fib_multipliers:
            # -> Downtrend Fibonacci Retracement Formula we use in here
            retracement_levels = low_price + (high_price - low_price) * multi
            fib.append(retracement_levels)

    def drop_null():  # Drop NULL values

        for col in df.columns:
            index_null = df[df[col] == "NULL"].index
            df.drop(index_null, inplace=True)
            df.isna().sum()

    drop_null()

    df = df[:len(df)]
    fig = go.Figure([go.Candlestick(
        name="Candlestick",
        text=df['date'].dt.strftime('%b-%d-%y'),
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'])])

    ss = []  # ss : Support list
    rr = []  # rr : Resistance list

    # Sensitivity -> As the number increases, the detail decreases. (3,1) probably is the ideal one for daily charts.
    for row in range(3, len(df) - 1):
        if support(df, row, 3, 1):
            ss.append((row, df.low[row]))
        if resistance(df, row, 3, 1):
            rr.append((row, df.high[row]))

    # Closest sup-res lines
    sup_below = []
    res_above = []
    sup = list(map(lambda sup1: sup1[1], ss))
    res = list(map(lambda res1: res1[1], rr))
    latest_close = list(df['close'])[-1]

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

    sup_below.extend(new_sup)
    res_above.extend(new_res)
    sup_below = sorted(sup_below, reverse=True)
    fib_pl(res_above[-1], sup_below[-1])  # Fibonacci func
    res_above = [float(a) for a in res_above]
    sup_below = [float(a) for a in sup_below]

    c = 0
    # Drawing support lines
    while 1:
        if c > len(ss) - 1:
            break
        # Support Lines
        fig.add_shape(type='line', x0=ss[c][0] - 1, y0=ss[c][1],
                      x1=len(df) + 25,
                      y1=ss[c][1], line=dict(color="LightSeaGreen", width=2))
        # Support annotations
        fig.add_annotation(x=len(df) + 7, y=ss[c][1], text=str(ss[c][1]),
                           font=dict(size=15, color="LightSeaGreen"))
        c += 1

    # Drawing resistance lines
    c = 0
    while 1:
        if c > len(rr) - 1:
            break
        # Resistance Lines
        fig.add_shape(type='line', x0=rr[c][0] - 1, y0=rr[c][1],
                      x1=len(df) + 25,
                      y1=rr[c][1], line=dict(color="MediumPurple", width=1))
        # Resistance annotations
        fig.add_annotation(x=len(df) + 20, y=rr[c][1], text=str(rr[c][1]),
                           font=dict(size=15, color="MediumPurple"))
        c += 1
    # Legend -> Resistance
    fig.add_trace(go.Scatter(
        y=[ss[0]], name="Resistance", mode="lines", marker=dict(color="MediumPurple", size=10)))
    # Legend -> Support
    fig.add_trace(go.Scatter(
        y=[ss[0]], name="Support", mode="lines", marker=dict(color="LightSeaGreen", size=10)))
    # Legend -> Current Resistance
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Current Resistance : {float(res_above[0])}", mode="markers+lines",
        marker=dict(color="MediumPurple", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Next Resistances: {', '.join(map(str, res_above[1:4]))}", mode="lines",
        marker=dict(color="MediumPurple", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"|-> : {', '.join(map(str, res_above[4:8]))}", mode="lines",
        marker=dict(color="#fcedfa", size=10)))
    # Legend -> Current Support
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Current Support : {float(sup_below[0])}", mode="markers+lines",
        marker=dict(color="LightSeaGreen", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Next Supports: {', '.join(map(str, sup_below[1:4]))}", mode="lines",
        marker=dict(color="LightSeaGreen", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"|-> : {', '.join(map(str, sup_below[4:8]))}", mode="lines",
        marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f" --------------------------------- ", mode="markers", marker=dict(color="#f5efc4", size=0)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Indicators", mode="markers", marker=dict(color="#fcedfa", size=14)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"RSI         : {int(rsi[-3])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"MACD      : {int(macd['MACDh_12_26_9'][1])}", mode="lines",
        marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Volume    : {int(volume[2]):,.1f} $ ", mode="lines", marker=dict(color="#fcedfa", size=10)))
    mtp = 6
    for _ in fib:
        fig.add_trace(go.Scatter(
            y=[ss[0]], name=f"Fib {fib_multipliers[mtp]:.3f} : {fib[mtp]:.1f}", mode="lines",
            marker=dict(color="#fcedfa", size=10)))
        mtp -= 1

    # Chart updates
    fig.update_layout(title=str(df['symbol'][0] + ' Chart'), hovermode='x', dragmode="zoom",
                      paper_bgcolor='#FFE4F5', plot_bgcolor='#fcedfa', xaxis_rangeslider_visible=False,
                      xaxis_title="Date", yaxis_title="Price", legend_title="Legend",
                      legend=dict(bgcolor='#fcedfa'))  # Ignore slider -> xaxis_rangeslider_visible=False
    fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)
    if not os.path.exists("images"):
        os.mkdir("images")
    image = f"images/{df['date'].dt.strftime('%b-%d-%y')[candle_count]}{settings.file_name}.jpeg"
    fig.write_image(image, width=1920, height=1080)  # Save image for tweet
    fig.write_html(f"images/{df['date'].dt.strftime('%b-%d-%y')[candle_count]}{settings.file_name}.html")
    text_image = f"#{settings.exchange_name} #{settings.coin_name}{settings.pair_name} support and resistance levels \n {df['date'].dt.strftime('%b-%d-%Y')[candle_count]}\n#{settings.coin_name} ${settings.coin_name}"

    def for_tweet():
        tweet.send_tweet(image, text_image)
        while tweet.is_image_tweet().text != text_image:
            time.sleep(1)
            if tweet.is_image_tweet().text != text_image:
                tweet.api.update_status(status=
                                        f"#{settings.coin_name}{settings.pair_name} "
                                        f"{df['date'].dt.strftime('%b-%d-%Y')[candle_count]} "
                                        f"support and resistance levels "
                                        f"#{settings.coin_name}\nRes={res_above[:7]} \nSup={sup_below[:7]}",
                                        in_reply_to_status_id=tweet.is_image_tweet().id)
            break

    for_tweet()
    fig.show()


if __name__ == "__main__":

    settings.check_names()
    get_data.download_data()
    if os.path.isfile(settings.full_filename):  # <- Checks .csv file is there or not
        print(f"{settings.full_filename} downloaded and created.")
    else:
        print(
            "One or more issues caused the download to fail. Make sure you typed the filename correctly in the settings. ")
    main()
    delete_file.remove()
