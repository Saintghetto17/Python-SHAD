from collections.abc import Iterable, Iterator
from typing import Any


def flat_it(sequence: Iterable[Any]) -> Iterator[Any]:
    """
    :param sequence: iterable with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    for elem in sequence:
        try:
            if type(elem) is str and len(elem) == 1:
                raise TypeError
            iter(elem)
        except TypeError:
            yield elem
        else:
            yield from flat_it(elem)
