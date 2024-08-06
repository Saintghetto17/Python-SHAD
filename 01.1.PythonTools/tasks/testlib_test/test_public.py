import pytest
import testlib

from .testlib_test import sum_two_numbers


class Case:
    def __init__(self, name: str, a: int, b: int, expected: int):
        self._name = name
        self.a = a
        self.b = b
        self.expected = expected

    def __str__(self) -> str:
        return 'test_{}'.format(self._name)


TEST_CASES = [
    Case(name='basic', a=1, b=1, expected=2),
    Case(name='negative', a=-1, b=-1, expected=-2),
    Case(name='zero_sum', a=1, b=-1, expected=0),
]


###################
# Structure asserts
###################


def test_banned_functions() -> None:
    assert not testlib.is_global_used(sum_two_numbers, 'sum'), 'You can not use sum function in the task'


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(sum_two_numbers), 'You should not delete function docstring'


###################
# Tests
###################


@pytest.mark.parametrize('test_case', TEST_CASES, ids=str)
def test_hello_world(test_case: Case) -> None:
    answer = sum_two_numbers(test_case.a, test_case.b)
    assert answer == test_case.expected
