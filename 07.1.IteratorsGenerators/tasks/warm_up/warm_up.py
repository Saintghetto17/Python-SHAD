from collections import ChainMap
from collections.abc import Generator
from typing import Any


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """
    :param matrix: rectangular matrix
    :return: transposed matrix
    """
    return [list(it) for it in zip(*matrix)]


def uniq(sequence: list[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: arbitrary sequence of comparable elements
    :return: generator of elements of `sequence` in
    the same order without duplicates
    """
    seen = set()
    for elem in sequence:
        if elem in seen:
            continue
        seen.add(elem)
        yield elem


def dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    :param *dicts: flat dictionaries to be merged
    :return: merged dictiona
    ry
    """
    return dict(ChainMap(*(dicts[::-1])))


def product(lhs: list[int], rhs: list[int]) -> int:
    """
    :param rhs: first factor
    :param lhs: second factor
    :return: scalar product
    """
    return sum([tpl[0] * tpl[1] for tpl in zip(lhs, rhs)])
