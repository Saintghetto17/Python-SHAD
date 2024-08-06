def get_middle_value(a: int, b: int, c: int) -> int:
    """
    Takes three values and returns middle value.
    """
    if (a - b) * (a - c) <= 0:
        return a
    elif (b - c) * (b - a) <= 0:
        return b
    else:
        return c
