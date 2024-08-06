import inspect

from .flat_it import flat_it


def test_type() -> None:
    flat = flat_it((1, 2, 3))
    assert inspect.isgenerator(flat)


def test_on_flat_seq() -> None:
    flatten = list(flat_it((1, 2, 3)))
    assert flatten == [1, 2, 3]


def test_on_nested_lists() -> None:
    flatten = list(flat_it((1, (2, 3), [4, [5, 6], 7])))
    assert flatten == list(range(1, 8))


def test_on_etalon() -> None:
    flatten = list(flat_it([[1, [[2, [5, [6, [2, 'sample']]]], 3], range(-5, -3, 1)]]))
    assert flatten == [1, 2, 5, 6, 2, 's', 'a', 'm', 'p', 'l', 'e',  3, -5, -4]


def test_huge_list() -> None:
    inner_list = list(range(10))
    level_size = 12
    levels = 6

    huge_list = inner_list

    for _ in range(levels):
        huge_list = [huge_list for _ in range(level_size)]  # type: ignore

    assert list(flat_it(huge_list)) == list(inner_list * level_size ** levels)
