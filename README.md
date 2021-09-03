# Sup-Res

A great companion for drawing support and resistance lines.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

```bash
pip install pandas
pip install pandas-ta
pip install plotly
```

## Usage

Your csv file should be in the folder where the python code is. Then you should write the file name to the csv variable in the code, probably "Binance_BTCUSDT_d.csv" is written in the code, you will write the name of your csv file there.

````bash
csv="Binance_BTCUDT_d.csv"
````
You can get various csv files from [here](https://www.cryptodatadownload.com/data/). You can select the exchanges and then download the csv files of the what crypto you want.

When you run the code, the local web page will open where you can see the support resistance zones, rsi, sma, fibonacci.

*May not be able to catch some support and resistance lines due to sensitivity. You can get more precise lines by changing the data. 
![btc_daily](https://user-images.githubusercontent.com/32988819/131736526-fdd818d1-f52b-4f33-be98-eb8810f4fa01.png)
If you encounter an index error, try the only_chart.py version. 
## Main Motivation
A lot of investors are investing without having any technical knowledge. Those with a little experience follow the price movements and make their buys and sells according to various charts. Technical analysis is the bulk of this work. 

I worked on a code that could provide help for users who don't have much experience. Errors can happen, support and resistance are generally zones, not just lines. Especially in cryptocurrencies, markets push you towards the points where you can stop. Watch out for high volume breakouts, sudden price changes and trend reversals.

Every investor's wallet and strategy is different. Stay away from high leverage if you don't trust your experience. Your priority should not be to make money, you should be try to protect your money. 
Supports and resistances formed in short time frames (5m, 15m, 1h) may be easier to break. Not every support and resistance works. 

![candle](https://user-images.githubusercontent.com/32988819/131737076-f52ac75e-1f4d-4d79-b14c-61a81ee8ecfe.png)


## Support-Resistance Lines
If a pair has failed to break a point multiple times or has risen by repeatedly tapping that point, you can draw a reliable line there. The general opinion is that this process is touched at least 2 times, if possible 3 times. If there are more touches, the reliability increases. 

## Indicators
[MA](https://www.investopedia.com/terms/m/movingaverage.asp), 
[RSI](https://www.investopedia.com/terms/r/rsi.asp), [Fibonacci Retracement Levels](https://www.investopedia.com/terms/f/fibonacciretracement.asp)

Never rely on just one piece of data, it can be misleading. Always include fundamental analysis alongside technical analysis. Be careful not to miss the news. 

![legend](https://user-images.githubusercontent.com/32988819/131736679-16f3b6c7-7a63-474d-a776-c9e24d8467f1.png)
