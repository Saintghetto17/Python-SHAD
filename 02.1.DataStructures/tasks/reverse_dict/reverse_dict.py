import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    keys = list(dct.keys())
    values = list(dct.values())
    dictionary_res: dict[str, list[str]] = {}
    for e in values:
        if e in dictionary_res:
            continue
        else:
            dictionary_res[e] = []
    for e in keys:
        val = dct[e]
        dictionary_res[val].append(e)
    return dict(dictionary_res)
