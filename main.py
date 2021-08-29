"""
This program can detect support-resistance, some candle patterns,rsi,macd...
"""
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta
#rest ile api yaz-kripto seçmece yap
#class ata bazi şeylere
# ilk sitenin web sayfa tanıtımı var onu kendim sildim belki if yazıp o sitelinn linki varsa sil kodu yazabilirim--csvdeki ilk satırı sil,sildiyse devam silmediyse sil
df = pd.read_csv("BTC.csv", delimiter=',', encoding="utf-8-sig", index_col=False,
                 nrows=254)  # nrows kaç tane veriyi incelediğini gösteriyor onu kullanıcıya seçtirebiliriz mi?
df = df.iloc[::-1]
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
df.reset_index(drop=True, inplace=True)
#REV OLANLARI NULL GELENLERİ SİLEREK HALLEDEBİLİRİZ TEK LİSTTEN YAPMAK İÇİN. BÖYLE GÜZEL DURMUYOR
volume = list(reversed((df['Volume USDT'])))
sma10 = list((df.ta.sma(10)))
sma10_rev=list(reversed(df.ta.sma(10)))
sma50 = list((df.ta.sma(50)))
sma50_rev = list(reversed(df.ta.sma(50)))
sma100 = list((df.ta.sma(100)))
sma100_rev = list(reversed(df.ta.sma(100)))
rsi = list((ta.rsi(df['close'])))


def support(btcPrice1, l, n1, n2):
    for i in range(l - n1 + 1, l + 1):
        if btcPrice1.low[i] > btcPrice1.low[i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if btcPrice1.low[i] < btcPrice1.low[i - 1]:
            return 0
    return 1


def resistance(btcPrice1, l, n1, n2):
    for i in range(l - n1 + 1, l + 1):
        if btcPrice1.high[i] < btcPrice1.high[i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if btcPrice1.high[i] > btcPrice1.high[i - 1]:
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


ss = rr = []  # ss:Support list # rr:Resistance list
# sensitive yapıyoruz,(2,2)ler o anlama geliyor.higher(2den fazla mesela 3 olunca sens azalır daha detyaylı verir veriyi grafiği)
# sensitivity change 3,1
for row in range(3, len(df)):
    if support(df, row, 3, 1):
        ss.append((row, df.low[row], 1))
    if resistance(df, row, 3, 1):
        rr.append((row, df.high[row], 1))  # if birbirlerine çok yakınlarsa diğerini sil ya da yazı olarak yazma ya
        # da sadece 1 tanesini yaz
        # eğer dirençler birbirleri çok yakınsa x noktalarını biraz sağa sola kaydır??????????

c = 0
# Draw Support line
while 1:
    if c > len(ss) - 1:
        break
    # Support Line
    fig.add_shape(type='line', x0=ss[c][0] - 1, y0=ss[c][1],
                  x1=len(df) + 30,
                  y1=ss[c][1],
                  line=dict(color="LightSeaGreen", width=2))
    # Support annotations
    fig.add_annotation(x=len(df) + 10, y=ss[c][1], text=str(ss[c][1]),
                       font=dict(size=12, color="LightSeaGreen"))

    c += 1

# Draw Resistance line
c = 0
while 1:
    if c > len(rr) - 1:
        break
    # Resistance Line
    fig.add_shape(type='line', x0=rr[c][0] - 1, y0=rr[c][1],
                  x1=len(df) + 30,
                  y1=rr[c][1],
                  line=dict(color="MediumPurple", width=1))
    # Resistance annotations
    fig.add_annotation(x=len(df) + 30, y=rr[c][1], text=str(rr[c][1]),
                       font=dict(

                           size=14,
                           color="MediumPurple"
                       ))

    c += 1


#buraya class ata
# Legend->Resistance
fig.add_trace(go.Scatter(
    y=[ss[0]],
    name="Resistance",
    mode="lines",
    marker=dict(color="MediumPurple", size=10)
))
# Legend->Support
fig.add_trace(go.Scatter(
    y=[ss[0]],
    name="Support",
    mode="lines",
    marker=dict(color="LightSeaGreen", size=10)
))
# Legend->Current Resistance
fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f"Current Resistance : {int(rr[-1][1])}",
    mode="markers+lines",
    marker=dict(color="MediumPurple", size=10)
))
# Legend->Current Support
fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f"Current Support : {int(ss[-1][1])}",
    mode="markers+lines",
    marker=dict(color="LightSeaGreen", size=10)))


fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f" ",
    mode="markers",
    marker=dict(color="#E2E2E2", size=0)))

fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f" -------------------------- ",
    mode="markers",
    marker=dict(color="#E2E2E2", size=0)))

fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f" ",
    mode="markers",
    marker=dict(color="#E2E2E2", size=0)))

fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f"Indicators",
    mode="markers",
    marker=dict(color="#E2E2E2", size=14)))
fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f"RSI : {int(rsi[100])}",
    mode="lines",
    marker=dict(color="#E2E2E2", size=10)))
fig.add_trace(go.Scatter(
    y=[ss[0]],
    name=f"Volume : {int(volume[1])} $ ",
    mode="lines",
    marker=dict(color="#E2E2E2", size=10)))

fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma10, name=f"SMA10 : {int(sma10_rev[0])}",
                         line=dict(color='#5c6cff', width=3)))
fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma50, name=f"SMA50 : {int(sma50_rev[0])}",
                         line=dict(color='#950fba', width=3)))
fig.add_trace(go.Scatter(x=df['date'].dt.strftime('%b-%d-%y'), y=sma100, name=f"SMA100 : {int(sma100_rev[0])}",
                         line=dict(color='#a69b05', width=3)))

#fib levelleri???#fib levelleri???#fib levelleri???
#fib levelleri???#fib levelleri???#fib levelleri???
#fib levelleri???#fib levelleri???#fib levelleri???

fig.update_layout(title=str(df['symbol'][0] + ' Daily Chart'), hovermode='x', dragmode="zoom", width=1900, height=1250,
                  xaxis_title="Date", yaxis_title="Price", legend_title="Legend", legend = dict(bgcolor = '#E2E2E2'),
                  )

fig.update_xaxes(showspikes=True, spikecolor="green", spikethickness=2)
fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=2)

fig.show()
# candle 2den başlamalı yoksa algoritma gg hatırlatma olarak ekle-->buna gerek olmayabilir belki
# main kısmını ekle program başlamadan önce website adresini islsin
# background color?
#ilk 5 direnç ilk 3 supportu yazsın karışmasın ortalık?
#candle pattern?
