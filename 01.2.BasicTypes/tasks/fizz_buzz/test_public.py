import dataclasses
import typing as tp

import pytest
import testlib

from .fizz_buzz import get_fizz_buzz


@dataclasses.dataclass
class Case:
    name: str
    n: int
    expected: tp.Mapping[int, int | str]

    def __str__(self) -> str:
        return 'test_{}'.format(self.name)


TEST_CASES = [
    Case(name="test_zero_element", n=1, expected={0: 1}),
    Case(name="test_first_three_elements", n=3, expected={0: 1, 1: 2, 2: "Fizz"}),
    Case(name="check_fizz", n=100, expected={i - 1: "Fizz" for i in range(3, 101, 3) if i % 15 != 0}),
    Case(name="test_first_two_elements", n=2, expected={0: 1, 1: 2}),
    Case(name="check_buzz", n=100, expected={i - 1: "Buzz" for i in range(5, 101, 5) if i % 15 != 0}),
    Case(name="check_fizz_buzz", n=100, expected={i - 1: "FizzBuzz" for i in range(15, 101, 15)}),
    Case(name="check_digits", n=100, expected={i - 1: i for i in range(101) if i % 3 != 0 and i % 5 != 0})
]


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(get_fizz_buzz)


###################
# Tests
###################

@pytest.mark.parametrize("test_case", TEST_CASES, ids=str)
def test_get_fizz_buzz(test_case: Case) -> None:
    fizz_buzz_list = get_fizz_buzz(test_case.n)
    assert len(fizz_buzz_list) == test_case.n
    for key, value in test_case.expected.items():
        assert fizz_buzz_list[key] == value
