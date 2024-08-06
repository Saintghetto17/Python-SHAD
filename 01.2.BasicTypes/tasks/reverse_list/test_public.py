import dataclasses
import copy

import pytest
import testlib

from .reverse_list import reverse_iterative, reverse_inplace_iterative, reverse_inplace, reverse_reversed, reverse_slice


@dataclasses.dataclass
class Case:
    lst: list[int]
    result: list[int]

    def __str__(self) -> str:
        return 'reverse_{}'.format(self.lst)


TEST_CASES = [
    Case(lst=[], result=[]),
    Case(lst=[1, 2, 3], result=[3, 2, 1]),
    Case(lst=[1, 2, 1], result=[1, 2, 1]),
    Case(lst=[1, 2, 3, 4], result=[4, 3, 2, 1]),
    Case(lst=[1], result=[1]),
    Case(lst=[2, 2, 2, 2], result=[2, 2, 2, 2]),
]


###################
# Structure asserts
###################


def test_reverse_iterative_structure() -> None:
    assert not testlib.is_global_used(reverse_iterative, 'reversed')
    assert not testlib.is_bytecode_op_used(reverse_iterative, 'BUILD_SLICE')


def test_reverse_inplace_iterative_structure() -> None:
    assert not testlib.is_instruction_used(reverse_inplace_iterative, 'argval', 'reverse')
    assert not testlib.is_bytecode_op_used(reverse_inplace_iterative, 'BUILD_SLICE')


def test_reverse_inplace_structure() -> None:
    assert testlib.is_instruction_used(reverse_inplace, 'argval', 'reverse')


def test_reverse_reversed_structure() -> None:
    assert testlib.is_global_used(reverse_reversed, 'reversed')
    assert not testlib.is_bytecode_op_used(reverse_reversed, 'BUILD_SLICE')


def test_reverse_slice_structure() -> None:
    assert not testlib.is_global_used(reverse_slice, 'reversed')
    assert testlib.is_bytecode_op_used(reverse_slice, 'BUILD_SLICE')


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(reverse_inplace)
    assert testlib.is_function_docstring_exists(reverse_inplace_iterative)
    assert testlib.is_function_docstring_exists(reverse_iterative)
    assert testlib.is_function_docstring_exists(reverse_reversed)
    assert testlib.is_function_docstring_exists(reverse_slice)


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_iterative(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)
    answer = reverse_iterative(given_lst)
    assert answer == t.result

    assert given_lst == t.lst, "You shouldn't change input"


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_inplace_iterative(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)
    reverse_inplace_iterative(given_lst)
    assert given_lst == t.result


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_inplace(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)
    reverse_inplace(given_lst)
    assert given_lst == t.result


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_reversed(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)
    answer = reverse_reversed(given_lst)
    assert answer == t.result

    assert given_lst == t.lst, "You shouldn't change input"


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_slice(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)
    answer = reverse_slice(given_lst)
    assert answer == t.result

    assert given_lst == t.lst, "You shouldn't change input"
