import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    lst_keys: list[str] = list(dct.keys())
    lst_res: list[tuple[str, int]] = []
    for e in lst_keys:
        if type(dct[e]) is not dict:
            string = list(prefix)
            string.append(e)
            elem = ''.join(string)
            tup = (elem, dct[e])
            lst_res.append(tup)
        else:
            string = list(prefix)
            string.append(e)
            string.append(".")
            new_pref = ''.join(string)
            list_to_iter = traverse_dictionary_immutable(dct[e], new_pref)
            for i in range(len(list_to_iter)):
                lst_res.append(list_to_iter[i])
    return lst_res


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    lst_keys: list[str] = list(dct.keys())
    for e in lst_keys:
        if type(dct[e]) is not dict:
            string = list(prefix)
            string.append(e)
            elem = ''.join(string)
            tup = (elem, dct[e])
            result.append(tup)
        else:
            string = list(prefix)
            string.append(e)
            string.append(".")
            new_pref = ''.join(string)
            new_res: list[tuple[str, int]] = []
            traverse_dictionary_mutable(dct[e], new_res, new_pref)
            for i in range(len(new_res)):
                result.append(new_res[i])
    return None


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """

    prefix = ''
    stack = [iter(dct.items())]
    result = []

    while bool(stack):
        try:
            key, value = next(stack[-1])
        except StopIteration:
            stack.pop()
            prefix = prefix[:prefix.rfind('.') - 1]
        else:
            if type(value) is dict:
                stack.append(iter(value.items()))
                prefix += key + '.'
            else:
                result.append((prefix + key, value))

    return result
