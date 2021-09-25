import os
import pandas as pd
import plotly.graph_objects as go
from itertools import repeat
import delete_file
import get_data
import settings


def main():
    csv = settings.full_filename
    print(f"{csv} data analysis in progress.")
    candle_count = 254  # Number of candlesticks
    df = pd.read_csv(csv, delimiter=',', encoding="utf-8-sig", index_col=False, skiprows=[0], nrows=candle_count,
                     keep_default_na=False)
    df = df.iloc[::-1]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)
    df = df.append(df.tail(1), ignore_index=True)  # Dodging algorithm issue
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
    if len(sup_below) < 10:
        sup_below.extend(repeat(sup_below[0], 9))

    res_above = sorted(res_above)
    if len(res_above) < 10:
        res_above.extend(repeat(res_above[0], 9))

    fib_pl(res_above[-1], sup_below[-1])  # Fibonacci func
    res_above = [int(a) for a in res_above]
    sup_below = [int(a) for a in sup_below]

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

    # Chart updates
    fig.update_layout(title=str(df['symbol'][0] + ' Daily Chart'), hovermode='x', dragmode="zoom",
                      paper_bgcolor='#FFE4F5', plot_bgcolor='#fcedfa', height=1250, width=2100,
                      xaxis_title="Date", yaxis_title="Price", legend_title="Legend",
                      legend=dict(bgcolor='#fcedfa'))
    fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)
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
