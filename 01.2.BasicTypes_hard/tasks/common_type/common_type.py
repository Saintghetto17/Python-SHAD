def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    str_1 = str(type1)
    str_2 = str(type2)

    sym_1 = str_1[8]
    sym_2 = str_2[8]

    if (sym_1 == 'l' or sym_1 == 't' or sym_1 == 'r') and (
            sym_2 == 'b' or sym_2 == 'i' or sym_2 == 'f' or sym_2 == 'c'):
        sym_1 = 's'

    if (sym_2 == 'l' or sym_2 == 't' or sym_2 == 'r') and (
            sym_1 == 'b' or sym_1 == 'i' or sym_1 == 'f' or sym_1 == 'c'):
        sym_2 = 's'

    priority_types = {1: bool, 2: int, 3: float, 4: complex, 6: tuple, 7: list, 8: str}
    priority_reverse = {'b': 1, 'i': 2, 'f': 3, 'c': 4, 'r': 6, 't': 6, 'l': 7, 's': 8}

    value_1 = priority_reverse[sym_1]
    value_2 = priority_reverse[sym_2]

    if value_1 <= value_2:
        print(value_2)
        res = priority_types[value_2]
        return res
    else:
        res = priority_types[value_1]
        return res
