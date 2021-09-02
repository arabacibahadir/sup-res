import pandas as pd
import plotly.graph_objects as go


def main():
    # nrows -> Number of candlesticks
    csv = "Binance_ETHUSDT_d.csv"
    df = pd.read_csv(csv, delimiter=',', encoding="utf-8-sig", index_col=False, nrows=254,
                     skiprows=[0])
    df = df.iloc[::-1]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.reset_index(drop=True, inplace=True)

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
            ss.append((row, df.low[row], 1))
        if resistance(df, row, 3, 1):
            rr.append((row, df.high[row], 1))

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

    # Chart updates
    fig.update_layout(title=str(df['symbol'][0] + ' Daily Chart'), hovermode='x', dragmode="zoom",
                      paper_bgcolor='#FFE4F5', plot_bgcolor='#fcedfa', height=1250, width=1900,
                      xaxis_title="Date", yaxis_title="Price", legend_title="Legend",
                      legend=dict(bgcolor='#fcedfa'))
    fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)
    fig.show()


if __name__ == "__main__":
    main()
