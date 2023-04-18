import pandas_ta.momentum as ta


def indicators(
    df_sma, ma_length1, ma_length2, ma_length3
) -> tuple[tuple, tuple, tuple, tuple]:
    """
    The function "indicators" calculates and returns four tuples containing simple moving averages and
    relative strength index values.

    :param df_sma: The input dataframe containing the closing prices for a financial asset
    :param ma_length1: The length of the first Simple Moving Average (SMA) to be calculated
    :param ma_length2: The length of the second Simple Moving Average (SMA) that will be calculated in
    the function
    :param ma_length3: ma_length3 is a parameter that represents the length of the third Simple Moving
    Average (SMA) that will be calculated in the function. The function takes in a DataFrame of stock
    data (df_sma) and calculates three SMAs of different lengths (ma_length1, ma_length2, and
    :return: a tuple of four tuples. The first three tuples contain the simple moving averages (SMAs) of
    the input dataframe `df_sma` with lengths `ma_length1`, `ma_length2`, and `ma_length3`,
    respectively. The fourth tuple contains the relative strength index (RSI) values of the `close`
    column of the input dataframe `df_sma`,
    """
    sma_1 = tuple(df_sma.ta.sma(ma_length1))
    sma_2 = tuple(df_sma.ta.sma(ma_length2))
    sma_3 = tuple(df_sma.ta.sma(ma_length3))
    rsi_tuple = tuple(ta.rsi(df_sma["close"][:-1]))
    return sma_1, sma_2, sma_3, rsi_tuple
