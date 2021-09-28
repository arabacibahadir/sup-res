# Sup-Res
_For online preview_ -> https://arabacibahadir.github.io/sup-res/

Sup-Res is  mobile-ready, offline-storage compatible and a great companion for drawing support and resistance lines with a scalable chart.

![cropedgif](https://user-images.githubusercontent.com/32988819/134764951-b52bb659-f0d6-455d-a995-05c716564a12.gif)

## Features

- Easily find support and resistance levels on the chart
- Using it in almost any time series with sensitivity adjustment 
- Export documents as HTML, PDF, .jpeg, .png
- Share to twitter easily with image and support and resistance levels text automatically
![twitter](https://user-images.githubusercontent.com/32988819/134763396-4f5ef8a9-ffa3-4a71-99ad-ec3ea8b9770e.png)

## Installation
Sup-Res requires Python 3.6+ to run.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

```bash
pip install candlestick-patterns-subodh101
pip install pandas
pip install pandas-ta
pip install plotly
pip install tweepy 
```

## Usage
In 'settings.py' file you should change what pair do you want to use.
````python
exchange_name = 'Binance' # Which exchange you want to use
coin_name = 'BTC' 
pair_name = 'USDT'
time_series = 'd' # "d" for daily chart
# Example -> Output should looks like "Binance_BTCUSDT_d.csv" end of the code
````
If you want to share as a tweet, change api keys with yours in 'git_tw_access.py' file.

````python
# Twitter api keys
tw_api = 'YOUR-API'
tw_key_secret = 'API-SECRET'
tw_token = 'TOKEN'
tw_token_secret = 'TOKEN-SECRET'
````


When you run the code, the local web page will open where you can see the support resistance zones, rsi, sma, macd, fibonacci, candlestick patterns. It will share tweet automatically.


>Alghoritms may not be able to catch some support and resistance lines due to sensitivity. You can get more precise lines by changing sensitivity of the data in the code. 

![btcusdt](https://user-images.githubusercontent.com/32988819/134763427-a4578891-a430-40cd-9b4c-dbf45bff6cc3.png)



>If you encounter an index error, try the *only_chart.py* version. Some data may be corrupt or not working. 
## Main Motivation
A lot of new investors are investing without having any technical knowledge. Also those with a little experience follow the price movements and make their buys and sells according to various charts. Technical analysis is the bulk of this work. 

I worked on a code that could provide help for users who don't have much experience about _price action_. If you really have no idea and are investing, then don't. Before investing, you should observe the market movements and do not get **FOMO**. This is not a game and every day people lose all their money. Get your priorities straight.

Support and resistance are generally zones, not just lines. Especially in cryptocurrencies, markets push you towards the points where you can stop. Watch out for high volume breakouts, sudden price changes and trend reversals. If you are investing low volume coin, it is very dangerous to trade on new coin charts without support and resistance levels. 

- Every investor's wallet and strategy is different.
- Stay away from **high leverage** if you don't trust your experience.
- Your priority should **not** be to make money, you should be try to save your money. 
- Supports and resistances formed in short time frames (5m, 15m, 1h) may be easier to break. 
- Not every support and resistance works in **high volatility**. 

![candle](https://user-images.githubusercontent.com/32988819/131737076-f52ac75e-1f4d-4d79-b14c-61a81ee8ecfe.png)


## Support-Resistance Lines
If a pair has failed to break a point multiple times or has risen by repeatedly tapping that point, you can draw a reliable line there. The general opinion is that this price is touched at least 2 times, if possible 3 times. If there are more touches, the reliability increases. 
If the current price is above the old resistance, this resistance will act as support. Vice versa is also true. 

![28sep](https://user-images.githubusercontent.com/32988819/135044659-579b26c8-8141-41c2-9b4e-d3c99b41b571.png)


_28 September 2021 BTCUSDT Binance_

## Indicators
[MA](https://www.investopedia.com/terms/m/movingaverage.asp), 
[RSI](https://www.investopedia.com/terms/r/rsi.asp), 
[MACD](https://www.investopedia.com/terms/m/macd.asp),
[Fibonacci Retracement Levels](https://www.investopedia.com/terms/f/fibonacciretracement.asp),
[Candlestick Patterns](https://www.elearnmarkets.com/blog/30-candlestick-charts-in-stock-market/).

Never rely on just one piece of data and indicators, it can be misleading. Always include _fundamental analysis_ alongside _technical analysis_. **Be careful** not to miss the _news_ and _fundamental analysis_. 

![legend](https://user-images.githubusercontent.com/32988819/134764245-18551144-ec9c-4489-9a0a-495e49de9a9d.png)


## Some screenshots
_ETHUSDT_ example chart

![ethusdt](https://user-images.githubusercontent.com/32988819/134763471-d5abe6ac-bb80-4dcb-94db-5d491802a8d7.png)

_BTCUSDT_ levels

![proofsups](https://user-images.githubusercontent.com/32988819/134022109-31c46da5-f1d3-4865-990e-91dd2fd75367.png)

![proof22](https://user-images.githubusercontent.com/32988819/134344483-7bb93cb7-ab29-4505-82bd-06f387e992c5.png)

![48500proof](https://user-images.githubusercontent.com/32988819/133648941-de7f0b2d-0780-4a11-8e6f-98d06b1f6ad1.png)

![works](https://user-images.githubusercontent.com/32988819/133649195-6645e31b-1736-4076-ba26-385063d4915e.png)

## Contributing
Pull requests are welcome. Before PR please open an issue what you would like to change.

Follow [PEP 8 Coding Style guidelines](https://www.python.org/dev/peps/pep-0008/).

## License
Sup-Res is licensed under the GNU General Public License v3.0

