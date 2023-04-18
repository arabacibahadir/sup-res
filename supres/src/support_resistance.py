def support(
    candle_value, candle_index, before_candle_count, after_candle_count
) -> bool | None:
    """
    The function checks if a given candle value meets certain criteria based on its low values and the
    number of candles before and after it.

    :param candle_value: This parameter is likely a data structure or object that contains information
    about a candlestick chart, such as the open, high, low, and close prices for each candlestick
    :param candle_index: The index of the current candle in the candle_value data structure
    :param before_candle_count: The number of candles to look at before the current candle index
    :param after_candle_count: The number of candles after the current candle that the function should
    check
    :return: a boolean value or None. If the function executes successfully, it will return True if the
    low value of the candle at the given index is decreasing for the number of candles specified before
    and after the given index. If the low value is not decreasing as expected, the function will return
    False. If there is a KeyError, the function will return None.
    """
    try:
        for current_value in range(
            candle_index - before_candle_count + 1, candle_index + 1
        ):
            if candle_value.low[current_value] > candle_value.low[current_value - 1]:
                return False
        for current_value in range(
            candle_index + 1, candle_index + after_candle_count + 1
        ):
            if candle_value.low[current_value] < candle_value.low[current_value - 1]:
                return False
        return True
    except KeyError:
        pass


def resistance(
    candle_value, candle_index, before_candle_count, after_candle_count
) -> bool | None:
    """
    The function checks if a given candle value represents a resistance level based on the high values
    of the candles before and after it.

    :param candle_value: This parameter is likely a data structure or object that contains information
    about a candlestick chart, such as the high, low, open, and close prices for each candlestick
    :param candle_index: The index of the current candle in the candle_value data
    :param before_candle_count: The number of candles to look at before the current candle
    :param after_candle_count: The number of candles after the current candle that we want to check for
    resistance
    :return: a boolean value (True or False) or None if a KeyError is caught.
    """
    try:
        for current_value in range(
            candle_index - before_candle_count + 1, candle_index + 1
        ):
            if candle_value.high[current_value] < candle_value.high[current_value - 1]:
                return False
        for current_value in range(
            candle_index + 1, candle_index + after_candle_count + 1
        ):
            if candle_value.high[current_value] > candle_value.high[current_value - 1]:
                return False
        return True
    except KeyError:
        pass
