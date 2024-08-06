import copy
import dataclasses

import pytest
import testlib

from .filter_list_by_list import filter_list_by_list


@dataclasses.dataclass
class Case:
    lst_a: list[int] | range
    lst_b: list[int] | range
    result: list[int]


TEST_CASES = [
    Case(lst_a=[], lst_b=[], result=[]),
    Case(lst_a=[1, 2, 3], lst_b=[], result=[1, 2, 3]),
    Case(lst_a=[], lst_b=[1, 2, 3], result=[]),
    Case(lst_a=[], lst_b=[1], result=[]),
    Case(lst_a=[1], lst_b=[], result=[1]),
    Case(lst_a=[1], lst_b=[1], result=[]),
    Case(lst_a=[1, 1], lst_b=[1], result=[]),
    Case(lst_a=[1, 2], lst_b=[3, 4], result=[1, 2]),
    Case(lst_a=[1, 3], lst_b=[2, 4], result=[1, 3]),
    Case(lst_a=[3, 4], lst_b=[1, 2], result=[3, 4]),
    Case(lst_a=[1, 3], lst_b=[2, 4], result=[1, 3]),
    Case(lst_a=[2, 3], lst_b=[1, 2], result=[3]),
    Case(lst_a=[1, 1], lst_b=[1, 1], result=[]),
    Case(lst_a=[1, 2], lst_b=[1, 1], result=[2]),
    Case(lst_a=[1, 2], lst_b=[1, 2], result=[]),
    Case(lst_a=[2, 3], lst_b=[1, 4], result=[2, 3]),
    Case(lst_a=[1, 4], lst_b=[4, 4], result=[1]),
    Case(lst_a=range(10**5), lst_b=[0] * 10**5, result=list(range(1, 10**5)))
]


###################
# Structure asserts
###################


def test_filter_list_by_list_structure() -> None:
    assert not testlib.is_global_used(filter_list_by_list, 'set')


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(filter_list_by_list)


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES)
def test_filter_list_by_list(t: Case) -> None:
    lst_a_copy, lst_b_copy = copy.deepcopy(t.lst_a), copy.deepcopy(t.lst_b)

    answer = filter_list_by_list(lst_a_copy, lst_b_copy)
    assert answer == t.result

    assert lst_a_copy == t.lst_a and lst_b_copy == t.lst_b, "You shouldn't change inputs"
