import dataclasses

import pytest
import testlib

from .middle_value_of_triple import get_middle_value


@dataclasses.dataclass
class Case:
    a: int
    b: int
    c: int
    result: int

    def __str__(self) -> str:
        return 'median_of_{}_{}_{}'.format(self.a, self.b, self.c)


TEST_CASES = [
    Case(a=1, b=2, c=3, result=2),
    Case(a=3, b=2, c=1, result=2),
    Case(a=2, b=3, c=1, result=2),
    Case(a=2, b=1, c=3, result=2),
    Case(a=3, b=1, c=2, result=2),
    Case(a=1, b=3, c=2, result=2),
    Case(a=-100, b=-10, c=100, result=-10),
    Case(a=100, b=-10, c=-100, result=-10),
    Case(a=-10, b=-10, c=-5, result=-10),
    Case(a=-10, b=-10, c=-10, result=-10),
    Case(a=-100, b=10, c=100, result=10),
    Case(a=0, b=0, c=0, result=0),
    Case(a=10**12, b=-10**12, c=10**10, result=10**10)
]


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(get_middle_value)


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_get_middle_value(t: Case) -> None:
    answer = get_middle_value(t.a, t.b, t.c)
    assert answer == t.result
