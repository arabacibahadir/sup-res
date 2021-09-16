import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta
from itertools import repeat


# daily working but hourly gives same date -> add hours for chart !DAILY -> try without dates--x-line
# check csv files some data broken -> eth daily
# daily-hourly? hourly priced model?
# Rest api for other coins
# Twitter api add
# Refactor var's
# Add classes
# price>res -> support, price< support -> res ->>> add
# under current price, res'es are supports-> change line colors and for reverse
# from other exchanges(ftx,coinbase etc.) sup res levels and difference and percentage of sup res levels?
def main():
    # nrows -> Number of candlesticks
    csv = "Binance_btcUSDT_d.csv"
    df = pd.read_csv(csv, delimiter=',', encoding="utf-8-sig", index_col=False, nrows=254, skiprows=[0])
    df = df.iloc[::-1]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)
    volume = list(reversed((df['Volume USDT'])))
    sma10 = list((df.ta.sma(10)))
    sma50 = list((df.ta.sma(50)))
    sma100 = list((df.ta.sma(100)))
    rsi = list((ta.rsi(df['close'])))
    fib = []
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
        fib_multipliers = [0.236, 0.382, 0.5, 0.618, 0.786, 1.382, 1.618]
        for multi in fib_multipliers:
            # -> Downtrend Fibonacci Retracement Formula we use in here
            retracement_levels = low_price + (high_price - low_price) * multi
            fib.append(retracement_levels)

    df = df[:len(df)]
    fig = go.Figure([go.Candlestick(x=df['date'].dt.strftime('%b-%d-%y'),
                                    name="Candlestick",
                                    text=df['date'].dt.strftime('%b-%d-%y'),
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close'])])

    ss = []  # ss : Support list
    rr = []  # rr : Resistance list

    # Sensitivity -> As the number increases, the detail decreases. (3,1) probably is the ideal one for daily charts.
    for row in range(3, len(df)):
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
    # print(new_sup,"newres",new_res)
    sup_below.extend(new_sup)
    res_above.extend(new_res)
    sup_below = sorted(sup_below, reverse=True)
    if len(sup_below) < 5:
        sup_below.extend(repeat(sup_below[0], 4))

    res_above = sorted(res_above)
    if len(res_above) < 5:
        res_above.extend(repeat(res_above[0], 4))

    fib_pl(res_above[-1], sup_below[0])  # Fibonacci func

    c = 0
    # Drawing support lines
    while 1:
        if c > len(ss) - 1:
            break
        # Support Lines
        fig.add_shape(type='line', x0=ss[c][0] - 1, y0=ss[c][1],
                      x1=len(df) + 30,
                      y1=ss[c][1], line=dict(color="LightSeaGreen", width=2))
        # Support annotations
        fig.add_annotation(x=len(df) + 10, y=ss[c][1], text=str(ss[c][1]),
                           font=dict(size=15, color="LightSeaGreen"))
        c += 1

    # Drawing resistance lines
    c = 0
    while 1:
        if c > len(rr) - 1:
            break
        # Resistance Lines
        fig.add_shape(type='line', x0=rr[c][0] - 1, y0=rr[c][1],
                      x1=len(df) + 30,
                      y1=rr[c][1], line=dict(color="MediumPurple", width=1))
        # Resistance annotations
        fig.add_annotation(x=len(df) + 30, y=rr[c][1], text=str(rr[c][1]),
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
        y=[ss[0]], name=f"Current Resistance : {int(rr[-1][1])}", mode="markers+lines",
        marker=dict(color="MediumPurple", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Next Resistances: {', '.join(map(str, res_above[1:4]))}", mode="lines",
        marker=dict(color="MediumPurple", size=10)))
    # Legend -> Current Support
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Current Support : {int(ss[-1][1])}", mode="markers+lines",
        marker=dict(color="LightSeaGreen", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Next Supports: {', '.join(map(str, sup_below[2:5]))}", mode="lines",
        marker=dict(color="LightSeaGreen", size=8)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f" -------------------------- ", mode="markers", marker=dict(color="#f5efc4", size=0)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Indicators", mode="markers", marker=dict(color="#fcedfa", size=14)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"RSI : {int(rsi[100])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Volume : {int(volume[1])} $ ", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma10, name=f"SMA10 : {int(sma10[-1])}",
                             line=dict(color='#5c6cff', width=3)))
    fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma50, name=f"SMA50 : {int(sma50[-1])}",
                             line=dict(color='#950fba', width=3)))
    fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma100, name=f"SMA100 : {int(sma100[-1])}",
                             line=dict(color='#a69b05', width=3)))
    # fibs [0.236, 0.382, 0.5, 0.618, 0.786, 1.382, 1.618]
    # add class
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 1.618: {int(fib[6])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 1.382: {int(fib[5])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 0.786: {int(fib[4])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 0.618: {int(fib[3])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 0.500: {int(fib[2])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 0.382: {int(fib[1])}", mode="lines", marker=dict(color="#fcedfa", size=10)))
    fig.add_trace(go.Scatter(
        y=[ss[0]], name=f"Fib 0.236: {int(fib[0])}", mode="lines", marker=dict(color="#fcedfa", size=10)))

    # Chart updates
    fig.update_layout(title=str(df['symbol'][0] + ' Daily Chart'), hovermode='x', dragmode="zoom",
                      paper_bgcolor='#FFE4F5', plot_bgcolor='#fcedfa', height=1250, width=2100,
                      xaxis_title="Date", yaxis_title="Price", legend_title="Legend",
                      legend=dict(bgcolor='#fcedfa'))
    fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.show()


if __name__ == "__main__":
    main()
