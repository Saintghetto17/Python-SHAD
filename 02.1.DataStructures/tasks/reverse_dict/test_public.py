import copy
import dataclasses
import typing as tp
from collections import defaultdict

import pytest
import testlib

from .reverse_dict import revert


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(revert)


###################
# Tests
###################


@dataclasses.dataclass
class Case:
    dct: tp.Mapping[str, str]
    result: tp.Mapping[str, list[str]]

    def __str__(self) -> str:
        return 'revert_{}'.format(self.dct)


TEST_CASES = [
    Case(dct={}, result={}),
    Case(dct={"a": "1"}, result={"1": ["a"]}),
    Case(dct={"ab": "12"}, result={"12": ["ab"]}),
    Case(dct={"": "1", "a": ""}, result={"1": [""], "": ["a"]}),
    Case(dct={"a": "1", "b": "2"}, result={"1": ["a"], "2": ["b"]}),
    Case(dct={"a": "1", "b": "2", "c": "1"}, result={"1": ["a", "c"], "2": ["b"]}),
    Case(dct={"a": "1", "b": "2", "c": "1", "d": "1"}, result={"1": ["a", "c", "d"], "2": ["b"]}),
    Case(
        dct={"aaa": "1", "bbb": "2", "ccc": "1", "ddd": "1", "eee": "2"},
        result={"1": ["aaa", "ccc", "ddd"], "2": ["bbb", "eee"]}
    ),
    Case(dct={"": "1", "a": "", "b": ""}, result={"1": [""], "": ["a", "b"]}),
    Case(
        dct={"a": "1", "b": "2", "c": "1", "d": "1", "e": "2", "g": "3"},
        result={"1": ["a", "c", "d"], "2": ["b", "e"], "3": ["g"]}
    ),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_dict(t: Case) -> None:
    given_dct = copy.deepcopy(t.dct)

    answer = revert(given_dct)

    assert t.dct == given_dct, "You shouldn't change input dict"

    for k, v in answer.items():
        v.sort()

    assert answer == t.result
    assert isinstance(answer, dict)
    assert not isinstance(answer, defaultdict), "Please cast your defaultdict to dict in the end"


def _crappy_solution(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    return {value: [key for key, val in dct.items() if val == value] for value in dct.values()}


def test_reverse_dict_heavy() -> None:
    import time
    given_dct = {str(i): "1" for i in range(10000)}

    t0 = time.perf_counter()
    _ = _crappy_solution(given_dct)  # O(n^2)
    t1 = time.perf_counter() - t0
    _ = revert(given_dct)  # O(n) ~ 10000 times faster
    t2 = time.perf_counter() - t1 - t0
    assert t2 < t1 / 1000, f"Your solution runs in {t2}; achieve {t1 / 1000} or less"
