import typing as tp
from collections import Counter


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    cnt = Counter(seq)
    dictionary = dict(cnt)
    keys = list(dictionary.keys())
    max = 0
    for e in keys:
        if (dictionary[e] > max):
            max = dictionary[e]
        else:
            continue
    return len(seq) - max
