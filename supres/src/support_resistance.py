def support(
    candle_value, candle_index, before_candle_count, after_candle_count
) -> bool | None:
    """
    This function checks if the given `candle_value` at `candle_index` forms a support level.

    Args:
        candle_value (pandas.DataFrame): A DataFrame representing the candle values.
        candle_index (int): The index of the candle value to check.
        before_candle_count (int): The number of candles to check before the `candle_index`.
        after_candle_count (int): The number of candles to check after the `candle_index`.

    Returns:
        If the given `candle_value` at `candle_index` forms a support level, it returns True,
        otherwise, it returns False. If there are any missing keys in the `candle_value`, it returns None.
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
        return None


def resistance(
    candle_value, candle_index, before_candle_count, after_candle_count
) -> bool | None:
    """
    This function checks if the given `candle_value` at `candle_index` forms a resistance level.

    Args:
        candle_value (pandas.DataFrame): A DataFrame representing the candle values.
        candle_index (int): The index of the candle value to check.
        before_candle_count (int): The number of candles to check before the `candle_index`.
        after_candle_count (int): The number of candles to check after the `candle_index`.

    Returns:
        If the given `candle_value` at `candle_index` forms a resistance level, it returns True,
         otherwise, it returns False. If there are any missing keys in the `candle_value`, it returns None.
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
        return None
