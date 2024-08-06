import sys
import typing as tp
from pathlib import Path

import pytest
import testlib

from .object_by_id import get_object_by_id


###################
# Structure asserts
###################


def test_version() -> None:
    assert "3.11.5" == sys.version.split(" ", maxsplit=1)[0], "To do this task you need python=3.11.5"


def test_banned_modules() -> None:
    for banned_module in ["weakref", "_ctypes", "gc", "inspect"]:
        assert not testlib.is_module_imported(
            banned_module, Path(__file__).parent / "object_by_id.py"
        ), f"You should not use `{banned_module}` module"


def test_get_object_by_id_structure() -> None:
    assert not testlib.is_global_used(get_object_by_id, "locals")
    assert not testlib.is_global_used(get_object_by_id, "globals")

    assert not testlib.is_instruction_used(get_object_by_id, "argval", "cast")
    assert not testlib.is_instruction_used(get_object_by_id, "argval", "memmove")
    assert not testlib.is_instruction_used(get_object_by_id, "argval", "memset")
    assert not testlib.is_instruction_used(get_object_by_id, "argval", "py_object")
    assert not testlib.is_instruction_used(get_object_by_id, "argval", "get_objects")
    assert not testlib.is_instruction_used(get_object_by_id, "argval", "PyObject")


###################
# Tests
###################


INT_VALUES = [
    1,
    1024,
    -345,
    0,
    49563696592,
    1152921504606859288,
    2**31 - 1,
    2**61 - 1,
    808133502732476013716770273355210871119972365079352867510378823304233125541,
]


@pytest.mark.parametrize("int_value", INT_VALUES, ids=str)
def test_get_int_by_id(int_value: int) -> None:
    assert get_object_by_id(id(int_value)) == int_value


BOOL_VALUES = [
    True,
    False
]


@pytest.mark.parametrize("bool_value", BOOL_VALUES, ids=str)
def test_get_bool_by_id(bool_value: int) -> None:
    assert get_object_by_id(id(bool_value)) == bool_value


FLOAT_VALUES = [
    0.0,
    0.2 + 0.3,
    31413.6123412,
    -3.14,
]


@pytest.mark.parametrize("float_value", FLOAT_VALUES, ids=str)
def test_get_float_by_id(float_value: float) -> None:
    assert get_object_by_id(id(float_value)) == float_value


STR_VALUES = [
    "i_love_SHAD",
    "",
    "128" * 128,
]


@pytest.mark.parametrize("str_value", STR_VALUES, ids=str)
def test_get_str_by_id(str_value: str) -> None:
    assert get_object_by_id(id(str_value)) == str_value


LIST_VALUES = [
    [1, 2, 3],
    [2],
    [4313, "to be, or not to be", 3.45],
    [],
    [1, "H in SHAD is not from Hell", [34, 31, "c"], [True, 123, [45, 34, [312, 345, 3.4], 1.3]]],
    [[], [[], [[], [3, [45, [1, 2, 53, [3, [[], ["ohh, my... it's deep"]]]]]]]]],
]


@pytest.mark.parametrize("list_value", LIST_VALUES, ids=str)
def test_get_list_by_id(list_value: list[tp.Any]) -> None:
    assert get_object_by_id(id(list_value)) == list_value


TUPLE_VALUES = [
    (),
    (1,),
    (1, 2, 3, 9, 12, 45, -23),
    ((False,), (True,), (False)),
    ("abc", 2.3, 4),
    (1, (2, ((3), (4, (5,  (6,), (7, (8, (9, (0, ("deep again", )))))))))),
]


@pytest.mark.parametrize("tuple_values", TUPLE_VALUES, ids=str)
def test_get_tuple_by_id(tuple_values: tuple[tp.Any, ...]) -> None:
    assert get_object_by_id(id(tuple_values)) == tuple_values


DEEP_VALUES = [
    [1, [([34, [45]], [1, (-12.3, ["a place for your meme"])])], [(345, 34), (34, 1.2)], [3], (), (".")],
    ((1, 1-3, 3), [4, 5, (6,), [7, [8, 9]], 10, (11, 12, [13], 14), 15], 1600, 17.5),
    [[i, f"v_{i}"*i, (i,)]*i if i % 2 else tuple(f"{j}"*j if j % 4 else j**j for j in range(i+64)) for i in range(64)],
]


@pytest.mark.parametrize("deep_values", DEEP_VALUES, ids=str)
def test_get_deep_values_by_id(deep_values: tuple[tp.Any]) -> None:
    assert get_object_by_id(id(deep_values)) == deep_values


def test_wide_cycle() -> None:
    cycled_list: list[tp.Any] = [0 for _ in range(1024)]
    for i in range(len(cycled_list)):
        cycled_list[i] = cycled_list

    _object = get_object_by_id(id(cycled_list))

    assert isinstance(_object, list)
    assert len(_object) == len(cycled_list)
    for i in range(len(cycled_list)):
        assert isinstance(_object[i], list)
        assert len(_object[i]) == len(cycled_list)
        assert id(_object[i]) == id(_object)


def test_same_id_values() -> None:
    value: str = "test_same_id_values"
    list_: tuple[tp.Any, ...] = tuple([value] * 1024)

    _object = get_object_by_id(id(list_))
    assert isinstance(_object, tuple)

    assert len({id(i) for i in _object}) == 1


def test_direct_cycle() -> None:
    value: str = "test_direct_cycle"
    cycled_list: list[tp.Any] = [[value], [value], [value]]
    cycled_list.append(cycled_list)

    _object = get_object_by_id(id(cycled_list))
    assert isinstance(_object, list)
    assert len(_object) == 4

    assert len({id(i) for i in _object}) == 4
    assert len({id(i[0]) for i in _object[:3]}) == 1


def test_indirect_cycle() -> None:
    cycled_list_first: list[tp.Any] = []
    cycled_list_second: list[tp.Any] = []
    cycled_list_third: tuple[tp.Any, ...] = (cycled_list_first, cycled_list_second)
    cycled_list_first.extend([cycled_list_second, cycled_list_third])
    cycled_list_second.extend([cycled_list_third, cycled_list_first])

    _object = get_object_by_id(id(cycled_list_first))

    assert isinstance(_object, list) and len(_object) == 2
    assert isinstance(_object[0], list) and len(_object[0]) == 2
    assert isinstance(_object[0][0], tuple) and len(_object[0][0]) == 2

    first_id = id(_object)
    second_id = id(_object[0])
    third_id = id(_object[0][0])
    assert [id(i) for i in _object] == [second_id, third_id]
    assert [id(i) for i in _object[0]] == [third_id, first_id]
    assert [id(i) for i in _object[0][0]] == [first_id, second_id]
