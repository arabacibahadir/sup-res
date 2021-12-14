from binance import Client
from datetime import datetime, timedelta

""" Supported time frames:
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
"""


def frame_select(self: str):
    current = datetime.now()
    if self == "1M":
        time_frame = Client.KLINE_INTERVAL_1MINUTE
        start_date = current + timedelta(minutes=-260)
        start = start_date.strftime("%d %B, %Y")  # Start date to now
    elif self == "3M":
        time_frame = Client.KLINE_INTERVAL_3MINUTE
        start_date = current + timedelta(minutes=-780)
        start = start_date.strftime("%d %B, %Y")
    elif self == "5M":
        time_frame = Client.KLINE_INTERVAL_5MINUTE
        start_date = current + timedelta(minutes=-1300)
        start = start_date.strftime("%d %B, %Y")
    elif self == "15M":
        time_frame = Client.KLINE_INTERVAL_15MINUTE
        start_date = current + timedelta(minutes=-3900)
        start = start_date.strftime("%d %B, %Y")
    elif self == "30M":
        time_frame = Client.KLINE_INTERVAL_30MINUTE
        start_date = current + timedelta(minutes=-7800)
        start = start_date.strftime("%d %B, %Y")
    elif self == "1H":
        time_frame = Client.KLINE_INTERVAL_1HOUR
        start_date = current + timedelta(hours=-260)
        start = start_date.strftime("%d %B, %Y")
    elif self == "2H":
        time_frame = Client.KLINE_INTERVAL_2HOUR
        start_date = current + timedelta(hours=-520)
        start = start_date.strftime("%d %B, %Y")
    elif self == "4H":
        time_frame = Client.KLINE_INTERVAL_4HOUR
        start_date = current + timedelta(hours=-1040)
        start = start_date.strftime("%d %B, %Y")
    elif self == "6H":
        time_frame = Client.KLINE_INTERVAL_6HOUR
        start_date = current + timedelta(hours=-1560)
        start = start_date.strftime("%d %B, %Y")
    elif self == "8H":
        time_frame = Client.KLINE_INTERVAL_8HOUR
        start_date = current + timedelta(hours=-2080)
        start = start_date.strftime("%d %B, %Y")
    elif self == "12H":
        time_frame = Client.KLINE_INTERVAL_12HOUR
        start_date = current + timedelta(days=-15)
        start = start_date.strftime("%d %B, %Y")
    elif self == "1D":
        time_frame = Client.KLINE_INTERVAL_1DAY
        start_date = current + timedelta(days=-260)
        start = start_date.strftime("%d %B, %Y")
    elif self == "3D":
        time_frame = Client.KLINE_INTERVAL_3DAY
        start_date = current + timedelta(days=-780)
        start = start_date.strftime("%d %B, %Y")
    else:
        return print("This time frame is not allowed.")
    return time_frame, start
