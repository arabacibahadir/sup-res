import sys
import os
from datetime import datetime, timedelta

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main_supres"))
)
from frameselect import frame_select, frame_select_dict


def test_frame_select():
    for kline, values in frame_select_dict.items():
        expected_kline_interval = values[0]
        kline_interval = values[1]
        last_letter = expected_kline_interval[-1].upper()
        times = {
            "M": timedelta(minutes=kline_interval),
            "H": timedelta(hours=kline_interval),
            "D": timedelta(days=kline_interval),
            "W": timedelta(weeks=kline_interval),
        }
        expected_start_date = (datetime.now() + times[last_letter]).strftime(
            "%d %B, %Y"
        )
        assert frame_select(kline) == (expected_kline_interval, expected_start_date)
