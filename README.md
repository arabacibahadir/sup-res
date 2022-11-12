# Sup-Res :chart_with_upwards_trend:

_For online demonstration_ -> https://arabacibahadir.github.io/sup-res/ 

Sup-Res is  mobile-ready, offline-storage compatible and a great companion for finding liquidity pools, support and resistance levels with a scalable chart.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/32988819/166165397-af4c7f29-1746-49b6-be3a-9a12d838f7e6.gif)


## Features :star2:

- Easily find support-resistance and liquidity levels on the chart
- Using it in almost any time series with sensitivity adjustment 
- Export documents as `HTML, PDF, .jpeg, .png` 
- Automatically share to your twitter followers with an image and text of support-resistance levels
- Supports [Tradingview Pine Script](https://www.tradingview.com/pine-script-docs/en/v4/Introduction.html) 
- Manageable via [Telegram](https://python-telegram-bot.org)
- WebUI

![git](https://user-images.githubusercontent.com/32988819/148457547-45d47bc2-52a0-426a-8d4c-861fe6fd013d.png)

## Installation :hammer_and_wrench:
Sup-Res requires Python 3.10+ to run.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries. This process may take a long time.

```bash
pip install -r requirements.txt
```

## Usage :computer:

When you run the code, main function will ask ticker and time frame and then the local web page will open where you can see the support-resistance levels, RSI, SMA, MACD, Fibonacci and candlestick patterns. 
````
Ticker and Time Frame:
BTCUSDT 15M
````
````
Supported Tickers: All Binance tickers
Supported Time Frames: 1M, 3M, 5M, 15M, 30M, 1H, 2H, 4H, 6H, 8H, 12H, 1D, 3D (M: Minute, H: Hour, D: Day)
````

If you want to share as a tweet, change api keys with yours in `git_tw_access.py` file, and change your user handle name. [Twitter API guide](https://developer.twitter.com/en/docs/twitter-api). Then uncomment `save` and `twitter` functions in `main.py`.

````python
# Twitter api keys -> https://developer.twitter.com/en/docs/twitter-api
twitter_api = 'YOUR-API'
twitter_key_secret = 'API-SECRET'
twitter_token = 'TOKEN'
twitter_token_secret = 'TOKEN-SECRET'
user_handle = '@HANDLE-NAME'
````

Pine Script file will be created after run successfully main function. 

Your python alias could be different like "py, python3", you should change your alias if you are using telegram-bot if your python alias is different. 

>You can get more precise lines by changing sensitivity of the data in the code. 


![chart](https://user-images.githubusercontent.com/32988819/166165460-b1e2be3e-014c-4aea-83e6-c118075f68df.png)


 
## Main Motivation :books:
New investors are investing without having any technical knowledge. Also, those with little experience follow the price actions and make their buys and sells according to various charts. Technical analysis is the bulk of this work.

I worked on a code that could provide help for users who don't have much experience with _price action_. If you really have no idea and are investing, then don't. Before investing, you should observe the market movements and do not get **FOMO**.

Supports and resistances are generally zones, not just lines. Especially in cryptocurrencies, markets push you towards points where you can stop your position. Watch out for high volume breakouts, sudden price changes, and trend reversals. If you are investing in low volume coins, it is very dangerous to trade on new coin charts without support and resistance levels.


![image](https://user-images.githubusercontent.com/32988819/166165539-5a4eea0a-456e-482d-aa56-96b5eaffc37a.png)


## Support-Resistance Lines :chart_with_downwards_trend:

If a pair has failed to break a point multiple times or has risen by repeatedly tapping that point, you can draw a reliable line there. The general opinion is that this price should be touched at least 2 times, if possible, 3 times. If there are more touches, reliability increases. If the current price is above the old resistance, this resistance will act as support. Vice versa is also true.

![28sep](https://user-images.githubusercontent.com/32988819/135044659-579b26c8-8141-41c2-9b4e-d3c99b41b571.png)


_28 September 2021 BTCUSDT Binance_

## Indicators :bar_chart:
[MA](https://www.investopedia.com/terms/m/movingaverage.asp), 
[RSI](https://www.investopedia.com/terms/r/rsi.asp), 
[MACD](https://www.investopedia.com/terms/m/macd.asp),
[Fibonacci Retracement Levels](https://www.investopedia.com/terms/f/fibonacciretracement.asp),
[Candlestick Patterns](https://www.elearnmarkets.com/blog/30-candlestick-charts-in-stock-market/)

Never rely on just one piece of data and indicators, it can be misleading. Always include _fundamental analysis_ alongside _technical analysis_.

![legend](https://user-images.githubusercontent.com/32988819/168901021-81d885d4-19de-4ba6-a3d0-c69faf2ccbf5.png)


![candle](https://user-images.githubusercontent.com/32988819/131737076-f52ac75e-1f4d-4d79-b14c-61a81ee8ecfe.png)

## Some screenshots :camera_flash:
_BTCUSDT_ chart
![Jun-27-22BTCUSDT](https://user-images.githubusercontent.com/32988819/176189250-c4564312-cfd7-41d9-aaed-620ca4bcabc7.jpeg)


![proofsups](https://user-images.githubusercontent.com/32988819/134022109-31c46da5-f1d3-4865-990e-91dd2fd75367.png)

![proof22](https://user-images.githubusercontent.com/32988819/134344483-7bb93cb7-ab29-4505-82bd-06f387e992c5.png)

![48500proof](https://user-images.githubusercontent.com/32988819/133648941-de7f0b2d-0780-4a11-8e6f-98d06b1f6ad1.png)

![works](https://user-images.githubusercontent.com/32988819/133649195-6645e31b-1736-4076-ba26-385063d4915e.png)

## Pine Script :bookmark_tabs:

Sup-Res supports Pine Script scripting language. Just **run** *main.py* file, then **copy** "./pinescript.txt" and **paste** *Tradingview Pine Script* section.
Also telegram bot works with Pine Script.

![pinecodes](https://user-images.githubusercontent.com/32988819/136625978-355c9591-6865-441a-871a-dd3526b4308f.png)

![pine_trade](https://user-images.githubusercontent.com/32988819/136625994-1f0400a6-6c97-4126-b1b2-0f630f739133.png)

![lines](https://user-images.githubusercontent.com/32988819/136626000-85bb5d7d-73d3-4568-bd0d-61d17dbc67b6.png)


## Contributing :handshake:
Pull requests are welcome, any contributions you make are greatly appreciated. Before PR please open an issue what you would like to change.

Follow [PEP 8 Coding Style guidelines](https://www.python.org/dev/peps/pep-0008/).

- Fork the Project
- Create your Feature Branch `git checkout -b feature/NewFeature`
- Commit your Changes `git commit -m 'Add some NewFeature'`
- Push to the Branch `git push origin feature/NewFeature`
- Open a Pull Request


## License :page_with_curl:
Sup-Res is licensed under the GNU General Public License v3.0

