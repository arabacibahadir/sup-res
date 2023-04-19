import pandas_ta.momentum as ta


def indicators(
    df_sma, ma_length1, ma_length2, ma_length3
) -> tuple[tuple, tuple, tuple, tuple]:
    """
    This function calculates technical indicators for a given pandas DataFrame containing a moving average column.

    Args:
        df_sma: A DataFrame with a column named "sma".
        ma_length1: The length of the first simple moving average (SMA).
        ma_length2: The length of the second simple moving average (SMA).
        ma_length3: The length of the third simple moving average (SMA).

    Returns:
        tuple: A tuple of four tuples, where each inner tuple represents the respective calculated indicator:
            - sma_1, sma_2, sma_3: A tuple of SMA values for the first, second, and third moving averages.
            - rsi_tuple: A tuple of RSI values calculated using pandas_ta library.
    """
    sma_1 = tuple(df_sma.ta.sma(ma_length1))
    sma_2 = tuple(df_sma.ta.sma(ma_length2))
    sma_3 = tuple(df_sma.ta.sma(ma_length3))
    rsi_tuple = tuple(ta.rsi(df_sma["close"][:-1]))
    return sma_1, sma_2, sma_3, rsi_tuple
