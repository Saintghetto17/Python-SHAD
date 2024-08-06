from typing import List
import typing as tp


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    types = []
    map_values = {'N': 0, 'Z': 0, 'b': 2, 'i': 1, 'f': 3, 's': 4, 't': 5, 'l': 6}
    for e in data:
        typ = str(type(e))
        symbol = typ[8]
        if e == '':
            types.append('Z')
            continue
        types.append(symbol)
    common_type = ''
    for i in range(len(types)):
        if i == 0:
            common_type = types[i]
        else:
            if map_values[common_type] < map_values[types[i]]:
                common_type = types[i]
            else:
                continue
    if common_type == 'Z':
        return data
    if common_type == 'N':
        res_str: List[str] = []
        for e in data:
            res_str.append("")

    if common_type == 'b':
        res_b: List[bool] = []
        for e in data:
            res_b.append(bool(e))
        return res_b
    elif common_type == 'i':
        res1: List[int] = []
        for e in data:
            if e == '' or e is None:
                res1.append(0)
                continue
            res1.append(int(e))
        return res1
    elif common_type == 'f':
        res2: List[float] = []
        for e in data:
            if e == '' or e is None:
                res2.append(0.0)
                continue
            res2.append(float(e))
        return res2
    elif common_type == 'l' or common_type == 't':
        res3: List[tp.Any] = []
        for e in data:
            if e is None:
                res3.append([])
            elif type(e) is str:
                if e == "" or None:
                    ans1: List[tp.Any] = []
                    res3.append(ans1)
                else:
                    ans2: List[tp.Any] = []
                    ans2.append(e)
                    res3.append(ans2)
            elif type(e) is list:
                res3.append(e)
            elif type(e) is tuple:
                res3.append(list(e))
            else:
                ans_new: List[tp.Any] = []
                ans_new.append(e)
                res3.append(ans_new)
        return res3
    else:
        res4: List[str] = []
        for e in data:
            if e is None:
                res4.append("")
            else:
                res4.append(str(e))
        return res4


print(convert_to_common_type([1, 1, 1, '', True]))
