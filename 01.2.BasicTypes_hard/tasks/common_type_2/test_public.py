import copy
import dataclasses
import typing as tp

import pytest
import testlib

from .common_type_2 import convert_to_common_type


@dataclasses.dataclass
class Case:
    values: list[tp.Any]
    converted_values: list[tp.Any]
    common_type: type

    def __str__(self) -> str:
        return "convert_{}".format(self.values)


TEST_CASES = [
    Case(
        values=["ozon.ru", ["amazon.com", "vk.com"], ("py.manytask.ru", "yandex.ru"), None, ""],
        converted_values=[["ozon.ru"], ["amazon.com", "vk.com"], ["py.manytask.ru", "yandex.ru"], [], []],
        common_type=list
    ),
    Case(
        values=["ozon.ru", "amazon.com", "py.manytask.ru", None, ""],
        converted_values=["ozon.ru", "amazon.com", "py.manytask.ru", "", ""],
        common_type=str
    ),
    Case(
        values=[122334, [121223, 9389384], (123223, 4384934), None, ""],
        converted_values=[[122334], [121223, 9389384], [123223, 4384934], [], []],
        common_type=list
    ),
    Case(
        values=[122334, (121223, 9389384), (123223, 4384934), None, ""],
        converted_values=[[122334], [121223, 9389384], [123223, 4384934], [], []],
        common_type=list
    ),
    Case(
        values=[True, (True, False), None, ""],
        converted_values=[[True], [True, False], [], []],
        common_type=list
    ),
    Case(
        values=[122334, "", 4384934, None, ""],
        converted_values=[122334, 0, 4384934, 0, 0],
        common_type=int
    ),
    Case(
        values=[15, 10.75, 2, None, ""],
        converted_values=[15.0, 10.75, 2.0, 0.0, 0.0],
        common_type=float
    ),
    Case(
        values=[15, 2, None, ""],
        converted_values=[15, 2, 0, 0],
        common_type=int
    ),
    Case(
        values=[2.0, None, ""],
        converted_values=[2.0, 0.0, 0.0],
        common_type=float
    ),
    Case(
        values=[False, 0, True, "", None],
        converted_values=[False, False, True, False, False],
        common_type=bool
    ),
    Case(
        values=[1, 1, 1, "", True],
        converted_values=[True, True, True, False, True],
        common_type=bool
    ),
    Case(
        values=[None, "", None, None],
        converted_values=["", "", "", ""],
        common_type=str
    ),
    Case(
        values=[None],
        converted_values=[""],
        common_type=str
    ),
    Case(
        values=[None, None, None, None],
        converted_values=["", "", "", ""],
        common_type=str
    ),
    Case(
        values=[False, False, False],
        converted_values=[False, False, False],
        common_type=bool
    ),
    Case(
        values=[0, None, ""],
        converted_values=[0, 0, 0],
        common_type=int
    )
]


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(convert_to_common_type)


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_convert_to_common_type(t: Case) -> None:
    values_copy = copy.deepcopy(t.values)

    converted_values = convert_to_common_type(values_copy)

    assert converted_values == t.converted_values
    for value in converted_values:
        assert isinstance(value, t.common_type)

    assert values_copy == t.values, "You shouldn't change input"
