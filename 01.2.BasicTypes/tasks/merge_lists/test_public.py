import copy
import dataclasses

import pytest
import testlib

from .merge_lists import merge_iterative, merge_sorted


@dataclasses.dataclass
class Case:
    lst_a: list[int]
    lst_b: list[int]
    result: list[int]

    def __str__(self) -> str:
        return 'merge_{}_{}'.format(self.lst_a, self.lst_b)


TEST_CASES = [
    Case(lst_a=[], lst_b=[], result=[]),
    Case(lst_a=[1, 2, 3], lst_b=[], result=[1, 2, 3]),
    Case(lst_a=[], lst_b=[1, 2, 3], result=[1, 2, 3]),
    Case(lst_a=[], lst_b=[1], result=[1]),
    Case(lst_a=[1], lst_b=[], result=[1]),
    Case(lst_a=[1], lst_b=[1], result=[1, 1]),
    Case(lst_a=[1, 2], lst_b=[3, 4], result=[1, 2, 3, 4]),
    Case(lst_a=[1, 3], lst_b=[2, 4], result=[1, 2, 3, 4]),
    Case(lst_a=[3, 4], lst_b=[1, 2], result=[1, 2, 3, 4]),
    Case(lst_a=[1, 3], lst_b=[2, 4], result=[1, 2, 3, 4]),
    Case(lst_a=[2, 3], lst_b=[1, 2], result=[1, 2, 2, 3]),
    Case(lst_a=[1, 1], lst_b=[1, 1], result=[1, 1, 1, 1]),
    Case(lst_a=[1, 2], lst_b=[1, 1], result=[1, 1, 1, 2]),
    Case(lst_a=[1, 2], lst_b=[1, 2], result=[1, 1, 2, 2]),
    Case(lst_a=[2, 3], lst_b=[1, 4], result=[1, 2, 3, 4]),
    Case(lst_a=[1, 4], lst_b=[4, 4], result=[1, 4, 4, 4]),
]


###################
# Structure asserts
###################


def test_merge_iterative_structure() -> None:
    assert not testlib.is_global_used(merge_iterative, 'sorted')
    assert not testlib.is_bytecode_op_used(merge_iterative, 'BUILD_SLICE')


def test_merge_sorted_structure() -> None:
    assert testlib.is_global_used(merge_sorted, 'sorted')
    assert not testlib.is_bytecode_op_used(merge_sorted, 'BUILD_SLICE')


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(merge_iterative)
    assert testlib.is_function_docstring_exists(merge_sorted)


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_merge_iterative(t: Case) -> None:
    given_list_a, given_list_b = copy.deepcopy(t.lst_a), copy.deepcopy(t.lst_b)
    answer = merge_iterative(given_list_a, given_list_b)
    assert answer == t.result

    assert given_list_a == t.lst_a and given_list_b == t.lst_b, "You shouldn't change input"


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_merge_sorted(t: Case) -> None:
    given_list_a, given_list_b = copy.deepcopy(t.lst_a), copy.deepcopy(t.lst_b)
    answer = merge_sorted(given_list_a, given_list_b)
    assert answer == t.result

    assert given_list_a == t.lst_a and given_list_b == t.lst_b, "You shouldn't change input"
