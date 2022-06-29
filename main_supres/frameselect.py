from binance import Client
from datetime import datetime, timedelta

frame_select_dict = {
    "1M": [Client.KLINE_INTERVAL_1MINUTE, -260],
    "3M": [Client.KLINE_INTERVAL_3MINUTE, -780],
    "5M": [Client.KLINE_INTERVAL_5MINUTE, -1300],
    "15M": [Client.KLINE_INTERVAL_15MINUTE, -3900],
    "30M": [Client.KLINE_INTERVAL_30MINUTE, -7800],
    "1H": [Client.KLINE_INTERVAL_1HOUR, -260],
    "2H": [Client.KLINE_INTERVAL_2HOUR, -520],
    "4H": [Client.KLINE_INTERVAL_4HOUR, -1040],
    "6H": [Client.KLINE_INTERVAL_6HOUR, -1560],
    "8H": [Client.KLINE_INTERVAL_8HOUR, -2080],
    "12H": [Client.KLINE_INTERVAL_12HOUR, -15],
    "1D": [Client.KLINE_INTERVAL_1DAY, -260],
    "3D": [Client.KLINE_INTERVAL_3DAY, -780],
}


def frame_select(kline: str):
    start_date = datetime.now()
    last_letter = frame_select_dict[kline][0][-1].upper()
    kline_interval = frame_select_dict[kline][1]
    if last_letter.endswith("M"):
        start_date += timedelta(minutes=kline_interval)
    elif last_letter.endswith("H"):
        start_date += timedelta(hours=kline_interval)
    elif last_letter.endswith("D"):
        start_date += timedelta(days=kline_interval)
    else:
        return print("This time frame is not allowed.")
    return frame_select_dict[kline][0], start_date.strftime("%d %B, %Y")
