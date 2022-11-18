import pytest

from main_supres import frameselect
from datetime import datetime, timedelta


@pytest.fixture
def frame_select_data():
    today = datetime.now()
    return [
        ("1M", ("1m", (today - timedelta(minutes=260)).strftime("%d %B, %Y"))),
        ("3M", ("3m", (today - timedelta(minutes=780)).strftime("%d %B, %Y"))),
        ("5M", ("5m", (today - timedelta(minutes=1300)).strftime("%d %B, %Y"))),
        ("15M", ("15m", (today - timedelta(minutes=3900)).strftime("%d %B, %Y"))),
        ("30M", ("30m", (today - timedelta(minutes=7800)).strftime("%d %B, %Y"))),
        ("1H", ("1h", (today - timedelta(hours=260)).strftime("%d %B, %Y"))),
        ("2H", ("2h", (today - timedelta(hours=520)).strftime("%d %B, %Y"))),
        ("4H", ("4h", (today - timedelta(hours=1040)).strftime("%d %B, %Y"))),
        ("6H", ("6h", (today - timedelta(hours=1560)).strftime("%d %B, %Y"))),
        ("8H", ("8h", (today - timedelta(hours=2080)).strftime("%d %B, %Y"))),
        ("12H", ("12h", (today - timedelta(hours=3120)).strftime("%d %B, %Y"))),
        ("1D", ("1d", (today - timedelta(days=260)).strftime("%d %B, %Y"))),
        ("3D", ("3d", (today - timedelta(days=780)).strftime("%d %B, %Y"))),
    ]


def test_frameselect(frame_select_data):
    for frame, expected in frame_select_data:
        assert frameselect.frame_select(frame) == expected
