from binance import Client


def frame_select(self: str):
    if self == "1M":
        time_frame = Client.KLINE_INTERVAL_1MINUTE
    elif self == "3M":
        time_frame = Client.KLINE_INTERVAL_3MINUTE
    elif self == "5M":
        time_frame = Client.KLINE_INTERVAL_5MINUTE
    elif self == "15M":
        time_frame = Client.KLINE_INTERVAL_15MINUTE
    elif self == "30M":
        time_frame = Client.KLINE_INTERVAL_30MINUTE
    elif self == "1H":
        time_frame = Client.KLINE_INTERVAL_1HOUR
    elif self == "2H":
        time_frame = Client.KLINE_INTERVAL_2HOUR
    elif self == "4H":
        time_frame = Client.KLINE_INTERVAL_4HOUR
    elif self == "6H":
        time_frame = Client.KLINE_INTERVAL_6HOUR
    elif self == "8H":
        time_frame = Client.KLINE_INTERVAL_8HOUR
    elif self == "12H":
        time_frame = Client.KLINE_INTERVAL_12HOUR
    elif self == "1D":
        time_frame = Client.KLINE_INTERVAL_1DAY
    elif self == "3D":
        time_frame = Client.KLINE_INTERVAL_3DAY
    else:
        return print("This time frame is not allowed.")

    return time_frame
