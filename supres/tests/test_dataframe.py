import pandas as pd


# Path: tests\test_dataframe.py
# Test the dataframe
def test_dataframe():
    # read csv
    df = pd.read_csv("BTCUSDT_15m.csv")
    # is df null
    assert not df.isnull().values.any()
    # is the dataframe empty
    assert not df.empty
    # is the dataframe a dataframe
    assert isinstance(df, pd.DataFrame)
    # is the dataframe the correct width
    assert len(df.columns) == 7
    # is the dataframe the correct length
    assert len(df) > 250
    # is the dataframe the correct type
    assert df.dtypes[0] == "int64"
    assert df.dtypes[1] == "object"
    assert df.dtypes[2] == "float64"
    assert df.dtypes[3] == "float64"
    assert df.dtypes[4] == "float64"
    assert df.dtypes[5] == "float64"
    assert df.dtypes[6] == "float64"
    # is header correct
    assert df.columns[0] == "unix"
    assert df.columns[1] == "date"
    assert df.columns[2] == "open"
    assert df.columns[3] == "high"
    assert df.columns[4] == "low"
    assert df.columns[5] == "close"
    assert df.columns[6] == "Volume USDT"
    # is unix column unique
    assert df["unix"].is_unique
    # is date column unique
    assert df["date"].is_unique
    # is rows unique
    assert df.duplicated().sum() == 0
    # is date column sorted
    assert df["date"].is_monotonic_decreasing
    # is unix column sorted
    assert df["unix"].is_monotonic_decreasing
