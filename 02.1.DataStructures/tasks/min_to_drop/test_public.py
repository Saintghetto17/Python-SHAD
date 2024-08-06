import copy
import dataclasses
import typing as tp

import pytest
import testlib

from .min_to_drop import get_min_to_drop


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(get_min_to_drop)


###################
# Tests
###################


@dataclasses.dataclass
class Case:
    a: tp.Sequence[tp.Any]
    result: int

    def __str__(self) -> str:
        return 'min_to_drop_{}'.format(self.a)


TEST_CASES = [
    Case(a=[], result=0),
    Case(a=[1, 2, 3, 1], result=2),
    Case(a=[1, 2, 1], result=1),
    Case(a=[1, 1], result=0),
    Case(a=[1], result=0),
    Case(a=[2*30, 2*30], result=0),
    Case(a=["a"], result=0),
    Case(a=["a", "a"], result=0),
    Case(a=["a", "a", "b", "c"], result=2),
    Case(a=[1, 2, 3, 4], result=3),
    Case(a=[2, 3, 4, 1], result=3),
    Case(a=[1, 2, 3, 4, 5, 6, 1], result=5),
    Case(a=[1, 1, 1, 1, 2, 2, 1], result=2),
    Case(a=[1, 1, 1, 2, 2, 2, 2], result=3),
    Case(a=[2, 2, 2, 2, 1, 1, 1], result=3),
    Case(a=[1, 1, 2, 2, 3, 3], result=4),
    Case(a=[1, 1, 1, 2, 3, 3, 1], result=3),
    Case(a=[-1, 1, 1, -1, 3, 3, -1], result=4),
    Case(a=[-1, 1] * 1024, result=1024),
    Case(a=list(range(1024)), result=1024-1),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_min_to_drop(t: Case) -> None:
    given_a = copy.deepcopy(t.a)

    answer = get_min_to_drop(given_a)
    assert answer == t.result

    assert t.a == given_a, "You shouldn't change inputs"
