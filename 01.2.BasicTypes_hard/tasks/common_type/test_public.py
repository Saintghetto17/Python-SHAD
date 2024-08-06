import dataclasses
import typing as tp

import pytest
import testlib

from .common_type import get_common_type


@dataclasses.dataclass
class Case:
    value1: tp.Any
    value2: tp.Any
    common_type: type

    def __str__(self) -> str:
        return 'find_common_type_of_{}_and_{}'.format(type(self.value1), type(self.value2))


TEST_CASES = [
    Case(value1="[1,2,3]", value2=[3, 4, 5], common_type=str),
    Case(value1="(1,2,3)", value2=(3, 4, 5), common_type=str),
    Case(value1="[1,2,3]", value2=range(3), common_type=str),
    Case(value1="range(3)", value2=range(3), common_type=str),
    Case(value1="[1,2,3]", value2=10, common_type=str),
    Case(value1="[1,2,3]", value2=1.3, common_type=str),
    Case(value1="1.3", value2=1.3, common_type=str),
    Case(value1="[1,2,3]", value2=1j, common_type=str),
    Case(value1="Hello", value2=False, common_type=str),
    Case(value1="True", value2=True, common_type=str),
    Case(value1="False", value2=False, common_type=str),

    Case(value1=[1, 2, 3], value2=[3, 4, 5], common_type=list),
    Case(value1=[1, 2, 3], value2=(1, 2, 3), common_type=list),
    Case(value1=[1, 2, 3], value2=range(3), common_type=list),
    Case(value1=[1, 2, 3], value2=2, common_type=str),
    Case(value1=[1, 2, 3], value2=1.5, common_type=str),
    Case(value1=[1, 2, 3], value2=2j, common_type=str),
    Case(value1=[1, 2, 3], value2=True, common_type=str),

    Case(value1=(1, 2, 3), value2=(3, 4, 5), common_type=tuple),
    Case(value1=(1, 2, 3), value2=range(3), common_type=tuple),
    Case(value1=(1, 2, 3), value2=2, common_type=str),
    Case(value1=(1, 2, 3), value2=1.5, common_type=str),
    Case(value1=(1, 2, 3), value2=2j, common_type=str),
    Case(value1=(1, 2, 3), value2=False, common_type=str),

    Case(value1=range(3), value2=range(3), common_type=tuple),
    Case(value1=range(3), value2=1, common_type=str),
    Case(value1=range(3), value2=1.0, common_type=str),
    Case(value1=range(3), value2=1j, common_type=str),
    Case(value1=range(3), value2=False, common_type=str),

    Case(value1=True, value2=False, common_type=bool),
    Case(value1=True, value2=2, common_type=int),
    Case(value1=True, value2=1.5, common_type=float),
    Case(value1=True, value2=2j, common_type=complex),

    Case(value1=1.0, value2=2, common_type=float),
    Case(value1=1.0, value2=1.5, common_type=float),
    Case(value1=1.0, value2=2j, common_type=complex),

    Case(value1=1, value2=2, common_type=int),
    Case(value1=1, value2=2j, common_type=complex),

    Case(value1=1j, value2=2j, common_type=complex),
]


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(get_common_type)


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_common_convertible_type(t: Case) -> None:

    common_type = get_common_type(type(t.value1), type(t.value2))
    common_type_reverse = get_common_type(type(t.value2), type(t.value1))

    # Check that symmetric
    assert common_type == common_type_reverse

    # Check that doesn't fall
    common_type(t.value1)
    common_type(t.value2)

    # Check that is expected
    assert common_type is t.common_type
