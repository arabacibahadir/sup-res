from binance import Client
from datetime import datetime, timedelta


""" Timeframes:
Client.KLINE_INTERVAL_1MINUTE
Client.KLINE_INTERVAL_3MINUTE
Client.KLINE_INTERVAL_5MINUTE
Client.KLINE_INTERVAL_15MINUTE
Client.KLINE_INTERVAL_30MINUTE
Client.KLINE_INTERVAL_1HOUR
Client.KLINE_INTERVAL_2HOUR
Client.KLINE_INTERVAL_4HOUR
Client.KLINE_INTERVAL_6HOUR
Client.KLINE_INTERVAL_8HOUR
Client.KLINE_INTERVAL_12HOUR
Client.KLINE_INTERVAL_1DAY
Client.KLINE_INTERVAL_3DAY
Client.KLINE_INTERVAL_1WEEK
Client.KLINE_INTERVAL_1MONTH
"""


def timeframe(self):
    current = datetime.now()
    if self == Client.KLINE_INTERVAL_1MINUTE:
        start_date = current + timedelta(minutes=-260)
        start = start_date.strftime("%d %B, %Y")  # Start date to now

    elif self == Client.KLINE_INTERVAL_3MINUTE:
        start_date = current + timedelta(minutes=-780)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_5MINUTE:
        start_date = current + timedelta(minutes=-1300)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_15MINUTE:
        start_date = current + timedelta(minutes=-3900)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_30MINUTE:
        start_date = current + timedelta(minutes=-7800)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_1HOUR:
        start_date = current + timedelta(hours=-260)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_2HOUR:
        start_date = current + timedelta(hours=-520)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_4HOUR:
        start_date = current + timedelta(hours=-1040)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_6HOUR:
        start_date = current + timedelta(hours=-1560)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_8HOUR:
        start_date = current + timedelta(hours=-2080)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_12HOUR:
        start_date = current + timedelta(days=-15)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_1DAY:
        start_date = current + timedelta(days=-260)
        start = start_date.strftime("%d %B, %Y")

    elif self == Client.KLINE_INTERVAL_3DAY:
        start_date = current + timedelta(days=-780)
        start = start_date.strftime("%d %B, %Y")

    else:
        return print("This time frame is not allowed.")

    return start
