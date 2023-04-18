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
    "12H": [Client.KLINE_INTERVAL_12HOUR, -3120],
    "1D": [Client.KLINE_INTERVAL_1DAY, -260],
    "3D": [Client.KLINE_INTERVAL_3DAY, -780],
    "1W": [Client.KLINE_INTERVAL_1WEEK, -1040],
}


def frame_select(kline: str) -> tuple[str | int, str]:
    """
    The function takes a string input representing a time frame and returns a tuple containing a string
    and a formatted date string.

    :param kline: The input parameter `kline` is a string representing a time frame for financial data,
    such as "1m" for 1 minute, "1h" for 1 hour, "1d" for 1 day, or "1w" for 1 week
    :type kline: str
    :return: The function `frame_select` returns a tuple containing a string or integer and a string.
    The first element of the tuple is the value of the first item in the list associated with the input
    `kline` in the `frame_select_dict` dictionary. The second element of the tuple is a formatted string
    representing the date that is `kline_interval` time units after the current date, where the
    """
    start_date = datetime.now()
    last_letter = frame_select_dict[kline][0][-1].upper()
    kline_interval = frame_select_dict[kline][1]
    times = {
        "M": timedelta(minutes=kline_interval),
        "H": timedelta(hours=kline_interval),
        "D": timedelta(days=kline_interval),
        "W": timedelta(weeks=kline_interval),
    }
    start_date += times[last_letter]
    return frame_select_dict[kline][0], start_date.strftime("%d %B, %Y")
